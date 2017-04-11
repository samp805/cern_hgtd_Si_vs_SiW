python performance.py -Q el_cl_E/el_truth_E --tree TestTree -i /storage/turra/data_MVA/electron_flatEt_simple.v3a_Eaccordion/\*.root -v el_cl_eta --binning 0,0.6,1.4,2.4 --algo mean -o x --histo-binning "np.arange(0.8,1.5,0.01)"

python performance.py -Q el_cl_E/el_truth_E --title "el_cl_E/el_truth_E" --histo-binning "np.arange(0.8,1.5,0.01)" -o x \
--algo mean --compare-formula "x/y" \
--tree TestTree -i /storage/turra/data_MVA/electron_flatEt_simple.v3a_Eaccordion/\*.root --label v3a \
--tree TestTree -i /storage/turra/data_MVA/electron_flatEt_simple.v3_Eaccordion/\*.root --label v3 \
-v "abs(el_cl_eta)" --binning 0,0.6,1.4,2.4 --var-label "|el_cl_eta|" \
-v el_cl_E/1000. --binning 0,20,50,100,200 --var-label el_cl_E

python performance.py -Q "BDTG*el_rawcl_Eacc/el_truth_E" --title "BDTG*el_rawcl_Eacc/el_truth_E" --histo-binning "np.arange(0.8,1.5,0.01)" -o x \
--algo smallestInterval --compare-formula "x/y" \
--algo mean --compare-formula "abs(x-1)-abs(y-1)" \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" \
--algo rms --compare-formula "x/y" \
--tree TestTree -i /storage/turra/data_MVA/electron_flatEt_simple.v3a_Eaccordion/MVACalib_electron_Et80-100_eta0.8-1.0_Eaccordion.root --label "v3+material" \
--tree TestTree -i  /storage/turra/data_MVA/electron_flatEt_simple.v3_Eaccordion/MVACalib_electron_Et80-100_eta0.8-1.0_Eaccordion.root --label v3 \
-v "abs(el_truth_eta)" --binning "0, 0.55, 2.5" --var-label "|el_truth_eta|" \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning 0,160,200 --var-label "el_truth_E/cosh(el_truth_eta)"

# energy from jpsi
python performance.py --histo-binning "np.arange(0.5,1.4,0.01)" -o jpsi --title "energy / true energy" --histo-line 1 \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "el_cl_E / (el_truth_pt * cosh(el_truth_eta))" --label "standard" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "el_MVA0_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVA0" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "el_MVApeak_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVApeak" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "el_MVAmedian_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmedian" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "el_MVAmean10_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmean10" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "el_MVAmean20_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmean20" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
-v "abs(el_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|el_truth_eta|" \
--algo truncated_mean \
--algo peak_gaussian \
--algo width_smallest_interval \
--algo truncated_rms \
--algo truncated_rms_rel

# mass from jpsi
python performance.py --histo-binning "np.arange(1.5,4.2,0.01)" -o jpsi_mass --title "mass" --histo-line 3.096916 \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000." --label "standard" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000. * sqrt(el_MVA0_E[0] / el_cl_E[0] * el_MVA0_E[1] / el_cl_E[1])" --label "MVA0" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000. * sqrt(el_MVApeak_E[0] / el_cl_E[0] * el_MVApeak_E[1] / el_cl_E[1])" --label "MVApeak" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000. * sqrt(el_MVAmedian_E[0] / el_cl_E[0] * el_MVAmedian_E[1] / el_cl_E[1])" --label "MVAmedian" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000. * sqrt(el_MVAmean_E[0] / el_cl_E[0] * el_MVAmean_E[1] / el_cl_E[1])" --label "MVAmean" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000. * sqrt(el_MVAmean10_E[0] / el_cl_E[0] * el_MVAmean10_E[1] / el_cl_E[1])" --label "MVAmean10" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000. * sqrt(el_MVAmean20_E[0] / el_cl_E[0] * el_MVAmean20_E[1] / el_cl_E[1])" --label "MVAmean20" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
-v "(abs(el_cl_eta[0]) > 1.4) + (abs(el_cl_eta[1]) > 1.4)" --var-label "BB / BE / EE" --binning "range(4)" \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference standard \
--algo truncated_skew --compare-formula "x/y" --reference standard \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference standard \
--algo width_smallest_interval --compare-formula "x/y" --reference standard \
--algo truncated_rms --compare-formula "x/y" --reference standard \
--algo truncated_rms_rel --compare-formula "x/y" --reference standard



# energy from jpsi
python performance.py --histo-binning "np.arange(0.5,1.4,0.01)" -o jpsi --title "energy / true energy" --histo-line 1 \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_cl_E / (el_truth_pt * cosh(el_truth_eta))" --label "standard" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVA0_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVA0" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVApeak_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVApeak" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVAmedian_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmedian" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVAmean10_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmean10" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVAmean20_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmean20" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVAmedian10_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmedian10" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVAmedian20_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmedian20" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
-v "abs(el_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|el_truth_eta|" \
--algo truncated_mean --algo-line 1 \
--algo peak_gaussian --algo-line 1 \
--algo width_smallest_interval --algo-line None \
--algo truncated_rms --algo-line None \
--algo truncated_rms_rel --algo-line None

