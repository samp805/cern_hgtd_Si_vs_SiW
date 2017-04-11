#!/usr/bin/env python

__doc__ = "To run MVA regression for photon / electron calibration"
__author__ = "Bruno Lenzi <Bruno.Lenzi@cern.ch>"

import os
import ROOT
import datetime
import socket
import sys
try:
    import colorer
except ImportError:
    print "mmm... you don't have the colorer module, well... no colors for you"
import logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(format="%(funcname)s\t%(levelname)s:%(message)s")

particleNames = ['unconvertedPhoton', 'convertedPhoton', 'convertedSiSiPhoton', 'electron', 'photon']
calibNames = ['Ecluster', 'Eaccordion', 'Efull']


def create_TChain(inputfiles, treename):
  chain = ROOT.TChain(treename)
  for inputfile in inputfiles:
    chain.Add(inputfile)
  return chain


def create_file_list(managerdir, dataset_name):
  manager = ROOT.TDataSetManagerFile("dir:%s" % managerdir)
  file_collection = manager.GetDataSet(dataset_name)
  urls = [x.GetFirstUrl().GetUrl() for x in file_collection.GetList()]
  return (file_collection.GetDefaultTreeName(), urls)


def getTChain(inputfiles, treename, readFromFile=False, dataset=False):
  """getTChain(inputfiles, treename="", readFromFile=False, dataset=False) -->
    Return a chain from a list of inputfiles (ROOT or text files if readFromFile=True)
    or a dataset (TFileCollection). Raise ValueError if the chain is invalid/empty"""
  chain = None
  if dataset:
    if len(inputfiles) != 1:
      raise ValueError("When using -d, --datasetsdir you must specify only the name of the dataset")
    tree_name, file_list = create_file_list(dataset, inputfiles[0])
    chain = create_TChain(file_list, tree_name)
  else:
    if readFromFile:
      # filter is to remove empty strings
      file_list = filter(bool, (i.strip('\n') for f in inputfiles for i in open(f)))
    else:
      file_list = inputfiles
    chain = create_TChain(file_list, treename)

  if not chain or not chain.GetEntries():
    raise ValueError("Input files not given or not valid")
  return chain


def getParser(doc=''):
  "getParser(doc='') --> Get parser to run TMVACalib.py"
  from optparse import OptionParser, OptionGroup
  parser = OptionParser("%prog [options] <inputfiles>")
  parser.description = doc
  parser.epilog = "\n"

  io_group = OptionGroup(parser, "I/O options")
  io_group.add_option("-f", "--readFromFile", help="Read the list of inputfiles from a text file",
                      default=False, action="store_true")
  io_group.add_option("-d", "--datasetsdir", help="The directory with the datasetmanager. With this options the <inputfiles> must be the name of the dataset")
  io_group.add_option("-n", "--treename", help="Name of input tree (default: %default)", default="egamma")
  io_group.add_option("-o", "--outputDir", help="Output directory", type=str)
  io_group.add_option("--output-prefix", help="Prefix for the output ROOT file", default="MVACalib")
  parser.add_option_group(io_group)

  group1 = OptionGroup(parser, "Parameters of the optimization")
  group1.add_option("-e", "--etaRange", help="Eta range, NEEDED (default: %default)", default="0,2.47")
  group1.add_option("-E", "--etRange", help="Et range in GeV (e.g: 10,20)")
  group1.add_option("-m", "--methods", help="Regression methods to run (default: %default)", default="BDTG")
  group1.add_option("-t", "--particleType", help="Type of particle (0=unconvertedPhoton, 1=convertedPhoton, 2=Si+Si conversion, 3=electron, 4=photon) (default: %default)", default=2, type=int)
  group1.add_option("-T", "--calibrationType", help="Calibration type (0=correction to Ecluster, 1=correction to Eaccordion, 2=full calibration (default: %default)", default=1, type=int)
  group1.add_option("--target", help="Target variable (automatically set by --calibrationType)")
  parser.add_option_group(group1)

  group2 = OptionGroup(parser, "Variables and other options")
  group2.add_option("-c", "--cut", help="Selection to be applied, default=<STANDARD>", default="<STANDARD>")
  group2.add_option("-V", "--variables", help="Blocks / variables to use in the optmisation, in addition to default ones (comma separated)", default="default", type=str)
  group2.add_option("-S", "--spectators", help="Blocks / variables to add to output trees but NOT use in optmization (comma separated)", default="", type=str)
  group2.add_option("-I", "--ignore", help="Blocks / variables to ignore (comma separated)", default="", type=str)
  group2.add_option("--fTraining", help="Fraction of events to be used for training", default=0.5, type=float)
  group2.add_option("--downweightTails", help="Downweight tails outside the given fraction of events", default=0., type=float)
  group2.add_option("--weightFormula", help="Weight formula")
  group2.add_option("--cut-postprocessing", default="", help='cuts to use in the postprocessing, comma separated, example: "(ph_raw_cl>10E3 && ph_raw_cl<=15E3),(ph_raw_cl>15E3 && ph_raw_cl<=20E3)"')
  # group2.add_option("-N", "--Nevents", help="Number of events to run (all)", default=-1, type=int)
  parser.add_option_group(group2)
  parser.add_option('--help-cut', action='store_true', default=False)

  return parser


