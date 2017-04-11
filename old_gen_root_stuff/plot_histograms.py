import ROOT as root
from constants import Constants

class PlotHistograms():
    def __init__(self, tree):
        self._tree = tree
        self._histograms = []
        
    def plot_all(self):
        self._plot_untrained()
        self._plot_regressions()
    
    def _plot_untrained(self):
        c = root.TCanvas()
        c.cd()
        for energy in Constants.energies()():
            self._tree.Draw(energy + "/(pt*cosh(eta))>>histo", "eta>2.5")
            hist = root.gDirectory.Get("histo")
            hist.SetLineColorAlpha(Constants.energies().index(energy) + 1, 1)
            if Constants.energies().index(energy) == 0:
                hist.Draw()
            else:
                hist.Draw("SAME")
            root.gDirectory.Delete("histo")
            
    def _plot_regressions(self):
        c = root.TCanvas()
        c.cd()
        for energy in Constants.energies():
            self._tree.Draw("reg_" + energy + ">>histo", "eta>2.5")
            hist = root.gDirectory.Get("histo")
            hist.SetLineColorAlpha(Constants.energies().index(energy) + 1, 1)
            if Constants.energies().index(energy) == 0:
                hist.Draw()
            else:
                hist.Draw("SAME")
            root.gDirectory.Delete("histo")
            
        

 #==============================================================================
 #    def _plot_untrained(self):
 #        for energy in energies():
 #            hist = root.gDirectory.Get("{0}_hist".format(energy))
 #            hist.SetLineColorAlpha(energies().index(energy) + 1, 1) #gives a unique color
 #            self._histograms.append(hist)
 #         
 #        self._plot_sum()
 #        self._plot_combined9_energy()
 #        self._plot_combined4_energy()
 #        self._plot_combined2_energy()
 #        self._plot_max()
 #        self._draw_histograms()
 #         
 #    def _plot_sum(self):
 #        self._tree.Draw("Sum$(towerE)/(pt*cosh(eta))>>hSumw", "eta>2.5")
 #        hsw = root.gDirectory.Get("hSumw")
 #        hsw.SetLineColorAlpha(5, 1) #yellow
 #        self._histograms.append(hsw)
 # 
 #    def _plot_combined9_energy(self):
 #        self._tree.Draw("combined9_energy/(pt*cosh(eta))>>hComb9w", "eta>2.5")
 #        hc9w = root.gDirectory.Get("hComb9w")
 #        hc9w.SetLineColorAlpha(1, 1) #black
 #        self._histograms.append(hc9w)
 # 
 #    def _plot_combined4_energy(self):
 #        self._tree.Draw("combined4_energy/(pt*cosh(eta))>>hComb4w", "eta>2.5")
 #        hc4w = root.gDirectory.Get("hComb4w")
 #        hc4w.SetLineColorAlpha(2, 1) #red
 #        self._histograms.append(hc4w)
 #     
 #    def _plot_combined2_energy(self):
 #        self._tree.Draw("combined2_energy/(pt*cosh(eta))>>hComb2w", "eta>2.5")
 #        hc2w = root.gDirectory.Get("hComb2w")
 #        hc2w.SetLineColorAlpha(3, 1) #lime
 #        self._histograms.append(hc2w)
 #         
 #    def _plot_max(self):        
 #        self._tree.Draw("max_energy/(pt*cosh(eta))>>hMaxw", "eta>2.5")
 #        hmw = root.gDirectory.Get("hMaxw")
 #        hmw.SetLineColorAlpha(4, 1) #blue
 #        self._histograms.append(hmw)
 #==============================================================================
 
    #===========================================================================
    # def plot_regressions(self):
    #     energies() = ["max_energy", "combined2_energy", "combined4_energy", "combined9_energy"]
    #     for energy in energies():
    #         self._tree.Draw("reg_{0}/(pt*cosh(eta))>>{1}".format(energy, energy + "_hist"), "eta>2.5")
    #         hist = root.gDirectory.Get("{0}_hist".format(energy))
    #         hist.SetLineColorAlpha(energies().index(energy) + 1, 1) #gives a unique color
    #         self._histograms.append(hist)
    #===========================================================================
 
    def _draw_histograms(self):
        for i in range(len(self._histograms)):
            if i == 0:
                self._histograms[i].Draw()
            else:
                self._histograms[i].Draw("SAME")
         
