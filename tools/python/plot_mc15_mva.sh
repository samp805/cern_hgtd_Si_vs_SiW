INPUTEL_DC14="/storage_tmp/atlas/MVA2015/outputs1/electron.v1_Eaccordion_5803_noauthor/*.root"
INPUTPH_DC14_conv="/storage_tmp/atlas/MVA2015/outputs1/photon.v1_Eaccordion_5803/MVACalib_convertedPhoton*.root"
INPUTPH_DC14_unconv="/storage_tmp/atlas/MVA2015/outputs1/photon.v1_Eaccordion_5803/MVACalib_unconvertedPhoton*.root"
INPUTPH_DC14_incl="/storage_tmp/atlas/MVA2015/outputs1/photon.v1_Eaccordion_5803/*.root"

INPUTPH_MC12_conv="/storage_tmp/atlas/smanzoni/MVACalib/Bruno_output/photon_newShowerDepth_etaPhiCalo_convR_convPtRatiosB_95.v10_Eaccordion/MVACalib_convertedPhoton*.root"
INPUTPH_MC12_unconv="/storage_tmp/atlas/smanzoni/MVACalib/Bruno_output/photon_newShowerDepth_etaPhiCalo_convR_convPtRatiosB_95.v10_Eaccordion/MVACalib_unconvertedPhoton*.root"
INPUTPH_MC12_incl="/storage_tmp/atlas/smanzoni/MVACalib/Bruno_output/photon_newShowerDepth_etaPhiCalo_convR_convPtRatiosB_95.v10_Eaccordion/*.root"
INPUTEL_MC12="/storage_tmp/atlas/smanzoni/MVACalib/Bruno_output/electron_newShowerDepth_etaPhiCalo_95.v10tmp_Eaccordion/*.root"

INPUTPH_MC15_conv_v2="/storage_tmp/atlas/MVA2015/outputs_mc15/mc15_13TeV_v2.423001_photon/MVACalib_convertedPhoton*.root"
INPUTPH_MC15_unconv_v2="/storage_tmp/atlas/MVA2015/outputs_mc15/mc15_13TeV_v2.423001_photon/MVACalib_unconvertedPhoton*.root"
INPUTPH_MC15_incl_v2="/storage_tmp/atlas/MVA2015/outputs_mc15/mc15_13TeV_v2.423001_photon/*.root"
INPUTEL_MC15_v2="/storage_tmp/atlas/MVA2015/outputs_mc15/mc15_13TeV_v2.423000_electron/*.root"

INPUTPH_MC15_conv_v3="/storage_tmp/atlas/MVA2015/outputs_mc15/mc15_13TeV_v3.423001_photon/MVACalib_convertedPhoton*.root"
INPUTPH_MC15_unconv_v3="/storage_tmp/atlas/MVA2015/outputs_mc15/mc15_13TeV_v3.423001_photon/MVACalib_unconvertedPhoton*.root"
INPUTPH_MC15_incl_v3="/storage_tmp/atlas/MVA2015/outputs_mc15/mc15_13TeV_v3.423001_photon/*.root"
INPUTEL_MC15_v3="/storage_tmp/atlas/MVA2015/outputs_mc15/mc15_13TeV_v3.423000_electron/*.root"

INPUTEL_MC15_online_v2="/storage_tmp/atlas/MVA2015/outputs_mc15/mc15_13TeV_v2.423000_electron_Online/MVACalib*.root*"
INPUTEL_MC15_online_v3="/storage_tmp/atlas/MVA2015/outputs_mc15/mc15_13TeV_v3.423000_electron_Online/MVACalib*.root*"

# converted