def create_selection(selection_string, replacement=None, *args, **kwargs):
  string_cut = create_selection_string(selection_string, *args, **kwargs)
  if replacement:
    for k, v in replacement.iteritems():
      string_cut = string_cut.replace(k, v)
  cut = ROOT.TCut(string_cut)
  cut.SetName('MVA_CUT')
  cut.original_string = selection_string

  return cut


def get_dictionary_selection(eta_min=None, eta_max=None,
                             et_min=None, et_max=None):
  dictionary = {
    '<ETA_RAWET_BIN>': '<ETA_BIN> && <RAWET_BIN>',
    '<TRUTH_MATCHED>': 'ph_truth_matched',
    '<STDENERGY_MATCHED>': "abs(ph_cl_E/ph_truth_E - 1) < 0.5",
    '<ETA_BIN>': '(abs(ph_cl_eta) >= %f) && (abs(ph_cl_eta) < %f)' % (eta_min, eta_max) if (eta_min is not None and eta_max is not None) else '1',
    '<RAWET_BIN>': ('((ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta) >= %de3) &&'
                    '((ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta) < %de3)') % (et_min, et_max) if (et_min is not None and et_max is not None) else '1',
    '<SINGLE_PARTICLE_PHOTON>': 'ph_n == 1',
    '<SINGLE_PARTICLE_ELECTRON>': "el_refittedTrack_qoverp@.size() == 1",
    '<SISI_CONVERTED_D3PD>': "ph_convFlag%10 == 2 && ph_convtrk1nPixHits + ph_convtrk1nSCTHits > 1 && ph_convtrk2nPixHits + ph_convtrk2nSCTHits > 1",
    '<ALL_CONVERTED_D3PD>': "(ph_convFlag%10 == 1 || (ph_convFlag%10 == 2 && (ph_convtrk1nPixHits + ph_convtrk1nSCTHits == 0 || ph_convtrk2nPixHits + ph_convtrk2nSCTHits == 0)))",
    '<CONVERTED>': "ph_Rconv > 0. && ph_Rconv < 800.",
    '<UNCONVERTED_D3PD>': "ph_convFlag % 10 == 0",
    '<AUTHOR_ELECTRON>': "el_author == 1 || el_author == 3",
    '<LOOSE_PP_ELECTRON>': "el_loosePP",
    '<LOOSE_PHOTON>': "ph_loose",
    '<PDG_ID_ELECTRON>': "abs(el_truth_type) == 11",
    '<PDG_ID_PHOTON>': "ph_truth_type == 22",
    '<STANDARD_ELECTRON>': ('<ETA_RAWET_BIN> && <TRUTH_MATCHED> && <STDENERGY_MATCHED> && '
                            '<PDG_ID_ELECTRON> && <AUTHOR_ELECTRON> && <LOOSE_PP_ELECTRON>'),
    '<STANDARD_UNCONVERTED>': ('<ETA_RAWET_BIN> && <TRUTH_MATCHED> && <STDENERGY_MATCHED> && '
                               '<PDG_ID_PHOTON> && <UNCONVERTED_D3PD> && <LOOSE_PHOTON>'),
    '<STANDARD_CONVERTED>': ('<ETA_RAWET_BIN> && <TRUTH_MATCHED> && <STDENERGY_MATCHED> && '
                             '<PDG_ID_PHOTON> && <CONVERTED> && <LOOSE_PHOTON>'),
    '<STANDARD_PHOTON>': ('<ETA_RAWET_BIN> && <TRUTH_MATCHED> && <STDENERGY_MATCHED> && '
                          '<PDG_ID_PHOTON> && <LOOSE_PHOTON>'),
    '<STANDARD_SISICONVERTED>': ('<ETA_RAWET_BIN> && <TRUTH_MATCHED> && <STDENERGY_MATCHED> && '
                                 '<PDG_ID_PHOTON> && <SISI_CONVERTED_D3PD> && <LOOSE_PHOTON>'),
  }
  return dictionary


def create_selection_string(selection_string, eta_min=None, eta_max=None,
                            et_min=None, et_max=None):

  dictionary = get_dictionary_selection(eta_min, eta_max, et_min, et_max)

  repeat = False
  for k, v in dictionary.iteritems():
    if k in selection_string:
      selection_string = selection_string.replace(k, '(' + v + ')')
      repeat = True

  if repeat:
    selection_string = create_selection_string(selection_string, eta_min, eta_max, et_min, et_max)

  return selection_string


