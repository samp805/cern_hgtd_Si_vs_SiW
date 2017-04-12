#to be run from Workarea/AnalysisRelease/2.4.27/egammaMVACalibUtils/python

#NO HGTD INFORMATION
python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/noHGTD_max_energy_withWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/max_energy" --variables "eta,max_energy" $RESULTS/analysis_results/analysis_tree_withWv2.root --cut "" --spectators="hgtd_hits,selected_hgtd_energy"

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/noHGTD_combined2_energy_withWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined2_energy" --variables "eta,combined2_energy" $RESULTS/analysis_results/analysis_tree_withWv2.root --cut "" --spectators "hgtd_hits,selected_hgtd_energy"

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/noHGTD_combined4_energy_withWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined4_energy" --variables "eta,combined4_energy" $RESULTS/analysis_results/analysis_tree_withWv2.root --cut "" --spectators "hgtd_hits,selected_hgtd_energy"

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/noHGTD_combined9_energy_withWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined9_energy" --variables "eta,combined9_energy" $RESULTS/analysis_results/analysis_tree_withWv2.root --cut "" --spectators "hgtd_hits,selected_hgtd_energy"


python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/noHGTD_max_energy_withoutWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/max_energy" --variables "eta,max_energy" $RESULTS/analysis_results/analysis_tree_withoutWv2.root --cut "" --spectators "hgtd_hits,selected_hgtd_energy"

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/noHGTD_combined2_energy_withoutWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined2_energy" --variables "eta,combined2_energy" $RESULTS/analysis_results/analysis_tree_withoutWv2.root --cut "" --spectators "hgtd_hits,selected_hgtd_energy"

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/noHGTD_combined4_energy_withoutWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined4_energy" --variables "eta,combined4_energy" $RESULTS/analysis_results/analysis_tree_withoutWv2.root --cut "" --spectators "hgtd_hits,selected_hgtd_energy"

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/noHGTD_combined9_energy_withoutWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined9_energy" --variables "eta,combined9_energy" $RESULTS/analysis_results/analysis_tree_withoutWv2.root --cut "" --spectators "hgtd_hits,selected_hgtd_energy"

#WITH HGTD INFORMATION
python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/hgtd_max_energy_withWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/max_energy" --variables "eta,max_energy,hgtd_hits,selected_hgtd_energy" $RESULTS/analysis_results/analysis_tree_withWv2.root --cut "" --spectators ""

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/hgtd_combined2_energy_withWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined2_energy" --variables "eta,combined2_energy,hgtd_hits,selected_hgtd_energy" $RESULTS/analysis_results/analysis_tree_withWv2.root --cut "" --spectators ""

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/hgtd_combined4_energy_withWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined4_energy" --variables "eta,combined4_energy,hgtd_hits,selected_hgtd_energy" $RESULTS/analysis_results/analysis_tree_withWv2.root --cut "" --spectators ""

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/hgtd_combined9_energy_withWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined9_energy" --variables "eta,combined9_energy,hgtd_hits,selected_hgtd_energy" $RESULTS/analysis_results/analysis_tree_withWv2.root --cut "" --spectators ""


python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/hgtd_max_energy_withoutWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/max_energy" --variables "eta,max_energy,hgtd_hits,selected_hgtd_energy" $RESULTS/analysis_results/analysis_tree_withoutWv2.root --cut "" --spectators ""

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/hgtd_combined2_energy_withoutWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined2_energy" --variables "eta,combined2_energy,hgtd_hits,selected_hgtd_energy" $RESULTS/analysis_results/analysis_tree_withoutWv2.root --cut "" --spectators ""

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/hgtd_combined4_energy_withoutWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined4_energy" --variables "eta,combined4_energy,hgtd_hits,selected_hgtd_energy" $RESULTS/analysis_results/analysis_tree_withoutWv2.root --cut "" --spectators ""

python TMVACalib.py -n analysis_tree  -o $RESULTS/regression_results/hgtd_combined9_energy_withoutWv2 --etaRange "2.5,3.2" --etRange "0,100000" --particleType=3 --target="pt*cosh(eta)/combined9_energy" --variables "eta,combined9_energy,hgtd_hits,selected_hgtd_energy" $RESULTS/analysis_results/analysis_tree_withoutWv2.root --cut "" --spectators ""
