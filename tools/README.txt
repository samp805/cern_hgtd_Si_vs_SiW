Introduction
============

This tool has been originally developed by Bruno Lenzi <bruno.lenzi@cern.ch> and
Ruggero Turra <ruggero.turra@cern.ch>. It contains some python utilities to deal
with MVA energy calibration. There are two sets of utilities:

   * utilities related to the training of a new MVA calibration
   * utilities to check the performance and producing plots. This second utility
     is quite general and can be used also for other purposes


General description of the MVA calibration
==========================================

For the description of the present calibration and the physics performance see
the internal note: https://cds.cern.ch/record/1609589. Here the needed
information to use the tool are summarized.

Presently electrons, unconverted and converted photons are calibrated
separately. Converted photons are photons with a radius of conversion in (0,
800] mm.


Binning
-------

The present calibration uses a BDT algorithm with gradient boosting. The
calibration is built by many independent calibrations, every one is defined by a
specific region in |eta| x raw_pt, where raw_pt is raw_energy / cosh(eta) and
raw_energy is the sum of the energy in the calorimeter layers. In the present
calibration there are 102 optimization covering the range [0, 2.47] x [0, 50
TeV], the crack [1.37, 1.52] is not calibrated. The reason to split the
calibration is many calibration is performance: particles in different bins
behave in different way, and for unknown reason the algorithm is not able to
understand the difference for larger bins. Of course to reduce the number of
bins is desirable.

This means that the training should be executed 102 times, for every bin in
|eta| x raw_pt. Usually a batch system as LSF, PBS or Condor should be used for
a full calibration.


TMVA training output
--------------------

The output of one training (one bin) is a ROOT file and a XML file. The ROOT
file contains:

    * some inclusive histograms and plots about the performance of the
      optimizations
    * the Train and Test TTree. The branch of these TTree are: the input
      variables, the target variable and the spectator variables. The Test tree
      is usually used to produce performance plots.

The XML contains the configuration of the algorithm (usually called the
weights).


Input and targets
-----------------

The inputs and the target of the optimization can be configured by the python
scripts. For the present list of inputs refers to the internal note. The default
target is not Etrue but the correction to be applied to Eraw: Etrue / Eraw.

For the shower depth do not use the one from D3PD or xAOD, but
recompute is with the add_showerDepth.py utility.

Shifts
------

TMVA algorithm seems to optimize the average response, while we are most
interested to calibrate the peak position of the E / Etrue distribution (even
if it has never been proved to be the optimal solution from a mathematical point
of view). Since the E / Etrue is generally not symmetric the most probable value
(MPV) and the mean are not the same.

The present solution is to compute a set of multiplicative constant to shift the
E / Etrue distribution to center the MPV to 1.


Apply the calibration
---------------------

For testing purpose a tool to apply the calibration exists. This tool is the
same used by egamma, but it can used in a different way. In particular it is
possible to calibrate a ntuple with a generic (different set of inputs,
different algorithm as NN) TMVA optimization. The inputs of this tool are:

    * a folder with all the xml (one for every bin)
    * a ntuple in ROOT format (no xAOD) with all the input variable. The name of
      the branches in the input file must be equal to the name used in the
      training.

The output of the tool is a new ntuple containing a branch with the calibrated
energy. Many different optimization can be applied at the same time. The new
ntuple is friend of the original ntuple, so that it is possible to access to
the branch of the original inputs (the files must stay where they are
originally, if you move it you break the friendship). In addition branches of
the original ntuple can be copied in the new ntuple.


Packaging
---------

When the calibration is ready and validated it can be used by egamma official
packages. To do that the XML file must be converted in a ROOT format (this
reduce the size). A custom class is used to apply the BDT. The interface of the
egamma tools should be adapted do accept a specific set of inputs.


Setup
=====

The recommended setup is:

    export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
    source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

    # if you need a proxy (run this before the ROOT and python setup)
    localSetupEmi
    voms-proxy-init -voms atlas --valid 48:00
    # stop copy-and-paste here since you have to type a password
    
    localSetupROOT --skipConfirm
    localSetupSFT pyanalysis/1.4_python2.7,lapack/3.4.0,blas/20110419
    localSetupSFT pytools/1.8_python2.7

