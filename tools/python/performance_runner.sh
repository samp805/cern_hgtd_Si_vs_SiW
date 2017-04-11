#IMPORTANT, ADD PHI TO EVERYTHING, not just performance stuff. Training too

#noHGTD 20 GeV withW
python performance.py \
-o $RESULTS/performance_results/noHGTD_20GeV_withW \
--tree MVA \
-i $RESULTS/applied_results/applied_noHGTD_max_energy_withW20GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined2_energy_withW20GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined4_energy_withW20GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined9_energy_withW20GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(20000-10, 20000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,1200,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#noHGTD 20 GeV withoutW
python performance.py \
-o $RESULTS/performance_results/noHGTD_20GeV_withoutW \
--tree MVA \
-i $RESULTS/applied_results/applied_noHGTD_max_energy_withoutW20GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined2_energy_withoutW20GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined4_energy_withoutW20GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined9_energy_withoutW20GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(20000-10, 20000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,350,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#noHGTD 45 GeV withW
python performance.py \
-o $RESULTS/performance_results/noHGTD_45GeV_withW \
--tree MVA \
-i $RESULTS/applied_results/applied_noHGTD_max_energy_withW45GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined2_energy_withW45GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined4_energy_withW45GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined9_energy_withW45GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(45000-10, 45000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,1600,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#noHGTD 45 GeV withoutW
python performance.py \
-o $RESULTS/performance_results/noHGTD_45GeV_withoutW \
--tree MVA \
-i $RESULTS/applied_results/applied_noHGTD_max_energy_withoutW45GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined2_energy_withoutW45GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined4_energy_withoutW45GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined9_energy_withoutW45GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(45000-10, 45000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,450,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#noHGTD 100 GeV withW
python performance.py \
-o $RESULTS/performance_results/noHGTD_100GeV_withW \
--tree MVA \
-i $RESULTS/applied_results/applied_noHGTD_max_energy_withW100GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined2_energy_withW100GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined4_energy_withW100GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined9_energy_withW100GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(100000-10, 100000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,2000,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#noHGTD 100 GeV withoutW
python performance.py \
-o $RESULTS/performance_results/noHGTD_100GeV_withoutW \
--tree MVA \
-i $RESULTS/applied_results/applied_noHGTD_max_energy_withoutW100GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined2_energy_withoutW100GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined4_energy_withoutW100GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_noHGTD_combined9_energy_withoutW100GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(100000-10, 100000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,650,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#------------------------------------------------

#withHGTD 20 GeV withW
python performance.py \
-o $RESULTS/performance_results/hgtd_20GeV_withW \
--tree MVA \
-i $RESULTS/applied_results/applied_hgtd_max_energy_withW20GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_hgtd_combined2_energy_withW20GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_hgtd_combined4_energy_withW20GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_hgtd_combined9_energy_withW20GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(20000-10, 20000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,2000,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#withHGTD 20 GeV withoutW
python performance.py \
-o $RESULTS/performance_results/hgtd_20GeV_withoutW \
--tree MVA \
-i $RESULTS/applied_results/applied_hgtd_max_energy_withoutW20GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_hgtd_combined2_energy_withoutW20GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_hgtd_combined4_energy_withoutW20GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_hgtd_combined9_energy_withoutW20GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(20000-10, 20000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,1000,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#withHGTD 45 GeV withW
python performance.py \
-o $RESULTS/performance_results/hgtd_45GeV_withW \
--tree MVA \
-i $RESULTS/applied_results/applied_hgtd_max_energy_withW45GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_hgtd_combined2_energy_withW45GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_hgtd_combined4_energy_withW45GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_hgtd_combined9_energy_withW45GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(45000-10, 45000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,1600,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#withHGTD 45 GeV withoutW
python performance.py \
-o $RESULTS/performance_results/hgtd_45GeV_withoutW \
--tree MVA \
-i $RESULTS/applied_results/applied_hgtd_max_energy_withoutW45GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_hgtd_combined2_energy_withoutW45GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_hgtd_combined4_energy_withoutW45GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_hgtd_combined9_energy_withoutW45GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(45000-10, 45000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,450,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#withHGTD 100 GeV withW
python performance.py \
-o $RESULTS/performance_results/hgtd_100GeV_withW \
--tree MVA \
-i $RESULTS/applied_results/applied_hgtd_max_energy_withW100GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_hgtd_combined2_energy_withW100GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_hgtd_combined4_energy_withW100GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_hgtd_combined9_energy_withW100GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(100000-10, 100000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,2000,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 

#withHGTD 100 GeV withoutW
python performance.py \
-o $RESULTS/performance_results/hgtd_100GeV_withoutW \
--tree MVA \
-i $RESULTS/applied_results/applied_hgtd_max_energy_withoutW100GeV.root \
--label max_energy \
-i $RESULTS/applied_results/applied_hgtd_combined2_energy_withoutW100GeV.root \
--label combined2_energy \
-i $RESULTS/applied_results/applied_hgtd_combined4_energy_withoutW100GeV.root \
--label combined4_energy \
-i $RESULTS/applied_results/applied_hgtd_combined9_energy_withoutW100GeV.root \
--label combined9_energy \
--quantity="output_energy/(pt*cosh(eta))" \
--histo-binning="np.linspace(.5, 1.5, 100)" \
--variable="eta" \
--var-label Eta \
--binning="np.linspace(2.5,3.2,10)" \
--variable="pt" \
--var-label Momentum \
--binning="np.linspace(100000-10, 100000+10, 10)" \
--variable="hgtd_hits" \
--var-label numHits \
--binning="np.linspace(0,650,10)" \
--variable="selected_hgtd_energy" \
--var-label selected_hgtd_energy \
--binning="np.linspace(0,1,10)" \
--algo=mean --algo=rms --algo=interquartileEff \
--var-max-depth=1 \
--cut="eta>2.5" 
