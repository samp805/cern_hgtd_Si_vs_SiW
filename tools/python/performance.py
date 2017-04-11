#!/usr/bin/env python

__doc__ = "To make some plots for the MVA calibration (see performance_examples.txt)"

import os
import logging
from itertools import imap, izip, product
import pprint

import numpy as np
import ROOT

ATLASSTYLEDIR = os.getcwd()
if os.getenv("ATLASSTYLEDIR"):
    ATLASSTYLEDIR = os.getenv("ATLASSTYLEDIR")

import RootTools
from performanceTools import memoized, subtract, binData, binDataAndWeights, sliceUnderOverflows, getFcnName, BinningDescription, powerset, binning2array
from worker import PerformanceWorker

ROOT.PyConfig.IgnoreCommandLineOptions = True
logging.basicConfig(level=logging.INFO)
logging.basicConfig(format="%(funcname)s\t%(levelname)s:%(message)s")

# @memoized
# def digitize(tree, variables, binning, cut = ''):
#     ""
#     logging.debug("dumping binning values: %s", str(variables))
#     binning_values = [RootTools.GetValuesFromTree(tree, var, cut) for var in variables]
#     return np.transpose([np.digitize(value, bin) for value, bin in zip(binning_values, binning)])

@memoized
def getChain(tree_name, inputFiles, readFromFile = False, singleFile = False):
    import os
    expanded_path = os.path.expanduser(os.path.expandvars(inputFiles))
    chain = ROOT.TChain(tree_name)
    if readFromFile:
      file_list = filter(bool, (i.strip('\n') for i in open(inputFiles)))
      map(chain.Add, file_list)
    elif singleFile:
      f = ROOT.TFile.Open(inputFiles)
      return f.Get(tree_name)
    else:
      chain.Add(expanded_path)
    if len(list(chain.GetListOfFiles())) == 0:
        logging.error("Cannot find any file from %s", str(inputFiles))
    return chain

@memoized
def getData(chain, variable, cut='', nevents=None):
    if not variable:
        return None
    logging.info("downloading branch %s for chain %s with cut %s using %s events",
                 repr(variable), chain, repr(cut), nevents if nevents else "all")
    result = RootTools.GetValuesFromTree(chain, variable, cut, nevents=nevents)
    if len(result) == 0:
        logging.error('result is empty for chain="%s", variable="%s", cut="%s"', chain, variable, cut)
    else:
        logging.info("got %d entries" % len(result))
    return result

# @memoized
def digitize(values, bins):
    try:
        return np.digitize(values, bins)
    except ValueError:
        logging.error("bin are not ordered: %s", bins)
        raise