in particular the last lines setup numpy and scipy, widely used in the tools.

All the python scripts can give you help message with -h or --help option.

   ##############################################
   ###   --->>  TEMPORARY WORKAROUND  <<---   ###
   ##############################################

   There is a problem with the latest setup (wrong linking of
   g/ffortran). To avoid it:

    localSetupROOT 5.34.21-x86_64-slc6-gcc47-opt --skipConfirm
    localSetupSFT pyanalysis/1.3_python2.7,lapack/3.4.0,blas/20110419
    localSetupSFT pytools/1.8_python2.7
    localSetupSFT Boost/1.50.0_python2.7

   see: http://cern.ch/go/d8kw

  ################################################


From xAOD to TTree
==================

TMVA can not directly take xAOD sample as inputs. Therefore it is
necessary to convert the xAOD in .root file which contains a flat
TTree (i.e. one entry matches one particle). This is possible using
the RootCore algorithm dumpxAODntuple. This tool have to be run using
the steering macro run_dumpxAODntuple.py which includes several
options. The macro can get as input a .txt file or a Sample Handler
directory. With the option --driver it is possible to chose where the
tool have to run (direct, prooflite, prun, grid). It is also
available a macro (save_grid_SH.py) which gets as input the name of a
sample and saves the connected sample-handler in a folder. For
further information : python run_dumpxAODntuple.py -h python
save_grid_SH.py -h

For example:
    
    cd python
    python save_grid_SH.py --sample mc14_13TeV.184000.ParticleGenerator_e_ETspectrumMVAcalib.merge.AOD.e3145_s1982_s2008_r5721_r5853/ --output my_SH_electron_directory
   
    python run_dumpxAODntuple.py --sampleHandler my_SH_electron_directory --outputsample "user.<YOUR_GRID_NICKNAME>.tmp_electron"
    --particleType 1 --submitDir my_output_dir --flat --driver prun


Training
========

All the scripts to be used are in the python directory. Since some
files are stored remotely on EOS and accessed via xrootd you must have
a valid X509 proxy if you are not on lxplus.


Inputs
------

The dataset used as inputs in the Run1 MVA calibration are:

    * mc12_8TeV.184000.ParticleGenerator_e_ETspectrumMVAcalib.merge.AOD.e2173_s1748_s1741_r4807_r4540/
    * mc12_8TeV.184001.ParticleGenerator_gamma_ETspectrumMVAcalib.merge.AOD.e2173_s1748_s1741_r4807_r4540/

the files have been slimmed and some new variables added. The list of the files
are in the inputs directory.

Adding missing input variables (shower depth)
---------------------------------------------

The shower depth stored in D3PD / xAOD is not the one usually used by
the calibration. For this reason this input variable should be created
before running the training. With this command you can patch all the
files in a directory (you need write access to the ROOT files):

  python add_showerDepth.py -t egamma -i my_folder

after this in all the ROOT files a new TTree called showerDepthTree is
created. This new TTree has only one branch:
(el|ph)_rawcl_calibHitsShowerDepth. The original TTree becomes friend
of the new one, so you can access to the branches of the new TTree
from the original TTree (egamma).

The files used in the following examples have already been patched.

Training example
----------------

python TMVACalib.py -f \
../inputs/example_MiniD3PD.v4tmp.mc12_8TeV.184000.ParticleGenerator_e_ETspectrumMVAcalib.e2173_s1748_s1741_r4807_r4540.txt \
-o first_test -e 1.6,1.7 -E 10,50 -t 3 \
-V clusterEta,accordionE,showerDepth,f0,etaModCalo,cellIndexCalo,phiModCalo

the meaning of the options are described with python TMVACalib.py -h. In this
case the input files are read using xrootd, so it is not needed to run on
lxplus, but a grid certificate is needed. Messages as:

140829 12:40:04 27381 Xrd: XrdClientMessage::ReadRaw: Failed to read header (8 bytes).
140829 12:53:04 26942 Xrd: CheckErrorStatus: Server [lxbse15c06.cern.ch:1094] declared: session not found(error code: 3011)

can be ignored.