python performance.py --histo-binning "np.arange(0.6,1.4,0.01)" --histo-norm -o ~/MVA/plot2015/ph_conv_offline_lin --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTPH_MC15_conv_v2" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_conv_depth" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_MC15_conv_v3" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_conv_E12" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_DC14_conv" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "DC14_conv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 )"  \
--tree TestTree -i "$INPUTPH_MC12_conv" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC12_conv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 )"  \
-v "abs(ph_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(ph_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "ph_truth_pt" --action 2 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,30,80,180,1000" --var-label "pt" --action 1 \
--algo peak_gaussian  --algo-line 1 \
--algo peak_gaussian_minus_one_over_interquartileEff --algo-line 0 \
--algo truncated_mean10 --algo-line 1 \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs


python performance.py --histo-binning "np.arange(0.6,1.4,0.01)" --histo-norm -o ~/MVA/plot2015/ph_conv_offline_res --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTPH_MC15_conv_v2" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_conv_depth" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_MC15_conv_v3" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_conv_E12" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_DC14_conv" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "DC14_conv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 )"  \
--tree TestTree -i "$INPUTPH_MC12_conv" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC12_conv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 )"  \
-v "abs(ph_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(ph_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "ph_truth_pt" --action 2 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,30,80,180,1000" --var-label "pt" --action 1 \
--algo interquartileEff  --compare-formula "x/y" --reference MC15_conv_depth --algo-line None \
--algo rms  --compare-formula "x/y" --reference MC15_conv_depth --algo-line None \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs

# unconverted

python performance.py --histo-binning "np.arange(0.6,1.4,0.01)" --histo-norm -o ~/MVA/plot2015/ph_unconv_peak_offline_lin --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTPH_MC15_unconv_v2" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_unconv depth" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_MC15_unconv_v3" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_unconv E12" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_DC14_unconv" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "DC14_unconv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 )"  \
--tree TestTree -i "$INPUTPH_MC12_unconv" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC12_unconv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 )"  \
-v "abs(ph_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(ph_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "ph_truth_pt" --action 2 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,80,1000" --var-label "pt" --action 1 \
--algo peak_gaussian  --algo-line 1 \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs


python performance.py --histo-binning "np.arange(0.6,1.4,0.01)" --histo-norm -o ~/MVA/plot2015/ph_unconv_peak_offline_res --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTPH_MC15_unconv_v2" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_unconv_depth" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_MC15_unconv_v3" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_unconv_E12" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_DC14_unconv" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "DC14_unconv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 )"  \
--tree TestTree -i "$INPUTPH_MC12_unconv" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC12_unconv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 )"  \
-v "abs(ph_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(ph_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "ph_truth_pt" --action 2 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,30,80,1000" --var-label "pt" --action 1 \
--algo interquartileEff  --compare-formula "x/y" --reference MC15_unconv_depth --algo-line None \
--algo rms  --compare-formula "x/y" --reference MC15_unconv_depth --algo-line None \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs


# photon compare online / offline

python performance.py --histo-binning "np.arange(0.6,1.4,0.01)" --histo-norm -o ~/MVA/plot2015/ph_online_peak_v2 --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTPH_MC15_incl_online_v2" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_inclusive online depth" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_MC15_incl_online_v3" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_inclusive online E12" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
-v "abs(ph_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(ph_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "ph_truth_pt" --action 2 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,80,1000" --var-label "pt" --action 1 \
--algo peak_gaussian  --algo-line 1 \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs

python performance.py --histo-binning "np.arange(0.6,1.4,0.01)" --histo-norm -o ~/MVA/plot2015/ph_online_res_v2 --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTPH_MC15_incl_online_v2" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_inclusive online depth" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_MC15_incl_online_v3" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_inclusive online E12" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_MC15_incl_v2" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_inclusive_depth" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
-v "abs(ph_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(ph_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "ph_truth_pt" --action 2 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,80,1000" --var-label "pt" --action 1 \
--algo interquartileEff  --compare-formula "x/y" --reference MC15_inclusive_depth --algo-line None \
--algo rms  --compare-formula "x/y" --reference MC15_inclusive_depth --algo-line None \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs


# electron linearity

