import numpy as np
import ROOT
import logging
import RootTools
from itertools import izip, imap, product, cycle
from copy import copy
import os
import math

from performanceTools import slugify, shift_bin

if not hasattr(ROOT.TPad, 'DivideSquare'):
  def DivideSquare(pad, n):
    from math import ceil, floor, sqrt
    w = int(ceil(sqrt(n)))
    h = int(floor(sqrt(n)))
    if w*h < n:
      w += 1
    pad.Divide(w, h)
  ROOT.TPad.DivideSquare = DivideSquare

def color_generator():
#     return cycle(range(2, 10))
    return cycle([ROOT.kBlack, ROOT.kRed, ROOT.kBlue+1, ROOT.kGreen+1, ROOT.kYellow+1, ROOT.kViolet, ROOT.kMagenta-5, ROOT.kCyan, ROOT.kGray+1, ROOT.kGreen-8, ROOT.kOrange-1, ROOT.kGreen-2, ROOT.kViolet+3, ROOT.kAzure-2, ROOT.kOrange+8, ROOT.kPink+9])

def multigrapher(graphs, linestyles=None, linecolors=None, linewidths=None, markers=None):
    "Return a TMultiGraph adding the given graphs"
    mg = ROOT.TMultiGraph()
    if not linestyles or not all(linestyles): linestyles = [None] * len(graphs)
    if not linecolors or not all(linecolors): linecolors = color_generator()
    if not linewidths or not all(linewidths): linewidths = [None] * len(graphs)
    if not markers or not all(markers): markers = [None] * len(graphs)
    a = izip(graphs, linecolors, linestyles, linewidths,markers)
    for graph, linecolor, linestyle,linewidth,marker in a:
        if linewidth:
            graph.SetLineWidth(int(linewidth))
        if linestyle:
            graph.SetLineStyle(int(linestyle))
        if marker:
            graph.SetMarkerStyle(int(marker))
        graph.SetLineColor(int(linecolor))
        graph.SetMarkerColor(int(linecolor))
        graph.SetFillColor(ROOT.kWhite)
        mg.Add(graph)
    return mg

def stacker(histos, linestyles=None, linecolors=None, linewidths=None):
    "Return a THStack adding the given histos"
    stack = ROOT.THStack()
    if not linestyles or not all(linestyles): linestyles = [None] * len(histos)
    if not linecolors or not all(linecolors): linecolors = color_generator()
    if not linewidths or not all(linewidths): linewidths = [None] * len(histos)
    a = izip(histos, linecolors, linestyles, linewidths)
    for histo, linecolor, linestyle, linewidth in a:
        histo.SetLineColor(int(linecolor))
        if linestyle:
            histo.SetLineStyle(int(linestyle))
        if linewidth:
            histo.SetLineWidth(int(linewidth))
        stack.Add(histo)
    return stack


def saver(objects, titles=None):
    titles = titles or [obj.GetTitle() for obj in objects]
    for title, obj in zip(titles, objects):
        obj.Write(title)


def legender(objects, titles=None, x1=0, y1=0, x2=0.2, y2=0.2, loc=None):
    legend_position = None
    if loc is not None:
        if type(loc) is str:
            loc = {'upper right': 1,
                   'upper left': 2,
                   'lower left': 3,
                   'lower right': 4}[loc]
        legend_position = {1: (0.65, 0.65, 0.9, 0.9),
                           2: (0.2, 0.65, 0.45, 0.9),
                           3: (0.1, 0.2, 0.3, 0.5),
                           4: (0.65, 0.1, 0.9, 0.3)}[loc]
    else:
        legend_position = (x1, y1, x2, y2)

    titles = titles or [obj.GetTitle() for obj in objects]
    legend = ROOT.TLegend(*legend_position)
    legend.SetFillColor(0)
    for title, obj in zip(titles, objects):
        opt = 'L' if isinstance(obj, ROOT.TH1) else 'PL'
        legend.AddEntry(obj, title, opt)
    return legend