python performance.py --histo-binning "np.arange(0.5,1.4,0.01)" -o jpsi --title "energy / true energy" --histo-line 1 \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVAmean10_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmean10" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVAmean20_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmean20" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVAmedian10_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmedian10" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "el_MVAmedian20_E / (el_truth_pt * cosh(el_truth_eta))" --label "MVAmedian20" --cut "el_truth_pt>7000 && el_MVA0_E!=0" \
-v "abs(el_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|el_truth_eta|" \
--algo truncated_mean --algo-line 1 \
--algo peak_gaussian --algo-line 1 \
--algo width_smallest_interval --algo-line None \
--algo truncated_rms --algo-line None \
--algo truncated_rms_rel --algo-line None


python performance.py --histo-binning "np.arange(1.5,4.2,0.01)" -o jpsi_mass --title "mass" --histo-line 3.096916 \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "Mee/1000. * sqrt(el_MVAmean10_E[0] / el_cl_E[0] * el_MVAmean10_E[1] / el_cl_E[1])" --label "MVAmean10" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "Mee/1000. * sqrt(el_MVAmean20_E[0] / el_cl_E[0] * el_MVAmean20_E[1] / el_cl_E[1])" --label "MVAmean20" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "Mee/1000. * sqrt(el_MVAmedian10_E[0] / el_cl_E[0] * el_MVAmedian10_E[1] / el_cl_E[1])" --label "MVAmedian10" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "/storage/turra/data_MVA/input/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts2.root" -Q "Mee/1000. * sqrt(el_MVAmedian20_E[0] / el_cl_E[0] * el_MVAmedian20_E[1] / el_cl_E[1])" --label "MVAmedian20" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
-v "(abs(el_cl_eta[0]) > 1.4) + (abs(el_cl_eta[1]) > 1.4)" --var-label "BB / BE / EE" --binning "range(4)" \
--algo truncated_mean \
--algo truncated_skew \
--algo peak_gaussian \
--algo width_smallest_interval \
--algo truncated_rms \
--algo truncated_rms_rel


python performance.py --histo-binning "np.arange(1.5,4.2,0.01)" -o jpsi_mass_smal --title "mass" --histo-line 3.096916 \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000." --label "standard" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000. * sqrt(el_MVApeak_E[0] / el_cl_E[0] * el_MVApeak_E[1] / el_cl_E[1])" --label "MVApeak" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000. * sqrt(el_MVAmean10_E[0] / el_cl_E[0] * el_MVAmean10_E[1] / el_cl_E[1])" --label "MVAmean10" --cut "el_truth_pt[1]>7000 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
-v "(abs(el_cl_eta[0]) > 1.4) + (abs(el_cl_eta[1]) > 1.4)" --var-label "BB / BE / EE" --binning "range(4)" \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 3.096916 \
--algo truncated_skew --compare-formula "x/y" --reference standard --algo-line 3.096916 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 3.096916 \
--algo width_smallest_interval --compare-formula "x/y" --reference standard --algo-line 3.096916 \
--algo truncated_rms --compare-formula "x/y" --reference standard --algo-line 3.096916 \
--algo truncated_rms_rel --compare-formula "x/y" --reference standard --algo-line 3.096916 


python performance.py --histo-binning "np.arange(1.5,4.2,0.01)" -o jpsi_mass_small --title "mass" --histo-line 3.096916 \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000." --label "standard" --cut "el_cl_E[0] / cosh(el_tracketa[0]) > 8500 && el_cl_E[1] / cosh(el_tracketa[1]) > 8500 &&  el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000.*1.005" --label "standard_1.3" --cut "el_cl_E[0] / cosh(el_tracketa[0]) > 8500 && el_cl_E[1] / cosh(el_tracketa[1]) > 8500 &&  el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
--tree MVA -i "../../../data/Jsi_v3_simple/calibNtuple.v10.mc11_7TeV.119087.Pythia_direct_Jpsie3e8.merge.NTUP_EGAMMA.e896_s1310_s1300_r3044_r2993_p833+allShifts.root" -Q "Mee/1000. * sqrt(el_MVAmean10_E[0] / el_cl_E[0] * el_MVAmean10_E[1] / el_cl_E[1])" --label "MVAmean10" --cut "el_MVApeak_E[0] / cosh(el_tracketa[0]) > 8500 && el_MVApeak_E[1] / cosh(el_tracketa[1]) > 8500 && el_MVA0_E[0]!=0 && el_MVA0_E[1]!=0" \
-v "(abs(el_cl_eta[0]) > 1.4) + (abs(el_cl_eta[1]) > 1.4)" --var-label "BB / BE / EE" --binning "range(4)" \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 3.096916 \
--algo truncated_skew --compare-formula "x/y" --reference standard --algo-line 3.096916 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 3.096916 \
--algo width_smallest_interval --compare-formula "x/y" --reference standard --algo-line 3.096916 \
--algo truncated_rms --compare-formula "x/y" --reference standard --algo-line 3.096916 \
--algo truncated_rms_rel --compare-formula "x/y" --reference standard --algo-line 3.096916 


# higgs calibration ntuple mass / categories
python performance.py --histo-binning "np.arange(110, 130, .1)" -o higgs_mass2 --title "mass" --histo-line 120 \
--tree calibration_tree -i "../../../../Higgs2/higgs/calibration_tree.root" -Q "mass/1000." --label "standard" --cut "pass_selection && (ph_rawcl_Es1[index_leading] + ph_rawcl_Es2[index_leading] + ph_rawcl_Es3[index_leading])/cosh(ph_cl_eta[index_leading])<200E3 && (ph_rawcl_Es1[index_subleading] + ph_rawcl_Es2[index_subleading] + ph_rawcl_Es3[index_subleading])/cosh(ph_cl_eta[index_subleading])<200E3" \
--tree calibration_tree -i "../../../../Higgs2/higgs/calibration_tree.root" -Q "MVA_masses[0]/1000." --label "NOSHIFT" --cut "pass_selection && (ph_rawcl_Es1[index_leading] + ph_rawcl_Es2[index_leading] + ph_rawcl_Es3[index_leading])/cosh(ph_cl_eta[index_leading])<200E3 && (ph_rawcl_Es1[index_subleading] + ph_rawcl_Es2[index_subleading] + ph_rawcl_Es3[index_subleading])/cosh(ph_cl_eta[index_subleading])<200E3" \
--tree calibration_tree -i "../../../../Higgs2/higgs/calibration_tree.root" -Q "MVA_masses[1]/1000." --label "MEAN10" --cut "pass_selection && (ph_rawcl_Es1[index_leading] + ph_rawcl_Es2[index_leading] + ph_rawcl_Es3[index_leading])/cosh(ph_cl_eta[index_leading])<200E3 && (ph_rawcl_Es1[index_subleading] + ph_rawcl_Es2[index_subleading] + ph_rawcl_Es3[index_subleading])/cosh(ph_cl_eta[index_subleading])<200E3" \
-v "EPS_category" --var-label "EPS category" --binning "range(7)" \
--algo stat --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 120 \
--algo truncated_skew --compare-formula "x/y" --reference standard --algo-line None \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 120 \
--algo width_smallest_interval --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference standard --algo-line None

# higgs calibration ntuple energy leading / EPS categories

python performance.py --histo-binning "np.arange(0.85,1.1,0.002)" -o higgs_energy_leading_EPS --title "higgs_energy_leading" --histo-line 1 \
--tree calibration_tree -i "../../../../Higgs2/higgs/calibration_tree.root" -Q "ph_cl_E[index_leading]/ph_truth_E[index_leading]" --label "ph_cl_E" --cut "pass_selection && (ph_rawcl_Es1[index_leading] + ph_rawcl_Es2[index_leading] + ph_rawcl_Es3[index_leading])/cosh(ph_cl_eta[index_leading])<200E3" \
--tree calibration_tree -i "../../../../Higgs2/higgs/calibration_tree.root" -Q "MVACalib_SIMPLE[index_leading]/ph_truth_E[index_leading]" --label "SIMPLE" --cut "pass_selection && (ph_rawcl_Es1[index_leading] + ph_rawcl_Es2[index_leading] + ph_rawcl_Es3[index_leading])/cosh(ph_cl_eta[index_leading])<200E3" \
--tree calibration_tree -i "../../../../Higgs2/higgs/calibration_tree.root" -Q "MVACalib_R_SHOSHP_CONV[index_leading]/ph_truth_E[index_leading]" --label "NOMAT" --cut "pass_selection && (ph_rawcl_Es1[index_leading] + ph_rawcl_Es2[index_leading] + ph_rawcl_Es3[index_leading])/cosh(ph_cl_eta[index_leading])<200E3" \
-v "EPS_category" --var-label "EPS category" --binning "range(7)" \
--algo stat --compare-formula "x/y" --reference ph_cl_E --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference ph_cl_E --algo-line 1 \
--algo truncated_skew --compare-formula "x/y" --reference ph_cl_E --algo-line None \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference ph_cl_E --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference ph_cl_E --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference ph_cl_E --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference ph_cl_E --algo-line None

# higgs calibration ntuple energy leading / energy / eta / MVACat=0 (unconverted)

python performance.py --histo-binning "np.arange(0.85,1.1,0.002)" -o higgs_energy_leading_unc --title "higgs_energy_leading_unc" --histo-line 1 \
--tree calibration_tree -i "../../../../Higgs2/higgs/calibration_tree.root" -Q "ph_cl_E[index_leading]/ph_truth_E[index_leading]" --label "ph_cl_E" --cut "pass_selection && (ph_rawcl_Es1[index_leading] + ph_rawcl_Es2[index_leading] + ph_rawcl_Es3[index_leading])/cosh(ph_cl_eta[index_leading])<200E3 && MVA_category==0" \
--tree calibration_tree -i "../../../../Higgs2/higgs/calibration_tree.root" -Q "ph_cl_E_Rcorr[index_leading]/ph_truth_E[index_leading]" --label "ph_cl_ECORR" --cut "pass_selection && (ph_rawcl_Es1[index_leading] + ph_rawcl_Es2[index_leading] + ph_rawcl_Es3[index_leading])/cosh(ph_cl_eta[index_leading])<200E3 && MVA_category==0" \
--tree calibration_tree -i "../../../../Higgs2/higgs/calibration_tree.root" -Q "MVACalib_convR_rphi_reta_fside_ws3_convPtRatios_material_etaCalo_phiCalo[index_leading]/ph_truth_E[index_leading]" --label "convR_rphi_reta_fside_ws3_convPtRatios_material_etaCalo_phiCalo" --cut "pass_selection && (ph_rawcl_Es1[index_leading] + ph_rawcl_Es2[index_leading] + ph_rawcl_Es3[index_leading])/cosh(ph_cl_eta[index_leading])<200E3 && MVA_category==0" \
--tree calibration_tree -i "../../../../Higgs2/higgs/calibration_tree.root" -Q "MVACalib_convR_etaPhiCalo[index_leading]/ph_truth_E[index_leading]" --label "MVACalib_convR_etaPhiCalo" --cut "pass_selection && (ph_rawcl_Es1[index_leading] + ph_rawcl_Es2[index_leading] + ph_rawcl_Es3[index_leading])/cosh(ph_cl_eta[index_leading])<200E3 && MVA_category==0" \
-v "abs(ph_truth_eta[index_leading])" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|ph_truth_eta|" \
-v "ph_truth_E[index_leading]/cosh(ph_truth_eta[index_leading])/1000." --binning "np.arange(40,200,10)" --var-label "ph_truth_E/cosh(ph_truth_eta)" \
--algo stat --compare-formula "x/y" --reference ph_cl_ECORR --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference ph_cl_ECORR --algo-line 1 \
--algo truncated_skew --compare-formula "x/y" --reference ph_cl_ECORR --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference ph_cl_ECORR --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference ph_cl_ECORR --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference ph_cl_ECORR --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference ph_cl_ECORR --algo-line None

# single particle gamma
python performance.py --title "BDTG*el_rawcl_Eacc/el_truth_E" --histo-binning "np.arange(0.7,1.3,0.005)" --histo-line 1 \
-o ph_single_particle_vs_raw_energy_vs_true_energy \
--algo width_smallest_interval --compare-formula "x/y" --reference "ph_cl_E+Rcorr" --algo-line None \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "ph_cl_E+Rcorr" --algo-line 1 \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "ph_cl_E+Rcorr" --algo-line 1 \
--algo truncated_rms --compare-formula "x/y" --reference "ph_cl_E+Rcorr" --algo-line None \
--algo stat --compare-formula "x/y" --reference "ph_cl_E+Rcorr" --algo-line None \
--algo truncated_skew --compare-formula "x/y" --reference "ph_cl_E+Rcorr" --algo-line 0 \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i /afs/cern.ch/work/t/turra/convertedPhoton_flatEt_simple.v3+convR_Eaccordion_RPATCHED/\*.root --label "v3+convR" \
-Q "ph_cl_E/ph_truth_E" --tree TestTree -i /afs/cern.ch/work/t/turra/convertedPhoton_flatEt_simple.v3+convR_Eaccordion_RPATCHED/\*.root --label "ph_cl_E" \
-Q "ph_cl_E*conv_correction/ph_truth_E" --tree TestTree -i /afs/cern.ch/work/t/turra/convertedPhoton_flatEt_simple.v3+convR_Eaccordion_RPATCHED/\*.root --label "ph_cl_E+Rcorr" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(40,200,10)" --var-label "ph_truth_pt" \
-v "( ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3 )/cosh(ph_cl_eta)/1000." --binning "np.arange(40,200,10)" --var-label "ph_raw_pt"


# mass from Zee vs BE
python performance.py --histo-binning "np.arange(75,100,0.1)" -o Z_mass --title "mass" --histo-line 91.1876 \
--tree MVA -i "/afs/cern.ch/user/t/turra/eos/atlas/user/t/turra/Zee_weights_electron_flatEt_simple.v3_Eaccordion.root" -Q "Mee/1000." --label "standard" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "/afs/cern.ch/user/t/turra/eos/atlas/user/t/turra/Zee_weights_electron_flatEt_simple.v3_Eaccordion.root" -Q "Mee* sqrt(el_MVAmean10_E[0] / el_cl_E[0] * el_MVAmean10_E[1] / el_cl_E[1])/1000." --label "MVA_mean10" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "/afs/cern.ch/user/t/turra/eos/atlas/user/t/turra/Zee_weights_electron_flatEt_simple.v3_Eaccordion.root" -Q "Mee* sqrt(el_MVA0_E[0] / el_cl_E[0] * el_MVA0_E[1] / el_cl_E[1])/1000." --label "MVA_noshift" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
-v "(abs(el_cl_eta[0]) > 1.4) + (abs(el_cl_eta[1]) > 1.4)" --var-label "BB / BE / EE" --binning "range(4)" \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 91.1876 \
--algo truncated_skew --compare-formula "x/y" --reference standard --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 91.1876 \
--algo width_smallest_interval --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference standard --algo-line None


# mass from Zee vs pileup
python performance.py --histo-binning "np.arange(75,100,0.1)" -o Zee_MC_mass_vs_pileup --title "mass" --histo-line 91.1876 \
--tree MVA -i "/afs/cern.ch/user/t/turra/eos/atlas/user/t/turra/Zee_weights_electron_flatEt_simple.v3_Eaccordion.root" -Q "Mee/1000." --label "standard" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "/afs/cern.ch/user/t/turra/eos/atlas/user/t/turra/Zee_weights_electron_flatEt_simple.v3_Eaccordion.root" -Q "Mee* sqrt(el_MVAmean10_E[0] / el_cl_E[0] * el_MVAmean10_E[1] / el_cl_E[1])/1000." --label "MVA_mean10" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "/afs/cern.ch/user/t/turra/eos/atlas/user/t/turra/Zee_weights_electron_flatEt_simple.v3_Eaccordion.root" -Q "Mee* sqrt(el_MVA0_E[0] / el_cl_E[0] * el_MVA0_E[1] / el_cl_E[1])/1000." --label "MVA_noshift" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
-v "averageIntPerXing" --var-label "mu" --binning "range(42)" \
--algo stat --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 91.1876 \
--algo truncated_skew --compare-formula "x/y" --reference standard --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 91.1876 \
--algo width_smallest_interval --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference standard --algo-line None

# comparing v4 el
python performance.py --title "BDTG*el_rawcl_Eacc/el_truth_E" --histo-binning "np.arange(0.7,1.2,0.004)" --histo-line 1 --histo-logy \
-o el_single_particle_v4 \
-Q "el_cl_E/el_truth_E" --tree TestTree -i /tmp/electron_flatEt_simple.v4_Eaccordion/\*.root --label "std" \
-Q "BDTG*el_rawcl_Eacc/el_truth_E" --tree TestTree -i /tmp/electron_flatEt_simple.v4_Eaccordion/\*.root --label "v4" \
-Q "BDTG*el_rawcl_Eacc/el_truth_E" --tree TestTree -i /tmp/electron_flatEt_simple+etaPhiModCalo.v4_Eaccordion/\*.root --label "v4+EtaPhiModCalo" \
-Q "BDTG*el_rawcl_Eacc/el_truth_E" --tree TestTree -i /tmp/electron_flatEt_simple+rphi+wstot+material+z0.v4_Eaccordion/\*.root --label "v4+shr+material+z0" \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning "np.arange(10,200,10)" --var-label "el_truth_pt" \
-v "abs(el_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|el_truth_eta|" \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "std" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "std" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "std" --algo-line 1 \
--algo truncated_rms --compare-formula "x/y" --reference "ph_cl_E+Rcorr" --algo-line None \
--algo stat --compare-formula "x/y" --reference "std" --algo-line None \
--algo truncated_skew --compare-formula "x/y" --reference "std" --algo-line 0


# comparing v4 ph converted
python performance.py --title "BDTG*ph_rawcl_Eacc/ph_truth_E" --histo-binning "np.arange(0.7,1.2,0.004)" --histo-line 1 --histo-logy \
-o ph_conv_single_particle_v4 \
-Q "ph_cl_E/ph_truth_E" --tree TestTree -i /tmp/photon_flatEt_simple+convR.v4_Eaccordion/MVACalib_converted\*.root --label "std" \
-Q "ph_cl_E/ph_truth_E*conv_correction" --tree TestTree -i /tmp/photon_flatEt_simple.v4_Eaccordion_stdR/MVACalib_converted\*.root --label "std+R" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i /tmp/photon_flatEt_simple+convR.v4_Eaccordion/MVACalib_converted\*.root --label "v4+R" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i /tmp/photon_flatEt_simple+convR+rphi+wstot.v4_Eaccordion/MVACalib_converted\*.root --label "v4+R+shr" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i /tmp/photon_flatEt_simple+convR+rphi+wstot+convPtRatios.v4_Eaccordion/MVACalib_converted\*.root --label "v4+R+shr+convPtRatios" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i /tmp/photon_flatEt_simple+convR+rphi+wstot+convPtRatios+material+etaCalo+phiCalo.v4_Eaccordion/MVACalib_converted\*.root --label "v4+R+shr+convPtRatios+mat" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(10,200,10)" --var-label "ph_truth_pt" \
-v "abs(ph_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|ph_truth_eta|" \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "std+R" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "std+R" --algo-line 1 \
--algo truncated_rms --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo stat --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_skew --compare-formula "x/y" --reference "std+R" --algo-line 0


# comparing v4 ph unconverted
python performance.py --title "BDTG*ph_rawcl_Eacc/ph_truth_E" --histo-binning "np.arange(0.7,1.2,0.004)" --histo-line 1 --histo-logy \
-o ph_unconv_single_particle_v4 \
-Q "ph_cl_E/ph_truth_E" --tree TestTree -i /tmp/photon_flatEt_simple+convR.v4_Eaccordion/MVACalib_unconverted\*.root --label "std" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i /tmp/photon_flatEt_simple+convR.v4_Eaccordion/MVACalib_unconverted\*.root --label "v4" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i /tmp/photon_flatEt_simple+convR+rphi+wstot.v4_Eaccordion/MVACalib_unconverted\*.root --label "v4+shr" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i /tmp/photon_flatEt_simple+convR+rphi+wstot+convPtRatios+material+etaCalo+phiCalo.v4_Eaccordion/MVACalib_unconverted\*.root --label "v4+shr+mat+EtaPhiCalo" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(10,200,10)" --var-label "ph_truth_pt" \
-v "abs(ph_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|ph_truth_eta|" \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "std" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "std" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "std" --algo-line 1 \
--algo truncated_rms --compare-formula "x/y" --reference "std" --algo-line None \
--algo stat --compare-formula "x/y" --reference "std" --algo-line None \
--algo truncated_skew --compare-formula "x/y" --reference "std" --algo-line 0

# mass from Zee vs BE v4
python performance.py --histo-binning "np.arange(75,100,0.1)" -o Z_mass_v4 --title "mass" --histo-line 91.1876 \
--tree MVA -i "~/eos/atlas/user/t/turra/Zee_v4.root" -Q "Mee/1000." --label "standard" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "~/eos/atlas/user/t/turra/Zee_v4.root" -Q "Mee* sqrt(el_MVAmean10_E[0] / el_cl_E[0] * el_MVAmean10_E[1] / el_cl_E[1])/1000." --label "MVA_mean10" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "~/eos/atlas/user/t/turra/Zee_v4.root" -Q "Mee* sqrt(el_MVA0_E[0] / el_cl_E[0] * el_MVA0_E[1] / el_cl_E[1])/1000." --label "MVA_noshift" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "~/eos/atlas/user/b/blenzi/calibNtuple+MVA/calib.v16.mc12_8TeV.147806.PowhegPythia8_AU2CT10_Zee.merge.NTUP_EGAMMA.e1169_s1469_s1470_r3542_r3549_p1032+MVA.v4+rphi+wstot.root"  -Q "Mee* sqrt(el_MVA1_E[0] / el_cl_E[0] * el_MVA1_E[1] / el_cl_E[1])/1000." --label "MVA_mean10+shw" --cut "el_truth_pt[1]>7000 && el_MVA1_E[0]!=0 && el_MVA1_E[1]!=0" \
-v "(abs(el_cl_eta[0]) > 1.4) + (abs(el_cl_eta[1]) > 1.4)" --var-label "BB / BE / EE" --binning "range(4)" \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 91.1876 \
--algo truncated_skew --compare-formula "x/y" --reference standard --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 91.1876 \
--algo width_smallest_interval --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference standard --algo-line None

# mass from Zee vs mu
python performance.py --histo-binning "np.arange(75,100,0.1)" -o Z_pileup_v4 --title "mass" --histo-line 91.1876 \
--tree MVA -i "~/eos/atlas/user/t/turra/Zee_v4.root" -Q "Mee/1000." --label "standard" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "~/eos/atlas/user/t/turra/Zee_v4.root" -Q "Mee* sqrt(el_MVAmean10_E[0] / el_cl_E[0] * el_MVAmean10_E[1] / el_cl_E[1])/1000." --label "MVA_mean10" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "~/eos/atlas/user/t/turra/Zee_v4.root" -Q "Mee* sqrt(el_MVA0_E[0] / el_cl_E[0] * el_MVA0_E[1] / el_cl_E[1])/1000." --label "MVA_noshift" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "~/eos/atlas/user/b/blenzi/calibNtuple+MVA/calib.v16.mc12_8TeV.147806.PowhegPythia8_AU2CT10_Zee.merge.NTUP_EGAMMA.e1169_s1469_s1470_r3542_r3549_p1032+MVA.v4+rphi+wstot.root"  -Q "Mee* sqrt(el_MVA1_E[0] / el_cl_E[0] * el_MVA1_E[1] / el_cl_E[1])/1000." --label "MVA_mean10+shw" --cut "el_truth_pt[1]>7000 && el_MVA1_E[0]!=0 && el_MVA1_E[1]!=0" \
-v "averageIntPerXing" --var-label "mu" --binning "range(42)" \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 91.1876 \
--algo truncated_skew --compare-formula "x/y" --reference standard --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 91.1876 \
--algo width_smallest_interval --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference standard --algo-line None


# mass from Jpsiee vs BE v4
python performance.py --histo-binning "np.arange(1.5,4.2,0.01)" -o Jpsi_mass_v4 --title "mass" --histo-line 3.096916 \
--tree MVA -i "~/eos/atlas/user/t/turra/Jpsi_v4.root" -Q "Mee/1000." --label "standard" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "~/eos/atlas/user/t/turra/Jpsi_v4.root" -Q "Mee* sqrt(el_MVAmean10_E[0] / el_cl_E[0] * el_MVAmean10_E[1] / el_cl_E[1])/1000." --label "MVA_mean10" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
--tree MVA -i "~/eos/atlas/user/t/turra/Jpsi_v4.root" -Q "Mee* sqrt(el_MVA0_E[0] / el_cl_E[0] * el_MVA0_E[1] / el_cl_E[1])/1000." --label "MVA_noshift" --cut "el_truth_pt[1]>7000 && el_MVAmean10_E[0]!=0 && el_MVAmean10_E[1]!=0" \
-v "(abs(el_cl_eta[0]) > 1.4) + (abs(el_cl_eta[1]) > 1.4)" --var-label "BB / BE / EE" --binning "range(4)" \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 3.096916 \
--algo truncated_skew --compare-formula "x/y" --reference standard --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference standard --algo-line 3.096916 \
--algo width_smallest_interval --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference standard --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference standard --algo-line None

# comparing v4 same stat el
python performance.py --title "BDTG*el_rawcl_Eacc/el_truth_E" --histo-binning "np.arange(0.7,1.2,0.004)" --histo-line 1 --histo-logy \
-o el_single_particle_v5_same_sample2 --cut "el_truth_E/cosh(el_truth_eta)>60E3" --histo-norm \
-Q "el_cl_E/el_truth_E" --tree TestTree -i ~/eos/atlas/user/b/blenzi/MVACalib/electron_flatEt_simple.v4_Eaccordion/\*.root --label "std" \
-Q "BDTG*el_rawcl_Eacc/el_truth_E" --tree TestTree -i /tmp/electron_flatEt_simple.v5test_Eaccordion/MVA\*.root --label "v5-same-stat" \
-Q "BDTG*el_rawcl_Eacc/el_truth_E" --tree TestTree -i ~/eos/atlas/user/b/blenzi/MVACalib/electron_flatEt_simple.v4_Eaccordion/\*.root --label "v4" \
-v "el_truth_E/cosh(el_truth_eta)/1000." --binning "np.arange(40,200,10)" --var-label "el_truth_pt" \
-v "abs(el_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|el_truth_eta|" \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "std" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "std" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "std" --algo-line 1 \
--algo truncated_rms --compare-formula "x/y" --reference "ph_cl_E+Rcorr" --algo-line None \
--algo stat --compare-formula "x/y" --reference "std" --algo-line None \
--algo truncated_skew --compare-formula "x/y" --reference "std" --algo-line 0

# comparing stats, all shower shapes
python performance.py --title "BDTG*ph_rawcl_Eacc/ph_truth_E" --histo-binning "np.arange(0.7,1.2,0.004)" --histo-line 1 --histo-norm --histo-logy \
-o v5_stat_unc \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat30/MVACalib_unconvertedPhoton\*.root --label "v5-30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat40/MVACalib_unconvertedPhoton\*.root --label "v5-40" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat50/MVACalib_unconvertedPhoton\*.root --label "v5-50" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat60/MVACalib_unconvertedPhoton\*.root --label "v5-60" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat70/MVACalib_unconvertedPhoton\*.root --label "v5-70" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat80/MVACalib_unconvertedPhoton\*.root --label "v5-80" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat90/MVACalib_unconvertedPhoton\*.root --label "v5-90" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(40,500,10)" --var-label "ph_truth_pt" \
-v "abs(ph_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "eta" \
--algo stat --compare-formula "x/y" --reference "v5-50" --algo-line None \
--algo width_smallest_interval --compare-formula "x/y" --reference "v5-50" --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference "v5-50" --algo-line None

# study migration
python performance.py --title "BDTG*ph_rawcl_Eacc/ph_truth_E" --histo-binning "np.arange(0.7,1.2,0.004)" --histo-line 1 --histo-norm --histo-logy \
-o v5_migration \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat50/MVACalib_unconvertedPhoton_Et0-20_\*.root --label "0-20" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat50/MVACalib_unconvertedPhoton_Et20-40_\*.root --label "20-40" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat50/MVACalib_unconvertedPhoton_Et40-60_\*.root --label "40-60" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat50/MVACalib_unconvertedPhoton_Et60-80_\*.root --label "60-80" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat50/MVACalib_unconvertedPhoton_Et80-140\*.root --label "80-140" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i ~/work/stat50/MVACalib_unconvertedPhoton_Et140-200\*.root --label "140-200" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(0,250,2)" --var-label "ph_truth_pt" \
-v "abs(ph_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "eta" \
--algo stat --algo-line None \
--algo truncated_rms --algo-line None

# unconverted
python performance.py --histo-binning "np.arange(0.85,1.1,0.002)" -o higgs_unc --title "E/E_{true}" --histo-line 1 --histo-norm \
-Q "ph_cl_E/ph_truth_E" --tree TestTree -i "~/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_unconvertedPhoton*.root" --label "std" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_unconvertedPhoton*.root" --label "R+etaPhiCalo" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+material.v4_Eaccordion/MVACalib_unconvertedPhoton*.root" --label "+mat" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+convPtRatios+material.v4_Eaccordion/MVACalib_unconvertedPhoton*.root" --label "+PtRatios" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+rphi+reta+fside+ws3+convPtRatios+material+etaCalo+phiCalo.v4_Eaccordion/MVACalib_unconvertedPhoton*.root" --label "+shw" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "ph_cl_E_Rcorr/ph_truth_E" --label "H ph_cl_ECORR" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==0 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "MVACalib_convR_etaPhiCalo/ph_truth_E" --label "H R+etaPhiCalo" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==0 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "MVACalib_etaPhiCalo_convR_convPtRatios_material/ph_truth_E" --label "H +PtRatios+mat" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==0 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "MVACalib_convR_rphi_reta_fside_ws3_convPtRatios_material_etaCalo_phiCalo/ph_truth_E" --label "H +shw" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==0 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-v "abs(ph_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.37" --var-label "|ph_truth_eta|" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(30,120,10)" --var-label "ph_truth_E/cosh(ph_truth_eta)" \
--algo stat --compare-formula "x/y" --reference "H ph_cl_ECORR" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "H ph_cl_ECORR" --algo-line 1 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "H ph_cl_ECORR" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "H ph_cl_ECORR" --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference "H ph_cl_ECORR" --algo-line None


# converted
python performance.py --histo-binning "np.arange(0.85,1.1,0.002)" -o higgs_conv --title "E/E_{true}" --histo-line 1 --histo-norm \
-Q "ph_cl_E*conv_correction/ph_truth_E" --tree TestTree -i "~/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_convertedPhoton*.root" --label "std+R" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_convertedPhoton*.root" --label "R+etaPhiCalo" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+material.v4_Eaccordion/MVACalib_convertedPhoton*.root" --label "+mat" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+convPtRatios+material.v4_Eaccordion/MVACalib_convertedPhoton*.root" --label "+PtRatios" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+rphi+reta+fside+ws3+convPtRatios+material+etaCalo+phiCalo.v4_Eaccordion/MVACalib_convertedPhoton*.root" --label "+shw" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "ph_cl_E_Rcorr/ph_truth_E" --label "H ph_cl_ECORR" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==1 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "MVACalib_convR_etaPhiCalo/ph_truth_E" --label "H R+etaPhiCalo" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==1 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "MVACalib_etaPhiCalo_convR_convPtRatios_material/ph_truth_E" --label "H +PtRatios+mat" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==1 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "MVACalib_convR_rphi_reta_fside_ws3_convPtRatios_material_etaCalo_phiCalo/ph_truth_E" --label "H +shw" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==1 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-v "abs(ph_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.37" --var-label "|ph_truth_eta|" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(30,120,10)" --var-label "ph_truth_E/cosh(ph_truth_eta)" \
--algo stat --compare-formula "x/y" --reference "H ph_cl_ECORR" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "H ph_cl_ECORR" --algo-line 1 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "H ph_cl_ECORR" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "H ph_cl_ECORR" --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference "H ph_cl_ECORR" --algo-line None


# convertedSiSi

python performance.py --histo-binning "np.arange(0.85,1.1,0.002)" -o higgs_convSiSi --title "E/E_{true}" --histo-line 1 --histo-norm \
-Q "ph_cl_E*conv_correction/ph_truth_E" --tree TestTree -i "~/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "std+R" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "R+etaPhiCalo" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+material.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "+mat" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+convPtRatios+material.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "+PtRatios" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+rphi+reta+fside+ws3+convPtRatios+material+etaCalo+phiCalo.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "+shw" --cut "ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "ph_cl_E_Rcorr/ph_truth_E" --label "H ph_cl_ECORR" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==2 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "MVACalib_convR_etaPhiCalo/ph_truth_E" --label "H R+etaPhiCalo" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==2 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "MVACalib_etaPhiCalo_convR_convPtRatios_material/ph_truth_E" --label "H +PtRatios+mat" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==2 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
--tree calibration_tree -i "~/calibration_tree.root" -Q "MVACalib_convR_rphi_reta_fside_ws3_convPtRatios_material_etaCalo_phiCalo/ph_truth_E" --label "H +shw" --cut "pass_selection && (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)<200E3 && MVA_category==2 && (Iteration$==index_leading || Iteration$==index_subleading) && ph_truth_E/cosh(ph_truth_eta)/1000.<120 && ph_truth_E/cosh(ph_truth_eta)/1000.>30" \
-v "abs(ph_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.37" --var-label "|ph_truth_eta|" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(30,120,10)" --var-label "ph_truth_E/cosh(ph_truth_eta)" \
--algo stat --compare-formula "x/y" --reference "H ph_cl_ECORR" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "H ph_cl_ECORR" --algo-line 1 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "H ph_cl_ECORR" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "H ph_cl_ECORR" --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference "H ph_cl_ECORR" --algo-line None


# unconverted 2 (using ph_cl_eta instead of ph_truth_eta)
python performance.py --histo-binning "np.arange(0.85,1.1,0.002)" -o higgs_unc2 --title "E/E_{true}" --histo-line 1 --histo-norm \
-Q "ph_cl_E*Rcorr/ph_truth_E" --tree MVA -i "~/Hgg_mc12a_MVAv4.new.root" --label "std+R" --cut "MVA!=0 && pass_isol && ph_convFlag%10==0 && (Iteration$==index_leading || Iteration$==index_subleading)" \
-Q "MVA/ph_truth_E" --tree MVA -i "~/Hgg_mc12a_MVAv4.new.root" --label "R+etaPhiCalo" --cut "MVA!=0 && pass_isol && ph_convFlag%10==0 && (Iteration$==index_leading || Iteration$==index_subleading)" \
-Q "MVA_material/ph_truth_E" --tree MVA -i "~/Hgg_mc12a_MVAv4.new.root" --label "R+etaPhiCalo+mat" --cut "MVA!=0 && pass_isol && ph_convFlag%10==0 && (Iteration$==index_leading || Iteration$==index_subleading)" \
-Q "MVA_material_convPt_shapes/ph_truth_E" --tree MVA -i "~/Hgg_mc12a_MVAv4.new.root" --label "R+etaPhiCalo+mat+shw+PtConv" --cut "MVA!=0 && pass_isol && ph_convFlag%10==0 && (Iteration$==index_leading || Iteration$==index_subleading)" \
-v "abs(ph_cl_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|ph_cl_eta|" \
-v "ph_truth_E/cosh(ph_cl_eta)/1000." --binning "np.arange(30,200,10)" --var-label "ph_truth_E/cosh(ph_cl_eta)" \
--algo stat --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "std+R" --algo-line 1 \
--algo truncated_skew --compare-formula "x/y" --reference "std+R" --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "std+R" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference "std+R" --algo-line None


# converted + SiSi 2 (using ph_cl_eta instead of ph_truth_eta)
python performance.py --histo-binning "np.arange(0.85,1.1,0.002)" -o higgs_SiSi2 --title "E/E_{true}" --histo-line 1 --histo-norm \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "R+etaPhiCalo (single)" --cut "" \
-Q "ph_cl_E*Rcorr/ph_truth_E" --tree MVA -i "~/Hgg_mc12a_MVAv4.new.root" --label "std+R" --cut "MVA!=0 && ph_convFlag%10 == 2 && ph_convtrk1nPixHits + ph_convtrk1nSCTHits > 1 && ph_convtrk2nPixHits + ph_convtrk2nSCTHits > 1 && pass_isol && ph_convFlag%10!=0 && (Iteration$==index_leading || Iteration$==index_subleading)" \
-Q "MVA/ph_truth_E" --tree MVA -i "~/Hgg_mc12a_MVAv4.new.root" --label "R+etaPhiCalo" --cut "MVA!=0 &&  ph_convFlag%10 == 2 && ph_convtrk1nPixHits + ph_convtrk1nSCTHits > 1 && ph_convtrk2nPixHits + ph_convtrk2nSCTHits > 1 && pass_isol && ph_convFlag%10!=0 && (Iteration$==index_leading || Iteration$==index_subleading)" \
-Q "MVA_material/ph_truth_E" --tree MVA -i "~/Hgg_mc12a_MVAv4.new.root" --label "R+etaPhiCalo+mat" --cut "MVA!=0 &&  ph_convFlag%10 == 2 && ph_convtrk1nPixHits + ph_convtrk1nSCTHits > 1 && ph_convtrk2nPixHits + ph_convtrk2nSCTHits > 1 && pass_isol && ph_convFlag%10!=0 && (Iteration$==index_leading || Iteration$==index_subleading)" \
-Q "MVA_material_convPt_shapes/ph_truth_E" --tree MVA -i "~/Hgg_mc12a_MVAv4.new.root" --label "R+etaPhiCalo+mat+shw+PtConv" --cut "MVA!=0 &&  ph_convFlag%10 == 2 && ph_convtrk1nPixHits + ph_convtrk1nSCTHits > 1 && ph_convtrk2nPixHits + ph_convtrk2nSCTHits > 1 && pass_isol && ph_convFlag%10!=0 && (Iteration$==index_leading || Iteration$==index_subleading)" \
-v "abs(ph_cl_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|ph_cl_eta|" \
-v "ph_truth_E/cosh(ph_cl_eta)/1000." --binning "np.arange(30,200,10)" --var-label "ph_truth_E/cosh(ph_cl_eta)" \
-v "ph_materialTraversed" --binning "np.arange(0.5,5.5,0.2)" --var-label "material" \
--algo stat --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "std+R" --algo-line 1 \
--algo truncated_skew --compare-formula "x/y" --reference "std+R" --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "std+R" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference "std+R" --algo-line None






# unconverted single
python performance.py --histo-binning "np.arange(0.85,1.1,0.002)" -o single_unc --title "E/E_{true}" --histo-line 1 --histo-norm \
-Q "ph_cl_E/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_unconvertedPhoton*.root" --label "std" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_unconvertedPhoton*.root" --label "R+etaPhiCalo" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+material.v4_Eaccordion/MVACalib_unconvertedPhoton*.root" --label "R+etaPhiCalo+mat" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+convPtRatios+material.v4_Eaccordion/MVACalib_unconvertedPhoton*.root" --label "R+etaPhiCalo+PtRatios+mat" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+rphi+reta+fside+ws3+convPtRatios+material+etaCalo+phiCalo.v4_Eaccordion/MVACalib_unconvertedPhoton*.root" --label "R+etaPhiCalo+mat+shw+PtRatios" --cut "" \
-v "abs(ph_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|ph_truth_eta|" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(20,200,10)" --var-label "ph_truth_E/cosh(ph_truth_eta)" \
--algo stat --compare-formula "x/y" --reference "std" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "std" --algo-line 1 \
--algo truncated_skew --compare-formula "x/y" --reference "std" --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "std" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "std" --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference "std" --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference "std" --algo-line None


# converted single
python performance.py --histo-binning "np.arange(0.85,1.1,0.002)" -o single_conv --title "E/E_{true}" --histo-line 1 --histo-norm \
-Q "ph_cl_E*conv_correction/ph_truth_E" --tree TestTree -i "~/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_convertedPhoton*.root" --label "std+R" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_convertedPhoton*.root" --label "R+etaPhiCalo" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+material.v4_Eaccordion/MVACalib_convertedPhoton*.root" --label "R+etaPhiCalo+mat" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+convPtRatios+material.v4_Eaccordion/MVACalib_convertedPhoton*.root" --label "R+etaPhiCalo+PtRatios+mat" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+rphi+reta+fside+ws3+convPtRatios+material+etaCalo+phiCalo.v4_Eaccordion/MVACalib_convertedPhoton*.root" --label "R+etaPhiCalo+mat+shw+PtRatios" --cut "" \
-v "abs(ph_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|ph_truth_eta|" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(20,200,10)" --var-label "ph_truth_E/cosh(ph_truth_eta)" \
--algo stat --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "std+R" --algo-line 1 \
--algo truncated_skew --compare-formula "x/y" --reference "std+R" --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "std+R" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference "std+R" --algo-line None


# convertedSiSi single

python performance.py --histo-binning "np.arange(0.85,1.1,0.002)" -o single_convSiSi --title "E/E_{true}" --histo-line 1 --histo-norm \
-Q "ph_cl_E*conv_correction/ph_truth_E" --tree TestTree -i "~/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "std+R" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+etaPhiCalo.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "R+etaPhiCalo" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+material.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "R+etaPhiCalo+mat" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+etaPhiCalo+convR+convPtRatios+material.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "R+etaPhiCalo+PtRatios+mat" --cut "" \
-Q "BDTG*ph_rawcl_Eacc/ph_truth_E" --tree TestTree -i "/afs/cern.ch/work/b/blenzi/outputs/MVACalib/photon_flatEt_simple+convR+rphi+reta+fside+ws3+convPtRatios+material+etaCalo+phiCalo.v4_Eaccordion/MVACalib_convertedSiSiPhoton*.root" --label "R+etaPhiCalo+mat+shw+PtRatios" --cut "" \
-v "abs(ph_truth_eta)" --binning "0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.55, 1.6, 1.7,1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --var-label "|ph_truth_eta|" \
-v "ph_truth_E/cosh(ph_truth_eta)/1000." --binning "np.arange(20,200,10)" --var-label "ph_truth_E/cosh(ph_truth_eta)" \
--algo stat --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_mean --compare-formula "abs(x-1)-abs(y-1)" --reference "std+R" --algo-line 1 \
--algo truncated_skew --compare-formula "x/y" --reference "std+R" --algo-line 0 \
--algo peak_gaussian --compare-formula "abs(x-1)-abs(y-1)" --reference "std+R" --algo-line 1 \
--algo width_smallest_interval --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_rms --compare-formula "x/y" --reference "std+R" --algo-line None \
--algo truncated_rms_rel --compare-formula "x/y" --reference "std+R" --algo-line None
