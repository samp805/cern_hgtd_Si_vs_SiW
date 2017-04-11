"""
example:

python add_weight.py --input1 ~blenzi/outputs/HggMVA/higgs_analysis_MC12_ggH125_p1196_MCCALIB_ntuple3.root --tree1 MVA \
--input2 ~blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo.v4_Eaccordion/MVACalib_convertedP\*root --tree2 TestTree \
--files-to-patch example/\*.root --tree TestTree \
--cut1 "(pass_isol) && (Iteration$==index_leading || Iteration$==index_subleading)" \
-v "ph_cl_E/cosh(ph_cl_eta), abs(ph_cl_eta)"
"""

"""
python -i add_weight.py --input1 ~blenzi/outputs/HggMVA/higgs_analysis_MC12_ggH125_p1196_MCCALIB_ntuple3.root --tree1 MVA \
--input2 ~blenzi/outputs/MVACalibW2/photon_flatEt_simple+etaPhiCalo.v4_Eaccordion/MVACalib_unconvertedP\*root --tree2 TestTree \
--files-to-patch ~/outputs/MVACalibW2/photon_flatEt_simple+etaPhiCalo.v4_Eaccordion/MVACalib_unconvertedP\*root --tree TestTree \
--cut1 "(pass_isol) && (Iteration$==index_leading || Iteration$==index_subleading) && ph_convFlag%10 == 0" \
--cut2 "" \
--weight2 "ph_truth_E/cosh(ph_truth_eta) < 80e3 ? 5/(80-7) : 5/(500-80)" \
-v "ph_truth_E/cosh(ph_truth_eta), abs(ph_cl_eta)" --nbins 200,25
"""

import logging
logging.basicConfig(level=logging.INFO)

logging.debug("importing")
import ROOT
import numpy as np
from array import array
import os
histoFile = None

def slugify(value):
    import re
    value = value.replace("/", "div").replace(".", "p")
    # from django project: https://code.djangoproject.com/browser/django/trunk/django/core/template/defaultfilters.py?rev=1443
    "Converts to lowercase, removes non-alpha chars and converts spaces to hyphens"
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('\s+', '_', value)
    value = value.strip("_")
    return value

def equal_divide(data, divisions=None, minstatbin=None):
    if divisions is None:
        divisions = int(len(data) / float(minstatbin))
    try:
        from scipy import stats
        quantiles = stats.mstats.mquantiles(data, prob=np.linspace(0,1,divisions))
    except ImportError:
        data.sort()
        quantiles = [i[0] for i in np.array_split(data, divisions)] + [data[-1]]
    return quantiles

def loop_bin(bins):
    for i in range(len(bins)-1):
        yield [bins[i], bins[i+1]]

def step(data):
    data = np.array(data)
    data0 = np.array(data[0])
    q = equal_divide(data0, minstatbin=300)
    if len(data) == 1:
        for qleft,qright in loop_bin(q):
            yield [(qleft, qright)]
        return
    data1 = np.array(data[1:])
    for qleft,qright in loop_bin(q):
        mask = np.logical_and(data0>=qleft, data0<=qright)
        newdata = data1.flatten()[np.tile(mask, data1.shape[0])].reshape((data1.shape[0], np.count_nonzero(mask)))
        for i in step(newdata):
            yield [(qleft, qright)] + i

class Tree(object):
    __slots__ = ['data', 'children']
    def __init__(self, data):
        self.data = data
        self.children = []
    def add_child(self, child):
        self.children.append(child)
    def _str(self, indent=0):
        result = ""
        result += ' ' * indent * 2 + str(self.data) + '\n'
        for child in self.children:
            result += child._str(indent+1)
        return result
    def __str__(self):
        return self._str()
    def __repr__(self):
        return self.__str__()
    def unroll(self):
        for child in self.children:
            for c in child.unroll():
                yield [self.data] + c
        if not self.children:
            yield [self.data]

def step_tree(data):
    data = np.array(data)
    data0 = np.array(data[0])
    tree = Tree(equal_divide(data0, minstatbin=300))
    if len(data) == 1:
        return tree
    data1 = np.array(data[1:])
    for qleft,qright in loop_bin(tree.data):
        mask = np.logical_and(data0>=qleft, data0<=qright)
        newdata = data1.flatten()[np.tile(mask, data1.shape[0])].reshape((data1.shape[0], np.count_nonzero(mask)))
        tree.add_child(step_tree(newdata))
    return tree