The code is usually slow and it seems to be stucked, but if no errors are
prompted it should works. Some speed improvement are possible is the ntuple is
flat (one particle <-> one entry in the TTree).

Some important information are present in the output. 

The selection:

(((((((el_truth_matched)&&(abs(el_cl_E/el_truth_E - 1) < 0.5))&&(abs(el_cl_eta) >= 1.6))&&(abs(el_cl_eta) < 1.7))&&(( el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3)/cosh(el_cl_eta) >= 10e3))&&(( el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3 )/cosh(el_cl_eta) < 50e3))&&(el_author == 1 || el_author == 3))&&(el_loosePP && abs(el_truth_type) == 11)

the default selection is:

    * truth matching
    * very very loose matching between el_cl_E (energy calibrated with the old
      calibration) and the true energy. This is just to avoid patologic case
    * selection on cluster eta, as specified in the command line
    * selection on the raw pt, as specified in the command line
    * author selection (1 or 3)
    * loose selection
    * pdgId == electron

The algorithm: Booking method: BDTG
Number of events: 

    number of events       : 102971  / sum of weights: 102971

this correspond of the number of particle after the flattening (the events are
100000).

The input variables:

--- Id                       : Input : variable 'el_rawcl_f0' (index=0).   <---> Output : variable 'el_rawcl_f0' (index=0).
--- Id                       : Input : variable 'etaModCalo' (index=1).   <---> Output : variable 'etaModCalo' (index=1).
--- Id                       : Input : variable 'cellIndexCalo' (index=2).   <---> Output : variable 'cellIndexCalo' (index=2).
--- Id                       : Input : variable 'el_rawcl_Eacc' (index=3).   <---> Output : variable 'el_rawcl_Eacc' (index=3).
--- Id                       : Input : variable 'el_cl_eta' (index=4).   <---> Output : variable 'el_cl_eta' (index=4).
--- Id                       : Input : variable 'el_rawcl_calibHitsShowerDepth' (index=5).   <---> Output : variable 'el_rawcl_calibHitsShowerDepth' (index=5).
--- Id                       : Input : variable 'phiModCalo' (index=6).   <---> Output : variable 'phiModCalo' (index=6).

it is interesting to look at the range of the variables, sometimes there is some
advantages in trimming variables (newvar = max(min(var, MAX), MIN)) to restrict
the space of the input variable and cut the very long tail of the distributions.

Ranking of the input variable, with different metric (correlation, mutual
information, ...). The best variable usually is el_rawcl_f0 (the fraction of
presampler energy).


Input variables
---------------

The most important thing in an optimization is the set of input variables. These
can be specified with the -V option. The argument are comma separated and they
can be:

    * a formula using the branches, as "el_cl_eta", "(el_cl_eta)>0", "ph_Rconv
      ** 2 + ph_Zconv ** 2"
    * the name of a block. A block is a set of variables, the definition are
    inside TMVACalib.py, for example: middleShapes  = ['ph_rphi', 'ph_reta',
    'ph_weta2']

For example if you want to use wstot instead of the longitudinal shower:

python TMVACalib.py -f \
../inputs/example_MiniD3PD.v4tmp.mc12_8TeV.184000.ParticleGenerator_e_ETspectrumMVAcalib.e2173_s1748_s1741_r4807_r4540.txt \
-o first_test_wstot -e 1.6,1.7 -E 10,50 -t 3 \
-V clusterEta,accordionE,wstot,f0,etaModCalo,cellIndexCalo,phiModCalo


Changing selection
------------------

The script apply a default selection to the events used to train and
to test. For example the standard selection for electron is codified
as:

 <ETA_RAWET_BIN> && <TRUTH_MATCHED> && <STDENERGY_MATCHED> && <PDG_ID_ELECTRON> && <AUTHOR_ELECTRON> && <LOOSE_PP_ELECTRON>

if for example you have a different loose cut you can use the option:

 --cut "<ETA_RAWET_BIN> && <TRUTH_MATCHED> && <STDENERGY_MATCHED> && <PDG_ID_ELECTRON> && <AUTHOR_ELECTRON> && el_my_loose == 1"

if you want to add cut on top of the default selection you can do:

 --cut "<STANDARD_SELECTION> && el_rawcl_Es1 / el_rawcl_Es2 > 0.5"

