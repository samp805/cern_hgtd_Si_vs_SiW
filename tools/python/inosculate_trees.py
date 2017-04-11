import ROOT as root

class InosculateTrees():
    def __init__(self, trees, ext):
        self._trees = trees
        self._ext = ext

    def inosculate(self):
        self._initialize()
        self._load_trees()
        self._combine()

    def initialize(self):
        self._tf = root.TFile("~/workspace/hgtd/rootfiles/inosculated_" + self._ext)
        self._new_tree = root.TTree("big_tree", "combined tree")

    def _load_trees(self):
        for tree in self._trees:
            self._new_tree.AddBranch(tree.GetName(), tree)