def superimpose(objects, linestyles=None, linecolors=None, linewidths = None,
    markers=None):

    types = set([type(obj) for obj in objects])
    common_type = None
    if len(types) != 1:
        if len(types==2) and (ROOT.TGraph in types) and (ROOT.TGraphErrors in type):
            common_type = ROOT.TGraph
    else: common_type = type(objects[0])
    if common_type is None:
        raise ValueError("all types must be the same type, here: %s" % str(types))
    if common_type is ROOT.TGraph or common_type is ROOT.TGraphErrors:
        return multigrapher(objects, linestyles, linecolors, linewidths, markers)
    elif common_type is ROOT.TH1F:
        return stacker(objects, linestyles, linecolors, linewidths)
    else:
        raise ValueError("types must be TH1F, TGraph or TGraphErrors (not %s)" % str(common_type))

def uniform_scale2d(list_graphs):
    maxima_z, minima_z = [], []
    for g in list_graphs:
        values = [g.GetBinContent(x, y)
                  for (x,y) in product(range(1, g.GetNbinsX()+1), range(1, g.GetNbinsY()+1))]
        if len(set(values)) != 1:
          values = [x for x in values if x != 0]
        print values
        minima_z.append(min(values))
        maxima_z.append(max(values))
    minimum_z = min(minima_z)
    maximum_z = max(maxima_z)

    print "minimum: ", minimum_z
    print "maximum: ", maximum_z
    for g in list_graphs:
        g.GetZaxis().SetRangeUser(minimum_z, maximum_z)


def compare_graphs2d(graphs, compare_formula, ref_index):
    compare_formula = ROOT.TFormula(compare_formula, compare_formula)
    graph_ref = graphs[ref_index]
    other_graphs = graphs #graphs[:ref_index] + graphs[ref_index+1:]
    graphs_comp = []
    for other_graph in other_graphs:
        if (other_graph.GetNbinsX() != graph_ref.GetNbinsX()) or (other_graph.GetNbinsY() != graph_ref.GetNbinsY()):
            graphs_comp.append(None)
            continue
        graph_comp = copy(other_graph)
        while not isinstance(graph_comp, ROOT.TH2): # sometimes becomes TGraphErrors so let's insist
          copy(other_graph)
        graph_comp.Reset()
        for x,y in product(xrange(1,other_graph.GetNbinsX()+1), xrange(1,other_graph.GetNbinsX()+1)):
            value = other_graph.GetBinContent(x, y)
            value_ref = graph_ref.GetBinContent(x, y)
            value_comp = compare_formula.Eval(value, value_ref)
            graph_comp.SetBinContent(x, y, value_comp)
        graphs_comp.append(graph_comp)
    return graphs_comp