python performance.py --histo-binning "np.arange(0.6,1.4,0.01)" --histo-norm -o ~/MVA/plot2015/el_peak --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTEL_MC15_v2" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC15 depth" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
--tree TestTree -i "$INPUTEL_MC15_v3" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC15 E12" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
--tree TestTree -i "$INPUTEL_DC14" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "DC14" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
--tree TestTree -i "$INPUTEL_MC12" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC12" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
-v "abs(el_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(el_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "el_truth_pt" --action 2 \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning "0,30,80,1000" --var-label "pt" --action 1 \
--algo peak_gaussian  --algo-line 1 \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs



# electron resolution

python performance.py --histo-binning "np.arange(0.6,1.4,0.01)" --histo-norm -o ~/MVA/plot2015/el_res --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTEL_MC15_v2" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC15_depth" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
--tree TestTree -i "$INPUTEL_MC15_v3" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC15 E12" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
--tree TestTree -i "$INPUTEL_DC14" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "DC14" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
--tree TestTree -i "$INPUTEL_MC12" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC12" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
-v "abs(el_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(el_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "el_truth_pt" --action 2 \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning "0,30,80,1000" --var-label "pt" --action 1 \
--algo interquartileEff  --compare-formula "x/y" --reference MC15_depth --algo-line None \
--algo rms  --compare-formula "x/y" --reference MC15_depth --algo-line None \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs


# electron compare online / offline