class PerformanceMaster(object):
    ""

    def __init__(self, chains, quantities, weights, cuts, labels,
                 variables, binnings, var_labels, actions,
                 algos, compare_formulas, algo_lines,
                 histo_binning, histo_line, reference,
                 histo_reference=None,
                 histo_norm=False, histo_logy=False,
                 legend_position=None,
                 histo_max_depth=1, values_max_depth=1,
                 var_max_depth=None,
                 graph_linestyles=None,
                 graph_linecolors=None,
                 graph_linewidths=None,
                 graph_markers=None,
                 graph_log=None,
                 ignore_comb=[],
                 save_graphs=False,
                 no_2d=False,
                 nevents=None,
                 algo_labels=None,
                 atlas_label=None,
                 min_stat_bin=None,
                 min_ratio=None,
                 max_ratio=None):
        """
        chains, quantities, weights, cuts, labels (quantities to plot, e.g. E/Etrue)
        variables, binnings, var_labels, actions (independent variables, e.g. eta)
        algos, compare_formulas (estimators and how to compare them with the reference)
        histo_binning (binning used for histograms), reference (index of reference quantity)
        histo_norm (draw normalized histograms), legend_position,
        histo_max_depth (draw histos when splitting up to given dimension),
        values_max_depth (same as above for comparing values among quantities)
        """
        #     print 'chains, quantities, cuts, labels:',
        #     print chains, quantities, cuts, labels
        #     print 'variables, binnings, var_labels, actions:',
        #     print variables, binnings, var_labels, actions
        #     print 'algos, compare_formulas:',
        #     print algos, compare_formulas
        #     print 'histo_binning, reference:',
        #     print histo_binning, reference

        # TODO: define labels, var_labels if needed
        if labels == [''] * len(quantities):
            labels = ['q%s' % i for i,j in enumerate(quantities)]
        if var_labels == [''] * len(variables):
            var_labels = ['var%s' % i for i,j in enumerate(variables)]
        if any(i is None for i in algo_labels):
            algo_labels = {}

        if var_max_depth is not None:
            var_max_depth = dict(zip(var_labels, var_max_depth))
        else:
            var_max_depth = {}

        # Load data (quantities and independent variables)
        # Independent variables have to be associated to each quantity as they may use
        # different trees and cuts
        # TODO: avoid duplication, memoize does not work
        logging.debug("getting data")
        self.data = dict(izip(labels, imap(getData, chains, quantities, cuts, [nevents] * len(chains))) )
        self.weights = dict(izip(labels, imap(getData, chains, weights, cuts, [nevents] * len(chains))) )
        logging.debug("getting data for axis")
        self.varData = dict( ((label, var_label), getData(chain, v, cut, nevents)) \
                                 for (v, var_label), (label, chain, cut) in \
                                 product(izip(variables, var_labels), izip(labels, chains, cuts)) )

        # logging.debug("Data: %s" % self.data)
        # logging.debug("varData: %s" % self.varData)
        # Bin the data (quantities) according to the binning associated to each variable
        # (binning in multiple variables will be done later)
        varDataGrouped = [np.ravel(np.array([j for i,j in self.varData.iteritems() if v in i], dtype=object)) \
          for v in var_labels]
        self.npBinnings = map(self.fixBinning, binnings, varDataGrouped )
        logging.info('Binning data')
        logging.debug( 'Binnings: %s' % self.npBinnings)
        self.binnedData = {}
        self.binnedWeights = {}
        self.binning_indices = {}
        for (label, var_label), values in self.varData.iteritems():
            binning = self.npBinnings[var_labels.index(var_label)]
            indices = digitize(values, binning)
            key = (label, (var_label,))
            self.binnedData[key] = binData(self.data[label], binning, indices)
            self.binnedWeights[key] = binData(self.weights[label], binning, indices) \
              if self.weights.get(label) else None
            self.binning_indices[key] = indices
            
        # Prepare outputs
        output_file = ROOT.TFile("test_output.root", "recreate")

        estimators = map(np.vectorize, algos)
        for i,j in zip(estimators, algos):
            i.__name__ = j.__name__
        algo_names = [getFcnName(x) for x in estimators]

        # Loop over all the combinations of variables
        # (e.g. (), ('eta'), ('Et'), ('eta', 'Et') )
        # and define one worker for each combination and each "label" (chain, quantity, cut)
        # and one superimposer for each combination, grouping all workers of the same kind
        general_bin_description = BinningDescription(self.npBinnings, var_labels)
        self.workers = {}
        for comb in powerset(var_labels):
            if comb in ignore_comb or any(var_max_depth[v] < len(comb) for v in comb):
                logging.debug('Skipping %s' % repr(comb))
                continue
            bin_description = general_bin_description.subBinningDescriptionFromAxis(comb)


            graphs_dict = {}
            histograms_dict = {}
            values_dict = {}
            graphs2d_dict = {}

            indices = map(var_labels.index, comb)
            theVariables = map(variables.__getitem__, indices)
            theBinning = map(self.npBinnings.__getitem__, indices)
            theAction = map(actions.__getitem__, indices)
            theLog = map(graph_log.__getitem__, indices)
            logging.info('Defining workers for %s:', repr(comb))
            logging.debug('...binning: %s' % theBinning)
            Ndim = len(comb)

            # Define the workers
            for chain, label, cut in zip(chains, labels, cuts):
                # Retrieve the binned data or bin it in all the variables
                if Ndim == 0: # inclusive case
                    binnedData = self.data[label]
                    binnedWeights = self.weights[label]
                elif Ndim == 1: # already binned
                    binnedData = self.binnedData[(label, comb)]
                    binnedWeights = self.binnedWeights[(label, comb)]
                else: # multiple variables, use indices of the binning of each variable
                    # TODO: start from previous binnings
                    binning_indices = [self.binning_indices[(label, (v,))] for v in comb]
                    binnedData, binnedWeights = binDataAndWeights(self.data[label], theBinning, binning_indices, self.weights[label])
                    # Much slower than binData2
