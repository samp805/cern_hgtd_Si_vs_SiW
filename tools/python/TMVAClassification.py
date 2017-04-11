#!/usr/bin/env python

__doc__ = "To run MVA regression for photon / electron calibration"
__author__ = "Bruno Lenzi <Bruno.Lenzi@cern.ch>"

import ROOT

def create_TChain(inputfiles, treename):
  chain = ROOT.TChain(treename)
  for inputfile in inputfiles:
    chain.Add(inputfile)
  return chain

def create_file_list(list_filename, dataset_name):
  f = ROOT.TFile(list_filename)
  file_collection = f.Get(dataset_name)
  urls = map(lambda x: x.GetFirstUrl().GetUrl(), file_collection.GetList())
  return (file_collection.GetDefaultTreeName(), urls)

def TMVACalib(name, outfileName, input_chain, etaBin, methods='BDT,MLP', photonType=2, doFullCalibration=False):
  
  if not isinstance(methods, list):
    methods = methods.split(',')
  
  if not outfileName:
    outfileName = name + '.root'
  
  # Define the type of photon
  doConversions = photonType in [1,2]
  doSiSiConversions = (photonType == 2)
  
  ######################################################
  # Open files and create factory
  ######################################################
  from ROOT import TMVA  
  
  output_file = ROOT.TFile(outfileName, 'recreate')
  
  factory = TMVA.Factory(name, output_file);
  # factory.AddRegressionTree(input_chain);
  factory.AddSignalTree    ( input_chain );
  factory.AddBackgroundTree    ( input_chain );
  
  
  ######################################################
  # Define the selection
  ######################################################
  
  selection = ROOT.TCut("ph_loose && ph_truth_matched")
  selection += "abs(ph_cl_eta) > 0.012 && abs(ph_cl_eta) < 2.47"
  selection += "(abs(ph_cl_eta) < 1.37 || abs(ph_cl_eta) > 1.52)"
  selection += "abs(ph_cl_E/ph_truth_E - 1) < 0.5";
  
  if doSiSiConversions:
    selection += "ph_convFlag%10 == 2 && ph_convtrk1nPixHits + ph_convtrk1nSCTHits > 1 && ph_convtrk2nPixHits + ph_convtrk2nSCTHits > 1"; # Si+Si conversions
  elif doConversions:
    selection += "(ph_convFlag%10 == 1 || (ph_convFlag%10 == 2 && (ph_convtrk1nPixHits + ph_convtrk1nSCTHits == 0 || ph_convtrk2nPixHits + ph_convtrk2nSCTHits == 0)))"
  else:
    selection += "ph_convFlag%10 == 0"

  if etaBin is not None:
    try:
      etaBin = int(etaBin)
      eta_bins = [0, 0.65, 0.8, 1.0, 1.2, 1.37, 1.55, 1.74, 1.82, 2.0, 2.2, 2.47]      
      # if eta_bins[etaBin] == 1.37:
      #   etaBin -= 1
      selection += "abs(ph_cl_eta) > %s && abs(ph_cl_eta) < %s" % (eta_bins[etaBin], eta_bins[etaBin+1])
    except ValueError:
      selection += "abs(ph_cl_eta) > %s && abs(ph_cl_eta) < %s" % tuple(etaBin.split(','));

  ######################################################
  # Define variables, spectators, target
  ######################################################  
  # Add calibrated energy or raw energies and define target