python performance.py --histo-binning "np.arange(0.6,1.4,0.01)" --histo-norm -o ~/MVA/plot2015/el_online_peak_v2 --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTEL_MC15_online_v2" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC15_el online depth" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTEL_MC15_online_v3" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC15_el online E12" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))"  \
-v "abs(el_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(el_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "el_truth_pt" --action 2 \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning "0,80,1000" --var-label "pt" --action 1 \
--algo peak_gaussian  --algo-line 1 \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs

python performance.py --histo-binning "np.arange(0.6,1.4,0.01)" --histo-norm -o ~/MVA/plot2015/el_online_res_v2 --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTEL_MC15_online_v2" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC15_inclusive online depth" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTEL_MC15_online_v3" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC15_inclusive online E12" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTEL_MC15_v2" -Q "el_rawcl_Eacc * BDTG/ el_truth_E / Mean10" --label "MC15_inclusive_depth" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))"  \
-v "abs(el_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(el_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "el_truth_pt" --action 2 \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning "0,80,1000" --var-label "pt" --action 1 \
--algo interquartileEff  --compare-formula "x/y" --reference MC15_inclusive_depth --algo-line None \
--algo rms  --compare-formula "x/y" --reference MC15_inclusive_depth --algo-line None \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs


# raw energy unconverted
python performance.py --histo-binning "np.arange(0.5,1.2,0.01)" --histo-norm -o ~/MVA/plot2015/ph_unconv_raw_res --title "raw energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTPH_MC15_unconv_v2" -Q "ph_rawcl_Eacc / ph_truth_E" --label "MC15_unconv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_DC14_unconv" -Q "ph_rawcl_Eacc / ph_truth_E" --label "DC14_unconv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_MC12_unconv" -Q "ph_rawcl_Eacc / ph_truth_E" --label "MC12_unconv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
-v "abs(ph_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(ph_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "ph_truth_pt" --action 2 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,30,80,1000" --var-label "pt" --action 1 \
--algo interquartileEff  --compare-formula "x/y" --reference MC15_unconv --algo-line None \
--algo rms  --compare-formula "x/y" --reference MC15_unconv --algo-line None \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs \
--min-ratio=0.9 --max-ratio=1.1


 # raw energy converted
 python performance.py --histo-binning "np.arange(0.5,1.2,0.01)" --histo-norm -o ~/MVA/plot2015/ph_conv_raw_res --title "raw energy / true energy" --histo-line 1 \
 --tree TestTree -i "$INPUTPH_MC15_conv_v2" -Q "ph_rawcl_Eacc / ph_truth_E" --label "MC15_unconv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
 --tree TestTree -i "$INPUTPH_DC14_conv" -Q "ph_rawcl_Eacc / ph_truth_E" --label "DC14_unconv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
 --tree TestTree -i "$INPUTPH_MC12_conv" -Q "ph_rawcl_Eacc / ph_truth_E" --label "MC12_unconv" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
 -v "abs(ph_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
 -v "abs(ph_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
 -v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "ph_truth_pt" --action 2 \
 -v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,30,80,1000" --var-label "pt" --action 1 \
 --algo interquartileEff  --compare-formula "x/y" --reference MC15_unconv --algo-line None \
 --algo rms  --compare-formula "x/y" --reference MC15_unconv --algo-line None \
 --var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs \
 --min-ratio=0.9 --max-ratio=1.1

 # raw energy electron

 python performance.py --histo-binning "np.arange(0.5,1.2,0.01)" --histo-norm -o ~/MVA/plot2015/el_raw_res --title "raw energy / true energy" --histo-line 1 \
 --tree TestTree -i "$INPUTEL_MC15_v2" -Q "el_rawcl_Eacc / el_truth_E" --label "MC15" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
 --tree TestTree -i "$INPUTEL_DC14" -Q "el_rawcl_Eacc / el_truth_E" --label "DC14" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
 --tree TestTree -i "$INPUTEL_MC12" -Q "el_rawcl_Eacc / el_truth_E " --label "MC12" --cut "BDTG!=0 && (el_truth_E/cosh(el_truth_eta)>5E3 ) && ((abs(el_cl_eta) < 1.37) || (abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47))" \
 -v "abs(el_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
 -v "abs(el_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
 -v "el_truth_E/cosh(el_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "el_truth_pt" --action 2 \
 -v "el_truth_E/cosh(el_truth_eta)/1000." --binning "0,30,80,1000" --var-label "pt" --action 1 \
 --algo interquartileEff  --compare-formula "x/y" --reference MC15 --algo-line None \
 --algo rms  --compare-formula "x/y" --reference MC15 --algo-line None \
 --var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs \
 --min-ratio=0.9 --max-ratio=1.1

# check shift converted photons
python performance.py --histo-binning "np.arange(0.7,1.3,0.005)" --histo-norm -o ~/MVA/plot2015/ph_conv_check_shift_mc15 --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTPH_MC15_conv_v3" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC15_conv_E12_shift" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_MC15_conv_v3" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E" --label "MC15_conv_E12_noshift" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
-v "abs(ph_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(ph_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "ph_truth_pt" --action 2 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,20,30,80,180,1000" --var-label "pt" --action 1 \
--algo peak_gaussian  --algo-line 1 \
--algo truncated_mean10 --algo-line 1 \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs

python performance.py --histo-binning "np.arange(0.7,1.3,0.005)" --histo-norm -o ~/MVA/plot2015/ph_conv_check_shift_mc12 --title "energy / true energy" --histo-line 1 \
--tree TestTree -i "$INPUTPH_MC12_conv" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E / Mean10" --label "MC12 shift" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
--tree TestTree -i "$INPUTPH_MC12_conv" -Q "ph_rawcl_Eacc * BDTG/ ph_truth_E" --label "MC12 noshift" --cut "BDTG!=0 && (ph_truth_E/cosh(ph_truth_eta)>5E3 ) && ((abs(ph_cl_eta) < 1.37) || (abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.47))"  \
-v "abs(ph_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "abs(ph_truth_eta)" --binning "0,1.37,1.52,2.47" --var-label "|#eta|" --action 1 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,10,20,40,60,80,100,150,200,300,400,600,800,1000" --var-label "ph_truth_pt" --action 2 \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "0,20,30,80,180,1000" --var-label "pt" --action 1 \
--algo peak_gaussian  --algo-line 1 \
--algo truncated_mean10 --algo-line 1 \
--var-max-depth 2 --histo-max-depth 1 --no-2d --useAtlasStyle --save-graphs