def compare_graphs(graphs, compare_formula, ref_index):
    compare_formula = ROOT.TFormula(compare_formula, compare_formula)
    graph_ref = graphs[ref_index]
    other_graphs = graphs #graphs[:ref_index] + graphs[ref_index+1:]
    # remove graphs with different number of points
    other_graphs = [graph for graph in other_graphs if graph.GetN() == graph_ref.GetN()]
    ysref = [graph_ref.GetY()[i] for i in range(graph_ref.GetN())]
    ysref_err = [graph_ref.GetErrorY(i) for i in range(graph_ref.GetN())]
    mg = ROOT.TMultiGraph()
    for graph in other_graphs:
        graph_ratio = ROOT.TGraphErrors()
        graph_ratio.SetName(graph.GetName() + "_ref")
        graph_ratio.SetTitle(graph.GetTitle())
        graph_ratio.SetLineColor(graph.GetLineColor())
        graph_ratio.SetMarkerColor(graph.GetMarkerColor())
        graph_ratio.SetMarkerStyle(graph.GetMarkerStyle())
        graph_ratio.SetMarkerSize(graph.GetMarkerSize())
        if graph.GetN() != graph_ref.GetN():
            # TODO: better
            continue
        xs = [graph.GetX()[i] for i in range(graph.GetN())]
        ysold = np.array([graph.GetY()[i] for i in range(graph.GetN())])
        ysold_err = np.array([graph.GetErrorY(i) for i in range(graph.GetN())])
        for ipoint, (x, y1, y2, y1_err, y2_err) in enumerate(zip(xs, ysold, ysref, ysold_err, ysref_err)):
            y = compare_formula.Eval(y1, y2)
            graph_ratio.SetPoint(ipoint, x, y)
            xerror = graph_ref.GetErrorX(ipoint)
            yerror = 0
            if graph_ref != graph and compare_formula.GetTitle() == "x/y": # special case, TODO: how to handle others?
                try:
                    yerror =  np.abs(y) * np.sqrt( (y1_err/y1)**2 + (y2_err/y2)**2)
                except ZeroDivisionError:
                    logging.error("division by zero: y=%s, y1 = %s, y1_err = %s, y2=%s, y2_err=%s. Setting error to 0", y, y1, y1_err, y2, y2_err)
                    yerror = 0
            if graph == graph_ref:
              yerror = 0.
            graph_ratio.SetPointError(ipoint, xerror, yerror)
        mg.Add(graph_ratio)
    return mg

def mkdir_or_cd(self, new_dir):
    n = self.Get(new_dir)
    if n:
        n.cd()
    else:
        d = self.mkdir(new_dir)
        self.cd(new_dir)

ROOT.TDirectory.mkdir_or_cd = mkdir_or_cd

def mkdir(new_dir):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)


