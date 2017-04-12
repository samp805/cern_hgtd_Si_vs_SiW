import ROOT 
import numpy as np

tfw20 = ROOT.TFile("withW.root")
tfw45 = ROOT.TFile("withWv4.root")
tfw100 = ROOT.TFile("withWv3.root")
tfwflat = ROOT.TFile("withWv2.root")

t20 = tfw20.Get("tree")
t45 = tfw45.Get("tree")
t100 = tfw100.Get("tree")
tflat = tfwflat.Get("tree")

layer = int(raw_input("which HGTD layer to compare?  "))

#find the average time of the hgtd hits
h20 = ROOT.TH1F("h20", "20 GeV std spread layer {0} of SiW".format(str(layer)), 200, 0, 1)
h45 = ROOT.TH1F("h45", "45 GeV std spread layer {0} of SiW".format(str(layer)), 200, 0, 1)
h100 = ROOT.TH1F("h100", "100 GeV std spread layer {0} of SiW".format(str(layer)), 200, 0, 1)
hflat = ROOT.TH1F("hflat", "flat GeV std spread layer {0} of SiW".format(str(layer)), 200, 0, 1)
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


raw_input("want to continue? probably not")
#------------------------------------------------------------------


if layer == 0:
    correction = '((3506.43 - tree.z) * 1/(cos(2*atan(exp(-tree.eta)))))/300'
elif layer == 1:
    correction = '((3518.12 - tree.z) * 1/(cos(2*atan(exp(-tree.eta)))))/300'
elif layer == 2:
    correction = '((3529.83 - tree.z) * 1/(cos(2*atan(exp(-tree.eta)))))/300'
elif layer == 3:
    correction = '((3541.52 - tree.z) * 1/(cos(2*atan(exp(-tree.eta)))))/300'

c20o = ROOT.TCanvas("c20o", "20GeV_orig")
c20t = ROOT.TCanvas("c20t", "20GeV_test")
c20o.cd()
t20.Draw("hgtd_time", "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c20t.cd()
t20.Draw("hgtd_time - " + correction, "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c20o.SaveAs("time_spread_comparisons/SiW/20GeV_SiW_layer{0}_orig.png".format(layer))
c20t.SaveAs("time_spread_comparisons/SiW/20GeV_SiW_layer{0}_test.png".format(layer))

c45o = ROOT.TCanvas("c45o", "45GeV_orig")
c45t = ROOT.TCanvas("c45t", "45GeV_test")
c45o.cd()
t45.Draw("hgtd_time", "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c45t.cd()
t45.Draw("hgtd_time - " + correction, "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c45o.SaveAs("time_spread_comparisons/SiW/45GeV_SiW_layer{0}_orig.png".format(layer))
c45t.SaveAs("time_spread_comparisons/SiW/45GeV_SiW_layer{0}_test.png".format(layer))

c100o = ROOT.TCanvas("c100o", "100GeV_orig")
c100t = ROOT.TCanvas("c100t", "100GeV_test")
c100o.cd()
t100.Draw("hgtd_time", "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c100t.cd()
t100.Draw("hgtd_time - " + correction, "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
c100o.SaveAs("time_spread_comparisons/SiW/100GeV_SiW_layer{0}_orig.png".format(layer))
c100t.SaveAs("time_spread_comparisons/SiW/100GeV_SiW_layer{0}_test.png".format(layer))

cflato = ROOT.TCanvas("cflato", "20-100GeV_orig")
cflatt = ROOT.TCanvas("cflatt", "20-100GeV_test")
cflato.cd()
tflat.Draw("hgtd_time", "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
cflatt.cd()
tflat.Draw("hgtd_time - " + correction, "hgtd_sampling == {0} && hgtd_time < 1".format(layer))
cflato.SaveAs("time_spread_comparisons/SiW/20-100GeV_SiW_layer{0}_orig.png".format(layer))
cflatt.SaveAs("time_spread_comparisons/SiW/20-100GeV_SiW_layer{0}_test.png".format(layer))

raw_input("press enter to quit")




    