<STANDARD_SELECTION> is defined according to the particle you want to
calibrate. To get the definition of the predefined cuts use --help-cut


How to run the full calibration
-------------------------------

The command submit_TMVACalib it able to run in parallel different
trainings using several batch system as LSF (the one on lxplus), PBS
or Condor. If you run at CERN, Lyon or Milan it automatically
understand which system you want to use.

Since the data are on EOS at CERN, if you are running outside CERN you
need a valid X509 proxy.

This is for the training of the normal bins:

python submit_TMVACalib.py -q 8nh --etaRange "range(1,6) + range(8, 13)" -t 3 \
  --etRange 0,10,20,40,60,80,120,500,1000,5e4 \
  -V clusterEta,accordionE,showerDepth,f0,etaModCalo,cellIndexCalo,phiModCalo \
  -o full_detector/ \
  -f ../inputs/example_MiniD3PD.v4tmp.mc12_8TeV.184000.ParticleGenerator_e_ETspectrumMVAcalib.e2173_s1748_s1741_r4807_r4540.txt

This for the special bins

python submit_TMVACalib.py -q 8nh --etaRange "0,6" -t 3 \
  --etRange 0,25,50,100,500,1000,5e4 \
  -m BDTG \
  -V clusterEta,accordionE,showerDepth,f0,etaModCalo,cellIndexCalo,phiModCalo \
  -o full_detector \
  -f ../inputs/example_MiniD3PD.v4tmp.mc12_8TeV.184000.ParticleGenerator_e_ETspectrumMVAcalib.e2173_s1748_s1741_r4807_r4540.txt

This for the crack and 2.47<=|eta|<2.5 bins (std cut selection without loose request)

python submit_TMVACalib.py -q 8nh --etaRange "7,13" -t 3 \
  --etRange 0,25,50,100,500,1000,5e4 \
  -m BDTG \
  -V clusterEta,accordionE,showerDepth,f0,etaModCalo,cellIndexCalo,phiModCalo \
  --cut "<ETA_RAWET_BIN> && <TRUTH_MATCHED> && <STDENERGY_MATCHED> && <PDG_ID_ELECTRON> "
  -o full_detector \
  -f ../inputs/example_MiniD3PD.v4tmp.mc12_8TeV.184000.ParticleGenerator_e_ETspectrumMVAcalib.e2173_s1748_s1741_r4807_r4540.txt


Have a look to the help for the explaination of the options. The
script produces ROOT files in the full_detector folder containing the
TrainTree and the TestTree, with the output of the optimization
(branch BDTG). In the folder full_detector/weights the xml files
containing the tuning of the optimization are present.

Using condor on Milan cluster you need few minutes to have the full
calibration for electrons (using the example inputs, ~30 min using the
full inputs).

The log files should be in ../scripts


How to change the binning
-------------------------

submit_TMVACalib.py takes to input for the binning: --etRange and
--etaRange. The first specifies the binning in raw-pt, the second the
binning in absolute eta. For --etRange a list of float must be
provided. For --etaRange there are two cases: if all the comma
separated values are integer their values are interpreted as the index
of an eta-bin. The binning is inside the code (presently) it is:

    eta_bins = [0, 0.05, 0.65, 0.8, 1.0, 1.2, 1.37, 1.52, 1.55, 1.74, 1.82, 2.0, 2.2, 2.47, 2.5]

so --etaRange "0,6" means the bin [0, 0.05] and [1.37, 1.55]. The
second case is it the comma separated value contains a float value. In
this case the argument are interpreted as the edge of the binning. For
example if you want to calibrated with two bin in eta (barrel and
endcap) and three bins it raw-pt:

python submit_TMVACalib.py -q 8nh --etaRange "0, 1.37, 1.55, 2.47" -t 3 \
  --etRange 0,30,50,5e4 \
  -m BDTG \
  -V clusterEta,accordionE,showerDepth,f0,etaModCalo,cellIndexCalo,phiModCalo \
  -o full_detector_few_bins \
  -f ../inputs/example_MiniD3PD.v4tmp.mc12_8TeV.184000.ParticleGenerator_e_ETspectrumMVAcalib.e2173_s1748_s1741_r4807_r4540.txt