#                     binnedData = binData(self.data[label], theBinning, binning_indices)
#                     binnedWeights = binData(self.weights[label], theBinning, binning_indices) if self.weights[label] else None
                logging.debug('Shape of data: %s' % str(binnedData.shape))
                worker = PerformanceWorker(binnedData, binnedWeights, None, estimators,
                    theBinning, label, comb, histo_binning, theAction,
                    histo_max_depth, values_max_depth, min_stat_bin, do2d=not no_2d)
                self.workers[(comb, label)] = worker
                values, histograms, graphs, graphs2d = worker()

                for k,v in values.iteritems():
                    subkey = (label,) + (k,)
                    values_dict[subkey] = v

                histograms_dict[label] = histograms
                for k,v in graphs.iteritems():
                    subkey = (label,) + k
                    graphs_dict[subkey] = v
                for k,v in graphs2d.iteritems():
                    subkey = (label,) + k
                    graphs2d_dict[subkey] = v


            super_imposer = SuperImposer(bin_description, options.title,
                                         output_file,
                                         values_dict, histograms_dict, graphs_dict, graphs2d_dict, image_format=options.format,
                                         sorted_titles=labels, algo_names=algo_names,
                                         algo_labels=algo_labels,
                                         histo_norm = histo_norm, histo_logy = histo_logy,
                                         legend_position=legend_position, graph_log=theLog,
                                         min_ratio=min_ratio, max_ratio=max_ratio)
            logging.info("drawing values")
            super_imposer.draw_values(algo_lines = algo_lines,
                                      compare_formulas=None,
                                      compare_title=None) # TODO: use it

            logging.info("drawing histos")
            super_imposer.draw_histos(histo_lines = histo_line, reference_title=histo_reference)
            try:
                reference = int(reference)
            except ValueError:
                pass
            logging.info("drawing graphs")
            super_imposer.draw_graphs(compare_formulas=compare_formula,
                                      compare_title=reference,
                                      algo_lines=algo_lines,
                                      linestyles=graph_linestyles,
                                      linecolors=graph_linecolors,
                                      linewidths=graph_linewidths,
                                      markers=graph_markers,
                                      save_graphs=save_graphs,
                                      atlas_label=atlas_label,
                                      min_ratio=min_ratio,
                                      max_ratio=max_ratio)
            if not no_2d:
                logging.info("drawing graphs 2D")
                super_imposer.draw_graphs2d(compare_formulas=compare_formula, compare_title=reference, opt="colz", save_graphs = save_graphs)

    def fixBinning(self, binning, varData):
        ""
        if isinstance(binning, dict) and binning.get('type') == 'uniform':
            # find the binning that splits the data in nbins equal pieces
            #splitA = np.array_split(sorted(varData), binning['nbins'])
            #new_binning = np.array([i[0] for i in splitA if len(i)] + [max(varData)])
            #return new_binning
            import scipy.stats.mstats as ms
            return ms.mquantiles(varData, prob=np.linspace(0.005,0.995, binning['nbins']) )
        return binning2array(binning)

