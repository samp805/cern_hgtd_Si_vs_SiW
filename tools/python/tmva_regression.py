import ROOT as root
from constants import Constants
import os
from TMVACalibPostProcessing import TMVACalibPostProcessing
from TMVACalibPostProcessing import add_variablesname_to_xmlfile
#from analysis_regression_tree import AnalysisRegressionTree

class TMVARegression():
    def __init__(self, tree, tf, ext):
        self._tree = tree
        self._tf = tf
        self._ext = ext

    def run_all(self):
        #runs regressions for max_energy, combined2,4,9
        skip = raw_input("Skip regressions no hgtd (y/n):  ")
        if skip == "n":
            for energy in Constants.energies():
                self._run(energy)
            #===================================================================
            # AnalysisRegressionTree(self._tree, self._tf, self._ext).make()
            #===================================================================
        
        skip_hgtd = raw_input("Skip regression with hgtd information (y/n):  ")
        if skip_hgtd == "n":
            for energy in Constants.energies():
                self._run(energy, hgtd=True)
            #===================================================================
            # AnalysisRegressionTree(self._tree, self._tf, self._ext, hgtd=True).make()
            #===================================================================

        #THE TWO COMMENTED OUT BLOCKS ARE BECAUSE TMVA & SOURCE TREES AREN'T ONE TO ONE
        #SO YOU CAN'T BUILD A TREE AND MAKE IT SEEM ONE TO ONE

    def _run(self, energy, hgtd=False):
        detector = "hgtd_" if hgtd else ""
        outFile = root.TFile(Constants.regrDir() + 'TMVAReg_' + detector + energy + self._ext, "recreate")
        factory = root.TMVA.Factory("TMVAReg_{0}_{1}_{2}".format(detector, energy, self._ext[:-5]), outFile, "!V:!Silent:Color:DrawProgressBar")
        
        factory.AddVariable("eta", "Eta", "units", "F")
        factory.AddVariable("phiMod:=fmod(phi*32/pi, 1)", "Phi", "units", "F")
        factory.AddVariable(energy, "Tower Energy", "units", "F")
        if hgtd:
            factory.AddVariable("sumHits:=Sum$(hgtd_nHits)", "HGTD hits", "units")
            factory.AddVariable("sumHGTDenergy:=Sum$(hgtd_e)", "HGTD Energy", "units")
        
        factory.AddSpectator("sumHGTDenergy:=Sum$(hgtd_e)", "HGTD Energy", "units")
        factory.AddSpectator("sumHits:=Sum$(hgtd_nHits)", "Sum Num Hits",  "units")
        factory.AddSpectator("z", "Z",  "units")
        factory.AddSpectator("hgtd_time", "HGTD time",  "units")
        factory.AddTarget("EoverEtrue:={0}/(pt*cosh(eta))".format(energy))
        
        #SUMMARY OF WHAT I CAN USE FOR PERFORMANCE.PY
        #eta, phiMod, combined2_energy, Etrue, z, hgtd_time, EoverEtrue, BDTG
        #used sumHits & sumHGTDenergy for combined4&9
        
        regWeight = 1.0;
        factory.AddRegressionTree(self._tree, regWeight)
        factory.SetWeightExpression("eta", "Regression")
        mycut = root.TCut("eta>2.5")
        factory.PrepareTrainingAndTestTree(mycut, "nTrain_Regression=1000:nTest_Regression=0:SplitMode=Random:NormMode=NumEvents:!V")
        #we only need BDTG
        factory.BookMethod(root.TMVA.Types.kBDT, "BDTG", "!H:!V:NTrees=2000::BoostType=Grad:Shrinkage=0.1:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=3:MaxDepth=4")
        
        factory.TrainAllMethods()
        factory.TestAllMethods()
        factory.EvaluateAllMethods()
        
        #xml stuff
        xmlfile = os.path.join("weights", 'TMVAReg_{0}_{1}_{2}_BDTG.weights.xml'.format(detector, energy, self._ext[:-5]))
        TMVACalibPostProcessing(xmlfile)
        #make exception for hgtd
        add_variablesname_to_xmlfile(xmlfile, {"Variables":['eta', 'phiMod', energy]})

        
        
        outFile.Close()
        
        print("wrote root file: {0}".format(outFile.GetName()))
        #UNCOMMENT THIS IF YOU ACTUALLY WANT THE GUI
        #=======================================================================
        # root.TMVA.TMVARegGui(Constants.regrDir + 'TMVAReg' + self._ext)
        # raw_input("press enter to quit...")
        #=======================================================================
        