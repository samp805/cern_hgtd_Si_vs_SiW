OUTPUTDIR=~/work/public/performance_MVA_note
EXEC=~/MVACalib/egammaMVACalibUtils/python/performance.py

# electron
BARREL="( abs(el_cl_eta) < 1.37 )"       
ENDCAP="( abs(el_cl_eta) > 1.52 && abs(el_cl_eta) < 2.47 )"
CUT_ELECTRON="( ($BARREL || $ENDCAP) && (el_truth_E/cosh(el_truth_eta)>5E3) )" 

# photon
BARREL="( abs(ph_cl_eta) < 1.37 )"
ENDCAP="( abs(ph_cl_eta) > 1.52 && abs(ph_cl_eta) < 2.37 )"
CUT_PHOTON="( ($BARREL || $ENDCAP) && (ph_truth_E/cosh(ph_truth_eta)>5E3) )" 


#electron
INPUT_ELECTRON="root://eosatlas.cern.ch//eos/atlas/user/b/blenzi/egammaMVACalibD3PD/user.blenzi.MiniD3PD.v4tmp.mc12_8TeV.184000.ParticleGenerator_e_ETspectrumMVAcalib.e2173_s1748_s1741_r4807_r4540/*.root*"
INPUT_STD_ELECTRON=$INPUT_ELECTRON
INPUT_MVA_ELECTRON=$INPUT_ELECTRON
INPUT_RAW_ELECTRON=$INPUT_ELECTRON
OUTPUT_ELECTRON="$OUTPUTDIR/electron_residuals"
CONVCORRECTION="1"

#photon
INPUT_PHOTON="root://eosatlas.cern.ch//eos/atlas/user/b/blenzi/egammaMVACalibD3PD/user.blenzi.MiniD3PD.v4.mc12_8TeV.184000.ParticleGenerator_gamma_ETspectrumMVAcalib.e2173_s1748_s1741_r4807_r4540/*.root*"
INPUT_STD_PHOTON=$INPUT_PHOTON
INPUT_MVA_PHOTON=$INPUT_PHOTON
INPUT_RAW_PHOTON=$INPUT_PHOTON
CONVCORRECTION="conv_correction"

# electron
CUT=$CUT_ELECTRON
INPUT_STD=$INPUT_STD_ELECTRON
INPUT_MVA=$INPUT_MVA_ELECTRON
INPUT_RAW=$INPUT_RAW_ELECTRON
PPREFIX="el"
OUTPUT=$OUTPUT_ELECTRON

# converted
CUT="$CUT_PHOTON && (ph_Rconv > 0 && ph_Rconv < 800)"
INPUT_STD=$INPUT_STD_PHOTON
INPUT_MVA=$INPUT_MVA_PHOTON
INPUT_RAW=$INPUT_RAW_PHOTON
PPREFIX="ph"
OUTPUT="$OUTPUTDIR/converted_residuals"

# unconverted
CUT="$CUT_PHOTON && (ph_Rconv <= 0 || ph_Rconv >= 800)"
INPUT_STD=$INPUT_STD_PHOTON
INPUT_MVA=$INPUT_MVA_PHOTON
INPUT_RAW=$INPUT_RAW_PHOTON
PPREFIX="ph"
OUTPUT="$OUTPUTDIR/unconverted_residuals"



HIGHENERGY="(${PPREFIX}_truth_E / cosh(${PPREFIX}_truth_eta) > 100E3)"
EACC="(${PPREFIX}_rawcl_Es1+${PPREFIX}_rawcl_Es2+${PPREFIX}_rawcl_Es3)"
CELLINDEXCALO="(TMath::Floor(abs(${PPREFIX}_cl_etaCalo)/0.025))"
ETAMOD="(fmod(abs(${PPREFIX}_cl_eta), 0.025))"
ETAMODCALO="(fmod(abs(${PPREFIX}_cl_etaCalo), 0.025))"
PHIMOD="(abs(${PPREFIX}_cl_eta) < 1.425 ? fmod(abs(${PPREFIX}_cl_phi), TMath::Pi()/512) : fmod(abs(${PPREFIX}_cl_phi), TMath::Pi()/384))"
PHIMODCALO="(abs(${PPREFIX}_cl_eta) < 1.425 ? fmod(abs(${PPREFIX}_cl_phiCalo), TMath::Pi()/512) : fmod(abs(${PPREFIX}_cl_phiCalo), TMath::Pi()/384))"