#   if not doFullCalibration:
#     # factory.AddVariable("ph_cl_E", 'F');
#     # factory.AddTarget("K := ph_truth_E/ph_cl_E", "Correction");
#   else:
#     factory.AddVariable("ph_rawcl_Es0", 'F');
#     factory.AddVariable("ph_rawcl_Es1", 'F');
#     factory.AddVariable("ph_rawcl_Es2", 'F');
#     factory.AddVariable("ph_rawcl_Es3", 'F');
#     factory.AddTarget("ph_truth_E", "True energy", "MeV");  
  
  # Shower depth
  factory.AddVariable("ph_calibHitsShowerDepth", 'F');
  factory.AddVariable("f0 := ph_rawcl_Es0/( ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3 )")
  
  # Raw energies
  #     factory.AddVariable("ph_rawcl_Es0", 'F');
  #     factory.AddVariable("ph_rawcl_Es1", 'F');
  #     factory.AddVariable("ph_rawcl_Es2", 'F');
  #     factory.AddVariable("ph_rawcl_Es3", 'F');
  
  # E0, Eaccordion, X (longitudinal barycenter)    
  #     factory.AddVariable("ph_rawcl_Es0", 'F');
  #     factory.AddVariable("ph_rawcl_Es1", 'F');
  #     factory.AddVariable("ph_rawcl_Es2", 'F');
  #     factory.AddVariable("ph_rawcl_Es3", 'F');        
  #      factory.AddVariable("ph_raw_Eacc := ( ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3 )");
  #    factory.AddVariable("ph_E1overE2 := ph_rawcl_Es1 / ph_rawcl_Es2", 'F'); # . highly correlated with E0 and X
  
  # Positions
  #     factory.AddVariable("ph_cl_eta", 'F');
  #     factory.AddVariable("ph_cl_phi", 'F');
  
  # Shower shapes: middle layer
  factory.AddVariable("ph_rphi", 'F');
  factory.AddVariable("ph_reta", 'F');
  factory.AddVariable("ph_weta2", 'F');
  
  # Shower shapes: strips
  factory.AddVariable("ph_wstot", 'F', 0, 100.);
  factory.AddVariable("ph_fside", 'F', 0., 1.);
  factory.AddVariable("ph_ws3", 'F', 0., 100.);
  
  # Conversion info
  if doConversions:
    factory.AddVariable("ph_Rconv", 'F');
  if doSiSiConversions:
    factory.AddVariable("ph_ptconv", 'F');
    factory.AddVariable("ph_pt1conv", 'F');
    factory.AddVariable("ph_pt2conv", 'F');
    factory.AddVariable("ph_convMatchDeltaPhi1", 'F');
    factory.AddVariable("ph_convMatchDeltaPhi2", 'F');
  #     factory.AddVariable("ph_convTrk1_DeltaPhi_track_calo", 'F');
  #     factory.AddVariable("ph_convTrk2_DeltaPhi_track_calo", 'F');
  
  #----------- Spectators -----------------
  factory.AddSpectator("ph_loose", 'I');
  factory.AddSpectator("ph_tight", 'I');
  
  if doFullCalibration:
    factory.AddSpectator("ph_cl_E", 'F');
  else:
    factory.AddSpectator("ph_truth_E", 'F');
  
  factory.AddSpectator("ph_truth_eta", 'F');
  factory.AddSpectator("ph_truth_phi", 'F');
  factory.AddSpectator("ph_cl_eta", 'F');
  factory.AddSpectator("ph_cl_phi", 'F');
  
  #     factory.AddSpectator("ph_rawcl_Es0", 'F');
  #     factory.AddSpectator("ph_rawcl_Es1", 'F');
  #     factory.AddSpectator("ph_rawcl_Es2", 'F');
  #     factory.AddSpectator("ph_rawcl_Es3", 'F');
  #     factory.AddSpectator("ph_raw_Eacc := ( ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3 )");    
  
  
  
  sshapeVariables = "ph_rphi:ph_reta:ph_weta2:ph_wstot:ph_fside:ph_ws3";
  convVariables = "ph_Rconv:ph_ptconv:ph_pt1conv:ph_pt2conv:ph_convMatchDeltaPhi1:ph_convMatchDeltaPhi2";
  allVariables = sshapeVariables + ":" + convVariables;
  
  ######################################################
  # Add methods and run
  ######################################################  
  
  mycuts = selection + ROOT.TCut("ph_cl_E/ph_truth_E > 0.99 && ph_cl_E/ph_truth_E < 1.00668")
  mycutb = selection + ROOT.TCut("(ph_cl_E/ph_truth_E < 0.99)")# || ph_cl_E/ph_truth_E > 1.00668)")

  #factory.PrepareTrainingAndTestTree(selection, "SplitMode=Alternate");