def getdata():
    data1 = np.arange(10)
    data2 = np.arange(100, 200, 10)
    data3 = np.arange(1000, 2000, 100)
    np.random.shuffle(data1)
    np.random.shuffle(data2)
    np.random.shuffle(data3)
    data = [data1, data2, data3]
    return data

def bound_binning(binning):
    binning = np.concatenate(([-np.inf], binning, [np.inf]))
    return binning

def bound_binning2(binning):
    low = binning[0] - 2*(binning[1] - binning[0])
    high = binning[-1] + 2*(binning[-1] - binning[-2])
    return np.concatenate(([low], binning, [high]))

def get_var(tree, var, cut="1"):
    n = tree.Draw(var, cut, "goff")
    data = tree.GetV1()
    data.SetSize(n)
    return np.array(data)

def get_ratio(histo1, histo2):
    "Return the ratio between 2 (multi-dim) histograms"
    histo2[histo2 == 0] = 1
    ratio = np.array(histo1, dtype=np.float32) / np.array(histo2, dtype=np.float32)
    ratio = np.nan_to_num(ratio)
    # ratio *= len(data1) / float(len(data2))    
    return ratio

def getMidPoint(x):
    "return the mid-point between the values in x"
    return 0.5*(x[:-1] + x[1:])

def get_spline(bin1, bin2, ratio):
    "Return a bivariate spline interpolation given the bins in the x and y axis and the values"
    import scipy.interpolate as si
    x,y = map(getMidPoint, (bin1[1:-1], bin2[1:-1]))
    X = np.array([(x[i], y[j], k) for (i,j), k in np.ndenumerate(ratio[1:-1, 1:-1])])
    return si.bisplrep(*X.T)

def get_spline1(bin1, bin2, ratio):
    """Return a list of univariate spline interpolations (one for each bin of bin2)
     given the bins in the x and y axis and the values"""
    import scipy.interpolate as si
    x = getMidPoint(bin1[1:-1])
    print len(x), ratio.shape
#     return [si.splrep(x, r[1:-1]) for r in ratio.T]
    xb = bound_binning2(x)
    return [si.splrep(xb, r) for r in ratio.T]

def numpyHisto2TH1(binning, histo, name = 'h', title = ''):
    "numpyHisto2TH1(binning, histo, name = 'h', title = '')"
    h = ROOT.TH1F(name, title, len(binning)-1, array('f', binning))
    for i,j in enumerate(histo):
        h.SetBinContent(i+1, j)
    h.SetEntries(np.sum(histo))
    return h

def numpyHisto2TH2(xbinning, ybinning, histo, name = 'h', title = ''):
    "numpyHisto2TH2(xbinning, ybinning, histo, name = 'h', title = '')"
    from RootTools import getTH2, fillTH2fromMatrix
    h = getTH2(xbinning, ybinning)
    h.SetName(name)
    h.SetTitle(title)
    fillTH2fromMatrix(h, histo)
    h.SetEntries(np.sum(histo))
    return h


def save1Dhistos(histoFile, var, binning, histo1, histo2, ratio):
    fout = ROOT.TFile(histoFile, 'update')
    print histo1, histo2
    h1 = numpyHisto2TH1(binning[1:-1], histo1[1:-1], 'h1_%s' % var, var)
    h2 = numpyHisto2TH1(binning[1:-1], histo2[1:-1], 'h2_%s' % var, var)
    hr = numpyHisto2TH1(binning[1:-1], ratio[1:-1], 'hratio_%s' % var, var)
    for i in h1, h2, hr:
        i.Write("", ROOT.TObject.kOverwrite)
    fout.Close()