PHOTONVAR1='-v "${PPREFIX}_Rconv" --var-label "Rconv" --binning "0,100,200,300,400,500,600,700,800" --action 2'
PHOTONVAR2='-v "${PPREFIX}_zconv" --var-label "convz" --binning "-2000,-1000,-800,-600,-400,-200,-100,0,100,200,400,600,800,1000,2000" --action 2'
PHOTONVAR3='-v "(ph_rawcl_Es1+ph_rawcl_Es2+ph_rawcl_Es3)/cosh(ph_cl_eta)/ph_ptconv" --var-label "convEtOverPt" --binning "np.arange(0,2,0.2)" --action 2'
PHOTONVAR4='-v "TMath::Max(ph_pt1conv,ph_pt2conv)/(ph_pt1conv+ph_pt2conv)" --var-label "convPtRatio" --binning "0.4,0.6,0.7,0.8,0.95,1.01" --action 2'

PHOTONVAR="$PHOTONVAR1 $PHOTONVAR2 $PHOTONVAR3 $PHOTONVAR4"
PHOTONVAR=""

python $EXEC \
--histo-binning "np.arange(0.95,1.05,0.002)" \
-o ${OUTPUT}_${OUTPUT_LABEL} \
--title "E/E_{true}" --histo-line 1 --histo-norm \
-Q "${PPREFIX}_cl_E/${PPREFIX}_truth_E*$CONVCORRECTION" --tree MVA -i "$INPUT_STD" --label "std E_{T} > 100 GeV" --cut "$CUT && $HIGHENERGY" --graph-linestyle=1 --graph-marker=20 --graph-linecolor 632 \
-Q "${PPREFIX}_cl_E/${PPREFIX}_truth_E*$CONVCORRECTION" --tree MVA -i "$INPUT_STD" --label "std E_{T} < 100 GeV" --cut "$CUT && !(${HIGHENERGY})" --graph-linestyle=2 --graph-marker=20 --graph-linecolor 624 \
-Q "MVAv10/${PPREFIX}_truth_E" --tree MVA -i "$INPUT_MVA" --label "MVA E_{T} > 100 GeV" --cut "$CUT && $HIGHENERGY" --graph-linestyle=1 --graph-marker=20 --graph-linecolor 600 \
-Q "MVAv10/${PPREFIX}_truth_E" --tree MVA -i "$INPUT_MVA" --label "MVA E_{T} < 100 GeV" --cut "$CUT && !(${HIGHENERGY})" --graph-linestyle=2 --graph-marker=20 --graph-linecolor 592 \
-Q "${EACC}/${PPREFIX}_truth_E*1.05" --tree MVA -i "$INPUT_RAW" --label "raw #times 1.05 E_{T} > 100 GeV" --cut "$CUT && $HIGHENERGY" --graph-linestyle=1 --graph-marker=20 --graph-linecolor 1 \
-Q "${EACC}/${PPREFIX}_truth_E*1.05" --tree MVA -i "$INPUT_RAW" --label "raw #times 1.05 E_{T} < 100 GeV" --cut "$CUT && !(${HIGHENERGY})" --graph-linestyle=2 --graph-marker=20 --graph-linecolor 921 \
-v "abs(${PPREFIX}_cl_eta)" --var-label "#eta Atlas frame" --binning "0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0, 1.1, 1.2, 1.3, 1.425, 1.55, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5" --action 2 \
-v "${PPREFIX}_rphi" --var-label "rphi" --binning "0.9, 0.94, 0.95, 0.955, 0.96, 0.965, 0.97, 0.975, 0.98, 1" --action 2 \
-v "${PPREFIX}_reta" --var-label "reta" --binning "0.9, 0.94, 0.95, 0.955, 0.96, 0.965, 0.97, 0.975, 0.98, 1" --action 2 \
-v "${PPREFIX}_ws3" --var-label "w3" --binning "0.3, 0.5, 0.52, 0.55, 0.57, 0.58, 0.6, 0.65, 0.7, 0.8" --action 2 \
-v "${PPREFIX}_wstot" --var-label "wstot" --binning "0.7, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.0, 2.1, 2.2, 2.3, 2.5, 4" --action 2 \
-v "${PPREFIX}_fside" --var-label "fside" --binning "0, 0.02, 0.1, 0.13, 0.15, 0.16, 0.18, 0.2, 0.22, 0.25, 0.3, 0.4, 0.6" --action 2 \
-v "${PPREFIX}_rawcl_Es1/${EACC}" --var-label "E_{1} fraction" --binning "0, 0.05, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32, 0.34, 0.36, 0.4, 0.45, 0.5, 0.6" --action 2 \
-v "${PPREFIX}_rawcl_Es2/${EACC}" --var-label "E_{2} fraction" --binning "0, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.87, 0.9, 0.92, 0.94, 1" --action 2 \
-v "${PPREFIX}_rawcl_Es3/${EACC}" --var-label "E_{3} fraction" --binning "0, 0.005, 0.007, 0.01, 0.015, 0.02, 0.04, 0.06, 0.1 " --action 2 \
-v "${PPREFIX}_rawcl_Es0/${EACC}" --var-label "presampler fraction" --binning "0, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.07, 0.1, 0.2, 0.3" --action 2 \
-v "${PPREFIX}_calibHitsShowerDepth" --var-label "shower depth" --binning "0,9,10,11,12,12.5,13,13.5,14,15,16,19" --action 2 \
-v "${PPREFIX}_rawcl_Es1/${PPREFIX}_rawcl_Es2" --var-label "E_{1}/E_{2}" --binning "0,0.1,0.13,0.14,0.16,0.18,0.2,0.22,0.24,0.26,0.28,0.3,0.33,0.36,0.4,0.45,0.5,0.55,0.6,0.7,0.8,1.0" --action 2 \
--algo peak_gaussian --algo-line 1 \
--useAtlasStyle --histo-max-depth=0 --no-2d --save-graphs --var-max-depth=1 --nevents=20000


