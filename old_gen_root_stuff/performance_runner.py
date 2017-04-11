class PerformanceRunner():
    def __init__(self, tree, ext):
        self._tree = tree
        self._ext = ext

    def run(self):
        output_dir = "~/workspace/hgtd/python/tools/python/tmp"
        root_file = "~/workspace/hgtd/rootfiles/" + self._ext
        tree_name = "tree"
        target = "Sum$(towerE)/(pt*cosh(eta))" #might need to backslash the $
        histo_binnig = "np.linspace(0., 1., 2, 49)"
        variable = "eta"
        varibale_label = "eta"
        binning = "2.5, 2.7, 2.9, 3.1"
        algo = "mean"        
        execfile("~/workspace/hgtd/python/tools/python/performance.py " + options)
        