def TMVACalib(outputDir, input_chain, etaRange, etRange,
              methods='BDTG', particleType=2, calibrationType=1, selection_string='<STANDARD>',
              variables='default',
              spectators='', ignoreList='',
              fTraining=0.,
              downweightTails=0., output_prefix="MVACalib",
              weightFormula=None,
              cut_postprocessing=None,
              target=None):

  import numpy
  ######################################################
  # Define the particle type and associated parameters
  ######################################################

  unconvertedPhoton, convertedPhoton, convertedSiSiPhoton, electron, photon = range(len(particleNames))
  try:
    particleName = particleNames[particleType]
  except IndexError:
    raise ValueError('Invalid particleType: %s' % particleType)

  doElectron = particleType == electron  # in [electron, GSFelectron]
  doPhoton = not doElectron

  # Define the type of photon
  doConversions = particleType in [convertedPhoton, convertedSiSiPhoton]
  doSiSiConversions = (particleType == convertedSiSiPhoton)

  prefix = 'el_' if doElectron else 'ph_'

  ######################################################
  # Define the calibration type / name
  ######################################################
  calibName = calibNames[calibrationType]

  ######################################################
  # Define the eta and energy ranges
  ######################################################
  try:
    etaMin, etaMax = map(float, etaRange.split(','))
  except ValueError:
    try:
      eta_bins = [0, 0.05, 0.65, 0.8, 1.0, 1.2, 1.37, 1.4, 1.46, 1.52, 1.6, 1.74, 1.82, 2.0, 2.2, 2.47, 2.5]
     # eta_bins = [0, 0.05, 0.65, 0.8, 1.0, 1.2, 1.37, 1.52, 1.55, 1.74, 1.82, 2.0, 2.2, 2.47, 2.5]
      # normal bins: range(1,6) + range(7, 12)
      # special bins: 0,6 : (0-0.05) and (1.52-1.55)
      etaInt = int(etaRange)
#      if eta_bins[etaInt] == 1.37:
#        etaMin, etaMax = 1.52, 1.55
#      else:
      etaMin, etaMax = eta_bins[etaInt], eta_bins[etaInt + 1]
    except:
      raise ValueError('Invalid eta bin definition: %s' % etaRange)

  if etRange:
    etMin, etMax = map(float, etRange.split(','))

  if not isinstance(methods, list):
    methods = methods.split(',')

  if not etRange:
    name = '%s_%s_eta%s-%s_%s' % (output_prefix, particleName, etaMin, etaMax, calibName)
  else:
    name = '%s_%s_Et%d-%d_eta%s-%s_%s' % (output_prefix, particleName, etMin, etMax, etaMin, etaMax, calibName)

  ######################################################
  # create and cd to outputDir and create links to TMVA scripts
  ######################################################

  try:
    os.mkdir(outputDir)
  except OSError:  # probably directory already exists
    pass
    #if not os.path.isdir(outputDir):

  os.chdir(outputDir)
  os.system('ln -s $ROOTSYS/tmva/test/tmvaglob.C')
  os.system('ln -s $ROOTSYS/tmva/test/BDT_Reg.C')

  ######################################################
  # Open files and create factory
  ######################################################
  from ROOT import TMVA

  outfileName = name + '.root'
  output_file = ROOT.TFile(outfileName, 'recreate')

  factory = TMVA.Factory(name, output_file, "DrawProgressBar=False")
  factory.AddRegressionTree(input_chain)

  ######################################################
  # Define the selection
  ######################################################

  if "<STANDARD>" in selection_string:
    replacement = {electron: "<STANDARD_ELECTRON>",
                   photon: "<STANDARD_PHOTON>",
                   unconvertedPhoton: "<STANDARD_UNCONVERTED>",
                   convertedPhoton: "<STANDARD_CONVERTED>",
                   convertedSiSiPhoton: "<STANDARD_SISICONVERTED>"}[particleType]
    selection_string = selection_string.replace('<STANDARD>', "(" + replacement + ")")

  replacement = None
  if doElectron:
    replacement = {'ph_': 'el_'}

  selection = create_selection(selection_string, replacement, etaMin, etaMax, etMin, etMax)

  logging.info('Selection: %s', selection.GetTitle())

  ######################################################
  # Define weights if needed
  ######################################################

  if weightFormula is not None:
    factory.SetWeightExpression(weightFormula, "Regression")

  def smallestInterval(x, integral=0.683):
    ""
    N = len(x)
    # if w is None:    , w = None
    xsorted = numpy.sort(x)
    D = numpy.floor(integral * N)
    first_index = (xsorted[D:] - xsorted[:-D]).argmin()
    return xsorted[first_index], xsorted[D + first_index]

  if downweightTails > 0:
    x = '(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/ph_truth_E'.replace('ph_', prefix)
    # Determine the smallest interval containing N% of the events
    from RootTools import GetValuesFromTree
    data = numpy.fromiter(GetValuesFromTree(input_chain, x, selection), dtype=float)
    xmin, xmax = smallestInterval(data, integral=downweightTails)
    mean = data[numpy.logical_and(data > xmin, data < xmax)].mean()
    t = "(%s - %s)/(%s - %s)" % (x, mean, xmax, xmin)
    cutoff = 1
    factory.SetWeightExpression('abs(%(t)s) > %(cutoff)s ? exp(-abs(%(t)s) + %(cutoff)s) : 1' % {"t":t, "cutoff": cutoff}, "Regression") 
