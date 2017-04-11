import ROOT as root
from make_analysis_tree import AnalysisTree
from plot_histograms import PlotHistograms
from tmva_regression import TMVARegression
from constants import Constants

class ProcessRoots():
    def __init__(self, root_files, options):
        self._root_files = root_files
        self._options = int(options)
        self._tfs = []
        self._trees = []

    def process(self):
        "opens, builds analysis tree, befriends, regresses some root files"
        for i in range(len(self._root_files)):
            print("Processing " + self._root_files[i])
            
            self._tfs.append(root.TFile(Constants.rootDir() + self._root_files[i], "update"))
            self._trees.append(self._tfs[i].Get("tree"))
            
            if self._options % 2 == 0:
                AnalysisTree(self._trees[i], self._root_files[i]).make()
            self._trees[i].AddFriend("analysis_tree", Constants.rootDir() + "analysis_tree_" + self._root_files[i])
            self._tfs[i].Write("", root.TObject.kOverwrite)
            
            if self._options % 3 == 0:
                TMVARegression(self._trees[i], self._tfs[i], self._root_files[i]).run_all()
            
            if self._options % 5 == 0:
                PlotHistograms(self._trees[i]).plot_all()
                
                