def save2Dhistos(histoFile, variables, binnings, histo1, histo2, ratio):
    fout = ROOT.TFile(histoFile, 'update')
    xbinning, ybinning = binnings
    variables = tuple(variables)
    h1 = numpyHisto2TH2(xbinning[1:-1], ybinning[1:-1], histo1[1:-1,1:-1], 'h1_%s_%s' % variables, 'h1_%s_%s' % variables)
    h2 = numpyHisto2TH2(xbinning[1:-1], ybinning[1:-1], histo2[1:-1,1:-1], 'h2_%s_%s' % variables, 'h2_%s_%s' % variables)
    hr = numpyHisto2TH2(xbinning[1:-1], ybinning[1:-1], ratio[1:-1,1:-1], 'hratio_%s_%s' % variables, 'hratio_%s_%s' % variables)
    for i in h1, h2, hr:
        i.Write("", ROOT.TObject.kOverwrite)
    fout.Close()



def histo_weight(variables, chain1, chain2, cut1, cut2, divisions=None, minstatbin=300, weight1=None, weight2=None):        
    logging.debug("histo_weight with arguments %s", str(locals()))
    binnings = []
    weights_bin = []
    Data1 = []
    Data2 = []
    chain1.SetEstimate(chain1.GetEntries() * 10)
    chain2.SetEstimate(chain2.GetEntries() * 10)
    print "w1: ", weight1
    print "w2: ", weight2
    if divisions is None:
        divisions = [None]*len(variables)
    elif isinstance(divisions, str):
        divisions = map(int, divisions.split(','))
    if weight1 is not None:
      weight1 = get_var(chain1, weight1, cut1)
    if weight2 is not None:
      weight2 = get_var(chain2, weight2, cut2)
    for var, div in zip(variables, divisions):
        logging.info("getting variable %s", var)
        data1 = get_var(chain1, var, cut1)
        data2 = get_var(chain2, var, cut2)
        binning = equal_divide(data1, div, minstatbin)
        binning = bound_binning(binning)
        histo1 = np.histogram(data1, binning, weights=weight1)[0]
        histo2 = np.histogram(data2, binning, weights=weight2)[0]
        ratio = get_ratio(histo1, histo2)
        logging.debug("binning: %s", str(binning))
        logging.debug("ratio: %s", str(ratio))
        weights_bin.append(ratio)
        binnings.append(binning)
        Data1.append(data1)
        Data2.append(data2)
        if histoFile:
            save1Dhistos(histoFile, var, binning, histo1, histo2, ratio)
    # Multi-dimensional binning
    histo1 = np.histogramdd(Data1, binnings, weights=weight1)[0]
    histo2 = np.histogramdd(Data2, binnings, weights=weight2)[0]
    ratio = get_ratio(histo1, histo2)
    weights_bin.append(ratio)
    if histoFile and len(variables) == 2:
        save2Dhistos(histoFile, variables, binnings, histo1, histo2, ratio)
    return variables, binnings, weights_bin

def compute_friend(tree, variables, binnings, weights_bin, 
    initial_weight=None, doSpline=False):
    
    logging.debug("compute friend with arguments %s", str(locals()))
    variables = variables[:]

    # get the datas
    datas = []
    for var in variables:
        logging.debug("getting variable %s", var)
        data = get_var(tree, var)
        datas.append(data)
    if initial_weight is not None:
        initial_weight = get_var(tree, initial_weight)
    else:
        initial_weight = np.ones(len(data))

    # compute weights for every events
    weights_events = []
    multidim_indices = []
    for var, binning, data, weights_var in zip(variables, binnings, datas, weights_bin):
        indices = np.digitize(data, binning)-1
        ws = weights_var[indices]
        weights_events.append(ws)
        multidim_indices.append(indices)
    # Total weight: product of each weight
    total_weights = np.prod(weights_events, axis=0)
    weights_events.append(total_weights)
    variables.append("total")
    # Multi-dimensional weight: includes correlation
    multidim_weights = weights_bin[-1][multidim_indices]
    weights_events.append(multidim_weights)
    variables.append("multi")
    # Multi-dimensional weight, interpolated
    if len(binnings) == 2 and doSpline:
      spline = get_spline(binnings[0], binnings[1], weights_bin[-1])
      import scipy.interpolate as si
      F = np.vectorize(lambda x,y: si.bisplev(x, y, spline) )
      weights_events.append( np.clip(F(*datas), 0, np.inf) )
      variables.append('spline')
      # Univariate splines
      splines = get_spline1(binnings[0], binnings[1], weights_bin[-1])
      spline_index = binnings[1][1:-1].searchsorted(datas[1])
      F1 = np.vectorize( lambda x,y: si.splev(x, splines[y]) )
      weights_events.append( F1(datas[0], spline_index) )
      variables.append('spline1')
    # Create tree
    weights_events = np.array(weights_events)
    if initial_weight is not None:
        weights_events *= initial_weight
    newtree = ROOT.TTree("weight_tree", "tree weights")
    newtree.SetDirectory(0)
    # create the branches
    arrays = []
    for var in variables:
        ar = array('f', [0])
        arrays.append(ar)
        weight_name = "weight_" + slugify(var)
        newtree.Branch(weight_name, ar, weight_name + "/F")
    # fill
    for ws in weights_events.T:
        for i in range(len(arrays)):
            arrays[i][0] = ws[i]
        newtree.Fill()
    return newtree
    