#    factory.SetWeightExpression('abs(%(t)s) > %(cutoff)s ? 0.001 : 1' % {"t":t, "cutoff": cutoff}, "Regression") 
  ######################################################
  # Define variables, spectators, target
  ######################################################

  blocks = dict(
    rawEnergies   = ['ph_rawcl_Es0', 'ph_rawcl_Es1', 'ph_rawcl_Es2', 'ph_rawcl_Es3'],
    rawEratios    = ['f1 := ph_rawcl_Es1/(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)',
                     'f2 := ph_rawcl_Es2/(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)',
                     'f3 := ph_rawcl_Es3/(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)'],
    rawEratios12  = ['f1 := ph_rawcl_Es1/(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)',
                     'f2 := ph_rawcl_Es2/(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)'],
    rawE1overE2   = ['R12 := ph_rawcl_Es1/ph_rawcl_Es2'], 
    f0            = ['ph_rawcl_f0 := ph_rawcl_Es0/(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)'],
    f0a           = ['ph_rawcl_f0 := ph_rawcl_Es0/(ph_rawcl_Es0 + ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)'],
    clusterE      = ['ph_cl_E'],
    clusterEta    = ['ph_cl_eta'],
    absClusterEta = ['abs(ph_cl_eta)'],
    cellIndex     = ['cellIndex := TMath::Floor(abs(ph_cl_eta)/0.025)'],
    cellIndexCalo = ['cellIndexCalo := TMath::Floor(abs(ph_cl_etaCalo)/0.025)'],
    clusterPhi    = ['ph_cl_phi'],
    showerDepth   = ['ph_rawcl_calibHitsShowerDepth'],
    accordionE    = ['ph_rawcl_Eacc := (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)'],
    accordionEt   = ['ph_rawcl_Etacc := (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)'],
    etaSign       = ['signEta := TMath::Sign(1., ph_cl_eta)'],
    #---------- Shower shapes ----------
    wstot         = ['ph_wstot'],
    fside         = ['ph_fside'],
    ws3           = ['ph_ws3'], 
    stripShapes   = ['ph_wstot', 'ph_fside', 'ph_ws3'],
    rphi          = ['ph_rphi'],
    reta          = ['ph_reta'],
    weta2         = ['ph_weta2'],
    middleShapes  = ['ph_rphi', 'ph_reta', 'ph_weta2'],
    R9		  = ['ph_r9 := ph_rphi*ph_reta'],
    Ethad         = ['ph_Ethad'],
    Ethad1        = ['ph_Ethad1'],
    hadLeakage    = ['ph_Ethad', 'ph_Ethad1'],
    #---------- eta sampling 1, 2 ----------
    etaPointing   = ['ph_CaloPointing_eta'],
    etas12        = ['ph_etas1', 'ph_etas2'],
    #---------- eta / phi modulation ----------
    etaMod     = ['etaMod := fmod(abs(ph_cl_eta), 0.025)'],
    phiMod     = ['phiMod := abs(ph_cl_eta) < 1.425 ? fmod(abs(ph_cl_phi), TMath::Pi()/512) : fmod(abs(ph_cl_phi), TMath::Pi()/384)'],
    etaModCalo = ['etaModCalo := fmod(abs(ph_cl_etaCalo), 0.025)'], # calo coordinate
    phiModCalo = ['phiModCalo := abs(ph_cl_eta) < 1.425 ? fmod((ph_cl_phiCalo), TMath::Pi()/512) : fmod((ph_cl_phiCalo), TMath::Pi()/384)'], # calo coordinate
    phiModCaloOld = ['phiModCalo := abs(ph_cl_eta) < 1.425 ? fmod(abs(ph_cl_phiCalo), TMath::Pi()/512) : fmod(abs(ph_cl_phiCalo), TMath::Pi()/384)'], # calo coordinate
    phiModCell = ['phiModCell := fmod(abs(ph_cl_phiCalo), TMath::Pi()/128)'],
    #---------- Material traversed ----------
    material   = ['ph_materialTraversed'],
    #---------- Conversion info ----------
    convR         = ['ph_Rconv'],
    convR2        = ['convR := (ph_ptconv > 3e3 ? ph_Rconv : 799.)'],
    convZ         = ['convz'],
    convZ2        = ['convz := (ph_ptconv > 3e3 ? ph_zconv : 2700.)'],
    convRorZ      = ['convRorZ := abs(ph_cl_eta) < 1.4 ? ph_Rconv : ph_zconv'],
    convRorZ2     = ['convRorZ := abs(ph_cl_eta) < 1.4 ? (ph_ptconv > 3e3 ? ph_Rconv : 799.) : (ph_ptconv > 3e3 ? ph_zconv : 2700.)'],
    convPt        = ['ph_ptconv', 'ph_pt1conv', 'ph_pt2conv'],
    convPtRatios  = ['convEtOverPt := (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/(cosh(ph_cl_eta) * ph_ptconv)',
      'convPtRatio := TMath::Max(ph_pt1conv, ph_pt2conv)/(ph_pt1conv+ph_pt2conv)'], # only for SiSi
    convPtRatiosA = ['convEtOverPt := (ph_convtrk1nPixHits + ph_convtrk1nSCTHits > 1 && ph_convtrk2nPixHits + ph_convtrk2nSCTHits > 1) ? (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/(cosh(ph_cl_eta) * ph_ptconv) : 0',
      'convPtRatio := TMath::Max(ph_pt1conv, ph_pt2conv)/(ph_pt1conv+ph_pt2conv)'], # all
    convPtRatiosB = ['convEtOverPt := (ph_convtrk1nPixHits + ph_convtrk1nSCTHits > 1 && ph_convtrk2nPixHits + ph_convtrk2nSCTHits > 1) ? (ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/(cosh(ph_cl_eta) * ph_ptconv) : 0',
      'convPtRatio := (ph_convtrk1nPixHits + ph_convtrk1nSCTHits > 1 && ph_convtrk2nPixHits + ph_convtrk2nSCTHits > 1) ? TMath::Max(ph_pt1conv, ph_pt2conv)/(ph_pt1conv+ph_pt2conv) : 1.'], # all
      
    # Max deltaPhi between track and cluster. A and B are for different D3PD versions
    convDeltaPhiA  = ['ph_convMatchDeltaPhi1', 'ph_convMatchDeltaPhi2'],
    convDeltaPhiMaxA=['convDeltaPhiMax := TMath::Max(abs(ph_convMatchDeltaPhi1), abs(ph_convMatchDeltaPhi2))'],
    convDeltaPhiB  = ['ph_convTrk1_DeltaPhi_track_calo', 'ph_convTrk2_DeltaPhi_track_calo'],
    convDeltaPhiMaxB=['convDeltaPhiMax := TMath::Max(abs(ph_convTrk1_DeltaPhi_track_calo), abs(ph_convTrk2_DeltaPhi_track_calo))'],
    convIsSiSi     = ['ph_convtrk1nPixHits + ph_convtrk1nSCTHits > 1 && ph_convtrk2nPixHits + ph_convtrk2nSCTHits > 1'],
    #---------- Electron / photon ID ----------
    photonID      = ['ph_isEM', 'ph_tight'],
    electronID    = ['el_isEM', 'el_mediumPP', 'el_tightPP'],
    #---------- Electron deltaPhi / deltaP info ----------
    electronEta   = ['el_tracketa'],
    electronTrkP  = ['el_p0 := el_charge/Alt$(el_refittedTrack_qoverp, 1)', 'el_pLast := el_charge/Alt$(el_refittedTrack_LMqoverp, 1)'],
    electronFBrem  = ['fBrem := 1 - Alt$(el_refittedTrack_qoverp[][0]/el_refittedTrack_LMqoverp[][0], 1)'],
    electronTrkInfo= ['el_charge', 'el_refittedTrack_qoverp', 'el_refittedTrack_LMqoverp'],
    electronDeltaPhi= ['el_deltaphi2', 'el_deltaPhiFromLast'],
    electronDeltaPhiFirstLast= ['el_deltaPhiFirstLast := el_deltaphi2 - el_deltaPhiFromLast'],
    #---------- Photon / Electron z0 ----------
    photonZ0      = ['z0signEta := ph_HPV_zvertex*TMath::Sign(ph_cl_eta, 1.)'],
    electronZ0    = ['z0signEta := el_trackz0*TMath::Sign(1., el_cl_eta)'],    
    #---------- Truth info ----------
    trueE         = ['ph_truth_E'],
    trueEtaPhi    = ['ph_truth_eta', 'ph_truth_phi'],
    trueRconv     = ['ph_truth_Rconv'],
    truthRconv     = ['ph_truth_Rconv'],
    #---------- Event info -----------
    bcid     =['bcid'],
    #---------- Gap variables ---------
    fTG3     =[ 'fTG3 := ph_cl_E_TileGap3/(ph_rawcl_Es1+ph_rawcl_Es2+ph_rawcl_Es3)'],
    DeltaPhiTG3 =['dPhiTG3 :=fmod(2.*TMath::Pi()+ph_cl_phi,TMath::Pi()/32.)-TMath::Pi()/64.'],
    
    MVA =['MVAv10']
 )

  # Exclusive blocks for each particle type
  exclusiveBlocks = {
    unconvertedPhoton: ['photonID', 'etaPointing', 'photonZ0'],
    convertedPhoton: ['photonID', 'convR', 'convR2', 'convZ', 'etaPointing', 'photonZ0', 'material', 'convIsSiSi', 'convPtRatiosA', 'convPtRatiosB'],
    convertedSiSiPhoton: ['convR', 'convR2', 'convZ', 'trueRconv', 'convPt', 'convPtRatios',
      'convDeltaPhiA', 'convDeltaPhiMaxA', 'convDeltaPhiB', 'convDeltaPhiMaxB', 
      'etaPointing', 'photonZ0', 'material'],
    electron: ['electronID', 'electronDeltaP', 'electronDeltaPhi', 'electronEta',
      'electronTrkInfo', 'electronZ0', 'electronFBrem', 'electronTrkP', 'material']
  }

  ranges = dict(ph_wstot = [0, 15], ph_fside = [0,1], ph_ws3 = [0, 1],
                ph_weta2 = [0.006, 0.015], ph_rphi = [0,1.2], ph_reta = [0.75, 1.2],
                el_wstot = [0, 15], el_fside = [0,1], el_ws3 = [0, 1], 
                el_weta2 = [0, 0.025], el_rphi = [0,1.2], el_reta = [0,1], fBrem = [-0.2, 1.2],
                convEtOverPt = [0., 2.])
  # ph_weta2 for conv : [0.005, 0.025] --> probably not so important

  # ---------- Define variables --------- #