if __name__ == "__main__":
    import Estimators
    from superimposer import SuperImposer

    logging.basicConfig(level=logging.INFO)

    ROOT.gStyle.SetPalette(1)

    def split_callback_float(option, opt, value, parser):
        try:
            setattr(parser.values, option.dest, map(float,value.split(',')))
        except ValueError:
            raise OptionValueError("option %s: invalid list of float: %r" % (opt, value))

    def split_callback(option, opt, value, parser):
        setattr(parser.values, option.dest, [x.strip() for x in value.split(',')])

    def eval_callback(option, opt, value, parser):
        try:
            setattr(parser.values, option.dest, eval(value))
        except:
            raise ValueError("Invalid value for %s: %s" % (option.dest, value))

    def callback_eval_append(option, opt, value, parser):
        try:
            v = eval(value)
        except:
            raise ValueError("Invalid value for %s: %s" % (option.dest, value))
        getattr(parser.values, option.dest).append(eval(value))

    def string2color(color_string):
        """
        input kWhite, kOrange+2
        """
        separator = "+" if ("+" in color_string) else "-"
        splitted = [x.strip() for x in color_string.split(separator)]
        if len(splitted) == 1:
            return ROOT.__getattr__(splitted[0])
        elif len(splitted) == 2:
            if separator == "+":
                return ROOT.__getattr__(splitted[0]) + int(splitted[1])
            else:
                return ROOT.__getattr__(splitted[0]) - int(splitted[1])

    def checkSizes(dictionary, name=None):
        """
        Get a dictionary (and its name) with lists as values and raise an exception if
        elements have different sizes.
        If an element has size 1 the value is repeated to match the other sizes.
        """
        if name:
          logging.debug('Checking %s' % name.lower())
        else:
          name = 'options'
        # Get the key associated with the longest list (and the size of the list)
        try:
          kMax = max(dictionary, key=lambda x: len(dictionary[x])) # key with maximum size
          N = len(dictionary[kMax])
          if N == 1:
            return
        except TypeError:
          raise ValueError("Invalid values: %s" % dictionary)
        for key, value in dictionary.iteritems():
          if len(value) == 1:
            logging.debug("Using (%s = %s) for all items" % (key, repr(value[0])))
            value.extend( [value[0]]*(N-1) )
          elif len(value) != N:
            raise ValueError("Parameters in %s do not have the same size (%s and %s)" % \
              (name, kMax, key) )

    def checkType(value, types):
        "Raise TypeError if the given values does not correspond to the expected types"
        if not isinstance(value, types):
            raise TypeError

    from optparse import OptionParser, OptionValueError, OptionGroup
    parser = OptionParser("%prog [options]")
    parser.description = __doc__
    parser.epilog = "NB: You must supply the same number of options (or 1) for each group"
