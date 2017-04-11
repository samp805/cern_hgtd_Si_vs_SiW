export ROOT_GEN="/home/sam/workspace/hgtd/rootfiles"
export REGR_GEN="/home/sam/workspace/hgtd/rootfiles/regression_results"

printf "running performance.py suite\n\n"


printf "------generating raw performance plots--------\n"

printf "withw\n"
python performance.py -o ./withW_raw -i $ROOT_GEN/withW.root --tree tree --cut="eta>2.5" -Q "max_energy/(pt*cosh(eta))" --label max_energy -Q "combined2_energy/(pt*cosh(eta))" --label combined2_energy -Q "combined4_energy/(pt*cosh(eta))" --label combined4_energy -Q "combined9_energy/(pt*cosh(eta))" --label combined9_energy --histo-binning "np.linspace(0, 1.2, 1000)" --variable "pt" --var-label momentum --binning="np.linspace(19999, 20001, 10)" --variable "eta" --var-label Eta --binning="np.linspace(2.5, 3.2, 10)" --variable "fmod(phi*32/pi, 1)" --var-label Phi --binning="np.linspace(-1, 1, 10)" --algo mean --algo rms --algo interquartileEff --var-max-depth=1

printf "withoutW\n"
python performance.py -o ./withoutW_raw -i $ROOT_GEN/withoutW.root --tree tree --cut="eta>2.5" -Q "max_energy/(pt*cosh(eta))" --label max_energy -Q "combined2_energy/(pt*cosh(eta))" --label combined2_energy -Q "combined4_energy/(pt*cosh(eta))" --label combined4_energy -Q "combined9_energy/(pt*cosh(eta))" --label combined9_energy --histo-binning "np.linspace(0.4, 1.2, 1000)" --variable "pt" --var-label momentum --binning="np.linspace(19999, 20001, 10)" --variable "eta" --var-label Eta --binning="np.linspace(2.5, 3.2, 10)" --variable "fmod(phi*32/pi, 1)" --var-label Phi --binning="np.linspace(-1, 1, 10)" --algo mean --algo rms --algo interquartileEff --var-max-depth=1
echo
echo

#need to be plotted on logspace
printf "------generating regressed plots with no HGTD info---------\n"
print "withW\n"
#add pt to this later
python performance.py -o ./withW_noHGTD -i $REGR_GEN/TMVAReg_max_energywithW.root --label max_energy --tree dataset/TrainTree -Q "EoverEtrue/BDTG" --histo-binning "np.linspace(0.97,  1.02, 100)" --histo-logy --variable "eta" --var-label Eta --binning="np.linspace(2.5,3.2,10)" --variable "phiMod"  --var-label PhiMod --binning="np.linspace(-1,1,10)" --variable "sumHits" --var-label sumHits --binning="np.linspace(0, 1100, 10)" --algo mean --algo rms --algo interquartileEff --var-max-depth=1 -i $REGR_GEN/TMVAReg_combined2_energywithW.root --label combined2_energy -i $REGR_GEN/TMVAReg_combined4_energywithW.root --label combined4_energy --variable "sumHGTDenergy" --var-label sumHGTDenergy --binning="np.linspace(0, 130, 10)" -i $REGR_GEN/TMVAReg_combined9_energywithW.root --label combined9_energy --cut="eta>2.5"

python performance.py -o ./withoutW_noHGTD -i $REGR_GEN/TMVAReg_max_energywithoutW.root --label max_energy --tree dataset/TrainTree -Q "EoverEtrue/BDTG" --histo-binning "np.linspace(0.97,  1.02, 100)" --histo-logy --variable "eta" --var-label Eta --binning="np.linspace(2.5,3.2,10)" --variable "phiMod"  --var-label PhiMod --binning="np.linspace(-1,1,10)" --variable "sumHits" --var-label sumHits --binning="np.linspace(0, 1100, 10)" --algo mean --algo rms --algo interquartileEff --var-max-depth=1 -i $REGR_GEN/TMVAReg_combined2_energywithoutW.root --label combined2_energy -i $REGR_GEN/TMVAReg_combined4_energywithoutW.root --label combined4_energy --variable "sumHGTDenergy" --var-label sumHGTDenergy --binning="np.linspace(0, 130, 10)" -i $REGR_GEN/TMVAReg_combined9_energywithoutW.root --label combined9_energy --cut="eta>2.5"


#need to be plotted on logspace
printf "-------generating regressed plots with the HGTD info----------------\n"
python performance.py -o ./withW_withHGTD -i $REGR_GEN/TMVAReg_hgtd_max_energywithW.root --label max_energy --tree dataset/TrainTree -Q "EoverEtrue/BDTG" --histo-binning "np.linspace(0.97,  1.02, 100)" --histo-logy --variable "eta" --var-label Eta --binning="np.linspace(2.5,3.2,10)" --variable "phiMod"  --var-label PhiMod --binning="np.linspace(-1,1,10)" --variable "sumHits" --var-label sumHits --binning="np.linspace(0, 1100, 10)" --algo mean --algo rms --algo interquartileEff --var-max-depth=1 -i $REGR_GEN/TMVAReg_hgtd_combined2_energywithW.root --label combined2_energy -i $REGR_GEN/TMVAReg_hgtd_combined4_energywithW.root --label combined4_energy --variable "sumHGTDenergy" --var-label sumHGTDenergy --binning="np.linspace(0, 130, 10)" -i $REGR_GEN/TMVAReg_hgtd_combined9_energywithW.root --label combined9_energy --cut="eta>2.5"

python performance.py -o ./withoutW_withHGTD -i $REGR_GEN/TMVAReg_hgtd_max_energywithoutW.root --label max_energy --tree dataset/TrainTree -Q "EoverEtrue/BDTG" --histo-binning "np.linspace(0.97,  1.02, 100)" --histo-logy --variable "eta" --var-label Eta --binning="np.linspace(2.5,3.2,10)" --variable "phiMod"  --var-label PhiMod --binning="np.linspace(-1,1,10)" --variable "sumHits" --var-label sumHits --binning="np.linspace(0, 1100, 10)" --algo mean --algo rms --algo interquartileEff --var-max-depth=1 -i $REGR_GEN/TMVAReg_hgtd_combined2_energywithoutW.root --label combined2_energy -i $REGR_GEN/TMVAReg_hgtd_combined4_energywithoutW.root --label combined4_energy --variable "sumHGTDenergy" --var-label sumHGTDenergy --binning="np.linspace(0, 130, 10)" -i $REGR_GEN/TMVAReg_hgtd_combined9_energywithoutW.root --label combined9_energy --cut="eta>2.5"

#DO NOT CLOSE THIS WINDOW. !!!!!READ THIS!!!!!!!!
	#change TMVA_regression.py or whatever to add phi, z, & hgtd info as spectators to regression
	#update these tests to use the new spectators