#   if 'electronFBrem' in variables + spectators:
#     print '--> Generating dictionary for vector<vector<float> >'
#     ROOT.gInterpreter.GenerateDictionary("vector<vector<float> >","vector")

  if variables == 'all':
    variables = blocks.keys()
    # Remove true info
    for i in 'trueEtaPhi', 'trueRconv', 'trueE', 'photonID', 'electronID':
      variables.remove(i)
  elif variables == 'default':
    variables = ['stripShapes', 'middleShapes', 'f0', 'showerDepth', 'convR',
                 'convPtRatios', 'convDeltaPhiMaxA', 'accordionE', 'clusterE',
                 'electronFBrem', 'electronDeltaPhi', 'electronZ0', 'etaMod',
                 'etaPointing', 'cellIndex']
  elif not isinstance(variables, (list, tuple)):
    variables = variables.split(',')

  if not isinstance(spectators, (list, tuple)):
    spectators = spectators.split(',')

  if not isinstance(ignoreList, (list, tuple)):
    ignoreList = ignoreList.split(',')

  if etaMin > 1.8:
    ignoreList.append('f0')
  if (etaMin, etaMax) in [(0, 0.025), (1.52, 1.55), (2.47,2.5)]:
    ignoreList.extend(['cellIndex', 'cellIndexCalo'])
  if (etaMin, etaMax) in [(1.7, 1.74)]:
    ignoreList.append('material')


  ignoreList.extend(['electronFBrem', 'electronTrkInfo'])

  if target is None:
    target = ['K := ph_truth_E/ph_cl_E',
              'Kacc := ph_truth_E/(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)',
              'ph_truth_E'][calibrationType].replace('ph_', prefix)

  # Add calibrated energy or raw energies and define target
  factory.AddTarget(target)
  if calibrationType == 0 and 'accordionE' in variables:
    variables.remove('accordionE')
  if calibrationType != 0 and 'clusterE' in variables:
    variables.remove('clusterE')
  if calibrationType == 2:  # full calibration
    del blocks['trueE']  # already a target, no need to add as spectator

  if calibrationType != 0:
    spectators.append('clusterE')
  if 'accordionE' not in variables:
    spectators.append('accordionE')

  # Default spectators (TODO: define better)
  spectators.extend(['trueE', 'trueEtaPhi', 'convR', 'trueRconv', 'clusterPhi',
                     'rawEnergies'])

  #-------------------------------------------------------
  # Loop over the blocks and add each info to Variables or Spectators
  base_variables_list=[]
  for block, vars in blocks.iteritems():
    if block in ignoreList:
      continue

    # Do not use the blocks that are not relevant for this particle
    if block not in exclusiveBlocks.get(particleType, []) and \
      any(block in exBlocks for exBlocks in exclusiveBlocks.values()):
      continue
    if block in variables:
      command = factory.AddVariable
    elif block in spectators:
      command = factory.AddSpectator
    else:
      continue

    for variable in vars:
      variable = variable.replace('ph_', prefix)
      if variable in ignoreList:
         continue
      # Get the name and definition of the variable, removing whitespaces
      V = map(str.strip, variable.split(':='))
      try:
        varName, varDef = V
      except ValueError:
        varName = varDef = V[0]
      Min, Max = ranges.get(varName, (0, 0))
      # Force the variable to be in the given range and remove the prefix from its name
      # (e.g. ph_rphi becomes rphi := TMath::Min(TMath::Max(ph_rphi, 0), 1.2))
      if varName in ranges:
        variable = '%s := TMath::Min(TMath::Max(%s, %s), %s)' % (varName.strip(prefix), varDef, Min, Max)