#       """Each time you call it, a new option is appended and the size of each option should beYou should give a set of options


    quantityGroup = OptionGroup(parser, "Options for quantities",
                                "(quantities to plot and apply the estimators)")
    quantityGroup.add_option("-Q", "--quantity", action="append",
                             help="Branch/formula to be plotted / passed to the estimators (ph_cl_E/ph_truth_E)")
    quantityGroup.add_option("--label", action="append", help="Label of the plot")
    quantityGroup.add_option("--weight", action="append", help="Branch/formula for weight")
    quantityGroup.add_option("--tree", dest="tree", action="append", help="Tree name")
    quantityGroup.add_option("-i", "--input", dest="input", action="append",
                             help="Input ROOT file(s) (can use comma or wildcard as in the TChain constructor)")
    quantityGroup.add_option("--cut", help="Cut to apply to get each quantity",
                             action="append")
    quantityGroup.add_option("--log", action='append',
                             help="use logarithmic scale to plot quantity")
    quantityGroup.add_option("--graph-linestyle", action='append',
                             help="linestyle for the graph")
    quantityGroup.add_option("--graph-linecolor", action='append',
                             help="linecolor for the graph")
    quantityGroup.add_option("--graph-linewidth", action='append',
                             help="linewidth for the graph")
    quantityGroup.add_option("--graph-marker", action='append',
                              help="marker for the graph, better to use values from 20")
    quantityGroup.add_option("--readFromFile", choices=['0','1'], action='append',
                             help="Read input files from text file")
    quantityGroup.add_option("--singleFile", choices=['0','1'], action='append',
                             help="Read input from a single ROOT file")
    quantityGroup.add_option("--friend", action='append',
                             help="Add friend tree (inside the same file(s) )")
    parser.add_option_group(quantityGroup)
    # -------------------------------
    binningGroup = OptionGroup(parser, "Options for variables",
                               "(used for the binning and the dependences, i.e. the axis definition)")
    binningGroup.add_option("-v", "--variable", action="append",
                            help="Branch/formula of the variable to plot against or bin (e.g. ph_cl_eta)")
    binningGroup.add_option("--var-label", action="append", help="Label of the axis")
    binningGroup.add_option("--binning", type='string', action='callback',
                            callback=callback_eval_append, default=[],
                            help="Binning for variable (list, array or dict with nbins, min, max or nbins and type='uniform')")
    binningGroup.add_option("--action", choices=['0','1','2'], action='append',
                            help="Use variable for 0=plotting and binning, 1=binning, 2=plotting")
    binningGroup.add_option("--graph-log", choices=['0','1'], action='append',
                            help="Plot graphs in log scale for each variable")
    binningGroup.add_option("--var-max-depth", action='append',
                            help="Maximum dimension for each variable")
    parser.add_option_group(binningGroup)
    # -------------------------------
    estimatorGroup = OptionGroup(parser, "Options for estimators",
                                 "(like mean, median, etc)")
    estimatorGroup.add_option("--algo", type="string", action="append",
                              help="algorithm to use") # TODO: add nargs="*" and get arguments for algorithm
    estimatorGroup.add_option("--compare-formula", type="string", action='append',
                              help="formula to use in the comparison with the reference sample")
    estimatorGroup.add_option("--algo-line", type="string", action="callback",
                              callback=callback_eval_append, default=[])
    estimatorGroup.add_option("--algo-label", type="string", action="append", default=[],
                              help="Label for each algorithm (optional)")
    parser.add_option_group(estimatorGroup)
    # -------------------------------
    parser.add_option("-o", "--outputdir", help="Output directory", default=".")
    parser.add_option("--title",
                      help="Label that defines all the quantities (e.g.: E/Etrue)", default="Q")
    parser.add_option("--histo-binning", help="Binning for histograms", type='string',
                      action='callback', callback=eval_callback)
    parser.add_option("--histo-line", help="Vertical line position", type=float)
    parser.add_option("--histo-logy", default=False, action="store_true",
                      help="use logarithmic scale on y-axis of histograms")
    parser.add_option("--histo-norm", default=False, action="store_true",
                      help="draw normalized histograms")
    parser.add_option("--reference-histo", type=str,
                      help="Index or name of the histo to shade")
    parser.add_option("--reference", type=str, default="0",
                      help="Index or name of the reference sample to compare with (default: %default)")
    parser.add_option("--histo-max-depth", default=99, type=int,
                      help="draw histograms until Ndim <= max-depth")
    parser.add_option("--values-max-depth", default=99, type=int,
                      help="draw graphs with values until Ndim <= max-depth")
    parser.add_option("--legend-position", choices=['0', '1', '2', '3', '4'], default='1',
                      help="No legend: 0, upper right: 1, upper left: 2, lower left: 3, lower right: 4")
    parser.add_option("--debug", help="debug infos", action="store_true", default=False)
    parser.add_option("-f", "--format", default="png", choices=["png", "pdf", "ps", "root", "eps"],
                      help="image format")
    parser.add_option("-c", "--command", default="", type="string",
                      help="Commands, executed right after parsing the options")
    parser.add_option("--config", default="", type="string",
                      help="Config file, loaded right after parsing the options")                      
    parser.add_option("--alias", action="append", \
                      help="Set alias if branch not present (e.g.: etaMod = fmod(el_cl_eta,0.025))")
    parser.add_option("--useProof", action="store_true", default=False,
                      help="Use proof to load branches")
    parser.add_option("--useAtlasStyle", action="store_true", default=False,
                      help="Use AtlasStyle settings")
    parser.add_option("--save-graphs", action="store_true", default=False,
                      help="Save all the graphs in the output ROOT file")
    parser.add_option("--no-2d", action="store_true", default=False,
                      help="Do not produce 2d plots (faster)")
    parser.add_option("--nevents", type=int, help="number of events to process, default=all")
    parser.add_option("--ignore-comb", action="append", default=[],
                      help="Ignore combination of variables")
    parser.add_option("--atlas-label", type=str, help="a label as ATLAS label")
    parser.add_option("--min-stat-bin", type=int, help="minimun stat per bin")
    parser.add_option("--min-ratio", type=float, help="minimum y-axis for ratio")
    parser.add_option("--max-ratio", type=float, help="maximum y-axis for ratio")