# OSCILLATION

python $EXEC \
--histo-binning "np.arange(0.95,1.05,0.002)" \
-o ${OUTPUT}_${OUTPUT_LABEL}_oscl \
--title "E/E_{true}" --histo-line 1 --histo-norm \
-Q "${PPREFIX}_cl_E/${PPREFIX}_truth_E" --tree MVA -i "$INPUT_STD" --label "std E_{T} > 100 GeV" --cut "$CUT && $HIGHENERGY" --graph-linestyle=1 --graph-marker=20 --graph-linecolor 632 \
-Q "${PPREFIX}_cl_E/${PPREFIX}_truth_E" --tree MVA -i "$INPUT_STD" --label "std E_{T} < 100 GeV" --cut "$CUT && !(${HIGHENERGY})" --graph-linestyle=2 --graph-marker=20 --graph-linecolor 624 \
-Q "MVAv10/${PPREFIX}_truth_E" --tree MVA -i "$INPUT_MVA" --label "MVA E_{T} > 100 GeV" --cut "$CUT && $HIGHENERGY" --graph-linestyle=1 --graph-marker=20 --graph-linecolor 600 \
-Q "MVAv10/${PPREFIX}_truth_E" --tree MVA -i "$INPUT_MVA" --label "MVA E_{T} < 100 GeV" --cut "$CUT && !(${HIGHENERGY})" --graph-linestyle=2 --graph-marker=20 --graph-linecolor 592 \
-Q "${EACC}/${PPREFIX}_truth_E*1.05" --tree MVA -i "$INPUT_RAW" --label "raw #times 1.05 E_{T} > 100 GeV" --cut "$CUT && $HIGHENERGY" --graph-linestyle=1 --graph-marker=20 --graph-linecolor 1 \
-Q "${EACC}/${PPREFIX}_truth_E*1.05" --tree MVA -i "$INPUT_RAW" --label "raw #times 1.05 E_{T} < 100 GeV" --cut "$CUT && !(${HIGHENERGY})" --graph-linestyle=2 --graph-marker=20 --graph-linecolor 921 \
-v "${PPREFIX}_truth_E/cosh(${PPREFIX}_cl_eta)/1e3" --var-label Et  --binning "5,10,15,20,30,35,40,45,50,55,60,65,70,75,80,85,90,100,120,200,250,300,350,400,450,500" --action 2 \
-v "${ETAMODCALO}" --var-label "eta mod calo" --binning "np.linspace(0, 0.025, 20)" --action 2 \
-v "${PHIMODCALO}" --var-label "#phi mod calo" --binning "np.linspace(0, 0.008, 25)" --action 2 \
-v "abs(${PPREFIX}_cl_eta)" --var-label "#eta" --binning "0,0.6,1.425,1.55,1.8,2.5", --action 0 \
--algo truncated_mean --algo-line 1 \
--algo truncated_mean20 --algo-line 1 \
--algo truncated_mean10 --algo-line 1 \
--algo peak_gaussian --algo-line 1 \
--useAtlasStyle --histo-max-depth=0 --no-2d --save-graphs --var-max-depth=2 --nevents=400000

# TIGHT

TIGHT="el_tightPP"
TIGHT="ph_tight"
