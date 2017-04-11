import ROOT

def Normalize(h):
  h.Scale(1./h.GetSumOfWeights())

chain = ROOT.TChain('TestTree')
chain.Add('~/outputs/MVACalibW/photon_flatEt_simple+etaPhiCalo.v4_Eaccordion/MVACalib_unconvertedPhoton_Et*')

f0 = ROOT.TFile('~blenzi/outputs/HggMVA/higgs_analysis_MC12_ggH125_p1196_MCCALIB_ntuple3.root')

f0.MVA.Draw('ph_truth_E/cosh(ph_truth_eta)/1e3 >> h(100, 0, 200)', 'pass_isol && (Iteration$ == index_leading || Iteration$ == index_subleading)')

f0.MVA.Draw('ph_truth_E/cosh(ph_truth_eta)/1e3:abs(ph_cl_eta) >> h2D(50, 0, 2.5,100, 0, 200)', 'pass_isol && (Iteration$ == index_leading || Iteration$ == index_subleading)', 'col,z')
h2D = ROOT.gPad.GetListOfPrimitives()[1].Clone()
Normalize(h2D)

proof = ROOT.TProof.Open('')
chain.SetProof(True)

chain.Draw('ph_truth_E/cosh(ph_truth_eta)/1e3 >> hPt(100, 0, 200)', 'weight_ph_truth_edivcoshph_truth_eta')
chain.Draw('ph_truth_E/cosh(ph_truth_eta)/1e3 >> hMulti(100, 0, 200)', 'weight_multi')
chain.Draw('ph_truth_E/cosh(ph_truth_eta)/1e3 >> hInter(100, 0, 200)', 'weight_inter')

chain.Draw('ph_truth_E/cosh(ph_truth_eta)/1e3:abs(ph_cl_eta) >> h2Total(50, 0, 2.5,100, 0, 200)', 'weight_total', 'col,z')
h2Total = ROOT.gPad.GetListOfPrimitives()[1].Clone()
Normalize(h2Total)

chain.Draw('ph_truth_E/cosh(ph_truth_eta)/1e3:abs(ph_cl_eta) >> h2Multi(50, 0, 2.5,100, 0, 200)', 'weight_multi', 'col,z')
h2Multi = ROOT.gPad.GetListOfPrimitives()[1].Clone()
Normalize(h2Multi)

chain.Draw('ph_truth_E/cosh(ph_truth_eta)/1e3:abs(ph_cl_eta) >> h2Inter(50, 0, 2.5,100, 0, 200)', 'weight_inter', 'col,z')
h2Inter = ROOT.gPad.GetListOfPrimitives()[1].Clone()
Normalize(h2Inter)

hTotalRatio = h2Total.Clone('hTotalRatio')
hTotalRatio.Divide(h2D)

hMultiRatio = h2Total.Clone('hMultiRatio')
hMultiRatio.Divide(h2D)



chain.Draw('weight_ph_truth_edivcoshph_truth_eta:ph_truth_E/cosh(ph_truth_eta)/1e3')