#     parser.add_option("--npz", type=str, help="Save / load npz file with data")
    ################################################################################

    options, args = parser.parse_args()
    
    # Execute commands and load config file
    # TODO: parse args again to override ?
    exec(options.command)
    if os.path.isfile(options.config):
      if os.path.splitext(options.config)[1][1:] == 'pickle':
        from pickle import load
        options.__dict__.update( load(open(options.config)) )
      else:
        execfile(options.config)
    

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Check for required options
    required_options = 'input', 'tree', 'quantity', 'variable', 'binning', 'algo', 'histo_binning'
    for i in required_options:
        if getattr(options, i) is None:
            raise ValueError('No %s given' % i)

    # Set default values for options (if not given)
    defaults_if_void = dict(
        label=[''], cut=[''], action = [0], log=[False],
        compare_formula = [''], algo_label=[None],
        var_label=[''], algo_line=[None], weight=[''], graph_linecolor=[None], graph_linestyle=[None], graph_linewidth=[None], graph_marker=[None], graph_log=[False], var_max_depth=[99], readFromFile=[False], singleFile=[False], friend=[''] )
    for i,j in defaults_if_void.iteritems():
        if not getattr(options, i):
            logging.debug('Setting default for %s' % i)
            setattr(options, i, defaults_if_void[i])

    # Format some options
    options.action = map(int, options.action)
    options.graph_log = map(int, options.graph_log)
    options.var_max_depth = map(int, options.var_max_depth)
    options.ignore_comb = [tuple(map(str.strip, i.split(','))) for i in options.ignore_comb]
    options.readFromFile = map(int, options.readFromFile)
    options.singleFile = map(int, options.singleFile)

    # Print all options
    logging.info("options %s", pprint.pformat(options.__dict__))

    # Check if all items in the group have the same size (or repeat them if size = 1)
    for group in quantityGroup, binningGroup, estimatorGroup:
        values = dict( (i.dest, getattr(options,i.dest)) for i in group.option_list)
        checkSizes(values, group.title )

    # Check if 'reference' is valid
    if options.reference not in options.label:
        try:
            assert int(options.reference) < len(options.label)
        except (ValueError, AssertionError):
            raise ValueError("Invalid reference: %s" % options.reference)

    # Check if 'reference-histo' is valid
    if options.reference_histo and options.reference_histo not in options.label:
        raise ValueError("Invalid histo reference: %s" % options.reference_histo)

    # Define estimators
    import Estimators, re
    def getEstimator(est):
        try:
          return eval(est, vars(Estimators) )
        except NameError:
            fraction = 0.01*int(est[-2:])
            estimator = getattr(Estimators, est[:-2])
            fcn = lambda data, w: estimator(data, w, fraction)
            fcn.__name__ = est
            return fcn

    try:
        algos = map(getEstimator, options.algo)
    except AttributeError:
        print 'ERROR!!! Valid estimators: %s' % [i for i,j in vars(Estimators).iteritems() if hasattr(j, '__call__')]
        raise
    compare_formula = {}
    for algo, formula in zip(algos, options.compare_formula):
          compare_formula[getFcnName(algo)] = formula
    
    # Create chains
    chains = map(getChain, options.tree, options.input, options.readFromFile, options.singleFile)
    for c,f,i,r in zip(chains, options.friend, options.input, options.readFromFile):
      if f:
        friend = getChain(f, i, r)
        c.AddFriend(friend)

    for ichain, (chain, label) in enumerate(zip(chains, options.label)):
        logging.info("%s\t%s files", label, chain.GetListOfFiles().GetEntries())
        if chain.GetListOfFiles().GetEntries() == 0:
            logging.error("Cannot find find files for tree=%s, input=%s", options.tree[ichain], options.input[ichain])

    # Create aliases
    if options.alias is not None:
      for chain in chains:
          for alias in options.alias:
              try:
                  br, expression = alias.split(" = ")
              except ValueError:
                  raise ValueError("Invalid alias: %s" % alias)
              if not chain.GetBranch(br):
                  chain.SetAlias(br, expression)
                  logging.info("Alias created for %s: %s", chain, alias)

    # Create and cd to output directory
    directory = options.outputdir
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        logging.warning("directory %s already exist" % directory)

    ROOT.gROOT.SetBatch()
    ROOT.gSystem.ChangeDirectory(directory)
    if options.useProof:
      RootTools.GetValuesFromTree = RootTools.GetValuesFromTreeWithProof
    if options.useAtlasStyle:
      ROOT.gROOT.LoadMacro(ATLASSTYLEDIR + "/AtlasStyle.C")
      try:
          ROOT.SetAtlasStyle()
      except AttributeError:
          logging.error("you must copy the AtlasStyle.{h,C} from https://twiki.cern.ch/twiki/pub/AtlasProtected/PubComTemplates/atlasstyle-00-03-05.tar.gz to %s", ATLASSTYLEDIR)
          exit()
      ROOT.gStyle.SetMarkerSize(0.8)
      ROOT.gStyle.SetLegendBorderSize(0)
      ROOT.gStyle.SetPalette(1)
      ROOT.gStyle.SetNumberContours(256)

    # save the options and command to file
    import pickle
    foptions = open('command.pickle', 'w')
    pickle.dump(options.__dict__, foptions)
    foptions.close()
    
    import socket
    import datetime
    import sys
    try:
        fcommand = open("command.sh", "w")
        fcommand.write('# command executed on %s from %s by %s\n' % (datetime.datetime.today(), socket.gethostname(), os.getlogin()))
        fcommand.write(' '.join(sys.argv))
        fcommand.close()
    except OSError:
        print("something is weird with command.sh")

    logging.info("""
Run parameters:
quantity: %(quantity)s
weight: %(weight)s
cut: %(cut)s
label: %(label)s
variable: %(variable)s
binning: %(binning)s
var_label: %(var_label)s
action: %(action)s
algos: %(algos)s
algo_lines: %(algo_lines)s
compare formula %(compare_formula)s
histo_binning: %(histo_binning)s
histo_line: %(histo_line)s
reference: %(reference)s
""", {"quantity": str(options.quantity),
      "weight": str(options.weight),
      "cut": str(options.cut),
      "label": str(options.label),
      "variable": str(options.variable),
      "binning": str(options.binning),
      "var_label": str(options.var_label),
      "action": str(options.action),
      "algos": str(algos),
      "algo_lines": str(options.algo_line),
      "compare_formula": str(compare_formula),
      "histo_binning": str(options.histo_binning),
      "histo_line": str(options.histo_line),
      "reference": str(options.reference),
      "histo-norm": str(options.histo_norm),
      "legend-position": options.legend_position,
      "graph-log": options.graph_log,
      "ignore-comb": options.ignore_comb})

    if len(options.histo_binning) < 2:
        raise ValueError('histo binning in empty: %s' % options.histo_binning)
    if (len(set(options.label))) != len(options.label):
        raise ValueError('duplicate in labels: %s' % options.label)

    P = PerformanceMaster(chains, options.quantity, options.weight, options.cut, options.label,
                          options.variable, options.binning, options.var_label, options.action,
                          algos, compare_formula, options.algo_line,
                          options.histo_binning, options.histo_line, options.reference,
                          histo_reference=options.reference_histo,
                          histo_norm=options.histo_norm,
                          histo_logy=options.histo_logy,
                          legend_position=int(options.legend_position),
                          histo_max_depth=options.histo_max_depth,
                          values_max_depth=options.values_max_depth,
                          graph_linestyles=options.graph_linestyle,
                          graph_linecolors=options.graph_linecolor,
                          graph_linewidths=options.graph_linewidth,
                          graph_markers=options.graph_marker,
                          graph_log=options.graph_log,
                          var_max_depth=options.var_max_depth,
                          ignore_comb=options.ignore_comb,
                          save_graphs=options.save_graphs,
                          no_2d=options.no_2d,
                          nevents=options.nevents,
                          atlas_label=options.atlas_label,
                          algo_labels=options.algo_label,
                          min_stat_bin=options.min_stat_bin,
                          min_ratio=options.min_ratio,
                          max_ratio=options.max_ratio)