def add_friend(filename, treename, new_tree):
    logging.debug("add friend with arguments %s", str(locals()))
    f = ROOT.TFile(filename, "update")
    tree = f.Get(treename)
    new_tree.SetDirectory(f)
    while True:
        old_friend = tree.GetFriend("weight_tree")
        if not old_friend: break
        logging.info("removing old friend")
        tree.RemoveFriend(old_friend)        
    tree.AddFriend(new_tree)
    new_tree.Write("", ROOT.TObject.kOverwrite)
    tree.Write("", ROOT.TObject.kOverwrite)
    f.Close()


if __name__ == "__main__":
    logging.info("starting")
    from glob import glob
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--files-to-patch", help="file to patch with friend (wildcards)")
    parser.add_option("-t", "--tree", help="tree name")
    parser.add_option("--input1", help="numerator (wildcards)")
    parser.add_option("--input2", help="denominator (wildcards)")
    parser.add_option("--tree1")
    parser.add_option("--tree2")
    parser.add_option("--cut1", default="1")
    parser.add_option("--cut2", default="1")
    parser.add_option("--weight1", default="1", help="Initial weight for 1st sample")
    parser.add_option("--weight2", default="1", help="Initial weight for 2nd sample")
    parser.add_option("-n", "--friend-tree", default="weight_tree", help="new tree name (default=%default)")
    parser.add_option("-v", "--variables", help="comma separated variables")
    parser.add_option("--nbins", help="Number of bins per variable, comma separated")
    parser.add_option("--minstatbin", help="Minimum stat per bin, if nbins not given (%default)", default=300, type=int)
    parser.add_option("--spline", help="Calculate weights using splines",
                      default = False, action="store_true")

    (options, args) = parser.parse_args()

    if options.files_to_patch is None:
        parser.error('files-to-patch not given')
    files_to_patch = glob(os.path.expandvars(os.path.expanduser(options.files_to_patch)))
    if not files_to_patch:
        parser.error("no files to patch found")
    if options.tree is None:
        parser.error('tree not given')
    if options.input1 is None:
        parser.error('input1 not given')
    if options.input2 is None:
        parser.error('input2 not given')
    if options.tree1 is None:
        parser.error("tree1 not given")
    if options.tree2 is None:
        parser.error("tree2 not given")
    if options.variables is None:
        parser.error('variables not given')

    chain1 = ROOT.TChain(options.tree1)
    chain1.Add(options.input1)
    chain2 = ROOT.TChain(options.tree2)
    chain2.Add(options.input2)
    variables = [i.strip() for i in options.variables.split(',')]
    
    
#    from pprint import pprint
#    pprint(step_tree(data))
#    pprint(list(step(data)))
#    pprint(list(step_tree(data).unroll()))
#    pprint(foo(step(data), []))

    logging.info("binning and computing weights for every bin")
    variables, binnings, weights_bin = histo_weight(variables, chain1, chain2, options.cut1, options.cut2, options.nbins, options.minstatbin, options.weight1, options.weight2)
    for f in files_to_patch:
        logging.info("adding friend tree to %s", f)
        root_file = ROOT.TFile(f)
        tree = root_file.Get(options.tree)
        logging.info("computing friend")
        new_tree = compute_friend(tree, variables, binnings, weights_bin, 
            options.weight2, options.spline)
        root_file.Close()
        logging.info("adding friend")
        add_friend(f, options.tree, new_tree)