Shifts
------

After the TMVA optimization the TMVACalibPostProcessing is
automatically executed. A custom section is written in every xml,
writing some informations as the type of calibration but more
important the position of the peak of the distribution E/Etrue. This
is done for every xml, so for every bin in eta x raw_pt. The most
important quantity is the mean10 (the mean computed in the smallest
window containing 10% of the statistics). This quantity is very close
to the peak, but it is not 1. The inverse of this quantity can be used
as a shift, but a more precise procedure is used. This automatic
procedure is not the suggested one, and it is overwritten by the
procedure in the following paragraph.

The shift is very important at low-pt, since the distribution is more
asymmetric. For this reason the shifts for low-pt are computed for bin
smaller than the ones usually used during the training. In addition
the shifts are computed using all the bins it raw-pt, for a fixed eta
range. For a given eta-range (using the same eta binning of the
optimization) the shifts (mean 10) are computed in small bins in
mva-calibrated-pt and are interpolated with a piecewise
interpolation. To do this:

    python TMVACalibPostProcessing.py --overwrite --doTrainTreeFriend \
    --useCalibratedEt -d full_detector_few_bins/ \
    -c "0, 5, 7, 10, 15, 30, 50, 80" --doGlobal \
    --method spline1 --filter-files "MVACalib_electron*eta0.0-1.37*"

in this case the eta-slice [0, 1.37] is considered. The --ovewrite
option means that the shift information in the xml are
overwritten. The script modifies also the ROOT files (the output of
TMVA) creating a friend tree of the TestTree with one branch for every
shift (Mean20, Mean10, ...) so that is is easy to plot the mva-energy
corrected for the shift. With --doTrainTreeFriend the same is done for
the train tree. --useCalibratedEt means that the shift are paretrized
as a function of the calibrated (mva) pt (and not the raw-pt). -d is
the folder with the ROOT file and the weights directory. "-c" defines
the binning in GeV for pT. --doGlobal means that all the xml are used
according to --filter-files.

This command must be repeated for all the eta slice. A very long
formula should be present at the end of every xml file.

The shifted energy (the corrected one) is: mva_energy / Mean10


Performance check
=================

output file
-----------

TMVA output a ROOT file, in the example:
first_test/MVACalib_electron_Et10-50_eta1.6-1.7_Eaccordion.root. Many plots are
provided by default, but they are inclusive. The TestTree can be used to do
better plots, for example:

    TestTree->Draw("el_rawcl_Eacc * BDTG / el_truth_E - 1")

el_raw_Eacc is the uncalibrated energy, BDTG is the output of the MVA (the
correction to the accordion energy). Average of the response vs presample
fraction:

    TestTree->Draw("el_rawcl_Eacc / el_truth_E - 1:el_rawcl_f0 >> raw(200)", "", "prof")
    raw->SetLineColor(kRed)
    TestTree->Draw("el_rawcl_Eacc * BDTG/ el_truth_E - 1:el_rawcl_f0 >> MVA(200)", "", "profsames")