class SuperImposer(object):
    def __init__(self, bin_description, quantity, output_directory,
                 values=None, histos=None, graphs=None, graphs2d=None,
                 sorted_titles=None, algo_names=None, algo_labels={},
                 image_format=None, histo_norm=False, histo_logy=False,
                 legend_position=1, graph_log=False,
                 min_ratio=None, max_ratio=None):
        """
        Superimposer handles one binning setup and one quantity
        histos: {"title1": histo matrix from worker1, "title2": histo matrix from worker2, ...]
                you can use the add_histos method
        graphs: {("title1", axis_variables as tuple, "algorithm1"): matrix of graphs, ...]
                you can use the add_graphs method
        output_directory: directory to save the canvases
        image_format = format without '.', "png", "pdf", ...
        legend_position: upper right: 1, upper left: 2, lower left: 3, lower right: 4
        """
        logging.info("Starting superimposer, working dir %s", ROOT.gSystem.WorkingDirectory())
        self.values_matrices = values or dict()
        self.histo_matrices = histos or dict()
        self.graph_matrices = graphs or dict()
        self.graph2d_matrices = graphs2d or dict()
        self.bin_description = bin_description
        self.quantity = quantity
        self.output_directory = output_directory
        self.image_format = image_format.lower() if image_format else None
        self.sorted_titles = sorted_titles
        self.algo_names = algo_names
        if isinstance(algo_labels, (list, tuple)):
            self.algo_labels = dict(zip(algo_names, algo_labels))
        else:
            self.algo_labels = algo_labels
        self.histo_canvases = {}
        self.histo_norm = histo_norm
        self.histo_logy = histo_logy
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        self.graph_log = graph_log if isinstance(graph_log, list) else [graph_log]
        self.legend_position = legend_position

        self.root_directory = output_directory
        self.root_directory.cd()

    def add_values(self, key, values):
        """ add a set of values """
        self.values_matrices.update({key: values})

    def add_histos(self, key, histos):
        """ add a set of histos, for example from one worker, in this case key is the title """
        self.histo_matrices.update({key: histos})

    def add_graphs(self, key, graphs):
        """ add a set of graphs """
        self.graph_matrices.update({key: graphs})

    def add_graphs2d(self, key, graphs2d):
        """ add a set of graphs2d """
        self.graph2d_matrices.update({key: graphs2d})

    def draw_values(self, algo_lines=None, compare_formulas=None, compare_title=None):
        def fill_histo(data, errors, bin_labels):
            h = ROOT.TH1F()
            h.SetBins(len(data), 0, len(data))
            for i,(d, err, label) in enumerate(zip(data, errors, bin_labels),1):
                h.SetBinContent(i, d)
                h.SetBinError(i, err)
                h.GetXaxis().SetBinLabel(i, label)
            return h

        def compare_values(histo_values, compare_formula, compare_index):
            h = ROOT.TH1F()
            nbins = histo_values.GetXaxis().GetNbins()
            h.SetBins(nbins, 0, nbins)
            reference = histo_values.GetBinContent(compare_index+1)
            reference_error = histo_values.GetBinError(compare_index+1)
            for i in range(1, histo_values.GetXaxis().GetNbins()+1):
                v = h.GetBinContent(i)
                e = h.GetBinError(i)
                try:
                    ratio = v / reference
                    h.SetBinContent(i, ratio)
                except ZeroDivisionError:
                    h.SetBinContent(i, -1)
                    h.SetBinError(i, 0)
                else:
                    try:
                        h.SetBinError(i, ratio * ((e/v)**2 + (reference_error/reference)**2))
                    except ZeroDivisionError:
                        h.SetBinError(i, -1)
                h.GetXaxis().SetBinLabel(i, histo_values.GetXaxis().GetBinLabel(i))
            return h


        if all(x is None for x in self.values_matrices.values()):
          logging.warning('No values, not superimposing')
          return

        algo_names = self.algo_names
        if algo_names is None:
            algo_names = set([key[1] for key in self.values_matrices.iterkeys()])
        if algo_lines is None: algo_lines = [None] * len(algo_names)
        logging.info("found %d different algorithms" % len(algo_names))
        old_directory = ROOT.gDirectory.GetFile()
        directory_name = slugify(self.bin_description.directory_name())
        self.root_directory.mkdir_or_cd(directory_name)
        mkdir(directory_name)
        os.chdir(directory_name)
        for algo, algo_line in zip(algo_names, algo_lines):
            compare_formula = compare_formulas[algo] if compare_formulas else None
            selected_values_matrices = dict([(k,v[0]) for k,v in self.values_matrices.iteritems()
                                             if k[1] == algo])
            selected_errors_matrices = dict([(k,v[1]) for k,v in self.values_matrices.iteritems()
                                             if k[1] == algo])
            sorted_titles = self.sorted_titles
            if sorted_titles is None:
                sorted_titles = set([k[1] for k in selected_values_matrices.iterkeys()])
            iterators_values = [selected_values_matrices[(title, algo)].flat for title in sorted_titles] # --> [ [matrix0_value0, matrix0_value1, ...]
                                                                                                 #       [matrix1_value0, matrix1_value1, ...], ...
            iterators_errors = [selected_errors_matrices[(title, algo)].flat for title in sorted_titles]

            transposed_iterator_values = izip(*iterators_values)                       # --> [ [matrix0_value0, matrix1_value0, ...]
                                                                                                 #       [matrix0_value1, matrix1_value1, ...], ...
            transposed_iterator_errors = izip(*iterators_errors)
            titles = sorted_titles

            bins_iterator = np.ndindex(*(selected_values_matrices.values()[0].shape)) # assuming every one of the same shape
            for thebin, it, iterr in izip(bins_iterator, transposed_iterator_values, transposed_iterator_errors):
                values = np.nan_to_num(np.fromiter(it, np.float))
                errors = np.nan_to_num(np.fromiter(iterr, np.float))

                canvas_name = slugify(algo + "_" + self.quantity + "_" + self.bin_description.bin_name(thebin))
                canvas = ROOT.TCanvas(canvas_name, canvas_name, 800, 600)
                if compare_formula:
                    canvas.Divide(1,2)
                    canvas.cd(1)
                h = fill_histo(values, errors, titles)
                h.GetXaxis().SetLabelSize(0.05)
                h.GetYaxis().SetTitle(self.algo_labels.get(algo, algo))
                h.SetStats(0)
                h.Draw()

                if algo_line is not None:
                    canvas.cd(1).Update()
                    hline = RootTools.hLine(algo_line, fix_histo=h)
                    hline.SetLineStyle(2)
                    hline.Draw()
                    canvas.hline = hline
                label = self.label_contex_info(self.bin_description, thebin)
                label.Draw()
                canvas._label = label

                if compare_formula:
                    canvas.cd(2)
                    compare_index = len(titles) - 1
                    if type(compare_title) is int:
                        compare_index = compare_title
                    if type(compare_title) is str:
                        compare_index = titles.index(compare_title)
                    cg = compare_values(h, compare_formula, compare_index)
                    cg.Draw()