#   factory.PrepareTrainingAndTestTree(selection, "random:!V");
  factory.PrepareTrainingAndTestTree( mycuts, mycutb, "SplitMode=random:!V" );

  #     factory.PrepareTrainingAndTestTree(selection, "nTrain_Regression=5000:nTest_Regression=5000:random:!V");
  
  if 'BDT' in methods:
    factory.BookMethod( TMVA.Types.kBDT, "BDT", "!V:BoostType=Grad:nCuts=20:NNodesMax=5" );
  
  if 'LD' in methods:
    factory.BookMethod( TMVA.Types.kLD, "LD", "!H:!V:VarTransform=None" );
  
  #     factory.BookMethod( TMVA.Types.kKNN, "KNN", "nkNN=20:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim" );
      
  # Neural network (MLP) -. slooooooooowwww
  if 'MLP' in methods:
    factory.BookMethod( TMVA.Types.kMLP, "MLP", "!H:!V:VarTransform=Norm:NeuronType=tanh:NCycles=1000:HiddenLayers=N+2:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator" );

  if 'Likelihood' in methods:
    factory.BookMethod( TMVA.Types.kLikelihood, "Likelihood",
                      "H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50" );
  
  if 'kNN' in methods:  
    factory.BookMethod( TMVA.Types.kKNN, "KNN",
                           "H:nkNN=20:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim" );



    
  factory.TrainAllMethods();
  
  factory.TestAllMethods();
  
  factory.EvaluateAllMethods();
  
  # --------------------------------------------------------------
  
  # Save the output
  output_file.Close();
  
  print "==> Wrote root file: ", outfileName
  print "==> TMVARegression is done!"
  
  del factory;
  
  # Launch the GUI
#   if not ROOT.gROOT.IsBatch():
#     ROOT.gROOT.LoadMacro("TMVARegGui.C+")
#     ROOT.TMVARegGui(outfileName);
  
  
  

if __name__ == '__main__':
  from optparse import OptionParser
  
  parser = OptionParser("%prog [options] <inputfiles>")
  parser.description = __doc__
  parser.add_option("-f", "--readFromFile", help="Read the list of inputfiles from a text file", default=False, action="store_true")
  parser.add_option("-d", "--dataset", help="Name of the dataset used. With this options the <inputfiles> must be a ROOT file containing a TFileCollection", type=str)
  parser.add_option("-n", "--treename", help="Name of input tree (default: %default)", default="photon")
  parser.add_option("-N", "--name", help="Name of the job (default: %default)", default="calibration_MVA")  
  parser.add_option("-o", "--outfileName", help="Output file name", type=str)
  parser.add_option("-e", "--etaBin", help="Eta bin (default: %default)", default="1.52,1.8")
  parser.add_option("-m", "--methods", help="Regression methods to run (default: %default)", default="BDT,MLP")
  parser.add_option("-t", "--type", help="Type of photons (0=unconverted, 1=converted, 2=Si+Si conversion) (default: %default)", default=0, type=int)
  parser.add_option("-F", "--fullCalibration", help="Do full calibration instead of deriving correction factor wrt std calib", default=False, action="store_true")
  # parser.add_option("-N", "--Nevents", help="Number of events to run (all)", default=-1, type=int)
  parser.epilog = "\n"
  
  (options, inputfiles) = parser.parse_args()
  input_chain = None

  if options.dataset:
    if len(inputfiles) != 1:
      raise ValueError("When using -d, --dataset you must specify only the ROOT file containing the TFileCollection")
    tree_name, file_list = create_file_list(inputfiles[0], options.dataset)
    input_chain = create_TChain(file_list, tree_name)
  elif options.readFromFile:
    if len(inputfiles) != 1:
      raise ValueError("When using -f, --readFromFile you must specify only the text file containing the file list")
    file_list = filter(lambda x: not x in ('\n', ''), open(inputfiles[0]).read().split("\n"))
    input_chain = create_TChain(file_list, options.treename)
  else:
    input_chain = ROOT.TChain(options.treename)
    for f in inputfiles:
      input_chain.Add(f)

  if not input_chain:
    raise ValueError("Input files not given")
  
  print 'Running TMVACalib with options: %s' % options
  TMVACalib(options.name, options.outfileName, input_chain, options.etaBin, options.methods, options.type, options.fullCalibration)

#   import ROOT
#   f = ROOT.TFile(inputfiles[0])
#   chain = f.Get(options.treename)
#   print chain.GetEntries()
