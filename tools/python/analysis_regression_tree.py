import numpy as np
import ROOT as root
regression_dir = '~/workspace/hgtd/rootfiles/regression_results/'

class AnalysisRegressionTree():
    def __init__(self, start_tree, tf, ext, hgtd=False):
        self._start_tree = start_tree
        self._tf = tf
        self._ext = ext 
        self._detector = 'hgtd_' if hgtd else ''

    def make(self):
        self._tf = root.TFile('~/workspace/hgtd/rootfiles/reg_tree_' + self._detector + self._ext, 'RECREATE')
        self._reg_tree = root.TTree('reg_tree', 'Regression tree')
        self._add_branches()
        self._close_file()

    def _add_branches(self):
        energies = ['max_energy', 'combined2_energy', 'combined4_energy', 'combined9_energy']
        for energy in energies:
            #get the output of the regressions
            tf = root.TFile(regression_dir + 'TMVAReg_' + self._detector + energy + self._ext)
            dataset = tf.Get('dataset')
            tree = dataset.Get('TrainTree')
            
            combined_energy = np.zeros(1, dtype=float)
            self._reg_tree.Branch('reg_' + self._detector + energy, combined_energy, energy + '/D')
            
            #===================================================================
            # print(tree.GetEntries())
            # exit()
            #===================================================================
            
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                combined_energy[0] = tree.EoverEtrue / tree.BDTG
                self._reg_tree.Fill()

    def _close_file(self):
        self._tf.Write()
        print('wrote' + self._tf.GetPath())
        self._tf.Close()


#THIS FILE IS USELESS I THINK