#                    cg.GetXaxis().SetTitle(axis)
                    canvas.compare_histo = cg

                canvas.Write()
                if self.image_format is not None:
                    canvas.SaveAs(canvas.GetTitle() + "." + self.image_format)
        old_directory.cd()
        os.chdir("..")

    def draw_histos(self, histo_lines = None, reference_title=None):
        """ loop over all the set of histos and for every one it produces a canvas """
        if histo_lines is None: histo_lines = []
        if type(histo_lines) is float: histo_lines = [histo_lines]
        if all(x is None for x in self.histo_matrices.values()):
          logging.warning('No histograms, not superimposing')
          return

        iterators = [self.histo_matrices[label].flat for label in self.sorted_titles]
#         iterators = [matrix.flat for matrix in self.histo_matrices.itervalues()] # --> [ [matrix0_histo0, matrix0_histo1, ...],
                                                                                 #       [matrix1_histo0, matrix1_histo1, ...], ...
        histo_titles = self.sorted_titles#list(self.histo_matrices.iterkeys())
        transposed_iterator = izip(*iterators)                          # --> [ [matrix0_histo0, matrix1_histo0, ...],
                                                                                 #       [matrix0_histo1, matrix1_histo1, ...], ...
        bins_iterator = np.ndindex(*(self.histo_matrices.values()[0].shape)) # assuming every one of the same shape
        old_directory = ROOT.gDirectory.GetFile()
        directory_name = slugify(self.bin_description.directory_name())
        self.root_directory.mkdir_or_cd(directory_name)
        mkdir(directory_name)
        os.chdir(directory_name)
        for thebin, it in izip(bins_iterator, transposed_iterator):
            # Skip if all the histograms are empty
            if not any(histo.GetSumOfWeights() for histo in it):
                continue
            # at this point it iterate over the histograms you have to superimpose for one bin
            if self.histo_norm:
                for histo in it:
                    scaling = histo.GetSumOfWeights()
                    if scaling:
                        histo.Scale(1. / scaling)
            histo_stack = superimpose(it)
            if reference_title:
              h_reference = it[histo_titles.index(reference_title)]
              h_reference.SetFillColor(h_reference.GetLineColor())
            canvas_name = slugify(self.quantity + "_" + self.bin_description.bin_name(thebin))
            canvas = ROOT.TCanvas(canvas_name, canvas_name, 800, 600)
            histo_stack.Draw("nostack")
            histo_stack.GetXaxis().SetTitle(self.quantity)
            if self.histo_logy:
                canvas.SetLogy()
            canvas.Update()
            for line in histo_lines:
                frame = canvas.GetFrame()
                l = ROOT.TLine(line, frame.GetY1(), line, frame.GetY2())
                l.SetLineStyle(2)
                l.Draw()
            if self.legend_position != 0:
                legend = legender(it, titles = histo_titles, loc=self.legend_position)
                legend.Draw()
            latex_bin = self.label_contex_info(self.bin_description, thebin)
            latex_bin.Draw()
            self.histo_canvases.update({thebin: canvas}) # TODO: do we want to save them?

            logging.info("saving canvas %s", canvas.GetName())
            canvas.Write()
            if self.image_format is not None:
                canvas.SaveAs(canvas.GetTitle() + "." + self.image_format)
        old_directory.cd()
        os.chdir("..")

    def draw_graphs(self, compare_formulas=None, compare_title=None,
                    underflow=False, algo_lines=None, linestyles=None,
                    linecolors=None, linewidths=None, markers=None,
                    save_graphs=False, atlas_label=None,
                    min_ratio=None, max_ratio=None):
        """ loop over all the set of graphs and for every one it produces a canvas """
        axes_binvars_algorithms = set([(key[1], key[2], key[3]) for key in self.graph_matrices.iterkeys()])
        if algo_lines is None: algo_lines = [None] * len(algo_names)
        logging.info("found %d different algo, binvars, axis pairs", len(axes_binvars_algorithms))
        for axis, binvars, algo in axes_binvars_algorithms:
            compare_formula = compare_formulas[algo] if compare_formulas else None
            logging.info("superimposing graphs for algo: %s, binvars: %s and axes: %s", algo, str(binvars), str(axis))
            selected_graph_matrices = dict([(k,v) for k,v in self.graph_matrices.iteritems()
                                            if (k[3] == algo and k[1] == axis)])

            sorted_titles = self.sorted_titles
            if sorted_titles is None:
                sorted_titles = set([key[0] for key in selected_values_matrices.iterkeys()])
            iterators = [selected_graph_matrices[(title, axis, binvars, algo)].flat for title in sorted_titles]
            graph_titles = sorted_titles
            transposed_iterator = izip(*iterators)
            sub_binner = self.bin_description.subBinningDescriptionFromAxis(binvars)
            old_directory = ROOT.gDirectory.GetFile()
            directory_name = slugify(sub_binner.directory_name())
            self.root_directory.mkdir_or_cd(directory_name)
            mkdir(directory_name)
            os.chdir(directory_name)

            bins_iterator = np.ndindex(*(selected_graph_matrices.values()[0].shape)) # assuming every one of the same shape

            if type(axis) is str: # only one (only the x-axis)
                axis_str = axis
            else:
                axis_str = "_".join(axis)
            # Index of the axis on bin_description, to set it to log scale if needed
            try:
                axis_index = self.bin_description.axis_titles.index(axis)
            except:
                axis_index = 0
            try:
                algo_line = algo_lines[self.algo_names.index(algo)]
            except IndexError:
                algo_line = None
            logging.debug('Algo line: %s' % algo_line)
            for thebin, it in izip(bins_iterator, transposed_iterator):
                canvas_name = slugify(algo + "_" + self.quantity + "_vs_" + axis_str + "_" + (sub_binner.bin_name(thebin) or "inclusive"))
                canvas = ROOT.TCanvas(canvas_name, canvas_name, 800,600)
                canvas.mem = []
                if compare_formula:
                    canvas.Divide(1,2)
                    canvas.cd(1)
                if self.graph_log[axis_index]:
                    logging.info('Setting log-x')
                    ROOT.gPad.SetLogx()

                multi_graph = superimpose(it, linestyles, linecolors, linewidths, markers)
                multi_graph.Draw("APL")
                multi_graph.GetXaxis().SetTitle(axis)
                multi_graph.GetYaxis().SetTitle(self.algo_labels.get(algo, algo))
                for i in it:
                    i.GetXaxis().SetTitle(axis)
                    i.GetYaxis().SetTitle(self.algo_labels.get(algo, algo))
                if self.legend_position != 0:
                    legend = legender(it, titles = graph_titles, loc=self.legend_position)
                    legend.Draw()

                if atlas_label is not None:
                    atlas_latex = ROOT.TLatex(0.2, 0.2, atlas_label)
                    atlas_latex.SetNDC()
                    atlas_latex.Draw()
                    canvas.mem.append(atlas_label)

                if algo_line is not None:
                  hline = RootTools.hLine(algo_line, fix_histo=multi_graph)
                  hline.SetLineStyle(2)
                  hline.Draw()
                  canvas.hline = hline
                if save_graphs:
                    saver(it, titles = [slugify(canvas_name + "_" + f) for f in graph_titles])

                latex_bin = self.label_contex_info(sub_binner, shift_bin(thebin,1))
                latex_bin.Draw()

                if compare_formula:
                    canvas.cd(2)
                    if self.graph_log[axis_index]:
                        logging.info('Setting log-x')
                        ROOT.gPad.SetLogx()

                    compare_index = len(graph_titles) - 1
                    if type(compare_title) is int:
                        compare_index = compare_title
                    elif type(compare_title) is str:
                        compare_index = graph_titles.index(compare_title)
                    cg = compare_graphs(it, compare_formula, compare_index)
                    if compare_formula == 'x/y':
                        yaxis_compare = 'Ratio to %s' % compare_title
                    else:
                      yaxis_compare = compare_formula.replace("x", "#xxx123xxx#").replace("y", "#yyy123yyy#")
                      yaxis_compare = compare_formula.replace("#xxx123xxx#", algo).replace("#yyy123yyy#", algo + "_{%s}" % compare_title)
                    cg.Draw("APL")
                    cg.GetXaxis().SetTitle(axis)
                    cg.GetYaxis().SetTitle(yaxis_compare)
                    if min_ratio is not None and max_ratio is not None:
                        print min_ratio, max_ratio


                        cg.GetYaxis().SetLimits(min_ratio, max_ratio)
                        cg.GetYaxis().SetRangeUser(min_ratio, max_ratio)

                logging.info("saving canvas %s", canvas.GetName())
                canvas.Write()
                if self.image_format is not None:
                    canvas.SaveAs(canvas.GetTitle() + "." + self.image_format)
                del canvas
            old_directory.cd()
            os.chdir("..")

    def draw_graphs2d(self, compare_formulas=None, compare_title=None, underflow=False, opt="colz", save_graphs=False):
        axes_binvars_algorithms = set([(key[1], key[2], key[3]) for key in self.graph2d_matrices.iterkeys()])
        logging.info("found %d different algo, binvars, axis pairs", len(axes_binvars_algorithms))
        for axis, binvars, algo in axes_binvars_algorithms:
            compare_formula = compare_formulas[algo] if compare_formulas else None
            logging.info("superimposing graphs2D for algo: %s, binvars: %s and axes: %s", algo, str(binvars), str(axis))
            selected_graph2D_matrices = dict([(k,v) for k,v in self.graph2d_matrices.iteritems()
                                              if (k[3] == algo and k[1] == axis)])
            sorted_titles = self.sorted_titles
            if sorted_titles is None:
                sorted_titles = set([key[0] for key in selected_graph2D_matrices.iterkeys()])
            iterators = [selected_graph2D_matrices[(title, axis, binvars, algo)].flat for title in sorted_titles]
            graph2D_titles = sorted_titles
            transposed_iterator = izip(*iterators)
            sub_binner = self.bin_description.subBinningDescriptionFromAxis(binvars)
            old_directory = ROOT.gDirectory.GetFile()
            directory_name = slugify(sub_binner.directory_name())
            self.root_directory.mkdir_or_cd(directory_name)
            mkdir(directory_name)
            os.chdir(directory_name)
            bins_iterator = np.ndindex(*(selected_graph2D_matrices.values()[0].shape)) # assuming every one of the same shape
            if type(axis) is str: # only one (only the x-axis)
                axis_str = axis
            else:
                axis_str = "_".join(axis)
            for thebin, it in izip(bins_iterator, transposed_iterator):
                list_graphs = list(it)

                canvas_name = slugify("graph2d_" + algo + "_" + self.quantity + "_vs_" + axis_str + "_" + (sub_binner.bin_name(thebin) or "inclusive"))
                canvas = ROOT.TCanvas(canvas_name, canvas_name, 800, 600)
                canvas_top = body = ROOT.TPad("body", "body", 0, 0, 1, 0.9)
                body.Draw()
                body.cd()

                if compare_formula:
                    body.Divide(1,2)
                    canvas_top = body.cd(1)
                    while not isinstance(canvas_top, ROOT.TPad): # sometimes becomes TGraphErrors so let's insist
                      canvas_top = body.cd(1)

                canvas_top.DivideSquare(len(list_graphs))
                latex_bins = []
                for i, (g, title) in enumerate(zip(list_graphs,graph2D_titles), 1):
                    canvas_top.cd(i)
                    if self.graph_log[0]:
                        logging.info('Setting log-x')
                        canvas.SetLogx()
                    if self.graph_log[1]:
                        logging.info('Setting log-y')
                        canvas.SetLogy()

                    g.SetStats(0)
                    g.Draw(opt)
                    g.SetTitle(title)
                    g.SetName(slugify("g_" + algo + "_" + self.quantity + "_vs_" + axis_str + "_" + (sub_binner.bin_name(thebin) or "inclusive")))
                    if save_graphs:
                      g.Write()
                    g.GetXaxis().SetTitle(axis[0])
                    g.GetYaxis().SetTitle(axis[1])

                    latex_bin = self.label_contex_info(sub_binner, shift_bin(thebin,1))
                    latex_bin.Draw()
                    latex_bins.append(latex_bin) # without it is deleted

                # uniform the scale
                canvas_top.Update()
                uniform_scale2d(list_graphs)

                if compare_formula:
                    canvas_bottom = body.cd(2)
                    while not isinstance(canvas_bottom, ROOT.TPad): # sometimes becomes TGraphErrors so let's insist
                      canvas_bottom = body.cd(2)
                    compare_index = len(graph2D_titles) - 1
                    if type(compare_title) is int:
                        compare_index = compare_title
                    elif type(compare_title) is str:
                        compare_index = graph2D_titles.index(compare_title)
                    canvas_bottom.DivideSquare(len(list_graphs))
                    graphs_compare = compare_graphs2d(list_graphs, compare_formula, compare_index)
                    for igraph, graph in enumerate(graphs_compare, 1):
                        canvas_bottom.cd(igraph)
                        graph.Draw("colz")
                    canvas_bottom.Update()
                    uniform_scale2d(graphs_compare)
                    canvas_bottom.Update()

                canvas.cd(0)
                canvas_title = ROOT.TLatex(0.5, 0.95, "%s (%s)" % (algo, self.quantity))
                canvas_title.SetTextSize(0.04)
                canvas_title.SetNDC()
                canvas_title.SetTextAlign(21);
                canvas_title.Draw()


                logging.info("saving canvas %s", canvas.GetName())
                canvas.Write()
                if self.image_format is not None:
                    canvas.SaveAs(canvas.GetTitle() + "." + self.image_format)
            old_directory.cd()
            os.chdir("..")

    def label_contex_info(self, bin_description, keybin):
        bin_descr = bin_description.pretty_bin_description(keybin, use_title=True)
        if ROOT.gStyle.GetName() == 'ATLAS':
          latex_bin = ROOT.TLatex(0.16, 0.96, bin_descr)
        else:
          latex_bin = ROOT.TLatex(0.11, 0.91, bin_descr)
        latex_bin.SetTextSize(0.04)
        latex_bin.SetNDC()
        return latex_bin
