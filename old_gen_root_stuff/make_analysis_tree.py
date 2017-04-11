import ROOT as root
from add_max_energy import AddMaxEnergy
from add_combined2towers import AddCombined2Towers
from add_combined4towers import AddCombined4Towers
from add_combined9towers import AddCombined9Towers
from constants import Constants

class AnalysisTree():
    def __init__(self, start_tree, ext):
        self._start_tree = start_tree
        self._ext = ext

    def make(self):
        self._tf = self._make_tfile()
        self._analysis_tree = self._make_tree()
        self._add_branches()
        self._close_tfile()

    def _make_tfile(self):
        return root.TFile(Constants.rootDir() + "analysis_tree_" + self._ext, "UPDATE")
    
    def _make_tree(self):
        return root.TTree("analysis_tree", "analysis tree")
    
    def _add_branches(self):
        self._add_max_energy()
        self._add_combined_energies()
 
    def _add_max_energy(self):
        max_e = AddMaxEnergy(self._start_tree, self._analysis_tree)
        max_e.add()
        self._max_index = max_e.get_max_indicies() #must go after max_e.add()
        print("added max energy")
 
    def _add_combined_energies(self):
        AddCombined2Towers(self._start_tree, self._max_index, self._analysis_tree).add()
        print("added combined 2 towers")
        AddCombined4Towers(self._start_tree, self._max_index, self._analysis_tree).add()
        print("added combined 4 towers")
        AddCombined9Towers(self._start_tree, self._max_index, self._analysis_tree).add()
        print("added combined 9 towers")
        
    def _close_tfile(self):
        self._tfs[i].Write("", root.TObject.kOverwrite)
        print("wrote " + self._tf.GetPath())
        self._tf.Close()