#       print varName, Min, Max
      try:
        command(variable, '', '', 'F', Min, Max)  # AddVariable
	varformula=ROOT.TTreeFormula(varName,varDef,input_chain)
        for code in range(0,varformula.GetNcodes()):
		base_variables_list.append(varformula.GetLeaf(code).GetName())
         
      except TypeError:  # AddSpectator, does not take the same arguments
        command(variable, '', '', Min, Max)
	varformula=ROOT.TTreeFormula(varName,varDef,input_chain)
        for code in range(0,varformula.GetNcodes()):
		base_variables_list.append(varformula.GetLeaf(code).GetName())
  # Loop over user-defined <variables> and <spectators>
  # and add the ones which are not inside blocks
  for variable in variables:
    if bool(variable) and variable not in blocks and variable not in ignoreList:
      factory.AddVariable(variable, 'F')

  # Loop over user-defined spectators and add them
  for spectator in spectators:
    if bool(spectator) and spectator not in blocks and spectator not in ignoreList:
      factory.AddSpectator(spectator, 'F')

  ######################################################
  # Add methods and run
  ######################################################

  #factory.PrepareTrainingAndTestTree(selection, "SplitMode=Alternate")

  if not fTraining or fTraining == 0.5:
    factory.PrepareTrainingAndTestTree(selection, "random:!V:NormMode=None")
  else:
    nTrain = fTraining * input_chain.GetEntries()
    factory.PrepareTrainingAndTestTree(selection, "nTrain_Regression=%d:random:!V:NormMode=None:ScaleWithPreselEff" % nTrain)

  if 'BDTG' in methods:
    factory.BookMethod(TMVA.Types.kBDT, "BDTG", "!V:BoostType=Grad:nCuts=20:MaxDepth=3")

  if 'BDTG-1' in methods:
    factory.BookMethod(TMVA.Types.kBDT, "BDTG-1", "!V:BoostType=Grad:nCuts=-1:MaxDepth=2")

  if 'BDTG200' in methods:
    factory.BookMethod(TMVA.Types.kBDT, "BDTG200", "!V:BoostType=Grad:nCuts=200:MaxDepth=2")

  if 'BDTAdaLinear' in methods:
    factory.BookMethod(TMVA.Types.kBDT, "BDTAdaLinear", "!V:BoostType=AdaBoost:AdaBoostR2Loss=Linear:AdaBoostBeta=1:nCuts=20:MaxDepth=2")

  if 'BDTAdaQuadratic' in methods:
    factory.BookMethod(TMVA.Types.kBDT, "BDTAdaQuadratic", "!V:BoostType=AdaBoost:AdaBoostR2Loss=Quadratic:AdaBoostBeta=1:nCuts=20:MaxDepth=2")

  if 'BDTAdaExponential' in methods:
    factory.BookMethod(TMVA.Types.kBDT, "BDTAdaExponential", "!V:BoostType=AdaBoost:AdaBoostR2Loss=Exponential:AdaBoostBeta=1:nCuts=20:MaxDepth=2")
    #else:
      #raise ValueError("Invalid method: %s" % method)

  if 'LD' in methods:
    factory.BookMethod(TMVA.Types.kLD, "LD", "!H:!V:VarTransform=None")

  if 'KNN' in methods:
    factory.BookMethod(TMVA.Types.kKNN, "KNN", "nkNN=20:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim")
    factory.BookMethod(TMVA.Types.kKNN, "KNN2", "nkNN=40:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim")
    factory.BookMethod(TMVA.Types.kKNN, "KNN3", "nkNN=60:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim") # best
    factory.BookMethod(TMVA.Types.kKNN, "KNN4", "nkNN=80:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim")
    factory.BookMethod(TMVA.Types.kKNN, "KNN5", "nkNN=100:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim")
    factory.BookMethod(TMVA.Types.kKNN, "KNN6", "nkNN=120:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim")

  # Neural network (MLP) -. slooooooooowwww
  if 'MLP' in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLP", "!H:!V:VarTransform=Norm:NeuronType=tanh:NCycles=15000:HiddenLayers=N+10:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator")

  if 'MLPs' in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLPs", "!H:!V:VarTransform=Norm:NeuronType=sigmoid:NCycles=1000:HiddenLayers=4:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator")

  if 'MLPs_tanh' in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLPs_tanh", "!H:!V:VarTransform=Norm:NeuronType=tanh:NCycles=1000:HiddenLayers=4:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator")

  if 'MLPs_15000' in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLPs_15000", "!H:!V:VarTransform=Norm:NeuronType=sigmoid:NCycles=15000:HiddenLayers=4:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator")

  if 'MLPs_tanh_15000' in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLPs_tanh_15000", "!H:!V:VarTransform=Norm:NeuronType=tanh:NCycles=15000:HiddenLayers=4:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator")

  if 'MLPs_15000_l2' in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLPs_15000_l2", "!H:!V:VarTransform=Norm:NeuronType=sigmoid:NCycles=15000:HiddenLayers=2:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator")

  if 'MLPs_15000_l3' in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLPs_15000_l3", "!H:!V:VarTransform=Norm:NeuronType=sigmoid:NCycles=15000:HiddenLayers=3:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator")

  if 'MLPs_15000_l5' in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLPs_15000_l5", "!H:!V:VarTransform=Norm:NeuronType=sigmoid:NCycles=15000:HiddenLayers=5:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator")

  if 'MLP_500_1' in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLP_500_1", "!H:!V:VarTransform=Norm:NeuronType=sigmoid:NCycles=500:HiddenLayers=1:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator")

  if 'MLP_1000_1' in methods:
    factory.BookMethod(TMVA.Types.kMLP, "MLP_1000_1", "!H:!V:VarTransform=Norm:NeuronType=sigmoid:NCycles=1000:HiddenLayers=1:TestRate=6:TrainingMethod=BFGS:Sampling=0.4:SamplingEpoch=0.7:ConvergenceImprove=1e-5:ConvergenceTests=5:!UseRegulator")

  factory.TrainAllMethods()
  factory.TestAllMethods()
  factory.EvaluateAllMethods()

  # --------------------------------------------------------------

  # Save the output
  output_file.Close()

  print "==> Wrote root file: ", os.path.join(outputDir, outfileName)
  print "==> TMVARegression is done!"

