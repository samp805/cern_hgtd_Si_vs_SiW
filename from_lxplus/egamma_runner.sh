#this file is to be ran from Workarea/AnalysisRelease/2.4.27/egammaMVACalib/python

#FOR 100 GeV SAMPLES
#NO HGTD INFORMATION
python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_max_energy_withW100GeV.root $RESULTS/analysis_results/analysis_tree_withWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_max_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,max_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined2_energy_withW100GeV.root $RESULTS/analysis_results/analysis_tree_withWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined2_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,combined2_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined4_energy_withW100GeV.root $RESULTS/analysis_results/analysis_tree_withWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined4_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,combined4_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined9_energy_withW100GeV.root $RESULTS/analysis_results/analysis_tree_withWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined9_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,combined9_energy,hgtd_hits,selected_hgtd_energy"


python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_max_energy_withoutW100GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_max_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,max_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined2_energy_withoutW100GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined2_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,combined2_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined4_energy_withoutW100GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined4_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,combined4_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined9_energy_withoutW100GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined9_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,combined9_energy,hgtd_hits,selected_hgtd_energy"

#FOR 45 GeV SAMPLES
#NO HGTD INFORMATION
python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_max_energy_withW45GeV.root $RESULTS/analysis_results/analysis_tree_withWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_max_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,max_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined2_energy_withW45GeV.root $RESULTS/analysis_results/analysis_tree_withWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined2_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,combined2_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined4_energy_withW45GeV.root $RESULTS/analysis_results/analysis_tree_withWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined4_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,combined4_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined9_energy_withW45GeV.root $RESULTS/analysis_results/analysis_tree_withWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined9_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,combined9_energy,hgtd_hits,selected_hgtd_energy"


python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_max_energy_withoutW45GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_max_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,max_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined2_energy_withoutW45GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined2_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,combined2_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined4_energy_withoutW45GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined4_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,combined4_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined9_energy_withoutW45GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined9_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,combined9_energy,hgtd_hits,selected_hgtd_energy"

#FOR 20 GeV SAMPLES
#NO HGTD INFORMATION
python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_max_energy_withW20GeV.root $RESULTS/analysis_results/analysis_tree_withW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_max_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,max_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined2_energy_withW20GeV.root $RESULTS/analysis_results/analysis_tree_withW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined2_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,combined2_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined4_energy_withW20GeV.root $RESULTS/analysis_results/analysis_tree_withW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined4_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,combined4_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined9_energy_withW20GeV.root $RESULTS/analysis_results/analysis_tree_withW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined9_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,combined9_energy,hgtd_hits,selected_hgtd_energy"


python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_max_energy_withoutW20GeV.root $RESULTS/analysis_results/analysis_tree_withoutW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_max_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,max_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined2_energy_withoutW20GeV.root $RESULTS/analysis_results/analysis_tree_withoutW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined2_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,combined2_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined4_energy_withoutW20GeV.root $RESULTS/analysis_results/analysis_tree_withoutW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined4_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,combined4_energy,hgtd_hits,selected_hgtd_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_noHGTD_combined9_energy_withoutW20GeV.root $RESULTS/analysis_results/analysis_tree_withoutW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/noHGTD_combined9_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,combined9_energy,hgtd_hits,selected_hgtd_energy"


#FOR 100 GeV SAMPLES
#WITH HGTD INFORMATION
python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_max_energy_withW100GeV.root $RESULTS/analysis_results/analysis_tree_withWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_max_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,max_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined2_energy_withW100GeV.root $RESULTS/analysis_results/analysis_tree_withWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined2_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined2_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined4_energy_withW100GeV.root $RESULTS/analysis_results/analysis_tree_withWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined4_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined4_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined9_energy_withW100GeV.root $RESULTS/analysis_results/analysis_tree_withWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined9_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined9_energy"


python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_max_energy_withoutW100GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_max_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,max_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined2_energy_withoutW100GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined2_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined2_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined4_energy_withoutW100GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined4_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined4_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined9_energy_withoutW100GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv3.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined9_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined9_energy"


#FOR 45 GeV SAMPLES
#WITH HGTD INFORMATION
python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_max_energy_withW45GeV.root $RESULTS/analysis_results/analysis_tree_withWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_max_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,max_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined2_energy_withW45GeV.root $RESULTS/analysis_results/analysis_tree_withWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined2_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined2_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined4_energy_withW45GeV.root $RESULTS/analysis_results/analysis_tree_withWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined4_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined4_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined9_energy_withW45GeV.root $RESULTS/analysis_results/analysis_tree_withWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined9_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined9_energy"


python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_max_energy_withoutW45GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_max_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,max_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined2_energy_withoutW45GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined2_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined2_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined4_energy_withoutW45GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined4_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined4_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined9_energy_withoutW45GeV.root $RESULTS/analysis_results/analysis_tree_withoutWv4.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined9_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined9_energy"

#FOR 20 GeV SAMPLES 
#WITH HGTD INFORMATION
python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_max_energy_withW20GeV.root $RESULTS/analysis_results/analysis_tree_withW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_max_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,max_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined2_energy_withW20GeV.root $RESULTS/analysis_results/analysis_tree_withW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined2_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined2_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined4_energy_withW20GeV.root $RESULTS/analysis_results/analysis_tree_withW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined4_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined4_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined9_energy_withW20GeV.root $RESULTS/analysis_results/analysis_tree_withW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined9_energy_withWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined9_energy"


python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_max_energy_withoutW20GeV.root $RESULTS/analysis_results/analysis_tree_withoutW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_max_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar max_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,max_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined2_energy_withoutW20GeV.root $RESULTS/analysis_results/analysis_tree_withoutW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined2_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined2_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined2_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined4_energy_withoutW20GeV.root $RESULTS/analysis_results/analysis_tree_withoutW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined4_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined4_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined4_energy"

python run_egammaMVACalib.py $RESULTS/applied_results/applied_hgtd_combined9_energy_withoutW20GeV.root $RESULTS/analysis_results/analysis_tree_withoutW.root -n analysis_tree --useTMVA True -t 1 -i $RESULTS/regression_results/hgtd_combined9_energy_withoutWv2/weights --energyBin "pt" --etaBin "eta" --initialEnergyVar combined9_energy --copyBranches="pt,eta,hgtd_hits,selected_hgtd_energy,combined9_energy"