TMVAGui
-------

    root -l $ROOTSYS/tmva/test/TMVARegGui.C\(\"MVACalib_electron_Et10-50_eta1.6-1.7_Eaccordion.root\"\)

you can get a similar plot (to the last one) with "Regression Output Deviation
versus Input Variables (test sample)"

You can see the correlation with the shower depth with "2a...", select the
shower depth.

The problem with this automatic tools is that they are inclusive, you cannot bin
in eta, pt, ...


performance.py
--------------
This is the most complete method. See detail with python performace.py -h. Use absolute path:

ROOTFILESPATH="/afs/cern.ch/user/t/turra/MVACalib/egammaMVACalibUtils/python/full_detector_few_bins"

python performance.py --histo-binning "np.arange(0.2,1.4,0.05)" \
--histo-norm -o performance_few_bins --title "energy / true energy" --histo-line 1 \
--tree TestTree -i $ROOTFILESPATH/*.root -Q "el_rawcl_Eacc / el_truth_E" --label "raw energy" \
--tree TestTree -i $ROOTFILESPATH/*.root -Q "el_rawcl_Eacc * BDTG / el_truth_E" --label "MVA no shift" \
--tree TestTree -i $ROOTFILESPATH/*.root -Q "el_rawcl_Eacc * BDTG / el_truth_E / Mean10" --label "MVA" \
-v "abs(el_truth_eta)" --binning "np.arange(0, 2.5, 0.05)" --var-label "|true-#eta|" --action 2 \
-v "el_rawcl_f0" --binning "(0, 0.1, 0.2, 0.6)" --var-label "ps fraction" --action 2 \
-v "el_rawcl_calibHitsShowerDepth" --binning "(7, 10, 12, 20)" --var-label "shower depth" --action 1 \
--algo truncated_mean --algo-line 1 \
--algo peak_gaussian --algo-line 1 \
--algo interquartileEff --algo-line None \
--algo madEff --algo-line None \
--algo HSM --algo-line 1 \
--algo EPDFM --algo-line 1 \
--algo modeHistogram --algo-line 1 \
--algo width_smallest_interval --algo-line None \
--algo truncated_rms --algo-line None \
--algo truncated_rms_rel --algo-line None \
--values-max-depth 0 --histo-max-depth 1 --no-2d --useAtlasStyle

usually the performance are quoted with the peak of the gaussian and the
effective interquartile (the others can removed). The most important plot are in
the inclusive directory. In shower_depth directory you can find the plots
divided in three bins of shower depth.


Plot the shifts
---------------

If the shift are present for all the xml files they can be plotted with:

    python plot_shift2.py -r full_detector_few_bins/ -p electron

in addition some other control plots are produced.


How to apply the calibration
============================

The calibration is applied during analysis with the
ElectronPhotonFourMomentumCorrection tool, which is able to apply also
other corrections (layer scale calibration, HV corrections, ...), scale
factors, smearing, systematics, ... The tool incorporate the
egammaMVACalibration tool, which is able to apply the MVA calibration
without additional correction. This tool has some features dedicated
to debug and development. A python script uses it to calibrate all the
electron or photon in a ntuple, creating a new file. The tool is
available at:

svn.cern.ch/reps/atlasoff/Reconstruction/egamma/egammaMVACalib/trunk

this code must be compiled. The recomended way is to setup Analysis
Release with (from the main directory):

    rcSetup Base, 2.0.8

or using latest version (check with rcSetup -r).

   rc find_packages --restrict egammaMVACalib
   rc compile

to execute, example:

   cd MVACalib/egammaMVACalib/python
   python run_egammaMVACalib.py --useTMVA 1 -f --treename egamma \
          -i ../../egammaMVACalibUtils/python/first_test/weights -t 1 \
	  --copyBranches input,el_wstot \
          --shift 0 --spec test_output.root \
          ../../egammaMVACalibUtils/inputs/example_MiniD3PD.v4tmp.mc12_8TeV.184000.ParticleGenerator_e_ETspectrumMVAcalib.e2173_s1748_s1741_r4807_r4540.txt

flag useTMVA 1 means that we want to read the calibration
configuration from XML files, the one generated by TMVA; without this
option the tool search for a ROOT file containing the same information
of the XML files. The option -f specifies that the input is a txt file
containing the path of all the ROOT file inputs. --shift 0 means we
are not applying any shift to the output. --spec add the spectators to
the output ntuple. --copyBranches selects which branch to copy to the
output, input means that all the input variables need be copied. See
-h for more help.

If you open the output file test_output.root you can access to the
calibrated electron:

    MVA->Scan("BDTG:BDTG/el_truth_E", "(abs(el_cl_eta) >=1.6) && (abs(el_cl_eta) < 1.7) && (( el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3)/cosh(el_cl_eta) >= 10e3) && (( el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3 )/cosh(el_cl_eta) < 50e3)")

Usualy it is better to use a training covering the whole detector.


How to converted xml weights to ROOT weights
============================================

To be used in production throught the official tool, the weights in
xml format must be converted in ROOT format. To do that you need the
egammaMVACalib package. For example:

cd egammaMVACalib/python
python xml2Root.py ../../egammaMVACalibUtils/python/full_detector_few_bins/weights . -t 1

see the help with -h