#  traint_tree = output_file.Get("TrainTree")
#  MVA_energy_formula = ['BDT * %s_cl_E' % prefix,
#                        'BDT * %s_rawcl_Eacc' % prefix,
#                        'BDT'][calibrationType]
#  MVA_linearity_formula = "(" + MVA_energy_formula + ")" + "/ (%s_truth_E)" % prefix
#  MVA_energy_data = numpy.fromiter(GetValuesFromTree(MVA_linearity_formula))

  del factory

  # Post-processing: add information to each xmlfile
  from TMVACalibPostProcessing import TMVACalibPostProcessing
  from TMVACalibPostProcessing import add_variablesname_to_xmlfile
  print "==> Adding information to the xml"
  for method in methods:
    xmlfile = os.path.join("weights", '%s_%s.weights.xml' % (name, method))
    TMVACalibPostProcessing(xmlfile, cuts=cut_postprocessing,
                            doTrainTreeFriend=(fTraining > 0.6))
    
    add_variablesname_to_xmlfile(xmlfile,{"Variables":list(set(base_variables_list))})
  print "==> added additional information to %s" % xmlfile

  # Launch the GUI
#   if not ROOT.gROOT.IsBatch():
#     ROOT.gROOT.ProcessLine(".L TMVARegGui.C")
#     ROOT.TMVARegGui(outfileName)

if __name__ == '__main__':
  parser = getParser(__doc__)
  (options, inputfiles) = parser.parse_args()

  if options.help_cut:
    print "example with eta (0.1, 0.3), pt (10, 20)"
    for k, v in sorted(get_dictionary_selection(0.1, 0.3, 10, 20).iteritems()):
      print " {:>30} = {}".format(k, v)
    exit()

  print datetime.datetime.today()
  print socket.gethostname()
  print 'command executed on %s from %s' % (datetime.datetime.today(), socket.gethostname())
  print ' '.join(sys.argv)
  print 'Running TMVACalib with options:'
  print "  " + "\n  ".join(["{0:20}: {1}".format(k, v) for k, v in options.__dict__.iteritems()])

  chain = getTChain(inputfiles, options.treename, options.readFromFile, options.datasetsdir)

  os.system('uname -a')

  

  TMVACalib(options.outputDir, chain, options.etaRange, options.etRange, options.methods,
            options.particleType, options.calibrationType, options.cut,
            options.variables, options.spectators, options.ignore, options.fTraining,
            options.downweightTails,
            output_prefix=options.output_prefix,
            weightFormula=options.weightFormula,
            cut_postprocessing=options.cut_postprocessing,
            target=options.target)
