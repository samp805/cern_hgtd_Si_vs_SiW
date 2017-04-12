import ROOT 
import numpy as np

#open files
tfwo20 = ROOT.TFile("withoutW.root")
tfwo45 = ROOT.TFile("withoutWv4.root")
tfwo100 = ROOT.TFile("withoutWv3.root")
tfwoflat = ROOT.TFile("withoutWv2.root")

#import the trees
t20 = tfwo20.Get("tree")
t45 = tfwo45.Get("tree")
t100 = tfwo100.Get("tree")
tflat = tfwoflat.Get("tree")

#decide which layer you want
layer = int(raw_input("which HGTD layer to compare?  "))

#build the histogram of the original timing rms without correction
h20 = ROOT.TH1F("h20", "20 GeV std spread layer {0} of Si".format(str(layer)), 200, 0, 1)
h45 = ROOT.TH1F("h45", "45 GeV std spread layer {0} of Si".format(str(layer)), 200, 0, 1)
h100 = ROOT.TH1F("h100", "100 GeV std spread layer {0} of Si".format(str(layer)), 200, 0, 1)
hflat = ROOT.TH1F("hflat", "flat GeV std spread layer {0} of Si".format(str(layer)), 200, 0, 1)
max_entries = max([t20.GetEntriesFast(),t45.GetEntriesFast(),t100.GetEntriesFast(),tflat.GetEntriesFast()])

for i in range(max_entries):
    if t20.GetEntry(i) > 0:
       if t20.hgtd_nHits > 0:
            temp = filter(lambda x : x < 1.3, np.asarray(t20.hgtd_time)[np.where(np.asarray(t20.hgtd_sampling) == layer)])
            if any(temp):
                h20.Fill(np.std(temp))

    if t45.GetEntry(i) > 0:
       if t45.hgtd_nHits > 0:
            temp = filter(lambda x : x < 1.3, np.asarray(t45.hgtd_time)[np.where(np.asarray(t45.hgtd_sampling) == layer)])
            if any(temp):
                h45.Fill(np.std(temp))

    if t100.GetEntry(i) > 0:
       if t100.hgtd_nHits > 0:
            temp = filter(lambda x : x < 1.3, np.asarray(t100.hgtd_time)[np.where(np.asarray(t100.hgtd_sampling) == layer)])
            if any(temp):
                h100.Fill(np.std(temp))

    if tflat.GetEntry(i) > 0:
       if tflat.hgtd_nHits > 0:
            temp = filter(lambda x : x < 1.3, np.asarray(tflat.hgtd_time)[np.where(np.asarray(tflat.hgtd_sampling) == layer)])
            if any(temp):
                hflat.Fill(np.std(temp))


c20 = ROOT.TCanvas("c20", "20 GeV std time spread")
c20.cd()
ROOT.gPad.SetLogy()
h20.Draw()

c45 = ROOT.TCanvas("c45", "45 GeV std time spread")
c45.cd()
ROOT.gPad.SetLogy()
h45.Draw()

c100 = ROOT.TCanvas("c100", "100 GeV std time spread")
c100.cd()
ROOT.gPad.SetLogy()
h100.Draw()

cflat = ROOT.TCanvas("cflat", "flat GeV std time spread")
cflat.cd()
ROOT.gPad.SetLogy()
hflat.Draw()


raw_input("continue to the timing corrected plots")
#------------------------------------------------------------------


#adjust the z of the HGTD based on your chosen layer
if layer == 0:
    correction = '((3516.93 - tree.z) * 1/(cos(2*atan(exp(-tree.eta)))))/300'
elif layer == 1:
    correction = '((3525.12 - tree.z) * 1/(cos(2*atan(exp(-tree.eta)))))/300'
elif layer == 2:
    correction = '((3533.33 - tree.z) * 1/(cos(2*atan(exp(-tree.eta)))))/300'
elif layer == 3:
    correction = '((3541.52 - tree.z) * 1/(cos(2*atan(exp(-tree.eta)))))/300'

#plot 20 GeV
c20o = ROOT.TCanvas("c20o", "20GeV_orig")
c20t = ROOT.TCanvas("c20t", "20GeV_test")
c20o.cd()
t20.Draw("hgtd_time", "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c20t.cd()
t20.Draw("hgtd_time - " + correction, "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c20o.SaveAs("time_spread_comparisons/Si/20GeV_Si_layer{0}_orig.png".format(layer))
c20t.SaveAs("time_spread_comparisons/Si/20GeV_Si_layer{0}_test.png".format(layer))

#plot 45 GeV
c45o = ROOT.TCanvas("c45o", "45GeV_orig")
c45t = ROOT.TCanvas("c45t", "45GeV_test")
c45o.cd()
t45.Draw("hgtd_time", "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c45t.cd()
t45.Draw("hgtd_time - " + correction, "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c45o.SaveAs("time_spread_comparisons/Si/45GeV_Si_layer{0}_orig.png".format(layer))
c45t.SaveAs("time_spread_comparisons/Si/45GeV_Si_layer{0}_test.png".format(layer))

#plot 100 GeV
c100o = ROOT.TCanvas("c100o", "100GeV_orig")
c100t = ROOT.TCanvas("c100t", "100GeV_test")
c100o.cd()
t100.Draw("hgtd_time", "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c100t.cd()
t100.Draw("hgtd_time - " + correction, "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c100o.SaveAs("time_spread_comparisons/Si/100GeV_Si_layer{0}_orig.png".format(layer))
c100t.SaveAs("time_spread_comparisons/Si/100GeV_Si_layer{0}_test.png".format(layer))

#plot 20-100 flat GeV
cflato = ROOT.TCanvas("cflato", "20-100GeV_orig")
cflatt = ROOT.TCanvas("cflatt", "20-100GeV_test")
cflato.cd()
tflat.Draw("hgtd_time", "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
cflatt.cd()
tflat.Draw("hgtd_time - " + correction, "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
cflato.SaveAs("time_spread_comparisons/Si/20-100GeV_Si_layer{0}_orig.png".format(layer))
cflatt.SaveAs("time_spread_comparisons/Si/20-100GeV_Si_layer{0}_test.png".format(layer))

#keep the plots alive until you don't want them anymore 
raw_input("press enter to quit")
