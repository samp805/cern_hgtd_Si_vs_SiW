#include <iostream>

#include <TFile.h>
#include <TTree.h>

#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>
//#include <ElectronIsolationSelection/ShowerDepthTool.h>
#include <xAODRootAccess/Init.h>
#include <xAODRootAccess/TEvent.h>
#include <xAODEventInfo/EventInfo.h>
#include <xAODEventShape/EventShape.h>
#include <xAODEgamma/ElectronContainer.h>
#include <xAODEgamma/PhotonContainer.h>
#include <xAODMuon/MuonContainer.h>
#include <xAODEgamma/EgammaxAODHelpers.h>
#include <xAODEgamma/PhotonxAODHelpers.h>
#include <xAODEgamma/ElectronxAODHelpers.h>
#include <xAODCaloEvent/CaloCluster.h>
#include <xAODTruth/TruthParticle.h>
#include <xAODTruth/TruthVertex.h>
#include <xAODTracking/Vertex.h>
#include <xAODTracking/VertexContainer.h>
#include <xAODTracking/TrackParticle.h>
#include <xAODTracking/TrackingPrimitives.h>
#include <egammaMVACalibUtils/dumpxAODntuple.h>
#include "xAODTruth/xAODTruthHelpers.h"

// this is needed to distribute the algorithm to the workers
ClassImp(dumpxAODntuple)


dumpxAODntuple::dumpxAODntuple ()
{
  particleType = 0;
  outputStreamName="output";
  N_particle_saved= 11;
  FLAT=false;
  doOnline = false;
  m_sane=0;
  m_problems=0;
  std::cout << "base initialization" << std::endl;
}



EL::StatusCode dumpxAODntuple::setupJob (EL::Job& job)
{
  job.options()->setString (EL::Job::optXaodAccessMode, EL::Job::optXaodAccessMode_athena);
  job.useXAOD ();

  xAOD::Init("dumpxAODntuple").ignore(); // call before opening first file

  EL::OutputStream stream (outputStreamName.Data());
  job.outputAdd (stream);

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode dumpxAODntuple::histInitialize ()
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode dumpxAODntuple::fileExecute ()
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode dumpxAODntuple::changeInput (bool firstFile)
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode dumpxAODntuple::initialize ()
{
  std::cout << "Initialize" << std::endl;
  m_event = wk()->xaodEvent();
  Info("initialize()", "Number of events = %lli", m_event->getEntries() ); // print long long int

  m_eventCounter = 0;

  //photon_isem = new AsgPhotonIsEMSelector("photon_isem");
  //electron_isem = new AsgElectronIsEMSelector("electron_isem");
  //shower = new CP::ShowerDepthTool();
  //shower->initialize();

  m_LHToolTight2015    = new AsgElectronLikelihoodTool ("m_LHToolTight2015");
  m_LHToolMedium2015   = new AsgElectronLikelihoodTool ("m_LHToolMedium2015");
  m_LHToolLoose2015    = new AsgElectronLikelihoodTool ("m_LHToolLoose2015");

  // initialize the primary vertex container for the tool to have access to the number of vertices used to adapt cuts based on the pileup
  m_LHToolTight2015   ->setProperty("primaryVertexContainer","PrimaryVertices");
  m_LHToolMedium2015  ->setProperty("primaryVertexContainer","PrimaryVertices");
  m_LHToolLoose2015   ->setProperty("primaryVertexContainer","PrimaryVertices");

  m_LHToolTight2015    ->initialize();
  m_LHToolMedium2015   ->initialize();
  m_LHToolLoose2015    ->initialize();

  std::string confDir = "ElectronPhotonSelectorTools/offline/mc15_20150712/";
  m_LHToolTight2015->setProperty("ConfigFile",confDir+"ElectronLikelihoodTightOfflineConfig2015.conf");
  m_LHToolMedium2015->setProperty("ConfigFile",confDir+"ElectronLikelihoodMediumOfflineConfig2015.conf");
  m_LHToolLoose2015->setProperty("ConfigFile",confDir+"ElectronLikelihoodLooseOfflineConfig2015_CutBL.conf");

  m_LHToolTight2015    ->initialize();
  m_LHToolMedium2015   ->initialize();
  m_LHToolLoose2015    ->initialize();

  m_photonTightIsEMSelector = new AsgPhotonIsEMSelector ("PhotonTightIsEMSelector");
  m_photonTightIsEMSelector->setProperty("isEMMask",static_cast<unsigned int>(egammaPID::PhotonTight));
  m_photonTightIsEMSelector->setProperty("ConfigFile","ElectronPhotonSelectorTools/offline/mc15_20150712/PhotonIsEMTightSelectorCutDefs.conf");
  if (!m_photonTightIsEMSelector->initialize().isSuccess()) {
    Fatal("MyFunction", "Failed to initialize PhotonTightIsEMSelector");
  }

  m_photonLooseIsEMSelector = new AsgPhotonIsEMSelector ("PhotonLooseIsEMSelector");
  m_photonLooseIsEMSelector->setProperty("isEMMask",static_cast<unsigned int>(egammaPID::PhotonLoose));
  m_photonLooseIsEMSelector->setProperty("ConfigFile","ElectronPhotonSelectorTools/offline/mc15_20150712/PhotonIsEMLooseSelectorCutDefs.conf");
  if (!m_photonLooseIsEMSelector->initialize().isSuccess()) {
    Fatal("MyFunction", "Failed to initialize PhotonLooseIsEMSelector");
  }


// initialize isolation correction tool
  /*isoCorr_tool_20 = new CP::IsolationCorrectionTool("isoCorr_tool_20");
  isoCorr_tool_20->setProperty( "CorrFile", "IsolationCorrections/isolation_ptcorrections_rel20_2.root");
  isoCorr_tool_20->setProperty( "Apply_datadriven", false);
  isoCorr_tool_20->setProperty( "Correct_etcone", true);
  isoCorr_tool_20->setProperty( "IsMC", true);
  isoCorr_tool_20->setProperty( "AFII_corr", false);
  isoCorr_tool_20->setProperty( "ToolVer", "REL20_2");

  if (! isoCorr_tool_20->initialize().isSuccess() ){
    Error("initialize()", "Failed to properly initialize the isoCorr_tool_20. Exiting." );
    return EL::StatusCode::FAILURE;
  }*/


  outputFile = wk()->getOutputFile(outputStreamName.Data());
  outputTree = new TTree("egamma","egamma");
  outputTree->SetDirectory(outputFile);
  outputTree->SetAutoSave(100000000);
  outputTree->SetAutoFlush(30000000);
  TTree::SetBranchStyle(1);



  outputTree->Branch("PV_zvertex", &m_PV_zvertex,"PV_zvertex/F");
  outputTree->Branch("averageIntPerXing", &m_averageIntPerXing,"averageIntPerXing/F");
  outputTree->Branch("actualIntPerXing", &m_actualIntPerXing,"actualIntPerXing/F");
  outputTree->Branch("RunNumber", &m_RunNumber,"RunNumber/I");
  outputTree->Branch("bcid", &m_bcid,"bcid/I");
  outputTree->Branch("EventNumber", &m_EventNumber,"EventNumber/I");
  outputTree->Branch("PhotonPV_n", &m_PhotonPV_n,"PhotonPV_n/I");


  if (particleType==0) {

    if (N_particle_saved<10){
      tmp_vec_ph_CaloPointing_eta = new std::vector<float>();
      tmp_vec_ph_cl_E = new std::vector<float>();
      tmp_vec_ph_cl_eta = new std::vector<float>();
      tmp_vec_ph_cl_etaCalo = new std::vector<float>();
      tmp_vec_ph_cl_phi = new std::vector<float>();
      tmp_vec_ph_cl_phiCalo = new std::vector<float>();
      tmp_vec_ph_author = new std::vector<int>();
      tmp_vec_ph_convFlag = new std::vector<int>();
      tmp_vec_ph_convMatchDeltaPhi1 = new std::vector<float>();
      tmp_vec_ph_convMatchDeltaPhi2 = new std::vector<float>();
      tmp_vec_ph_convMatchDeltaEta1 = new std::vector<float>();
      tmp_vec_ph_convMatchDeltaEta2 = new std::vector<float>();
      tmp_vec_ph_convTrk1_DeltaPhi_track_calo = new std::vector<float>();
      tmp_vec_ph_convtrk1nPixHits = new std::vector<int>();
      tmp_vec_ph_convtrk1nSCTHits = new std::vector<int>();
      tmp_vec_ph_convTrk2_DeltaPhi_track_calo = new std::vector<float>();
      tmp_vec_ph_convtrk2nPixHits = new std::vector<int>();
      tmp_vec_ph_convtrk2nSCTHits = new std::vector<int>();
      tmp_vec_ph_etas1 = new std::vector<float>();
      tmp_vec_ph_etas2 = new std::vector<float>();
      tmp_vec_ph_Ethad = new std::vector<float>();
      tmp_vec_ph_Ethad1 = new std::vector<float>();
      tmp_vec_ph_fside = new std::vector<float>();
      tmp_vec_ph_HPV_zvertex = new std::vector<float>();
      tmp_vec_ph_isEM = new std::vector<int>();
      tmp_vec_ph_loose = new std::vector<bool>();
      tmp_vec_ph_materialTraversed = new std::vector<float>();
      tmp_vec_ph_pt1conv = new std::vector<float>();
      tmp_vec_ph_pt2conv = new std::vector<float>();
      tmp_vec_ph_ptconv = new std::vector<float>();
      tmp_vec_ph_raw_cl = new std::vector<float>();
      tmp_vec_ph_rawcl_calibHitsShowerDepth = new std::vector<float>();
      tmp_vec_ph_rawcl_Eacc = new std::vector<float>();
      tmp_vec_ph_rawcl_Eacc = new std::vector<float>();
      tmp_vec_ph_rawcl_Es0 = new std::vector<float>();
      tmp_vec_ph_rawcl_Es1 = new std::vector<float>();
      tmp_vec_ph_rawcl_Es2 = new std::vector<float>();
      tmp_vec_ph_rawcl_Es3 = new std::vector<float>();
      tmp_vec_ph_rawcl_Et = new std::vector<float>();
      tmp_vec_ph_rawcl_f0 = new std::vector<float>();
      tmp_vec_ph_Rconv = new std::vector<float>();
      tmp_vec_ph_E237 = new std::vector<float>();
      tmp_vec_ph_E233 = new std::vector<float>();
      tmp_vec_ph_E277 = new std::vector<float>();
      tmp_vec_ph_reta = new std::vector<float>();
      tmp_vec_ph_rphi = new std::vector<float>();
      tmp_vec_ph_tight = new std::vector<bool>();
      tmp_vec_ph_truth_E = new std::vector<float>();
      tmp_vec_ph_truth_pt = new std::vector<float>();
      tmp_vec_ph_truth_eta = new std::vector<float>();
      tmp_vec_ph_truth_matched = new std::vector<bool>();
      tmp_vec_ph_truth_phi = new std::vector<float>();
      tmp_vec_ph_truth_Rconv = new std::vector<float>();
      tmp_vec_ph_truth_type = new std::vector<int>();
      tmp_vec_ph_truth_parent_pdgId = new std::vector<int>();
      tmp_vec_ph_weta2 = new std::vector<float>();
      tmp_vec_ph_ws3 = new std::vector<float>();
      tmp_vec_ph_wstot = new std::vector<float>();
      tmp_vec_ph_zconv = new std::vector<float>();
      tmp_vec_ph_DeltaE = new std::vector<float>();
      tmp_vec_ph_Eratio = new std::vector<float>();
      tmp_vec_ph_Rhad = new std::vector<float>();
      tmp_vec_ph_Rhad1 = new std::vector<float>();
    }



    if(FLAT){
      outputTree->Branch("ph_truth_n", &m_ph_truth_n,"ph_truth_n/I");
      outputTree->Branch("ph_CaloPointing_eta", &m_ph_CaloPointing_eta,"ph_CaloPointing_eta/F");
      outputTree->Branch("ph_cl_E", &m_ph_cl_E,"ph_cl_E/F");
      outputTree->Branch("ph_cl_eta", &m_ph_cl_eta,"ph_cl_eta/F");
      outputTree->Branch("ph_E", &m_ph_E,"ph_E/F");
      outputTree->Branch("ph_eta", &m_ph_eta,"ph_eta/F");
      outputTree->Branch("ph_phi", &m_ph_phi,"ph_phi/F");
      outputTree->Branch("ph_cl_etaCalo", &m_ph_cl_etaCalo,"ph_cl_etaCalo/F");
      outputTree->Branch("ph_cl_etaS1Calo", &m_ph_cl_etaS1Calo,"ph_cl_etaS1Calo/F");
      outputTree->Branch("ph_cl_etaS2Calo", &m_ph_cl_etaS2Calo,"ph_cl_etaS2Calo/F");
      outputTree->Branch("ph_cl_phi", &m_ph_cl_phi,"ph_cl_phi/F");
      outputTree->Branch("ph_cl_phiCalo", &m_ph_cl_phiCalo,"ph_cl_phiCalo/F");
      outputTree->Branch("ph_cl_phiS1Calo", &m_ph_cl_phiS1Calo,"ph_cl_phiS1Calo/F");
      outputTree->Branch("ph_cl_phiS2Calo", &m_ph_cl_phiS2Calo,"ph_cl_phiS2Calo/F");
      outputTree->Branch("ph_author", &m_ph_author,"ph_author/I");
      outputTree->Branch("ph_convFlag", &m_ph_convFlag,"ph_convFlag/I");
      outputTree->Branch("ph_convMatchDeltaPhi1", &m_ph_convMatchDeltaPhi1,"ph_convMatchDeltaPhi1/F");
      outputTree->Branch("ph_convMatchDeltaPhi2", &m_ph_convMatchDeltaPhi2,"ph_convMatchDeltaPhi2/F");
      outputTree->Branch("ph_convMatchDeltaEta1", &m_ph_convMatchDeltaEta1,"ph_convMatchDeltaEta1/F");
      outputTree->Branch("ph_convMatchDeltaEta2", &m_ph_convMatchDeltaEta2,"ph_convMatchDeltaEta2/F");
      // outputTree->Branch("ph_convTrk1_DeltaPhi_track_calo", &m_ph_convTrk1_DeltaPhi_track_calo,"ph_convTrk1_DeltaPhi_track_calo/F");
      outputTree->Branch("ph_convtrk1nPixHits", &m_ph_convtrk1nPixHits,"ph_convtrk1nPixHits/I");
      outputTree->Branch("ph_convtrk1nSCTHits", &m_ph_convtrk1nSCTHits,"ph_convtrk1nSCTHits/I");
      //outputTree->Branch("ph_convTrk2_DeltaPhi_track_calo", &m_ph_convTrk2_DeltaPhi_track_calo,"ph_convTrk2_DeltaPhi_track_calo/F");
      outputTree->Branch("ph_convtrk2nPixHits", &m_ph_convtrk2nPixHits,"ph_convtrk2nPixHits/I");
      outputTree->Branch("ph_convtrk2nSCTHits", &m_ph_convtrk2nSCTHits,"ph_convtrk2nSCTHits/I");
      outputTree->Branch("ph_etas1", &m_ph_etas1,"ph_etas1/F");
      outputTree->Branch("ph_etas2", &m_ph_etas2,"ph_etas2/F");
      outputTree->Branch("ph_Ethad", &m_ph_Ethad,"ph_Ethad/F");
      outputTree->Branch("ph_Ethad1", &m_ph_Ethad1,"ph_Ethad1/F");
      outputTree->Branch("ph_fside", &m_ph_fside,"ph_fside/F");
      //outputTree->Branch("ph_HPV_zvertex", &m_ph_HPV_zvertex,"ph_HPV_zvertex/F");
      // outputTree->Branch("ph_isEM", &m_ph_isEM,"ph_isEM/I");
      outputTree->Branch("ph_loose", &m_ph_loose,"ph_loose/O");
      //outputTree->Branch("ph_materialTraversed", &m_ph_materialTraversed,"ph_materialTraversed/F");
      outputTree->Branch("ph_n", &m_ph_n,"ph_n/I");
      outputTree->Branch("ph_pt1conv", &m_ph_pt1conv,"ph_pt1conv/F");
      outputTree->Branch("ph_pt2conv", &m_ph_pt2conv,"ph_pt2conv/F");
      outputTree->Branch("ph_ptconv", &m_ph_ptconv,"ph_ptconv/F");
      //outputTree->Branch("ph_ShowerDepth", &m_ph_rawcl_calibHitsShowerDepth,"ph_ShowerDepth/F");
      outputTree->Branch("ph_rawcl_Eacc", &m_ph_rawcl_Eacc,"ph_rawcl_Eacc/F");
      outputTree->Branch("ph_rawcl_Es0", &m_ph_rawcl_Es0,"ph_rawcl_Es0/F");
      outputTree->Branch("ph_rawcl_Es1", &m_ph_rawcl_Es1,"ph_rawcl_Es1/F");
      outputTree->Branch("ph_rawcl_Es2", &m_ph_rawcl_Es2,"ph_rawcl_Es2/F");
      outputTree->Branch("ph_rawcl_Es3", &m_ph_rawcl_Es3,"ph_rawcl_Es3/F");
      outputTree->Branch("ph_rawcl_Et", &m_ph_rawcl_Et,"ph_rawcl_Et/F");
      outputTree->Branch("ph_rawcl_f0", &m_ph_rawcl_f0,"ph_rawcl_f0/F");
      outputTree->Branch("ph_Rconv", &m_ph_Rconv,"ph_Rconv/F");
      outputTree->Branch("ph_E237", &m_ph_E237,"ph_E237/F");
      outputTree->Branch("ph_E233", &m_ph_E233,"ph_E233/F");
      outputTree->Branch("ph_E277", &m_ph_E277,"ph_E277/F");
      outputTree->Branch("ph_reta", &m_ph_reta,"ph_reta/F");
      outputTree->Branch("ph_rphi", &m_ph_rphi,"ph_rphi/F");
      outputTree->Branch("ph_tight", &m_ph_tight,"ph_tight/O");
      outputTree->Branch("ph_truth_E", &m_ph_truth_E,"ph_truth_E/F");
      outputTree->Branch("ph_truth_pt", &m_ph_truth_pt,"ph_truth_pt/F");
      outputTree->Branch("ph_truth_eta", &m_ph_truth_eta,"ph_truth_eta/F");
      outputTree->Branch("ph_truth_matched", &m_ph_truth_matched,"ph_truth_matched/O");
      outputTree->Branch("ph_truth_phi", &m_ph_truth_phi,"ph_truth_phi/F");
      outputTree->Branch("ph_truth_Rconv", &m_ph_truth_Rconv,"ph_truth_Rconv/F");
      outputTree->Branch("ph_truth_type", &m_ph_truth_type,"ph_truth_type/I");
      outputTree->Branch("ph_truth_parent_pdgId", &m_ph_truth_parent_pdgId,"ph_truth_parent_pdgId/I");
      outputTree->Branch("ph_weta2", &m_ph_weta2,"ph_weta2/F");
      outputTree->Branch("ph_ws3", &m_ph_ws3,"ph_ws3/F");
      outputTree->Branch("ph_wstot", &m_ph_wstot,"ph_wstot/F");
      outputTree->Branch("ph_zconv", &m_ph_zconv,"ph_zconv/F");
      outputTree->Branch("ph_DeltaE",&m_ph_DeltaE, "ph_DeltaE/F");
      outputTree->Branch("ph_Eratio", &m_ph_Eratio,"ph_Eratio/F");
      outputTree->Branch("ph_Rhad", &m_ph_Rhad, "ph_Rhad/F");
      outputTree->Branch("ph_Rhad1", &m_ph_Rhad1, "ph_Rhad1/F");
      outputTree->Branch("ph_etcone40", &m_ph_etcone40, "ph_etcone40/F");
      outputTree->Branch("ph_etcone30", &m_ph_etcone30, "ph_etcone30/F");
      outputTree->Branch("ph_etcone20", &m_ph_etcone20, "ph_etcone20/F");
      outputTree->Branch("ph_topoetcone40", &m_ph_topoetcone40, "ph_topoetcone40/F");
      outputTree->Branch("ph_topoetcone30", &m_ph_topoetcone30, "ph_topoetcone30/F");
      outputTree->Branch("ph_topoetcone20", &m_ph_topoetcone20, "ph_topoetcone20/F");
      outputTree->Branch("ph_topoetcone40toolCorrected", &m_ph_topoetcone40toolCorrected, "ph_topoetcone40toolCorrected/F");
      outputTree->Branch("ph_topoetcone30toolCorrected", &m_ph_topoetcone30toolCorrected, "ph_topoetcone30toolCorrected/F");
      outputTree->Branch("ph_topoetcone20toolCorrected", &m_ph_topoetcone20toolCorrected, "ph_topoetcone20toolCorrected/F");
      outputTree->Branch("ph_topoetcone40toolCorrection", &m_ph_topoetcone40toolCorrection, "ph_topoetcone40toolCorrection/F");
      outputTree->Branch("ph_topoetcone30toolCorrection", &m_ph_topoetcone30toolCorrection, "ph_topoetcone30toolCorrection/F");
      outputTree->Branch("ph_topoetcone20toolCorrection", &m_ph_topoetcone20toolCorrection, "ph_topoetcone20toolCorrection/F");
      outputTree->Branch("ph_topoetcone40noCorrected", &m_ph_topoetcone40noCorrected, "ph_topoetcone40noCorrected/F");
      outputTree->Branch("ph_topoetcone30noCorrected", &m_ph_topoetcone30noCorrected, "ph_topoetcone30noCorrected/F");
      outputTree->Branch("ph_topoetcone20noCorrected", &m_ph_topoetcone20noCorrected, "ph_topoetcone20noCorrected/F");
      outputTree->Branch("ph_topoetcone40coreconeCorrected", &m_ph_topoetcone40coreconeCorrected, "ph_topoetcone40coreconeCorrected/F");
      outputTree->Branch("ph_topoetcone30coreconeCorrected", &m_ph_topoetcone30coreconeCorrected, "ph_topoetcone30coreconeCorrected/F");
      outputTree->Branch("ph_topoetcone20coreconeCorrected", &m_ph_topoetcone20coreconeCorrected, "ph_topoetcone20coreconeCorrected/F");
      outputTree->Branch("ph_topoetcone40coreconeCorrected", &m_ph_topoetcone40coreconeCorrected, "ph_topoetcone40coreconeCorrected/F");
      outputTree->Branch("ph_topoetcone30coreconeCorrected", &m_ph_topoetcone30coreconeCorrected, "ph_topoetcone30coreconeCorrected/F");
      outputTree->Branch("ph_topoetcone20coreconeCorrected", &m_ph_topoetcone20coreconeCorrected, "ph_topoetcone20coreconeCorrected/F");
      outputTree->Branch("ph_topoetcone40ptCorrection", &m_ph_topoetcone40ptCorrection, "ph_topoetcone40ptCorrection/F");
      outputTree->Branch("ph_topoetcone30ptCorrection", &m_ph_topoetcone30ptCorrection, "ph_topoetcone30ptCorrection/F");
      outputTree->Branch("ph_topoetcone20ptCorrection", &m_ph_topoetcone20ptCorrection, "ph_topoetcone20ptCorrection/F");
      outputTree->Branch("ph_topoetcone40pileupCorrection", &m_ph_topoetcone40pileupCorrection, "ph_topoetcone40pileupCorrection/F");
      outputTree->Branch("ph_topoetcone30pileupCorrection", &m_ph_topoetcone30pileupCorrection, "ph_topoetcone30pileupCorrection/F");
      outputTree->Branch("ph_topoetcone20pileupCorrection", &m_ph_topoetcone20pileupCorrection, "ph_topoetcone20pileupCorrection/F");
      outputTree->Branch("ph_topoetcone40coreconeCorrection", &m_ph_topoetcone40coreconeCorrection, "ph_topoetcone40coreconeCorrection/F");
      outputTree->Branch("ph_topoetcone30coreconeCorrection", &m_ph_topoetcone30coreconeCorrection, "ph_topoetcone30coreconeCorrection/F");
      outputTree->Branch("ph_topoetcone20coreconeCorrection", &m_ph_topoetcone20coreconeCorrection, "ph_topoetcone20coreconeCorrection/F");
      outputTree->Branch("ph_topoetcone40core57Correction", &m_ph_topoetcone40core57Correction, "ph_topoetcone40core57Correction/F");
      outputTree->Branch("ph_topoetcone30core57Correction", &m_ph_topoetcone30core57Correction, "ph_topoetcone30core57Correction/F");
      outputTree->Branch("ph_topoetcone20core57Correction", &m_ph_topoetcone20core57Correction, "ph_topoetcone20core57Correction/F");
      outputTree->Branch("ph_neflowisol40", &m_ph_neflowisol40, "ph_neflowisol40/F");
      outputTree->Branch("ph_neflowisol30", &m_ph_neflowisol30, "ph_neflowisol30/F");
      outputTree->Branch("ph_neflowisol20", &m_ph_neflowisol20, "ph_neflowisol20/F");
      outputTree->Branch("ph_cl_E_TileGap3", &m_ph_cl_E_TileGap3, "ph_cl_E_TileGap3/F");
      outputTree->Branch("ph_cl_E_TileGap2", &m_ph_cl_E_TileGap2, "ph_cl_E_TileGap2/F");
      outputTree->Branch("ph_cl_E_TileGap1", &m_ph_cl_E_TileGap1, "ph_cl_E_TileGap1/F");
    }
    else{


      m_vec_ph_CaloPointing_eta = new std::vector<float>();
      m_vec_ph_cl_E = new std::vector<float>();
      m_vec_ph_cl_eta = new std::vector<float>();
      m_vec_ph_cl_etaCalo = new std::vector<float>();
      m_vec_ph_cl_phi = new std::vector<float>();
      m_vec_ph_cl_phiCalo = new std::vector<float>();
      m_vec_ph_author = new std::vector<int>();
      m_vec_ph_convFlag = new std::vector<int>();
      m_vec_ph_convMatchDeltaPhi1 = new std::vector<float>();
      m_vec_ph_convMatchDeltaPhi2 = new std::vector<float>();
      m_vec_ph_convMatchDeltaEta1 = new std::vector<float>();
      m_vec_ph_convMatchDeltaEta2 = new std::vector<float>();
      m_vec_ph_convTrk1_DeltaPhi_track_calo = new std::vector<float>();
      m_vec_ph_convtrk1nPixHits = new std::vector<int>();
      m_vec_ph_convtrk1nSCTHits = new std::vector<int>();
      m_vec_ph_convTrk2_DeltaPhi_track_calo = new std::vector<float>();
      m_vec_ph_convtrk2nPixHits = new std::vector<int>();
      m_vec_ph_convtrk2nSCTHits = new std::vector<int>();
      m_vec_ph_etas1 = new std::vector<float>();
      m_vec_ph_etas2 = new std::vector<float>();
      m_vec_ph_Ethad = new std::vector<float>();
      m_vec_ph_Ethad1 = new std::vector<float>();
      m_vec_ph_fside = new std::vector<float>();
      m_vec_ph_HPV_zvertex = new std::vector<float>();
      m_vec_ph_isEM = new std::vector<int>();
      m_vec_ph_loose = new std::vector<bool>();
      m_vec_ph_materialTraversed = new std::vector<float>();
      m_vec_ph_pt1conv = new std::vector<float>();
      m_vec_ph_pt2conv = new std::vector<float>();
      m_vec_ph_ptconv = new std::vector<float>();
      m_vec_ph_raw_cl = new std::vector<float>();
      m_vec_ph_rawcl_calibHitsShowerDepth = new std::vector<float>();
      m_vec_ph_rawcl_Eacc = new std::vector<float>();
      m_vec_ph_rawcl_Es0 = new std::vector<float>();
      m_vec_ph_rawcl_Es1 = new std::vector<float>();
      m_vec_ph_rawcl_Es2 = new std::vector<float>();
      m_vec_ph_rawcl_Es3 = new std::vector<float>();
      m_vec_ph_rawcl_Et = new std::vector<float>();
      m_vec_ph_rawcl_f0 = new std::vector<float>();
      m_vec_ph_Rconv = new std::vector<float>();
      m_vec_ph_E237 = new std::vector<float>();
      m_vec_ph_E233 = new std::vector<float>();
      m_vec_ph_E277 = new std::vector<float>();
      m_vec_ph_reta = new std::vector<float>();
      m_vec_ph_rphi = new std::vector<float>();
      m_vec_ph_tight = new std::vector<bool>();
      m_vec_ph_truth_E = new std::vector<float>();
      m_vec_ph_truth_pt = new std::vector<float>();
      m_vec_ph_truth_eta = new std::vector<float>();
      m_vec_ph_truth_matched = new std::vector<bool>();
      m_vec_ph_truth_phi = new std::vector<float>();
      m_vec_ph_truth_Rconv = new std::vector<float>();
      m_vec_ph_truth_type = new std::vector<int>();
      m_vec_ph_truth_parent_pdgId = new std::vector<int>();
      m_vec_ph_weta2 = new std::vector<float>();
      m_vec_ph_ws3 = new std::vector<float>();
      m_vec_ph_wstot = new std::vector<float>();
      m_vec_ph_zconv = new std::vector<float>();
      m_vec_ph_DeltaE = new std::vector<float>();
      m_vec_ph_Eratio = new std::vector<float>();
      m_vec_ph_Rhad = new std::vector<float>();
      m_vec_ph_Rhad1 = new std::vector<float>();


      outputTree->Branch("ph_truth_n", &m_ph_truth_n,"ph_truth_n/I");
      outputTree->Branch("ph_n", &m_ph_n,"ph_n/I");
      outputTree->Branch("ph_CaloPointing_eta","vector<float>", &m_vec_ph_CaloPointing_eta);
      outputTree->Branch("ph_cl_E","vector<float>", &m_vec_ph_cl_E);
      outputTree->Branch("ph_cl_eta","vector<float>", &m_vec_ph_cl_eta);
      outputTree->Branch("ph_cl_etaCalo","vector<float>", &m_vec_ph_cl_etaCalo);
      outputTree->Branch("ph_cl_phi","vector<float>", &m_vec_ph_cl_phi);
      outputTree->Branch("ph_cl_phiCalo","vector<float>", &m_vec_ph_cl_phiCalo);
      outputTree->Branch("ph_author","vector<int>", &m_vec_ph_author);
      outputTree->Branch("ph_convFlag","vector<int>", &m_vec_ph_convFlag);
      outputTree->Branch("ph_convMatchDeltaPhi1","vector<float>", &m_vec_ph_convMatchDeltaPhi1);
      outputTree->Branch("ph_convMatchDeltaPhi2","vector<float>", &m_vec_ph_convMatchDeltaPhi2);
      outputTree->Branch("ph_convMatchDeltaEta1","vector<float>", &m_vec_ph_convMatchDeltaEta1);
      outputTree->Branch("ph_convMatchDeltaEta2","vector<float>", &m_vec_ph_convMatchDeltaEta2);
      // outputTree->Branch("ph_convTrk1_DeltaPhi_track_calo","vector<float>", &m_vec_ph_convTrk1_DeltaPhi_track_calo);
      outputTree->Branch("ph_convtrk1nPixHits","vector<int>", &m_vec_ph_convtrk1nPixHits);
      outputTree->Branch("ph_convtrk1nSCTHits","vector<int>", &m_vec_ph_convtrk1nSCTHits);
      //outputTree->Branch("ph_convTrk2_DeltaPhi_track_calo","vector<float>", &m_vec_ph_convTrk2_DeltaPhi_track_calo);
      outputTree->Branch("ph_convtrk2nPixHits","vector<int>", &m_vec_ph_convtrk2nPixHits);
      outputTree->Branch("ph_convtrk2nSCTHits","vector<int>", &m_vec_ph_convtrk2nSCTHits);
      outputTree->Branch("ph_etas1","vector<float>", &m_vec_ph_etas1);
      outputTree->Branch("ph_etas2","vector<float>", &m_vec_ph_etas2);
      outputTree->Branch("ph_Ethad","vector<float>", &m_vec_ph_Ethad);
      outputTree->Branch("ph_Ethad1","vector<float>", &m_vec_ph_Ethad1);
      outputTree->Branch("ph_fside","vector<float>", &m_vec_ph_fside);
      //outputTree->Branch("ph_HPV_zvertex","vector<float>", &m_vec_ph_HPV_zvertex);
      // outputTree->Branch("ph_isEM","vector<int>", &m_vec_ph_isEM);
      outputTree->Branch("ph_loose","vector<bool>", &m_vec_ph_loose);
      //outputTree->Branch("ph_materialTraversed","vector<float>", &m_vec_ph_materialTraversed);
      outputTree->Branch("ph_pt1conv","vector<float>", &m_vec_ph_pt1conv);
      outputTree->Branch("ph_pt2conv","vector<float>", &m_vec_ph_pt2conv);
      outputTree->Branch("ph_ptconv","vector<float>", &m_vec_ph_ptconv);
      //outputTree->Branch("ph_ShowerDepth","vector<float>", &m_vec_ph_rawcl_calibHitsShowerDepth);
      outputTree->Branch("ph_rawcl_Eacc","vector<float>", &m_vec_ph_rawcl_Eacc);
      outputTree->Branch("ph_rawcl_Es0","vector<float>", &m_vec_ph_rawcl_Es0);
      outputTree->Branch("ph_rawcl_Es1","vector<float>", &m_vec_ph_rawcl_Es1);
      outputTree->Branch("ph_rawcl_Es2","vector<float>", &m_vec_ph_rawcl_Es2);
      outputTree->Branch("ph_rawcl_Es3","vector<float>", &m_vec_ph_rawcl_Es3);
      outputTree->Branch("ph_rawcl_Et","vector<float>", &m_vec_ph_rawcl_Et);
      outputTree->Branch("ph_rawcl_f0","vector<float>", &m_vec_ph_rawcl_f0);
      outputTree->Branch("ph_Rconv","vector<float>", &m_vec_ph_Rconv);
      outputTree->Branch("ph_E237","vector<float>", &m_vec_ph_E237);
      outputTree->Branch("ph_E233","vector<float>", &m_vec_ph_E233);
      outputTree->Branch("ph_E277","vector<float>", &m_vec_ph_E277);
      outputTree->Branch("ph_reta","vector<float>", &m_vec_ph_reta);
      outputTree->Branch("ph_rphi","vector<float>", &m_vec_ph_rphi);
      outputTree->Branch("ph_tight","vector<bool>", &m_vec_ph_tight);
      outputTree->Branch("ph_truth_E","vector<float>", &m_vec_ph_truth_E);
      outputTree->Branch("ph_truth_pt","vector<float>", &m_vec_ph_truth_pt);
      outputTree->Branch("ph_truth_eta","vector<float>", &m_vec_ph_truth_eta);
      outputTree->Branch("ph_truth_matched","vector<bool>", &m_vec_ph_truth_matched);
      outputTree->Branch("ph_truth_phi","vector<float>", &m_vec_ph_truth_phi);
      outputTree->Branch("ph_truth_Rconv","vector<float>", &m_vec_ph_truth_Rconv);
      outputTree->Branch("ph_truth_type","vector<int>", &m_vec_ph_truth_type);
      outputTree->Branch("ph_truth_parent_pdgId","vector<int>", &m_vec_ph_truth_parent_pdgId);
      outputTree->Branch("ph_weta2","vector<float>", &m_vec_ph_weta2);
      outputTree->Branch("ph_ws3","vector<float>", &m_vec_ph_ws3);
      outputTree->Branch("ph_wstot","vector<float>", &m_vec_ph_wstot);
      outputTree->Branch("ph_zconv","vector<float>", &m_vec_ph_zconv);
      outputTree->Branch("ph_DeltaE","vector<float>", &m_vec_ph_DeltaE);
      outputTree->Branch("ph_Eratio","vector<float>", &m_vec_ph_Eratio);
      outputTree->Branch("ph_Rhad","vector<float>", &m_vec_ph_Rhad);
      outputTree->Branch("ph_Rhad1","vector<float>", &m_vec_ph_Rhad1);
    }

  }


  else if (particleType==1) {

    if (N_particle_saved<10){
      tmp_vec_el_cl_E = new std::vector<float>();
      tmp_vec_el_cl_etaCalo = new std::vector<float>();
      tmp_vec_el_cl_phi = new std::vector<float>();
      tmp_vec_el_cl_phiCalo = new std::vector<float>();
      tmp_vec_el_author = new std::vector<int>();
      tmp_vec_el_charge = new std::vector<int>();
      tmp_vec_el_cl_eta = new std::vector<float>();
      tmp_vec_el_deltaphi2 = new std::vector<float>();
      tmp_vec_el_deltaPhiFirstLast = new std::vector<float>();
      tmp_vec_el_deltaPhiFromLast = new std::vector<float>();
      tmp_vec_el_fside = new std::vector<float>();
      tmp_vec_el_isEM = new std::vector<int>();
      tmp_vec_el_loosePP = new std::vector<bool>();
      tmp_vec_el_mediumPP = new std::vector<bool>();
      tmp_vec_el_p0 = new std::vector<float>();
      tmp_vec_el_pLast = new std::vector<float>();
      tmp_vec_el_refittedTrack_author = new std::vector<float>();
      tmp_vec_el_refittedTrack_LMqoverp = new std::vector<float>();
      tmp_vec_el_refittedTrack_qoverp = new std::vector<float>();
      tmp_vec_el_E237 = new std::vector<float>();
      tmp_vec_el_E233 = new std::vector<float>();
      tmp_vec_el_E277 = new std::vector<float>();
      tmp_vec_el_reta = new std::vector<float>();
      tmp_vec_el_rphi = new std::vector<float>();
      tmp_vec_el_Ethad = new std::vector<float>();
      tmp_vec_el_Ethad1 = new std::vector<float>();
      tmp_vec_el_tightPP = new std::vector<bool>();
      tmp_vec_el_rawcl_calibHitsShowerDepth = new std::vector<float>();
      tmp_vec_el_rawcl_Eacc = new std::vector<float>();
      tmp_vec_el_rawcl_Es0 = new std::vector<float>();
      tmp_vec_el_rawcl_Es1 = new std::vector<float>();
      tmp_vec_el_rawcl_Es2 = new std::vector<float>();
      tmp_vec_el_rawcl_Es3 = new std::vector<float>();
      tmp_vec_el_rawcl_Et = new std::vector<float>();
      tmp_vec_el_rawcl_f0 = new std::vector<float>();
      tmp_vec_el_tracketa = new std::vector<float>();
      tmp_vec_el_trackpt = new std::vector<float>();
      tmp_vec_el_trackz0 = new std::vector<float>();
      tmp_vec_el_truth_E = new std::vector<float>();
      tmp_vec_el_truth_pt = new std::vector<float>();
      tmp_vec_el_truth_eta = new std::vector<float>();
      tmp_vec_el_truth_phi = new std::vector<float>();
      tmp_vec_el_truth_type = new std::vector<int>();
      tmp_vec_el_truth_parent_pdgId = new std::vector<int>();
      tmp_vec_el_truth_matched = new std::vector<bool>();
      tmp_vec_el_weta2 = new std::vector<float>();
      tmp_vec_el_ws3 = new std::vector<float>();
      tmp_vec_el_wstot = new std::vector<float>();
      tmp_vec_el_DeltaE = new std::vector<float>();
      tmp_vec_el_Eratio = new std::vector<float>();
      tmp_vec_el_Rhad = new std::vector<float>();
      tmp_vec_el_Rhad1 = new std::vector<float>();

    }



    if(FLAT){
      outputTree->Branch("el_n", &m_el_n,"el_n/I");
      outputTree->Branch("el_truth_n", &m_el_truth_n,"el_truth_n/I");
      outputTree->Branch("el_author", &m_el_author,"el_author/I");
      outputTree->Branch("el_charge", &m_el_charge,"el_charge/I");
      outputTree->Branch("el_cl_E", &m_el_cl_E,"el_cl_E/F");
      outputTree->Branch("el_cl_eta", &m_el_cl_eta,"el_cl_eta/F");
      outputTree->Branch("el_cl_phi", &m_el_cl_phi,"el_cl_phi/F");
      outputTree->Branch("el_E", &m_el_E,"el_E/F");
      outputTree->Branch("el_eta", &m_el_eta,"el_eta/F");
      outputTree->Branch("el_phi", &m_el_phi,"el_phi/F");
 outputTree->Branch("el_cl_m", &m_el_cl_m,"el_cl_m/F");
 outputTree->Branch("el_m", &m_el_m,"el_m/F");
 outputTree->Branch("el_cl_pt", &m_el_cl_pt,"el_cl_pt/F");
       outputTree->Branch("el_cl_etaCalo", &m_el_cl_etaCalo,"el_cl_etaCalo/F");
      outputTree->Branch("el_cl_etaS1Calo", &m_el_cl_etaS1Calo,"el_cl_etaS1Calo/F");
      outputTree->Branch("el_cl_etaS2Calo", &m_el_cl_etaS2Calo,"el_cl_etaS2Calo/F");
      outputTree->Branch("el_cl_phi", &m_el_cl_phi,"el_cl_phi/F");
      outputTree->Branch("el_cl_phiCalo", &m_el_cl_phiCalo,"el_cl_phiCalo/F");
      outputTree->Branch("el_cl_phiS1Calo", &m_el_cl_phiS1Calo,"el_cl_phiS1Calo/F");
      outputTree->Branch("el_cl_phiS2Calo", &m_el_cl_phiS2Calo,"el_cl_phiS2Calo/F");
      // outputTree->Branch("el_deltaphi2", &m_el_deltaphi2,"el_deltaphi2/F");
      // outputTree->Branch("el_deltaPhiFirstLast", &m_el_deltaPhiFirstLast,"el_deltaPhiFirstLast/F");
      outputTree->Branch("el_deltaPhiFromLast", &m_el_deltaPhiFromLast,"el_deltaPhiFromLast/F");
      outputTree->Branch("el_fside", &m_el_fside,"el_fside/F");
      // outputTree->Branch("el_isEM", &m_el_isEM,"el_isEM/I");
      outputTree->Branch("el_loosePP", &m_el_loosePP,"el_loosePP/O");
      outputTree->Branch("el_mediumPP", &m_el_mediumPP,"el_mediumPP/O");
      // outputTree->Branch("el_p0", &m_el_p0,"el_p0/F");
      // outputTree->Branch("el_pLast", &m_el_pLast,"el_pLast/F");
      // outputTree->Branch("el_refittedTrack_author", &m_el_refittedTrack_author,"el_refittedTrack_author/F");
      outputTree->Branch("el_refittedTrack_LMqoverp", &m_el_refittedTrack_LMqoverp,"el_refittedTrack_LMqoverp/F");
      outputTree->Branch("el_trackcov_qoverp", &m_el_trackcov_qoverp,"el_trackcov_qoverp/F");
      outputTree->Branch("el_trackqoverp", &m_el_trackqoverp,"el_trackqoverp/F");
      outputTree->Branch("el_rawcl_Eacc", &m_el_rawcl_Eacc,"el_rawcl_Eacc/F");
      outputTree->Branch("el_rawcl_Es0", &m_el_rawcl_Es0,"el_rawcl_Es0/F");
      outputTree->Branch("el_rawcl_Es1", &m_el_rawcl_Es1,"el_rawcl_Es1/F");
      outputTree->Branch("el_rawcl_Es2", &m_el_rawcl_Es2,"el_rawcl_Es2/F");
      outputTree->Branch("el_rawcl_Es3", &m_el_rawcl_Es3,"el_rawcl_Es3/F");
      outputTree->Branch("el_rawcl_Et", &m_el_rawcl_Et,"el_rawcl_Et/F");
      //outputTree->Branch("el_ShowerDepth", &m_el_rawcl_calibHitsShowerDepth,"el_ShowerDepth/F");
      outputTree->Branch("el_rawcl_f0", &m_el_rawcl_f0,"el_rawcl_f0/F");
      outputTree->Branch("el_E237", &m_el_E237,"el_E237/F");
      outputTree->Branch("el_E233", &m_el_E233,"el_E233/F");
      outputTree->Branch("el_E277", &m_el_E277,"el_E277/F");
      outputTree->Branch("el_reta", &m_el_reta,"el_reta/F");
      outputTree->Branch("el_rphi", &m_el_rphi,"el_rphi/F");
      outputTree->Branch("el_Ethad", &m_el_Ethad,"el_Ethad/F");
      outputTree->Branch("el_Ethad1", &m_el_Ethad1,"el_Ethad1/F");
      outputTree->Branch("el_tightPP", &m_el_tightPP,"el_tightPP/O");
 outputTree->Branch("el_trackphi", &m_el_trackphi,"el_trackphi/F");      
outputTree->Branch("el_tracketa", &m_el_tracketa,"el_tracketa/F");
      outputTree->Branch("el_trackpt", &m_el_trackpt,"el_trackpt/F");
      outputTree->Branch("el_trackz0", &m_el_trackz0,"el_trackz0/F");
      outputTree->Branch("el_truth_E", &m_el_truth_E,"el_truth_E/F");
      outputTree->Branch("el_truth_eta", &m_el_truth_eta,"el_truth_eta/F");
      outputTree->Branch("el_truth_pt", &m_el_truth_pt,"el_truth_pt/F");
      outputTree->Branch("el_truth_phi", &m_el_truth_phi,"el_truth_phi/F");
      outputTree->Branch("el_truth_type", &m_el_truth_type,"el_truth_type/I");
      outputTree->Branch("el_truth_parent_pdgId", &m_el_truth_parent_pdgId,"el_truth_parent_pdgId/I");
      outputTree->Branch("el_truth_matched", &m_el_truth_matched,"el_truth_matched/O");
      outputTree->Branch("el_weta2", &m_el_weta2,"el_weta2/F");
      outputTree->Branch("el_ws3", &m_el_ws3,"el_ws3/F");
      outputTree->Branch("el_wstot", &m_el_wstot,"el_wstot/F");
      outputTree->Branch("el_DeltaE",&m_el_DeltaE, "el_DeltaE/F");
      outputTree->Branch("el_Eratio", &m_el_Eratio,"el_Eratio/F");
      outputTree->Branch("el_Rhad", &m_el_Rhad, "m_el_Rhad/F");
      outputTree->Branch("el_Rhad1", &m_el_Rhad1, "m_el_Rhad1/F");
      outputTree->Branch("el_etas1", &m_el_etas1, "el_etas1/F");
      outputTree->Branch("el_etas2", &m_el_etas2, "el_etas2/F");
      outputTree->Branch("el_FTFseed",&m_el_FTFseed, "el_FTFseed/I");
      outputTree->Branch("el_topoetcone40", &m_el_topoetcone40, "el_topoetcone40/F");
      outputTree->Branch("el_topoetcone30", &m_el_topoetcone30, "el_topoetcone30/F");
      outputTree->Branch("el_topoetcone20", &m_el_topoetcone20, "el_topoetcone20/F");
      outputTree->Branch("el_topoetcone40noCorrected", &m_el_topoetcone40noCorrected, "el_topoetcone40noCorrected/F");
      outputTree->Branch("el_topoetcone30noCorrected", &m_el_topoetcone30noCorrected, "el_topoetcone30noCorrected/F");
      outputTree->Branch("el_topoetcone20noCorrected", &m_el_topoetcone20noCorrected, "el_topoetcone20noCorrected/F");
      outputTree->Branch("el_topoetcone40toolCorrected", &m_el_topoetcone40toolCorrected, "el_topoetcone40toolCorrected/F");
      outputTree->Branch("el_topoetcone30toolCorrected", &m_el_topoetcone30toolCorrected, "el_topoetcone30toolCorrected/F");
      outputTree->Branch("el_topoetcone20toolCorrected", &m_el_topoetcone20toolCorrected, "el_topoetcone20toolCorrected/F");
      outputTree->Branch("el_topoetcone40toolCorrection", &m_el_topoetcone40toolCorrection, "el_topoetcone40toolCorrection/F");
      outputTree->Branch("el_topoetcone30toolCorrection", &m_el_topoetcone30toolCorrection, "el_topoetcone30toolCorrection/F");
      outputTree->Branch("el_topoetcone20toolCorrection", &m_el_topoetcone20toolCorrection, "el_topoetcone20toolCorrection/F");
      outputTree->Branch("el_topoetcone40coreconeCorrected", &m_el_topoetcone40coreconeCorrected, "el_topoetcone40coreconeCorrected/F");
      outputTree->Branch("el_topoetcone30coreconeCorrected", &m_el_topoetcone30coreconeCorrected, "el_topoetcone30coreconeCorrected/F");
      outputTree->Branch("el_topoetcone20coreconeCorrected", &m_el_topoetcone20coreconeCorrected, "el_topoetcone20coreconeCorrected/F");
      outputTree->Branch("el_topoetcone40coreconeCorrected", &m_el_topoetcone40coreconeCorrected, "el_topoetcone40coreconeCorrected/F");
      outputTree->Branch("el_topoetcone30coreconeCorrected", &m_el_topoetcone30coreconeCorrected, "el_topoetcone30coreconeCorrected/F");
      outputTree->Branch("el_topoetcone20coreconeCorrected", &m_el_topoetcone20coreconeCorrected, "el_topoetcone20coreconeCorrected/F");
      outputTree->Branch("el_topoetcone40ptCorrection", &m_el_topoetcone40ptCorrection, "el_topoetcone40ptCorrection/F");
      outputTree->Branch("el_topoetcone30ptCorrection", &m_el_topoetcone30ptCorrection, "el_topoetcone30ptCorrection/F");
      outputTree->Branch("el_topoetcone20ptCorrection", &m_el_topoetcone20ptCorrection, "el_topoetcone20ptCorrection/F");
      outputTree->Branch("el_topoetcone40pileupCorrection", &m_el_topoetcone40pileupCorrection, "el_topoetcone40pileupCorrection/F");
      outputTree->Branch("el_topoetcone30pileupCorrection", &m_el_topoetcone30pileupCorrection, "el_topoetcone30pileupCorrection/F");
      outputTree->Branch("el_topoetcone20pileupCorrection", &m_el_topoetcone20pileupCorrection, "el_topoetcone20pileupCorrection/F");
      outputTree->Branch("el_topoetcone40coreconeCorrection", &m_el_topoetcone40coreconeCorrection, "el_topoetcone40coreconeCorrection/F");
      outputTree->Branch("el_topoetcone30coreconeCorrection", &m_el_topoetcone30coreconeCorrection, "el_topoetcone30coreconeCorrection/F");
      outputTree->Branch("el_topoetcone20coreconeCorrection", &m_el_topoetcone20coreconeCorrection, "el_topoetcone20coreconeCorrection/F");
      outputTree->Branch("el_topoetcone40core57Correction", &m_el_topoetcone40core57Correction, "el_topoetcone40core57Correction/F");
      outputTree->Branch("el_topoetcone30core57Correction", &m_el_topoetcone30core57Correction, "el_topoetcone30core57Correction/F");
      outputTree->Branch("el_topoetcone20core57Correction", &m_el_topoetcone20core57Correction, "el_topoetcone20core57Correction/F");
      outputTree->Branch("el_neflowisol40", &m_el_neflowisol40, "el_neflowisol40/F");
      outputTree->Branch("el_neflowisol30", &m_el_neflowisol30, "el_neflowisol30/F");
      outputTree->Branch("el_neflowisol20", &m_el_neflowisol20, "el_neflowisol20/F");
      outputTree->Branch("el_cl_E_TileGap3", &m_el_cl_E_TileGap3, "el_cl_E_TileGap3/F");
      outputTree->Branch("el_cl_E_TileGap2", &m_el_cl_E_TileGap2, "el_cl_E_TileGap2/F");
      outputTree->Branch("el_cl_E_TileGap1", &m_el_cl_E_TileGap1, "el_cl_E_TileGap1/F");

    }
    else {

      m_vec_el_cl_E = new std::vector<float>();
      m_vec_el_cl_etaCalo = new std::vector<float>();
      m_vec_el_cl_phi = new std::vector<float>();
      m_vec_el_cl_phiCalo = new std::vector<float>();
      m_vec_el_author = new std::vector<int>();
      m_vec_el_charge = new std::vector<int>();
      m_vec_el_cl_eta = new std::vector<float>();
      m_vec_el_deltaphi2 = new std::vector<float>();
      m_vec_el_deltaPhiFirstLast = new std::vector<float>();
      m_vec_el_deltaPhiFromLast = new std::vector<float>();
      m_vec_el_fside = new std::vector<float>();
      m_vec_el_isEM = new std::vector<int>();
      m_vec_el_loosePP = new std::vector<bool>();
      m_vec_el_mediumPP = new std::vector<bool>();
      m_vec_el_p0 = new std::vector<float>();
      m_vec_el_pLast = new std::vector<float>();
      m_vec_el_refittedTrack_author = new std::vector<float>();
      m_vec_el_refittedTrack_LMqoverp = new std::vector<float>();
      m_vec_el_refittedTrack_qoverp = new std::vector<float>();
      m_vec_el_E237 = new std::vector<float>();
      m_vec_el_E233 = new std::vector<float>();
      m_vec_el_E277 = new std::vector<float>();
      m_vec_el_reta = new std::vector<float>();
      m_vec_el_rphi = new std::vector<float>();
      m_vec_el_Ethad = new std::vector<float>();
      m_vec_el_Ethad1 = new std::vector<float>();
      m_vec_el_tightPP = new std::vector<bool>();
      m_vec_el_rawcl_calibHitsShowerDepth = new std::vector<float>();
      m_vec_el_rawcl_Eacc = new std::vector<float>();
      m_vec_el_rawcl_Es0 = new std::vector<float>();
      m_vec_el_rawcl_Es1 = new std::vector<float>();
      m_vec_el_rawcl_Es2 = new std::vector<float>();
      m_vec_el_rawcl_Es3 = new std::vector<float>();
      m_vec_el_rawcl_Et = new std::vector<float>();
      m_vec_el_rawcl_f0 = new std::vector<float>();
      m_vec_el_tracketa = new std::vector<float>();
      m_vec_el_trackpt = new std::vector<float>();
      m_vec_el_trackz0 = new std::vector<float>();
      m_vec_el_truth_E = new std::vector<float>();
      m_vec_el_truth_pt = new std::vector<float>();
      m_vec_el_truth_eta = new std::vector<float>();
      m_vec_el_truth_phi = new std::vector<float>();
      m_vec_el_truth_type = new std::vector<int>();
      m_vec_el_truth_parent_pdgId = new std::vector<int>();
      m_vec_el_truth_matched = new std::vector<bool>();
      m_vec_el_weta2 = new std::vector<float>();
      m_vec_el_ws3 = new std::vector<float>();
      m_vec_el_wstot = new std::vector<float>();
      m_vec_el_DeltaE = new std::vector<float>();
      m_vec_el_Eratio = new std::vector<float>();
      m_vec_el_Rhad = new std::vector<float>();
      m_vec_el_Rhad1 = new std::vector<float>();


      outputTree->Branch("el_n", &m_el_n,"el_n/I");
      outputTree->Branch("el_truth_n", &m_el_truth_n,"el_truth_n/I");
      outputTree->Branch("el_author","vector<int>", &m_vec_el_author);
      outputTree->Branch("el_charge","vector<int>", &m_vec_el_charge);
      outputTree->Branch("el_cl_E","vector<float>", &m_vec_el_cl_E);
      outputTree->Branch("el_cl_eta","vector<float>", &m_vec_el_cl_eta);
      outputTree->Branch("el_cl_phi","vector<float>", &m_vec_el_cl_phi);
      outputTree->Branch("el_cl_etaCalo","vector<float>", &m_vec_el_cl_etaCalo);
      outputTree->Branch("el_cl_phiCalo","vector<float>", &m_vec_el_cl_phiCalo);
      // outputTree->Branch("el_deltaphi2","vector<float>", &m_vec_el_deltaphi2);
      // outputTree->Branch("el_deltaPhiFirstLast","vector<float>", &m_vec_el_deltaPhiFirstLast);
      outputTree->Branch("el_deltaPhiFromLast","vector<float>", &m_vec_el_deltaPhiFromLast);
      outputTree->Branch("el_fside","vector<float>", &m_vec_el_fside);
      // outputTree->Branch("el_isEM","vector<int>", &m_vec_el_isEM);
      outputTree->Branch("el_loosePP","vector<bool>", &m_vec_el_loosePP);
      outputTree->Branch("el_mediumPP","vector<bool>", &m_vec_el_mediumPP);
      // outputTree->Branch("el_p0","vector<float>", &m_vec_el_p0);
      // outputTree->Branch("el_pLast","vector<float>", &m_vec_el_pLast);
      // outputTree->Branch("el_refittedTrack_author","vector<float>", &m_vec_el_refittedTrack_author);
      // outputTree->Branch("el_refittedTrack_LMqoverp","vector<float>", &m_vec_el_refittedTrack_LMqoverp);
      outputTree->Branch("el_refittedTrack_qoverp","vector<float>", &m_vec_el_refittedTrack_qoverp);
      outputTree->Branch("el_rawcl_Eacc","vector<float>", &m_vec_el_rawcl_Eacc);
      outputTree->Branch("el_rawcl_Es0","vector<float>", &m_vec_el_rawcl_Es0);
      outputTree->Branch("el_rawcl_Es1","vector<float>", &m_vec_el_rawcl_Es1);
      outputTree->Branch("el_rawcl_Es2","vector<float>", &m_vec_el_rawcl_Es2);
      outputTree->Branch("el_rawcl_Es3","vector<float>", &m_vec_el_rawcl_Es3);
      outputTree->Branch("el_rawcl_Et","vector<float>", &m_vec_el_rawcl_Et);
      //outputTree->Branch("el_ShowerDepth","vector<float>", &m_vec_el_rawcl_calibHitsShowerDepth);
      outputTree->Branch("el_rawcl_f0","vector<float>", &m_vec_el_rawcl_f0);
      outputTree->Branch("el_E237","vector<float>", &m_vec_el_E237);
      outputTree->Branch("el_E233","vector<float>", &m_vec_el_E233);
      outputTree->Branch("el_E277","vector<float>", &m_vec_el_E277);
      outputTree->Branch("el_reta","vector<float>", &m_vec_el_reta);
      outputTree->Branch("el_rphi","vector<float>", &m_vec_el_rphi);
      outputTree->Branch("el_Ethad","vector<float>", &m_vec_el_Ethad);
      outputTree->Branch("el_Ethad1","vector<float>", &m_vec_el_Ethad1);
      outputTree->Branch("el_tightPP","vector<bool>", &m_vec_el_tightPP);
      outputTree->Branch("el_tracketa","vector<float>", &m_vec_el_tracketa);
      outputTree->Branch("el_trackpt","vector<float>", &m_vec_el_trackpt);
      outputTree->Branch("el_trackz0","vector<float>", &m_vec_el_trackz0);
      outputTree->Branch("el_truth_E","vector<float>", &m_vec_el_truth_E);
      outputTree->Branch("el_truth_pt","vector<float>", &m_vec_el_truth_pt);
      outputTree->Branch("el_truth_eta","vector<float>", &m_vec_el_truth_eta);
      outputTree->Branch("el_truth_phi","vector<float>", &m_vec_el_truth_phi);
      outputTree->Branch("el_truth_type","vector<int>", &m_vec_el_truth_type);
      outputTree->Branch("el_truth_el_truth_parent_pdgId","vector<int>", &m_vec_el_truth_parent_pdgId);
      outputTree->Branch("el_truth_matched","vector<bool>", &m_vec_el_truth_matched);
      outputTree->Branch("el_weta2","vector<float>", &m_vec_el_weta2);
      outputTree->Branch("el_ws3","vector<float>", &m_vec_el_ws3);
      outputTree->Branch("el_wstot","vector<float>", &m_vec_el_wstot);
      outputTree->Branch("el_DeltaE","vector<float>", &m_vec_el_DeltaE);
      outputTree->Branch("el_Eratio","vector<float>", &m_vec_el_Eratio);
      outputTree->Branch("m_el_Rhad","vector<float>", &m_vec_el_Rhad);
      outputTree->Branch("m_el_Rhad1","vector<float>", &m_vec_el_Rhad1);
    }

  }
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode dumpxAODntuple::execute ()
{
  if( (m_eventCounter % 1000) == 0 ) Info("execute()", "Event number = %i", m_eventCounter );
  m_eventCounter++;


  const xAOD::EventInfo* eventInfo = 0;
  if( ! m_event->retrieve( eventInfo, "EventInfo").isSuccess() ) {
    Error("execute()", "Failed to retrieve event info collection. Exiting." );
    return EL::StatusCode::FAILURE;
  }
  m_actualIntPerXing = eventInfo->actualInteractionsPerCrossing();
  m_averageIntPerXing= eventInfo->averageInteractionsPerCrossing();
  m_EventNumber=eventInfo->eventNumber();
  m_RunNumber=eventInfo->runNumber();
  m_bcid=eventInfo->bcid();

  int npv=0;
  const xAOD::VertexContainer* vtx = 0;

  if ( !m_event->retrieve( vtx, "PrimaryVertices" ).isSuccess() ){ // retrieve arguments: container type, container key
    Error("execute()", "Failed to retrieve Vertex container. Exiting." );
    return EL::StatusCode::FAILURE;
  }


  xAOD::VertexContainer::const_iterator vtx_itr = vtx->begin();
  xAOD::VertexContainer::const_iterator vtx_end = vtx->end();
  for( ; vtx_itr != vtx_end; ++vtx_itr ) {
    if( (*vtx_itr)->vertexType() == 1 || (*vtx_itr)->vertexType() == 3 ){
      if( (*vtx_itr)->nTrackParticles() >= 2 ){
        npv++;
      }
    }
  }
  m_PhotonPV_n=npv;
  
  
  
   const xAOD::EventShape* eventShape_central_xaod = 0;
    if( ! m_event->retrieve( eventShape_central_xaod, "TopoClusterIsoCentralEventShape").isSuccess() ){
        Error("execute()", "Failed to retrieve event TopoClusterIsoCentralEventShape collection. Exiting." );
        return EL::StatusCode::FAILURE;
    }

    double density_central_xaod = 0;
    eventShape_central_xaod->getDensity(xAOD::EventShape::Density, density_central_xaod);
    //std::cout<<"eventShape_central_xaod: "<<density_central_xaod<<std::endl;
    //std::cout<<"  eventShape_central_diff: "<<density_central - density_central_xaod<<std::endl;

    double ED_central_xaod = density_central_xaod;

    const xAOD::EventShape* eventShape_forward_xaod = 0;
    if( ! m_event->retrieve( eventShape_forward_xaod, "TopoClusterIsoForwardEventShape").isSuccess() ){
      Error("execute()", "Failed to retrieve event TopoClusterIsoForwardEventShape collection. Exiting." );
      return EL::StatusCode::FAILURE;
    }

    double density_forward_xaod = 0;
    eventShape_forward_xaod->getDensity(xAOD::EventShape::Density, density_forward_xaod);
    //std::cout<<"eventShape_forward_xaod: "<<density_forward_xaod<<std::endl;
    //std::cout<<"  eventShape_forward_diff: "<<density_forward - density_forward_xaod<<std::endl;
    double ED_forward_xaod = density_forward_xaod;

  if(particleType==0){




    if(!FLAT){
      m_vec_ph_CaloPointing_eta->clear();
      m_vec_ph_cl_E->clear();
      m_vec_ph_cl_eta->clear();
      m_vec_ph_cl_etaCalo->clear();
      m_vec_ph_cl_phi->clear();
      m_vec_ph_cl_phiCalo->clear();
      m_vec_ph_author->clear();
      m_vec_ph_convFlag->clear();
      m_vec_ph_convMatchDeltaPhi1->clear();
      m_vec_ph_convMatchDeltaPhi2->clear();
      m_vec_ph_convMatchDeltaEta1->clear();
      m_vec_ph_convMatchDeltaEta2->clear();
      m_vec_ph_convTrk1_DeltaPhi_track_calo->clear();
      m_vec_ph_convtrk1nPixHits->clear();
      m_vec_ph_convtrk1nSCTHits->clear();
      m_vec_ph_convTrk2_DeltaPhi_track_calo->clear();
      m_vec_ph_convtrk2nPixHits->clear();
      m_vec_ph_convtrk2nSCTHits->clear();
      m_vec_ph_etas1->clear();
      m_vec_ph_etas2->clear();
      m_vec_ph_Ethad->clear();
      m_vec_ph_Ethad1->clear();
      m_vec_ph_fside->clear();
      m_vec_ph_HPV_zvertex->clear();
      m_vec_ph_isEM->clear();
      m_vec_ph_loose->clear();
      m_vec_ph_materialTraversed->clear();
      m_vec_ph_pt1conv->clear();
      m_vec_ph_pt2conv->clear();
      m_vec_ph_ptconv->clear();
      m_vec_ph_raw_cl->clear();
      m_vec_ph_rawcl_calibHitsShowerDepth->clear();
      m_vec_ph_rawcl_Eacc->clear();
      m_vec_ph_rawcl_Es0->clear();
      m_vec_ph_rawcl_Es1->clear();
      m_vec_ph_rawcl_Es2->clear();
      m_vec_ph_rawcl_Es3->clear();
      m_vec_ph_rawcl_Et->clear();
      m_vec_ph_rawcl_f0->clear();
      m_vec_ph_Rconv->clear();
      m_vec_ph_E237->clear();
      m_vec_ph_E233->clear();
      m_vec_ph_E277->clear();
      m_vec_ph_reta->clear();
      m_vec_ph_rphi->clear();
      m_vec_ph_tight->clear();
      m_vec_ph_truth_E->clear();
      m_vec_ph_truth_pt->clear();
      m_vec_ph_truth_eta->clear();
      m_vec_ph_truth_matched->clear();
      m_vec_ph_truth_phi->clear();
      m_vec_ph_truth_Rconv->clear();
      m_vec_ph_truth_type->clear();
      m_vec_ph_truth_parent_pdgId->clear();
      m_vec_ph_weta2->clear();
      m_vec_ph_ws3->clear();
      m_vec_ph_DeltaE->clear();
      m_vec_ph_Eratio->clear();
      m_vec_ph_Rhad->clear();
      m_vec_ph_Rhad1->clear();
      m_vec_ph_wstot->clear();
      m_vec_ph_zconv->clear();
    }

    if (N_particle_saved<10){
      tmp_vec_ph_CaloPointing_eta->clear();
      tmp_vec_ph_cl_E->clear();
      tmp_vec_ph_cl_eta->clear();
      tmp_vec_ph_cl_etaCalo->clear();
      tmp_vec_ph_cl_phi->clear();
      tmp_vec_ph_cl_phiCalo->clear();
      tmp_vec_ph_author->clear();
      tmp_vec_ph_convFlag->clear();
      tmp_vec_ph_convMatchDeltaPhi1->clear();
      tmp_vec_ph_convMatchDeltaPhi2->clear();
      tmp_vec_ph_convMatchDeltaEta1->clear();
      tmp_vec_ph_convMatchDeltaEta2->clear();
      tmp_vec_ph_convTrk1_DeltaPhi_track_calo->clear();
      tmp_vec_ph_convtrk1nPixHits->clear();
      tmp_vec_ph_convtrk1nSCTHits->clear();
      tmp_vec_ph_convTrk2_DeltaPhi_track_calo->clear();
      tmp_vec_ph_convtrk2nPixHits->clear();
      tmp_vec_ph_convtrk2nSCTHits->clear();
      tmp_vec_ph_etas1->clear();
      tmp_vec_ph_etas2->clear();
      tmp_vec_ph_Ethad->clear();
      tmp_vec_ph_Ethad1->clear();
      tmp_vec_ph_fside->clear();
      tmp_vec_ph_HPV_zvertex->clear();
      tmp_vec_ph_isEM->clear();
      tmp_vec_ph_loose->clear();
      tmp_vec_ph_materialTraversed->clear();
      tmp_vec_ph_pt1conv->clear();
      tmp_vec_ph_pt2conv->clear();
      tmp_vec_ph_ptconv->clear();
      tmp_vec_ph_raw_cl->clear();
      tmp_vec_ph_rawcl_calibHitsShowerDepth->clear();
      tmp_vec_ph_rawcl_Eacc->clear();
      tmp_vec_ph_rawcl_Es0->clear();
      tmp_vec_ph_rawcl_Es1->clear();
      tmp_vec_ph_rawcl_Es2->clear();
      tmp_vec_ph_rawcl_Es3->clear();
      tmp_vec_ph_rawcl_Et->clear();
      tmp_vec_ph_rawcl_f0->clear();
      tmp_vec_ph_Rconv->clear();
      tmp_vec_ph_E237->clear();
      tmp_vec_ph_E233->clear();
      tmp_vec_ph_E277->clear();
      tmp_vec_ph_reta->clear();
      tmp_vec_ph_rphi->clear();
      tmp_vec_ph_tight->clear();
      tmp_vec_ph_truth_E->clear();
      tmp_vec_ph_truth_pt->clear();
      tmp_vec_ph_truth_eta->clear();
      tmp_vec_ph_truth_matched->clear();
      tmp_vec_ph_truth_phi->clear();
      tmp_vec_ph_truth_Rconv->clear();
      tmp_vec_ph_truth_type->clear();
      tmp_vec_ph_truth_parent_pdgId->clear();
      tmp_vec_ph_weta2->clear();
      tmp_vec_ph_ws3->clear();
      tmp_vec_ph_DeltaE->clear();
      tmp_vec_ph_Eratio->clear();
      tmp_vec_ph_Rhad->clear();
      tmp_vec_ph_Rhad1->clear();
      tmp_vec_ph_wstot->clear();
      tmp_vec_ph_zconv->clear();
    }

    const xAOD::TruthParticleContainer* truth = 0;
    if ( !m_event->retrieve( truth, "egammaTruthParticles" ).isSuccess() ){ // retrieve arguments: container type, container key
      Error("execute()", "Failed to retrieve Truth Electron container. Exiting." );
      return EL::StatusCode::FAILURE;
    }
    //xAOD::TruthParticleContainer::const_iterator ph_th_itr = truth->begin();
    //xAOD::TruthParticleContainer::const_iterator ph_th_end = truth->end();
    m_ph_truth_n = 0;
    for ( auto ph_th_itr : *truth ) {
      if((ph_th_itr)->absPdgId()==22) m_ph_truth_n++;
    }

    const xAOD::PhotonContainer* photon = 0;

    if(doOnline){
      if ( !m_event->retrieve( photon, "HLT_xAOD__PhotonContainer_egamma_Photons" ).isSuccess() ){
        Error("execute()", "Failed to retrieve HLT_xAOD__PhotonContainer_egamma_Photons. Exiting." );
        return EL::StatusCode::FAILURE;
      }
    } else {
      if ( !m_event->retrieve( photon, "Photons" ).isSuccess() ){ // retrieve arguments: container type, container key
        Error("execute()", "Failed to retrieve Photon container. Exiting." );
        return EL::StatusCode::FAILURE;
      }
    }



    m_ph_n=photon->size();

    if (photon->size()>0){
      for( auto ph_itr : *photon ) {
        if( !(ph_itr)->caloCluster() ) { m_problems++; continue;}
        m_sane++;
        /*(ph_itr)->isAvailable<char>("Loose");
        if(((ph_itr)->auxdata<char>("Loose"))==1)m_ph_loose=true;
        else m_ph_loose=false;
        (ph_itr)->isAvailable<char>("Tight");
        if(((ph_itr)->auxdata<char>("Tight"))==1) m_ph_tight=true;
        else m_ph_tight=false;
        (ph_itr)->passSelection(m_ph_loose, "Loose");
        m_ph_tight=m_photonTightIsEMSelector->accept(*ph_itr);*/
        m_ph_cl_E=(ph_itr)->caloCluster()->e();
        m_ph_cl_eta=(ph_itr)->caloCluster()->eta();
        //m_ph_cl_etaCalo=(ph_itr)->caloCluster()->auxdata<float>("etaCalo");
        m_ph_cl_phi=(ph_itr)->caloCluster()->phi();
        m_ph_E=(ph_itr)->e();
        m_ph_eta=(ph_itr)->eta();
        m_ph_phi=(ph_itr)->phi();
        //m_ph_cl_phiCalo=(ph_itr)->caloCluster()->auxdata<float>("phiCalo");
        m_ph_author=(ph_itr)->auxdata<unsigned short int>("author");

        double etaCalo, etaS1Calo,etaS2Calo,phiCalo,phiS1Calo,phiS2Calo;
        (ph_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::ETACALOFRAME,etaCalo);
        m_ph_cl_etaCalo=etaCalo;
        (ph_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::ETA1CALOFRAME,etaS1Calo);
        m_ph_cl_etaS1Calo=etaS1Calo;
        (ph_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::ETA2CALOFRAME,etaS2Calo);
        m_ph_cl_etaS2Calo=etaS2Calo;
        (ph_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::PHICALOFRAME,phiCalo);
        m_ph_cl_phiCalo=phiCalo;
        (ph_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::PHI1CALOFRAME,phiS1Calo);
        m_ph_cl_phiS1Calo=phiS1Calo;
        (ph_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::PHI1CALOFRAME,phiS2Calo);
        m_ph_cl_phiS2Calo=phiS2Calo;

        (ph_itr)->showerShapeValue(m_ph_Ethad, xAOD::EgammaParameters::ShowerShapeType::ethad);
        (ph_itr)->showerShapeValue(m_ph_Ethad1,xAOD::EgammaParameters::ShowerShapeType::ethad1);
        (ph_itr)->showerShapeValue(m_ph_weta2, xAOD::EgammaParameters::ShowerShapeType::weta2);
        (ph_itr)->showerShapeValue(m_ph_wstot, xAOD::EgammaParameters::ShowerShapeType::wtots1);
        (ph_itr)->showerShapeValue(m_ph_ws3, xAOD::EgammaParameters::ShowerShapeType::weta1);
        (ph_itr)->showerShapeValue(m_ph_fside, xAOD::EgammaParameters::ShowerShapeType::fracs1);
        (ph_itr)->showerShapeValue(m_ph_DeltaE, xAOD::EgammaParameters::ShowerShapeType::DeltaE);
        (ph_itr)->showerShapeValue(m_ph_Eratio, xAOD::EgammaParameters::ShowerShapeType::Eratio);
        (ph_itr)->showerShapeValue(m_ph_Rhad, xAOD::EgammaParameters::ShowerShapeType::Rhad);
        (ph_itr)->showerShapeValue(m_ph_Rhad1, xAOD::EgammaParameters::ShowerShapeType::Rhad1);
        (ph_itr)->showerShapeValue(m_ph_E237, xAOD::EgammaParameters::ShowerShapeType::e237);
        (ph_itr)->showerShapeValue(m_ph_E277, xAOD::EgammaParameters::ShowerShapeType::e277);
        (ph_itr)->showerShapeValue(m_ph_E233, xAOD::EgammaParameters::ShowerShapeType::e233);
        (ph_itr)->showerShapeValue(m_ph_e2tsts1, xAOD::EgammaParameters::ShowerShapeType::e2tsts1);
        (ph_itr)->showerShapeValue(m_ph_emaxs1, xAOD::EgammaParameters::ShowerShapeType::emaxs1);
        (ph_itr)->showerShapeValue(m_ph_emins1, xAOD::EgammaParameters::ShowerShapeType::emins1);

        //(ph_itr)->showerShapeValue( m_ph_rawcl_calibHitsShowerDepth, xAOD::EgammaParameters::ShowerShapeType::depth);

        m_ph_reta= m_ph_E277 !=0 ? (m_ph_E237/m_ph_E277) : -999. ;

        m_ph_rphi= m_ph_E237 !=0 ? (m_ph_E233/m_ph_E237) : -999;

        /*m_ph_Eratio= (m_ph_emaxs1+m_ph_e2tsts1)!=0 ? (m_ph_emaxs1-m_ph_e2tsts1)/(m_ph_emaxs1+m_ph_e2tsts1) : -999.;

        m_ph_DeltaE= (m_ph_e2tsts1-m_ph_emins1);

        m_ph_Rhad= (m_ph_cl_E/cosh(m_ph_etas2))!=0. ?   m_ph_Ethad / (m_ph_cl_E/cosh(m_ph_etas2)) : -999;

        m_ph_Rhad1= (m_ph_cl_E/cosh(m_ph_etas2))!=0. ?  m_ph_Ethad1 / (m_ph_cl_E/cosh(m_ph_etas2)) : -999;*/

        //std::cout<<m_ph_reta<<" "<<m_ph_rphi<<" "<<m_ph_E237<<" "<<m_ph_E277<<" "<<m_ph_E233<<" "<<m_ph_Eratio<<" "<<m_ph_DeltaE<<" "<<m_ph_Rhad<<" "<<m_ph_Rhad1<<std::endl;
        // photon_isem->accept((*ph_itr));
        //m_ph_isEM=photon_isem->IsemValue();
        (ph_itr)->vertexCaloMatchValue( m_ph_convMatchDeltaPhi1,xAOD::EgammaParameters::convMatchDeltaPhi1);
        (ph_itr)->vertexCaloMatchValue( m_ph_convMatchDeltaPhi2,xAOD::EgammaParameters::convMatchDeltaPhi2);
        (ph_itr)->vertexCaloMatchValue( m_ph_convMatchDeltaEta1,xAOD::EgammaParameters::convMatchDeltaEta1);
        (ph_itr)->vertexCaloMatchValue( m_ph_convMatchDeltaEta2,xAOD::EgammaParameters::convMatchDeltaEta2);
        m_ph_convFlag=xAOD::EgammaHelpers::conversionType((ph_itr));

        if(doOnline){

        m_ph_topoetcone40 = -999.;
        m_ph_topoetcone30 = -999.;
        m_ph_topoetcone20 = -999.;
        m_ph_etcone40 = -999.;
        m_ph_etcone30 = -999.;
        m_ph_etcone20 = -999.;
        }
        else{
        m_ph_topoetcone40 = ((ph_itr)->isolationValue(xAOD::Iso::topoetcone40));
        m_ph_topoetcone40ptCorrection = (ph_itr)->auxdata<float>("topoetcone40ptCorrection");
        m_ph_topoetcone30 = ((ph_itr)->isolationValue(xAOD::Iso::topoetcone30));
        m_ph_topoetcone30ptCorrection =(ph_itr)->auxdata<float>("topoetcone30ptCorrection");
        m_ph_topoetcone20 = ((ph_itr)->isolationValue(xAOD::Iso::topoetcone20));
        m_ph_topoetcone20ptCorrection = (ph_itr)->auxdata<float>("topoetcone20ptCorrection");
        
        
         float etas2 = (ph_itr)->caloCluster()->etaBE(2);
    if(etas2>-1.5 && etas2<1.5){
        m_ph_topoetcone40pileupCorrection = ED_central_xaod * 3.1415 * (0.16 - 0.875/128);
        m_ph_topoetcone30pileupCorrection = ED_central_xaod * 3.1415 * (0.09 - 0.875/128);
        m_ph_topoetcone20pileupCorrection = ED_central_xaod * 3.1415 * (0.04 - 0.875/128);
    }else{
        m_ph_topoetcone40pileupCorrection = ED_forward_xaod * 3.1415 * (0.16 - 0.875/128);
        m_ph_topoetcone30pileupCorrection = ED_forward_xaod * 3.1415 * (0.09 - 0.875/128);
        m_ph_topoetcone20pileupCorrection = ED_forward_xaod * 3.1415 * (0.04 - 0.875/128);
    }



      (ph_itr)->isolationCaloCorrection(m_ph_topoetcone40coreconeCorrection,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::coreCone, xAOD::Iso::coreEnergy);
      (ph_itr)->isolationCaloCorrection(m_ph_topoetcone30coreconeCorrection,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::coreCone, xAOD::Iso::coreEnergy);
      (ph_itr)->isolationCaloCorrection(m_ph_topoetcone20coreconeCorrection,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::coreCone, xAOD::Iso::coreEnergy);
      (ph_itr)->isolationCaloCorrection(m_ph_topoetcone40core57Correction,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::core57cells, xAOD::Iso::coreEnergy);
      (ph_itr)->isolationCaloCorrection(m_ph_topoetcone30core57Correction,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::core57cells, xAOD::Iso::coreEnergy);
      (ph_itr)->isolationCaloCorrection(m_ph_topoetcone20core57Correction,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::core57cells, xAOD::Iso::coreEnergy);
      m_ph_neflowisol40=((ph_itr)->isolationValue(xAOD::Iso::neflowisol40));
      m_ph_neflowisol30=((ph_itr)->isolationValue(xAOD::Iso::neflowisol30));
      m_ph_neflowisol20=((ph_itr)->isolationValue(xAOD::Iso::neflowisol20));

      m_ph_topoetcone40coreconeCorrected = m_ph_topoetcone40+m_ph_topoetcone40ptCorrection+m_ph_topoetcone40pileupCorrection+m_ph_topoetcone40core57Correction-m_ph_topoetcone40coreconeCorrection;
      m_ph_topoetcone30coreconeCorrected = m_ph_topoetcone30+m_ph_topoetcone30ptCorrection+m_ph_topoetcone30pileupCorrection+m_ph_topoetcone30core57Correction-m_ph_topoetcone30coreconeCorrection;
      m_ph_topoetcone20coreconeCorrected = m_ph_topoetcone20+m_ph_topoetcone20ptCorrection+m_ph_topoetcone20pileupCorrection+m_ph_topoetcone20core57Correction-m_ph_topoetcone20coreconeCorrection;

      m_ph_topoetcone40noCorrected = m_ph_topoetcone40+m_ph_topoetcone40ptCorrection+m_ph_topoetcone40pileupCorrection;
      m_ph_topoetcone30noCorrected = m_ph_topoetcone30+m_ph_topoetcone30ptCorrection+m_ph_topoetcone30pileupCorrection;
      m_ph_topoetcone20noCorrected = m_ph_topoetcone20+m_ph_topoetcone20ptCorrection+m_ph_topoetcone20pileupCorrection;

        m_ph_etcone40 = ((ph_itr)->isolationValue(xAOD::Iso::etcone40));
        m_ph_etcone30 = ((ph_itr)->isolationValue(xAOD::Iso::etcone30));
        m_ph_etcone20 = ((ph_itr)->isolationValue(xAOD::Iso::etcone20));

        const   xAOD::Egamma * ph_cast= (xAOD::Egamma *)ph_itr;
        /*m_ph_topoetcone20toolCorrection=isoCorr_tool_20->GetPtCorrection(*ph_cast,xAOD::Iso::IsolationType::topoetcone20);
        m_ph_topoetcone30toolCorrection=isoCorr_tool_20->GetPtCorrection(*ph_cast,xAOD::Iso::IsolationType::topoetcone30);
        m_ph_topoetcone40toolCorrection=isoCorr_tool_20->GetPtCorrection(*ph_cast,xAOD::Iso::IsolationType::topoetcone40);
        m_ph_topoetcone30toolCorrected=m_ph_topoetcone30noCorrected-m_ph_topoetcone30toolCorrection-m_ph_topoetcone30pileupCorrection;
        m_ph_topoetcone20toolCorrected=m_ph_topoetcone20noCorrected-m_ph_topoetcone20toolCorrection-m_ph_topoetcone20pileupCorrection;
        m_ph_topoetcone40toolCorrected=m_ph_topoetcone40noCorrected-m_ph_topoetcone40toolCorrection-m_ph_topoetcone40pileupCorrection;*/
        
        
        }
        if(m_ph_convFlag==3 ) m_ph_convFlag=2 ;
        else if(m_ph_convFlag!=0) m_ph_convFlag=1;


        m_ph_rawcl_Es0=(ph_itr)->caloCluster()->energyBE(0);
        m_ph_rawcl_Es1=(ph_itr)->caloCluster()->energyBE(1);
        m_ph_rawcl_Es2=(ph_itr)->caloCluster()->energyBE(2);
        m_ph_rawcl_Es3=(ph_itr)->caloCluster()->energyBE(3);
        m_ph_rawcl_Eacc=m_ph_rawcl_Es1+m_ph_rawcl_Es2+m_ph_rawcl_Es3;
        m_ph_rawcl_f0=m_ph_rawcl_Es0/m_ph_rawcl_Eacc;
        m_ph_etas1=(ph_itr)->caloCluster()->etaBE(1);
        m_ph_etas2=(ph_itr)->caloCluster()->etaBE(2);
        m_ph_cl_E_TileGap1=((ph_itr))->caloCluster()->eSample(CaloSampling::TileGap1);
        m_ph_cl_E_TileGap2=((ph_itr))->caloCluster()->eSample(CaloSampling::TileGap2);
        m_ph_cl_E_TileGap3=((ph_itr))->caloCluster()->eSample(CaloSampling::TileGap3);
        m_ph_rawcl_Et = m_ph_rawcl_Eacc/cosh(m_ph_etas2);

        //m_ph_CaloPointing_eta=shower->getCaloPointingEta(m_ph_etas1,m_ph_etas2,m_ph_cl_phi,eventInfo->eventType(xAOD::EventInfo::IS_SIMULATION));

        //m_ph_CaloPointing_eta=CP::IShowerDepthTool::getCaloPointingEta(m_ph_etas1, m_ph_etas2, m_ph_cl_phi, eventInfo->eventType(xAOD::EventInfo::IS_SIMULATION));
        //conversion
        const xAOD::Vertex* phVertex = (ph_itr)->vertex();
        if(!phVertex){
          m_ph_ptconv = 0;
          m_ph_pt1conv = 0;
          m_ph_pt2conv = 0;
          m_ph_convtrk1nPixHits = 0;
          m_ph_convtrk1nSCTHits = 0;
          m_ph_convtrk2nPixHits = 0;
          m_ph_convtrk2nSCTHits = 0;
          m_ph_Rconv = 0;
          m_ph_zconv = 0;
        }
        else{
          const Amg::Vector3D pos = phVertex->position();
          m_ph_Rconv = static_cast<float>(hypot (pos.x(), pos.y()));
          m_ph_zconv = pos.z();
          const xAOD::TrackParticle* tp0 = phVertex->trackParticle(0);
          const xAOD::TrackParticle* tp1 = phVertex->trackParticle(1);

          TLorentzVector sum;
          if(tp0){
            sum += tp0->p4();
            uint8_t hits;
            tp0->summaryValue(hits,xAOD::numberOfPixelHits);
            m_ph_convtrk1nPixHits = hits;
            tp0->summaryValue(hits,xAOD::numberOfSCTHits);
            m_ph_convtrk1nSCTHits = hits;

            //    m_ph_pt1conv = static_cast<float>(tp0->pt());
          }
          else{m_ph_convtrk1nPixHits=m_ph_convtrk1nSCTHits=0;}

          if(tp1){
            sum += tp1->p4();
            uint8_t hits;
            tp1->summaryValue(hits,xAOD::numberOfPixelHits);
            m_ph_convtrk2nPixHits = hits;
            tp1->summaryValue(hits,xAOD::numberOfSCTHits);
            m_ph_convtrk2nSCTHits = hits;

            //  m_ph_pt2conv = static_cast<float>(tp1->pt());
          }
          else{m_ph_convtrk2nPixHits=m_ph_convtrk2nSCTHits=0;}

          static SG::AuxElement::Accessor<float> accPt1("pt1");
          static SG::AuxElement::Accessor<float> accPt2("pt2");
          if (accPt1.isAvailable(*phVertex) && accPt2.isAvailable(*phVertex) )
          {
            m_ph_pt1conv = accPt1(*phVertex);
            m_ph_pt2conv = accPt2(*phVertex);
          }
          else
          {
            Info("execute()","pt1/pt2 not available, will approximate from first measurements");
            m_ph_pt1conv = getPtAtFirstMeasurement( tp0 );
            m_ph_pt2conv = getPtAtFirstMeasurement( tp1 );
          }

          m_ph_ptconv = sum.Perp();
        }

        // Matching to offline to retrieve the truth object and other stuff
        const xAOD::TruthParticle* true_photon = NULL;

        if(doOnline){
          const xAOD::PhotonContainer* photons = 0;
          if( !m_event->retrieve(photons, "Photons").isSuccess() ){
            Error("execute()", "Failed to retrieve PhotonCollection. Exiting.");
            return EL::StatusCode::FAILURE;
          }

          /*The real matching*/
          const xAOD::Photon* phOff = NULL;
          {
            //double GeV = 1000.;
            double drMax = 100.;
            TLorentzVector phEF;
            phEF.SetPtEtaPhiE( (ph_itr)->pt(), (ph_itr)->eta(),
            (ph_itr)->phi(), (ph_itr)->e());

            const xAOD::Photon* current = NULL;
            for( xAOD::PhotonContainer::const_iterator phOff_itr = photons->begin();
            phOff_itr != photons->end();
            ++phOff_itr){
              //if( (*phOff_itr)->e()/cosh((*phOff_itr)->eta()) < 20.*GeV) continue;
              TLorentzVector phVec;
              phVec.SetPtEtaPhiE((*phOff_itr)->pt(), (*phOff_itr)->eta(),
              (*phOff_itr)->phi(), (*phOff_itr)->e());

              double dr = phVec.DeltaR(phEF);
              if( fabs(dr) < fabs(drMax) ){
                drMax = dr;
                current = *phOff_itr;
              }
            } // for
            if( fabs(drMax) < 0.1 ) phOff = current;
            else phOff = NULL;
          }
          /*End of matching*/
          if(phOff){
            true_photon =  xAOD::TruthHelpers::getTruthParticle(*phOff);

            m_ph_tight=m_photonTightIsEMSelector->accept(phOff);
            m_ph_loose=m_photonLooseIsEMSelector->accept(phOff);
          }
        } else {
          std::cout<<"Here truth matching"<<std::endl;
          true_photon =  xAOD::TruthHelpers::getTruthParticle(*ph_itr);
          m_ph_tight=m_photonTightIsEMSelector->accept(ph_itr);
          m_ph_loose=m_photonLooseIsEMSelector->accept(ph_itr);
        }



        if (not true_photon) {
          Error("execute()", "Failed to retrive true particle");
          m_ph_truth_phi=  -999;
          m_ph_truth_eta=   -999;
          m_ph_truth_pt=   -999;
          m_ph_truth_E=   -999;
          m_ph_truth_type=   -999;
          m_ph_truth_Rconv= -999;
          m_ph_truth_parent_pdgId= -999;
          m_ph_truth_matched= false;
        }
        else{
          m_ph_truth_matched= true;
          m_ph_truth_pt= true_photon->pt();
          m_ph_truth_phi= true_photon->phi();
          m_ph_truth_eta=  true_photon->eta() ;
          m_ph_truth_E=  true_photon->e() ;
          m_ph_truth_type= true_photon->pdgId() ;

          const xAOD::TruthParticle* true_parent= true_photon->parent();
          if(true_parent)
          m_ph_truth_parent_pdgId= true_parent->pdgId();
          else  m_ph_truth_parent_pdgId= -999;

          if (true_photon->hasDecayVtx()) {
            const xAOD::TruthVertex* true_vtx = true_photon->decayVtx();
            if (true_vtx) {

              m_ph_truth_Rconv = static_cast<float>(sqrt(true_vtx->x()*true_vtx->x() + true_vtx->y()*true_vtx->y()) );
            }

          }
          else m_ph_truth_Rconv=0;


          //std::cout<<"truth "<<m_ph_truth_type<<" "<<m_ph_truth_phi<<" "<<m_ph_truth_eta<<std::endl;
        }



        if (FLAT && (N_particle_saved>10 || m_ph_n==1)) outputTree->Fill() ;

        else if (!FLAT && (N_particle_saved>10 || m_ph_n==1)){
          m_vec_ph_CaloPointing_eta->push_back(m_ph_CaloPointing_eta);
          m_vec_ph_cl_E->push_back(m_ph_cl_E);
          m_vec_ph_cl_eta->push_back(m_ph_cl_eta);
          m_vec_ph_cl_etaCalo->push_back(m_ph_cl_etaCalo);
          m_vec_ph_cl_phi->push_back(m_ph_cl_phi);
          m_vec_ph_cl_phiCalo->push_back(m_ph_cl_phiCalo);
          m_vec_ph_author->push_back(m_ph_author);
          m_vec_ph_convFlag->push_back(m_ph_convFlag);
          m_vec_ph_convMatchDeltaPhi1->push_back(m_ph_convMatchDeltaPhi1);
          m_vec_ph_convMatchDeltaPhi2->push_back(m_ph_convMatchDeltaPhi2);
          m_vec_ph_convMatchDeltaEta1->push_back(m_ph_convMatchDeltaEta1);
          m_vec_ph_convMatchDeltaEta2->push_back(m_ph_convMatchDeltaEta2);
          // m_vec_ph_convTrk1_DeltaPhi_track_calo->push_back(m_ph_convTrk1_DeltaPhi_track_calo);
          m_vec_ph_convtrk1nPixHits->push_back(m_ph_convtrk1nPixHits);
          m_vec_ph_convtrk1nSCTHits->push_back(m_ph_convtrk1nSCTHits);
          // m_vec_ph_convTrk2_DeltaPhi_track_calo->push_back(m_ph_convTrk2_DeltaPhi_track_calo);
          m_vec_ph_convtrk2nPixHits->push_back(m_ph_convtrk2nPixHits);
          m_vec_ph_convtrk2nSCTHits->push_back(m_ph_convtrk2nSCTHits);
          m_vec_ph_etas1->push_back(m_ph_etas1);
          m_vec_ph_etas2->push_back(m_ph_etas2);
          m_vec_ph_Ethad->push_back(m_ph_Ethad);
          m_vec_ph_Ethad1->push_back(m_ph_Ethad1);
          m_vec_ph_fside->push_back(m_ph_fside);
          // m_vec_ph_HPV_zvertex->push_back(m_ph_HPV_zvertex);
          // m_vec_ph_isEM->push_back(m_ph_isEM);
          m_vec_ph_loose->push_back(m_ph_loose);
          // m_vec_ph_materialTraversed->push_back(m_ph_materialTraversed);
          m_vec_ph_pt1conv->push_back(m_ph_pt1conv);
          m_vec_ph_pt2conv->push_back(m_ph_pt2conv);
          m_vec_ph_ptconv->push_back(m_ph_ptconv);
          m_vec_ph_rawcl_calibHitsShowerDepth->push_back(m_ph_rawcl_calibHitsShowerDepth);
          m_vec_ph_rawcl_Eacc->push_back(m_ph_rawcl_Eacc);
          m_vec_ph_rawcl_Es0->push_back(m_ph_rawcl_Es0);
          m_vec_ph_rawcl_Es1->push_back(m_ph_rawcl_Es1);
          m_vec_ph_rawcl_Es2->push_back(m_ph_rawcl_Es2);
          m_vec_ph_rawcl_Es3->push_back(m_ph_rawcl_Es3);
          m_vec_ph_rawcl_Et->push_back(m_ph_rawcl_Et);
          m_vec_ph_rawcl_f0->push_back(m_ph_rawcl_f0);
          m_vec_ph_Rconv->push_back(m_ph_Rconv);
          m_vec_ph_E237->push_back(m_ph_E237);
          m_vec_ph_E233->push_back(m_ph_E233);
          m_vec_ph_E277->push_back(m_ph_E277);
          m_vec_ph_reta->push_back(m_ph_reta);
          m_vec_ph_rphi->push_back(m_ph_rphi);
          m_vec_ph_tight->push_back(m_ph_tight);
          m_vec_ph_truth_pt->push_back(m_ph_truth_pt);
          m_vec_ph_truth_E->push_back(m_ph_truth_E);
          m_vec_ph_truth_eta->push_back(m_ph_truth_eta);
          m_vec_ph_truth_matched->push_back(m_ph_truth_matched);
          m_vec_ph_truth_phi->push_back(m_ph_truth_phi);
          m_vec_ph_truth_Rconv->push_back(m_ph_truth_Rconv);
          m_vec_ph_truth_type->push_back(m_ph_truth_type);
          m_vec_ph_truth_parent_pdgId->push_back(m_ph_truth_parent_pdgId);
          m_vec_ph_weta2->push_back(m_ph_weta2);
          m_vec_ph_ws3->push_back(m_ph_ws3);
          m_vec_ph_wstot->push_back(m_ph_wstot);
          m_vec_ph_DeltaE->push_back(m_ph_DeltaE);
          m_vec_ph_Eratio->push_back(m_ph_Eratio);
          m_vec_ph_Rhad1->push_back(m_ph_Rhad1);
          m_vec_ph_Rhad->push_back(m_ph_Rhad);
          // m_vec_ph_zconv->push_back(m_ph_zconv);
        }


        else{


          tmp_vec_ph_CaloPointing_eta->push_back(m_ph_CaloPointing_eta);
          tmp_vec_ph_cl_E->push_back(m_ph_cl_E);
          tmp_vec_ph_cl_eta->push_back(m_ph_cl_eta);
          tmp_vec_ph_cl_etaCalo->push_back(m_ph_cl_etaCalo);
          tmp_vec_ph_cl_phi->push_back(m_ph_cl_phi);
          tmp_vec_ph_cl_phiCalo->push_back(m_ph_cl_phiCalo);
          tmp_vec_ph_author->push_back(m_ph_author);
          tmp_vec_ph_convFlag->push_back(m_ph_convFlag);
          tmp_vec_ph_convMatchDeltaPhi1->push_back(m_ph_convMatchDeltaPhi1);
          tmp_vec_ph_convMatchDeltaPhi2->push_back(m_ph_convMatchDeltaPhi2);
          tmp_vec_ph_convMatchDeltaEta1->push_back(m_ph_convMatchDeltaEta1);
          tmp_vec_ph_convMatchDeltaEta2->push_back(m_ph_convMatchDeltaEta2);
          // tmp_vec_ph_convTrk1_DeltaPhi_track_calo->push_back(m_ph_convTrk1_DeltaPhi_track_calo);
          tmp_vec_ph_convtrk1nPixHits->push_back(m_ph_convtrk1nPixHits);
          tmp_vec_ph_convtrk1nSCTHits->push_back(m_ph_convtrk1nSCTHits);
          // tmp_vec_ph_convTrk2_DeltaPhi_track_calo->push_back(m_ph_convTrk2_DeltaPhi_track_calo);
          tmp_vec_ph_convtrk2nPixHits->push_back(m_ph_convtrk2nPixHits);
          tmp_vec_ph_convtrk2nSCTHits->push_back(m_ph_convtrk2nSCTHits);
          tmp_vec_ph_etas1->push_back(m_ph_etas1);
          tmp_vec_ph_etas2->push_back(m_ph_etas2);
          tmp_vec_ph_Ethad->push_back(m_ph_Ethad);
          tmp_vec_ph_Ethad1->push_back(m_ph_Ethad1);
          tmp_vec_ph_fside->push_back(m_ph_fside);
          // tmp_vec_ph_HPV_zvertex->push_back(m_ph_HPV_zvertex);
          // tmp_vec_ph_isEM->push_back(m_ph_isEM);
          tmp_vec_ph_loose->push_back(m_ph_loose);
          // tmp_vec_ph_materialTraversed->push_back(m_ph_materialTraversed);
          tmp_vec_ph_pt1conv->push_back(m_ph_pt1conv);
          tmp_vec_ph_pt2conv->push_back(m_ph_pt2conv);
          tmp_vec_ph_ptconv->push_back(m_ph_ptconv);
          tmp_vec_ph_rawcl_calibHitsShowerDepth->push_back(m_ph_rawcl_calibHitsShowerDepth);
          tmp_vec_ph_rawcl_Eacc->push_back(m_ph_rawcl_Eacc);
          tmp_vec_ph_rawcl_Es0->push_back(m_ph_rawcl_Es0);
          tmp_vec_ph_rawcl_Es1->push_back(m_ph_rawcl_Es1);
          tmp_vec_ph_rawcl_Es2->push_back(m_ph_rawcl_Es2);
          tmp_vec_ph_rawcl_Es3->push_back(m_ph_rawcl_Es3);
          tmp_vec_ph_rawcl_Et->push_back(m_ph_rawcl_Et);
          tmp_vec_ph_rawcl_f0->push_back(m_ph_rawcl_f0);
          tmp_vec_ph_Rconv->push_back(m_ph_Rconv);
          tmp_vec_ph_E237->push_back(m_ph_E237);
          tmp_vec_ph_E233->push_back(m_ph_E233);
          tmp_vec_ph_E277->push_back(m_ph_E277);
          tmp_vec_ph_reta->push_back(m_ph_reta);
          tmp_vec_ph_rphi->push_back(m_ph_rphi);
          tmp_vec_ph_tight->push_back(m_ph_tight);
          tmp_vec_ph_truth_pt->push_back(m_ph_truth_pt);
          tmp_vec_ph_truth_E->push_back(m_ph_truth_E);
          tmp_vec_ph_truth_eta->push_back(m_ph_truth_eta);
          tmp_vec_ph_truth_matched->push_back(m_ph_truth_matched);
          tmp_vec_ph_truth_phi->push_back(m_ph_truth_phi);
          tmp_vec_ph_truth_Rconv->push_back(m_ph_truth_Rconv);
          tmp_vec_ph_truth_type->push_back(m_ph_truth_type);
          tmp_vec_ph_truth_parent_pdgId->push_back(m_ph_truth_parent_pdgId);
          tmp_vec_ph_weta2->push_back(m_ph_weta2);
          tmp_vec_ph_ws3->push_back(m_ph_ws3);
          tmp_vec_ph_wstot->push_back(m_ph_wstot);
          tmp_vec_ph_DeltaE->push_back(m_ph_DeltaE);
          tmp_vec_ph_Eratio->push_back(m_ph_Eratio);
          tmp_vec_ph_Rhad1->push_back(m_ph_Rhad1);
          tmp_vec_ph_Rhad->push_back(m_ph_Rhad);
          // tmp_vec_ph_zconv->push_back(m_ph_zconv);

        }



      }


      if(N_particle_saved<10 && m_ph_n>1) {
        double pt=0;
        std::vector<int>index_pt(N_particle_saved,-999);
        std::vector<int>::iterator it;

        for (int k=0; k<N_particle_saved; k++){
          for(unsigned int i=0; i<tmp_vec_ph_cl_E->size(); i++){
            if( (tmp_vec_ph_cl_E->at(i)/cosh(tmp_vec_ph_cl_eta->at(i)))>pt ){
              it = find (index_pt.begin(), index_pt.end(), i);
              if (it == index_pt.end()){
                pt=(tmp_vec_ph_cl_E->at(i)/cosh(tmp_vec_ph_cl_eta->at(i)));
                index_pt[k]=i;
              }
            }
          }
          pt=0;
        }


        if (FLAT) {
          for(unsigned int i=0; i<index_pt.size(); i++){
            if (index_pt[i]==-999) continue;
            m_ph_CaloPointing_eta=tmp_vec_ph_CaloPointing_eta->at(index_pt[i]);
            m_ph_cl_E=tmp_vec_ph_cl_E->at(index_pt[i]);
            m_ph_cl_eta=tmp_vec_ph_cl_eta->at(index_pt[i]);
            m_ph_cl_etaCalo=tmp_vec_ph_cl_etaCalo->at(index_pt[i]);
            m_ph_cl_phi=tmp_vec_ph_cl_phi->at(index_pt[i]);
            m_ph_cl_phiCalo=tmp_vec_ph_cl_phiCalo->at(index_pt[i]);
            m_ph_author=tmp_vec_ph_author->at(index_pt[i]);
            m_ph_convFlag=tmp_vec_ph_convFlag->at(index_pt[i]);
            m_ph_convMatchDeltaPhi1=tmp_vec_ph_convMatchDeltaPhi1->at(index_pt[i]);
            m_ph_convMatchDeltaPhi2=tmp_vec_ph_convMatchDeltaPhi2->at(index_pt[i]);
            m_ph_convMatchDeltaEta1=tmp_vec_ph_convMatchDeltaEta1->at(index_pt[i]);
            m_ph_convMatchDeltaEta2=tmp_vec_ph_convMatchDeltaEta2->at(index_pt[i]);
            // m_ph_convTrk1_DeltaPhi_track_calo=tmp_vec_ph_convTrk1_DeltaPhi_track_calo->at(index_pt[i]);
            m_ph_convtrk1nPixHits=tmp_vec_ph_convtrk1nPixHits->at(index_pt[i]);
            m_ph_convtrk1nSCTHits=tmp_vec_ph_convtrk1nSCTHits->at(index_pt[i]);
            // m_ph_convTrk2_DeltaPhi_track_calo=tmp_vec_ph_convTrk2_DeltaPhi_track_calo->at(index_pt[i]);
            m_ph_convtrk2nPixHits=tmp_vec_ph_convtrk2nPixHits->at(index_pt[i]);
            m_ph_convtrk2nSCTHits=tmp_vec_ph_convtrk2nSCTHits->at(index_pt[i]);
            m_ph_etas1=tmp_vec_ph_etas1->at(index_pt[i]);
            m_ph_etas2=tmp_vec_ph_etas2->at(index_pt[i]);
            m_ph_Ethad=tmp_vec_ph_Ethad->at(index_pt[i]);
            m_ph_Ethad1=tmp_vec_ph_Ethad1->at(index_pt[i]);
            m_ph_fside=tmp_vec_ph_fside->at(index_pt[i]);
            // m_ph_HPV_zvertex=tmp_vec_ph_HPV_zvertex->at(index_pt[i]);
            // m_ph_isEM=tmp_vec_ph_isEM->at(index_pt[i]);
            m_ph_loose=tmp_vec_ph_loose->at(index_pt[i]);
            // m_ph_materialTraversed=tmp_vec_ph_materialTraversed->at(index_pt[i]);
            m_ph_pt1conv=tmp_vec_ph_pt1conv->at(index_pt[i]);
            m_ph_pt2conv=tmp_vec_ph_pt2conv->at(index_pt[i]);
            m_ph_ptconv=tmp_vec_ph_ptconv->at(index_pt[i]);
            m_ph_rawcl_calibHitsShowerDepth=tmp_vec_ph_rawcl_calibHitsShowerDepth->at(index_pt[i]);
            m_ph_rawcl_Eacc=tmp_vec_ph_rawcl_Eacc->at(index_pt[i]);
            m_ph_rawcl_Es0=tmp_vec_ph_rawcl_Es0->at(index_pt[i]);
            m_ph_rawcl_Es1=tmp_vec_ph_rawcl_Es1->at(index_pt[i]);
            m_ph_rawcl_Es2=tmp_vec_ph_rawcl_Es2->at(index_pt[i]);
            m_ph_rawcl_Es3=tmp_vec_ph_rawcl_Es3->at(index_pt[i]);
            m_ph_rawcl_Et=tmp_vec_ph_rawcl_Et->at(index_pt[i]);
            m_ph_rawcl_f0=tmp_vec_ph_rawcl_f0->at(index_pt[i]);
            m_ph_Rconv=tmp_vec_ph_Rconv->at(index_pt[i]);
            m_ph_E237=tmp_vec_ph_E237->at(index_pt[i]);
            m_ph_E233=tmp_vec_ph_E233->at(index_pt[i]);
            m_ph_E277=tmp_vec_ph_E277->at(index_pt[i]);
            m_ph_reta=tmp_vec_ph_reta->at(index_pt[i]);
            m_ph_rphi=tmp_vec_ph_rphi->at(index_pt[i]);
            m_ph_tight=tmp_vec_ph_tight->at(index_pt[i]);
            m_ph_truth_pt=tmp_vec_ph_truth_pt->at(index_pt[i]);
            m_ph_truth_E=tmp_vec_ph_truth_E->at(index_pt[i]);
            m_ph_truth_eta=tmp_vec_ph_truth_eta->at(index_pt[i]);
            m_ph_truth_matched=tmp_vec_ph_truth_matched->at(index_pt[i]);
            m_ph_truth_phi=tmp_vec_ph_truth_phi->at(index_pt[i]);
            m_ph_truth_Rconv=tmp_vec_ph_truth_Rconv->at(index_pt[i]);
            m_ph_truth_type=tmp_vec_ph_truth_type->at(index_pt[i]);
            m_ph_truth_parent_pdgId=tmp_vec_ph_truth_parent_pdgId->at(index_pt[i]);
            m_ph_weta2=tmp_vec_ph_weta2->at(index_pt[i]);
            m_ph_ws3=tmp_vec_ph_ws3->at(index_pt[i]);
            m_ph_wstot=tmp_vec_ph_wstot->at(index_pt[i]);
            m_ph_DeltaE=tmp_vec_ph_DeltaE->at(index_pt[i]);
            m_ph_Eratio=tmp_vec_ph_Eratio->at(index_pt[i]);
            m_ph_Rhad1=tmp_vec_ph_Rhad1->at(index_pt[i]);
            m_ph_Rhad=tmp_vec_ph_Rhad->at(index_pt[i]);
            outputTree->Fill() ;

          }
        }

        else{



          for(unsigned int idx=0; idx<index_pt.size(); idx++){

            if (index_pt.at(idx)==-999) continue;

            m_vec_ph_CaloPointing_eta->push_back(tmp_vec_ph_CaloPointing_eta->at(index_pt.at(idx)));
            m_vec_ph_cl_E->push_back(tmp_vec_ph_cl_E->at(index_pt.at(idx)));
            m_vec_ph_cl_eta->push_back(tmp_vec_ph_cl_eta->at(index_pt.at(idx)));
            m_vec_ph_cl_etaCalo->push_back(tmp_vec_ph_cl_etaCalo->at(index_pt.at(idx)));
            m_vec_ph_cl_phi->push_back(tmp_vec_ph_cl_phi->at(index_pt.at(idx)));
            m_vec_ph_cl_phiCalo->push_back(tmp_vec_ph_cl_phiCalo->at(index_pt.at(idx)));
            m_vec_ph_author->push_back(tmp_vec_ph_author->at(index_pt.at(idx)));
            m_vec_ph_convFlag->push_back(tmp_vec_ph_convFlag->at(index_pt.at(idx)));
            m_vec_ph_convMatchDeltaPhi1->push_back(tmp_vec_ph_convMatchDeltaPhi1->at(index_pt.at(idx)));
            m_vec_ph_convMatchDeltaPhi2->push_back(tmp_vec_ph_convMatchDeltaPhi2->at(index_pt.at(idx)));
            m_vec_ph_convMatchDeltaEta1->push_back(tmp_vec_ph_convMatchDeltaEta1->at(index_pt.at(idx)));
            m_vec_ph_convMatchDeltaEta2->push_back(tmp_vec_ph_convMatchDeltaEta2->at(index_pt.at(idx)));
            // m_vec_ph_convTrk1_DeltaPhi_track_calo->push_back(tmp_vec_ph_convTrk1_DeltaPhi_track_calo->at(index_pt.at(idx)));
            m_vec_ph_convtrk1nPixHits->push_back(tmp_vec_ph_convtrk1nPixHits->at(index_pt.at(idx)));
            m_vec_ph_convtrk1nSCTHits->push_back(tmp_vec_ph_convtrk1nSCTHits->at(index_pt.at(idx)));
            //m_vec_ph_convTrk2_DeltaPhi_track_calo->push_back(tmp_vec_ph_convTrk2_DeltaPhi_track_calo->at(index_pt.at(idx)));
            m_vec_ph_convtrk2nPixHits->push_back(tmp_vec_ph_convtrk2nPixHits->at(index_pt.at(idx)));
            m_vec_ph_convtrk2nSCTHits->push_back(tmp_vec_ph_convtrk2nSCTHits->at(index_pt.at(idx)));
            m_vec_ph_etas1->push_back(tmp_vec_ph_etas1->at(index_pt.at(idx)));
            m_vec_ph_etas2->push_back(tmp_vec_ph_etas2->at(index_pt.at(idx)));
            m_vec_ph_Ethad->push_back(tmp_vec_ph_Ethad->at(index_pt.at(idx)));
            m_vec_ph_Ethad1->push_back(tmp_vec_ph_Ethad1->at(index_pt.at(idx)));
            m_vec_ph_fside->push_back(tmp_vec_ph_fside->at(index_pt.at(idx)));
            //m_vec_ph_HPV_zvertex->push_back(tmp_vec_ph_HPV_zvertex->at(index_pt.at(idx)));
            //m_vec_ph_isEM->push_back(tmp_vec_ph_isEM->at(index_pt.at(idx)));
            m_vec_ph_loose->push_back(tmp_vec_ph_loose->at(index_pt.at(idx)));
            //m_vec_ph_materialTraversed->push_back(tmp_vec_ph_materialTraversed->at(index_pt.at(idx)));
            m_vec_ph_pt1conv->push_back(tmp_vec_ph_pt1conv->at(index_pt.at(idx)));
            m_vec_ph_pt2conv->push_back(tmp_vec_ph_pt2conv->at(index_pt.at(idx)));
            m_vec_ph_ptconv->push_back(tmp_vec_ph_ptconv->at(index_pt.at(idx)));
            m_vec_ph_rawcl_calibHitsShowerDepth->push_back(tmp_vec_ph_rawcl_calibHitsShowerDepth->at(index_pt.at(idx)));
            m_vec_ph_rawcl_Eacc->push_back(tmp_vec_ph_rawcl_Eacc->at(index_pt.at(idx)));
            m_vec_ph_rawcl_Es0->push_back(tmp_vec_ph_rawcl_Es0->at(index_pt.at(idx)));
            m_vec_ph_rawcl_Es1->push_back(tmp_vec_ph_rawcl_Es1->at(index_pt.at(idx)));
            m_vec_ph_rawcl_Es2->push_back(tmp_vec_ph_rawcl_Es2->at(index_pt.at(idx)));
            m_vec_ph_rawcl_Es3->push_back(tmp_vec_ph_rawcl_Es3->at(index_pt.at(idx)));
            m_vec_ph_rawcl_Et->push_back(tmp_vec_ph_rawcl_Et->at(index_pt.at(idx)));
            m_vec_ph_rawcl_f0->push_back(tmp_vec_ph_rawcl_f0->at(index_pt.at(idx)));
            m_vec_ph_Rconv->push_back(tmp_vec_ph_Rconv->at(index_pt.at(idx)));
            m_vec_ph_E237->push_back(tmp_vec_ph_E237->at(index_pt.at(idx)));
            m_vec_ph_E233->push_back(tmp_vec_ph_E233->at(index_pt.at(idx)));
            m_vec_ph_E277->push_back(tmp_vec_ph_E277->at(index_pt.at(idx)));
            m_vec_ph_reta->push_back(tmp_vec_ph_reta->at(index_pt.at(idx)));
            m_vec_ph_rphi->push_back(tmp_vec_ph_rphi->at(index_pt.at(idx)));
            m_vec_ph_tight->push_back(tmp_vec_ph_tight->at(index_pt.at(idx)));
            m_vec_ph_truth_E->push_back(tmp_vec_ph_truth_E->at(index_pt.at(idx)));
            m_vec_ph_truth_pt->push_back(tmp_vec_ph_truth_pt->at(index_pt.at(idx)));
            m_vec_ph_truth_eta->push_back(tmp_vec_ph_truth_eta->at(index_pt.at(idx)));
            m_vec_ph_truth_matched->push_back(tmp_vec_ph_truth_matched->at(index_pt.at(idx)));
            m_vec_ph_truth_phi->push_back(tmp_vec_ph_truth_phi->at(index_pt.at(idx)));
            m_vec_ph_truth_Rconv->push_back(tmp_vec_ph_truth_Rconv->at(index_pt.at(idx)));
            m_vec_ph_truth_type->push_back(tmp_vec_ph_truth_type->at(index_pt.at(idx)));
            m_vec_ph_truth_parent_pdgId->push_back(tmp_vec_ph_truth_parent_pdgId->at(index_pt.at(idx)));
            m_vec_ph_weta2->push_back(tmp_vec_ph_weta2->at(index_pt.at(idx)));
            m_vec_ph_ws3->push_back(tmp_vec_ph_ws3->at(index_pt.at(idx)));
            m_vec_ph_wstot->push_back(tmp_vec_ph_wstot->at(index_pt.at(idx)));
            //m_vec_ph_zconv->push_back(tmp_vec_ph_zconv->at(index_pt.at(idx)));
            m_vec_ph_DeltaE ->push_back(tmp_vec_ph_DeltaE ->at(index_pt.at(idx)));
            m_vec_ph_Eratio ->push_back(tmp_vec_ph_Eratio ->at(index_pt.at(idx)));
            m_vec_ph_Rhad1->push_back(tmp_vec_ph_Rhad1->at(index_pt.at(idx)));
            m_vec_ph_Rhad ->push_back(tmp_vec_ph_Rhad ->at(index_pt.at(idx)));



          }


        }
      }
    }
  }









  if(particleType==1){


    if(!FLAT){
      m_vec_el_cl_E->clear();
      m_vec_el_cl_etaCalo->clear();
      m_vec_el_cl_phi->clear();
      m_vec_el_cl_phiCalo->clear();
      m_vec_el_author->clear();
      m_vec_el_charge->clear();
      m_vec_el_cl_eta->clear();
      m_vec_el_deltaphi2->clear();
      m_vec_el_deltaPhiFirstLast->clear();
      m_vec_el_deltaPhiFromLast->clear();
      m_vec_el_fside->clear();
      m_vec_el_isEM->clear();
      m_vec_el_loosePP->clear();
      m_vec_el_mediumPP->clear();
      m_vec_el_p0->clear();
      m_vec_el_pLast->clear();
      m_vec_el_refittedTrack_author->clear();
      m_vec_el_refittedTrack_LMqoverp->clear();
      m_vec_el_refittedTrack_qoverp->clear();
      m_vec_el_E237->clear();
      m_vec_el_E233->clear();
      m_vec_el_E277->clear();
      m_vec_el_reta->clear();
      m_vec_el_rphi->clear();
      m_vec_el_Ethad->clear();
      m_vec_el_Ethad1->clear();
      m_vec_el_tightPP->clear();
      m_vec_el_rawcl_calibHitsShowerDepth->clear();
      m_vec_el_rawcl_Eacc->clear();
      m_vec_el_rawcl_Es0->clear();
      m_vec_el_rawcl_Es1->clear();
      m_vec_el_rawcl_Es2->clear();
      m_vec_el_rawcl_Es3->clear();
      m_vec_el_rawcl_Et->clear();
      m_vec_el_rawcl_f0->clear();
      m_vec_el_tracketa->clear();
      m_vec_el_trackpt->clear();
      m_vec_el_trackz0->clear();
      m_vec_el_truth_E->clear();
      m_vec_el_truth_pt->clear();
      m_vec_el_truth_eta->clear();
      m_vec_el_truth_phi->clear();
      m_vec_el_truth_type->clear();
      m_vec_el_truth_parent_pdgId->clear();
      m_vec_el_truth_matched->clear();
      m_vec_el_weta2->clear();
      m_vec_el_ws3->clear();
      m_vec_el_wstot->clear();
      m_vec_el_DeltaE->clear();
      m_vec_el_Eratio->clear();
      m_vec_el_Rhad->clear();
      m_vec_el_Rhad1->clear();

    }
    if (N_particle_saved<10){
      tmp_vec_el_cl_E->clear();
      tmp_vec_el_cl_etaCalo->clear();
      tmp_vec_el_cl_phi->clear();
      tmp_vec_el_cl_phiCalo->clear();
      tmp_vec_el_author->clear();
      tmp_vec_el_charge->clear();
      tmp_vec_el_cl_eta->clear();
      tmp_vec_el_deltaphi2->clear();
      tmp_vec_el_deltaPhiFirstLast->clear();
      tmp_vec_el_deltaPhiFromLast->clear();
      tmp_vec_el_fside->clear();
      tmp_vec_el_isEM->clear();
      tmp_vec_el_loosePP->clear();
      tmp_vec_el_mediumPP->clear();
      tmp_vec_el_p0->clear();
      tmp_vec_el_pLast->clear();
      tmp_vec_el_refittedTrack_author->clear();
      tmp_vec_el_refittedTrack_LMqoverp->clear();
      tmp_vec_el_refittedTrack_qoverp->clear();
      tmp_vec_el_E237->clear();
      tmp_vec_el_E233->clear();
      tmp_vec_el_E277->clear();
      tmp_vec_el_reta->clear();
      tmp_vec_el_rphi->clear();
      tmp_vec_el_Ethad->clear();
      tmp_vec_el_Ethad1->clear();
      tmp_vec_el_tightPP->clear();
      tmp_vec_el_rawcl_calibHitsShowerDepth->clear();
      tmp_vec_el_rawcl_Eacc->clear();
      tmp_vec_el_rawcl_Es0->clear();
      tmp_vec_el_rawcl_Es1->clear();
      tmp_vec_el_rawcl_Es2->clear();
      tmp_vec_el_rawcl_Es3->clear();
      tmp_vec_el_rawcl_Et->clear();
      tmp_vec_el_rawcl_f0->clear();
      tmp_vec_el_tracketa->clear();
      tmp_vec_el_trackpt->clear();
      tmp_vec_el_trackz0->clear();
      tmp_vec_el_truth_E->clear();
      tmp_vec_el_truth_pt->clear();
      tmp_vec_el_truth_eta->clear();
      tmp_vec_el_truth_phi->clear();
      tmp_vec_el_truth_type->clear();
      tmp_vec_el_truth_parent_pdgId->clear();
      tmp_vec_el_truth_matched->clear();
      tmp_vec_el_weta2->clear();
      tmp_vec_el_ws3->clear();
      tmp_vec_el_wstot->clear();
      tmp_vec_el_DeltaE->clear();
      tmp_vec_el_Eratio->clear();
      tmp_vec_el_Rhad->clear();
      tmp_vec_el_Rhad1->clear();

    }

    const xAOD::ElectronContainer* electron = 0;
    if( doOnline ){
      if ( !m_event->retrieve( electron, "HLT_xAOD__ElectronContainer_egamma_Electrons" ).isSuccess() ){
        Error("execute()", "Failed to retrieve HLT_xAOD__ElectronContainer_egamma_Electrons. Exiting." );
        return EL::StatusCode::FAILURE;
      }
    } else {
      if ( !m_event->retrieve( electron, "Electrons" ).isSuccess() ){ // retrieve arguments: container type, container key
        Error("execute()", "Failed to retrieve Electron container. Exiting." );
        return EL::StatusCode::FAILURE;
      }
    }
    xAOD::ElectronContainer::const_iterator el_itr = electron->begin();
    xAOD::ElectronContainer::const_iterator el_end = electron->end();



    m_el_n=electron->size();

    const xAOD::TruthParticleContainer* truth = 0;
    if ( !m_event->retrieve( truth, "egammaTruthParticles" ).isSuccess() ){ // retrieve arguments: container type, container key
      Error("execute()", "Failed to retrieve Truth Electron container. Exiting." );
      return EL::StatusCode::FAILURE;
    }

    xAOD::TruthParticleContainer::const_iterator el_th_itr = truth->begin();
    xAOD::TruthParticleContainer::const_iterator el_th_end = truth->end();
    m_el_truth_n=0;
    for( ; el_th_itr != el_th_end; ++el_th_itr ) {
      if((*el_th_itr)->absPdgId()==11) m_el_truth_n++;
    }

    if(electron->size()>0){
    std::vector<const xAOD::CaloCluster*>* caloclusters =new std::vector<const xAOD::CaloCluster*>;

      for( ; el_itr != el_end; ++el_itr ) {


        /*(*el_itr)->isAvailable<char>("Loose");
        if(((*el_itr)->auxdata<char>("Loose"))==1) m_el_loosePP=true;
        else m_el_loosePP=false;
        (*el_itr)->passSelection(m_el_loosePP, "Loose");
        (*el_itr)->isAvailable<char>("Tight");
        if(((*el_itr)->auxdata<char>("Tight"))==1) m_el_tightPP=true;
        else m_el_tightPP=false;
        (*el_itr)->passSelection(m_el_tightPP, "Tight");*/



       if(doOnline){
       m_el_FTFseed=((*el_itr)->trackParticle()->patternRecoInfo()[xAOD::FastTrackFinderSeed]);
       if(!m_el_FTFseed) continue;
          //if(!(*el_itr)->trackParticle()->patternRecoInfo()[xAOD::FastTrackFinderSeed])
         //continue;

          bool visitedCluster = false;
          for( auto calo : *caloclusters ){
            if( (*el_itr)->caloCluster() == calo ){
              visitedCluster = true;
              break;
            }
          }
          if(visitedCluster) continue;
          else caloclusters->push_back((*el_itr)->caloCluster());
        }
        m_el_cl_E=(*el_itr)->caloCluster()->e();
        m_el_cl_eta=(*el_itr)->caloCluster()->eta();
        m_el_cl_phi=(*el_itr)->caloCluster()->phi();
        m_el_cl_eta=(*el_itr)->caloCluster()->eta();
        m_el_E=(*el_itr)->e();
        m_el_eta=(*el_itr)->eta();
        m_el_phi=(*el_itr)->phi();


     /*    std::cout<<"eta_size: "<<(*el_itr)->caloCluster()->getClusterEtaSize()<<"phi_size: "<<(*el_itr)->caloCluster()->getClusterPhiSize()<<std::endl;
        for(auto cell: (*el_itr)->caloCluster()->getCellLinks()){
         std::cout<<"cell ID "<<cell->ID()<<"cell e"<<cell->e()<<std::endl;}*/
     


        double etaCalo, etaS1Calo,etaS2Calo,phiCalo,phiS1Calo,phiS2Calo;
        (*el_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::ETACALOFRAME,etaCalo);
        m_el_cl_etaCalo=etaCalo;
        (*el_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::ETA1CALOFRAME,etaS1Calo);
        m_el_cl_etaS1Calo=etaS1Calo;
        (*el_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::ETA2CALOFRAME,etaS2Calo);
        m_el_cl_etaS2Calo=etaS2Calo;
        (*el_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::PHICALOFRAME,phiCalo);
        m_el_cl_phiCalo=phiCalo;
        (*el_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::PHI1CALOFRAME,phiS1Calo);
        m_el_cl_phiS1Calo=phiS1Calo;
        (*el_itr)->caloCluster()->retrieveMoment(xAOD::CaloCluster::PHI1CALOFRAME,phiS2Calo);
        m_el_cl_phiS2Calo=phiS2Calo;

        //m_el_cl_etaCalo=(*el_itr)->caloCluster()->auxdata<float>("etaCalo");
        m_el_cl_phi=(*el_itr)->caloCluster()->phi();
m_el_cl_pt=(*el_itr)->caloCluster()->pt();
m_el_cl_m=(*el_itr)->caloCluster()->m();
m_el_m=(*el_itr)->m();
        //m_el_cl_phiCalo=(*el_itr)->caloCluster()->auxdata<float>("phiCalo");
        m_el_charge=(*el_itr)->charge();
        m_el_author=(*el_itr)->auxdata<unsigned short int>("author");
        //m_el_cl_etaCalo=(*el_itr)->caloCluster()->etaCalo();
        //m_el_cl_phiCalo=(*el_itr)->caloCluster()->phiCalo();
        m_el_tracketa =(*el_itr)->trackParticle()->eta();
        m_el_trackpt =(*el_itr)->trackParticle()->pt();
        m_el_trackz0 =(*el_itr)->trackParticle()->z0();
m_el_trackphi =(*el_itr)->trackParticle()->phi();
        m_el_trackqoverp=(*el_itr)->trackParticle()->qOverP();
        m_el_trackcov_qoverp=(*el_itr)->trackParticle()->definingParametersCovMatrix().coeff(4, 4);
        m_el_refittedTrack_LMqoverp=(*el_itr)->trackParticle()->auxdataConst<Float_t>("QoverPLM");


        m_el_etas2=((*el_itr)->caloCluster()->etaBE(2));
        m_el_etas1=((*el_itr)->caloCluster()->etaBE(1));
        m_el_cl_E_TileGap1=((*el_itr))->caloCluster()->eSample(CaloSampling::TileGap1);
        m_el_cl_E_TileGap2=((*el_itr))->caloCluster()->eSample(CaloSampling::TileGap2);
        m_el_cl_E_TileGap3=((*el_itr))->caloCluster()->eSample(CaloSampling::TileGap3);

        m_el_rawcl_Es0=(*el_itr)->caloCluster()->energyBE(0);
        m_el_rawcl_Es1=(*el_itr)->caloCluster()->energyBE(1);
        m_el_rawcl_Es2=(*el_itr)->caloCluster()->energyBE(2);
        m_el_rawcl_Es3=(*el_itr)->caloCluster()->energyBE(3);
        m_el_rawcl_Eacc=m_el_rawcl_Es1+m_el_rawcl_Es2+m_el_rawcl_Es3;
        m_el_rawcl_f0=m_el_rawcl_Es0/m_el_rawcl_Eacc;
        m_el_rawcl_Et=m_el_rawcl_Eacc/cosh(m_el_etas2);

        (*el_itr)->showerShapeValue(m_el_weta2, xAOD::EgammaParameters::ShowerShapeType::weta2);
        (*el_itr)->showerShapeValue(m_el_wstot, xAOD::EgammaParameters::ShowerShapeType::wtots1);
        (*el_itr)->showerShapeValue(m_el_ws3, xAOD::EgammaParameters::ShowerShapeType::weta1);
        (*el_itr)->showerShapeValue(m_el_Ethad, xAOD::EgammaParameters::ShowerShapeType::ethad);
        (*el_itr)->showerShapeValue(m_el_Ethad1,xAOD::EgammaParameters::ShowerShapeType::ethad1);
        (*el_itr)->showerShapeValue(m_el_DeltaE, xAOD::EgammaParameters::ShowerShapeType::DeltaE);
        (*el_itr)->showerShapeValue(m_el_Eratio, xAOD::EgammaParameters::ShowerShapeType::Eratio);
        (*el_itr)->showerShapeValue(m_el_Rhad, xAOD::EgammaParameters::ShowerShapeType::Rhad);
        (*el_itr)->showerShapeValue(m_el_Rhad1, xAOD::EgammaParameters::ShowerShapeType::Rhad1);
        (*el_itr)->showerShapeValue(m_el_fside, xAOD::EgammaParameters::ShowerShapeType::fracs1);
        (*el_itr)->showerShapeValue(m_el_E237, xAOD::EgammaParameters::ShowerShapeType::e237);
        (*el_itr)->showerShapeValue(m_el_E277, xAOD::EgammaParameters::ShowerShapeType::e277);
        (*el_itr)->showerShapeValue(m_el_E233, xAOD::EgammaParameters::ShowerShapeType::e233);
        //(*el_itr)->showerShapeValue( m_el_rawcl_calibHitsShowerDepth, xAOD::EgammaParameters::ShowerShapeType::depth);
        m_el_reta= m_el_E237/m_el_E277;
        m_el_rphi= m_el_E233/m_el_E237;

        if(doOnline){
m_el_topoetcone40 = -999.;
m_el_topoetcone30 = -999.;
m_el_topoetcone20 = -999.;
m_el_etcone40 = -999.;
m_el_etcone30 = -999.;
m_el_etcone20 = -999.;
}
else{
        m_el_topoetcone40 = ((*el_itr)->isolationValue(xAOD::Iso::topoetcone40));
        m_el_topoetcone40ptCorrection = (*el_itr)->auxdata<float>("topoetcone40ptCorrection");
        m_el_topoetcone30 = ((*el_itr)->isolationValue(xAOD::Iso::topoetcone30));
        m_el_topoetcone30ptCorrection =(*el_itr)->auxdata<float>("topoetcone30ptCorrection");
        m_el_topoetcone20 = ((*el_itr)->isolationValue(xAOD::Iso::topoetcone20));
        m_el_topoetcone20ptCorrection = (*el_itr)->auxdata<float>("topoetcone20ptCorrection");
        
        
         float etas2 = (*el_itr)->caloCluster()->etaBE(2);
    if(etas2>-1.5 && etas2<1.5){
        m_el_topoetcone40pileupCorrection = ED_central_xaod * 3.1415 * (0.16 - 0.875/128);
        m_el_topoetcone30pileupCorrection = ED_central_xaod * 3.1415 * (0.09 - 0.875/128);
        m_el_topoetcone20pileupCorrection = ED_central_xaod * 3.1415 * (0.04 - 0.875/128);
    }else{
        m_el_topoetcone40pileupCorrection = ED_forward_xaod * 3.1415 * (0.16 - 0.875/128);
        m_el_topoetcone30pileupCorrection = ED_forward_xaod * 3.1415 * (0.09 - 0.875/128);
        m_el_topoetcone20pileupCorrection = ED_forward_xaod * 3.1415 * (0.04 - 0.875/128);
    }



      (*el_itr)->isolationCaloCorrection(m_el_topoetcone40coreconeCorrection,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::coreCone, xAOD::Iso::coreEnergy);
      (*el_itr)->isolationCaloCorrection(m_el_topoetcone30coreconeCorrection,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::coreCone, xAOD::Iso::coreEnergy);
      (*el_itr)->isolationCaloCorrection(m_el_topoetcone20coreconeCorrection,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::coreCone, xAOD::Iso::coreEnergy);
      (*el_itr)->isolationCaloCorrection(m_el_topoetcone40core57Correction,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::core57cells, xAOD::Iso::coreEnergy);
      (*el_itr)->isolationCaloCorrection(m_el_topoetcone30core57Correction,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::core57cells, xAOD::Iso::coreEnergy);
      (*el_itr)->isolationCaloCorrection(m_el_topoetcone20core57Correction,xAOD::Iso::IsolationFlavour::topoetcone, xAOD::Iso::core57cells, xAOD::Iso::coreEnergy);
      m_el_neflowisol40=((*el_itr)->isolationValue(xAOD::Iso::neflowisol40));
      m_el_neflowisol30=((*el_itr)->isolationValue(xAOD::Iso::neflowisol30));
      m_el_neflowisol20=((*el_itr)->isolationValue(xAOD::Iso::neflowisol20));

      m_el_topoetcone40coreconeCorrected = m_el_topoetcone40+m_el_topoetcone40ptCorrection+m_el_topoetcone40pileupCorrection+m_el_topoetcone40core57Correction-m_el_topoetcone40coreconeCorrection;
      m_el_topoetcone30coreconeCorrected = m_el_topoetcone30+m_el_topoetcone30ptCorrection+m_el_topoetcone30pileupCorrection+m_el_topoetcone30core57Correction-m_el_topoetcone30coreconeCorrection;
      m_el_topoetcone20coreconeCorrected = m_el_topoetcone20+m_el_topoetcone20ptCorrection+m_el_topoetcone20pileupCorrection+m_el_topoetcone20core57Correction-m_el_topoetcone20coreconeCorrection;

      m_el_topoetcone40noCorrected = m_el_topoetcone40+m_el_topoetcone40ptCorrection+m_el_topoetcone40pileupCorrection;
      m_el_topoetcone30noCorrected = m_el_topoetcone30+m_el_topoetcone30ptCorrection+m_el_topoetcone30pileupCorrection;
      m_el_topoetcone20noCorrected = m_el_topoetcone20+m_el_topoetcone20ptCorrection+m_el_topoetcone20pileupCorrection;

        m_el_etcone40 = ((*el_itr)->isolationValue(xAOD::Iso::etcone40));
        m_el_etcone30 = ((*el_itr)->isolationValue(xAOD::Iso::etcone30));
        m_el_etcone20 = ((*el_itr)->isolationValue(xAOD::Iso::etcone20));

        const   xAOD::Egamma * el_cast= (xAOD::Egamma *)(*el_itr);
        /*m_el_topoetcone20toolCorrection=isoCorr_tool_20->GetPtCorrection(*el_cast,xAOD::Iso::IsolationType::topoetcone20);
        m_el_topoetcone30toolCorrection=isoCorr_tool_20->GetPtCorrection(*el_cast,xAOD::Iso::IsolationType::topoetcone30);
        m_el_topoetcone40toolCorrection=isoCorr_tool_20->GetPtCorrection(*el_cast,xAOD::Iso::IsolationType::topoetcone40);
        m_el_topoetcone30toolCorrected=m_el_topoetcone30noCorrected-m_el_topoetcone30toolCorrection-m_el_topoetcone30pileupCorrection;
        m_el_topoetcone20toolCorrected=m_el_topoetcone20noCorrected-m_el_topoetcone20toolCorrection-m_el_topoetcone20pileupCorrection;
        m_el_topoetcone40toolCorrected=m_el_topoetcone40noCorrected-m_el_topoetcone40toolCorrection-m_el_topoetcone40pileupCorrection;*/
        
}

        //   electron_isem->accept((*el_itr));
        //   m_el_isEM=electron_isem->IsemValue();

        (*el_itr)->trackCaloMatchValue(m_el_deltaphi2,xAOD::EgammaParameters::deltaPhi2);
        (*el_itr)->trackCaloMatchValue(m_el_deltaPhiFromLast,xAOD::EgammaParameters::deltaPhiFromLastMeasurement);

        const xAOD::TruthParticle* true_electron = NULL;

        // Matching to offline to retrieve the truth object
        if(doOnline){
          const xAOD::ElectronContainer* electrons = 0;
          if( !m_event->retrieve(electrons, "Electrons").isSuccess() ){
            Error("execute()", "Failed to retrieve ElectronCollection. Exiting.");
            return EL::StatusCode::FAILURE;
          }

          /*The real matching*/
          const xAOD::Electron* elOff = NULL;
          {
            //double GeV = 1000.;
            double drMax = 100.;
            TLorentzVector elEF;
            elEF.SetPtEtaPhiE( (*el_itr)->pt(), (*el_itr)->eta(),
            (*el_itr)->phi(), (*el_itr)->e());

            const xAOD::Electron* current = NULL;
            for( xAOD::ElectronContainer::const_iterator elOff_itr = electrons->begin();
            elOff_itr != electrons->end();
            ++elOff_itr){
              //if( (*elOff_itr)->e()/cosh((*elOff_itr)->eta()) < 20.*GeV) continue;
              TLorentzVector elVec;
              elVec.SetPtEtaPhiE((*elOff_itr)->pt(), (*elOff_itr)->eta(),
              (*elOff_itr)->phi(), (*elOff_itr)->e());

              double dr = elVec.DeltaR(elEF);
              if( fabs(dr) < fabs(drMax) ){
                drMax = dr;
                current = *elOff_itr;
              }
            } // for
            if( fabs(drMax) < 0.1 ) elOff = current;
            else elOff = NULL;
          }
          /*End of matching*/

          if( elOff){
            true_electron =  xAOD::TruthHelpers::getTruthParticle(*elOff);
            m_el_tightPP=m_LHToolTight2015->accept(elOff);
            m_el_mediumPP=m_LHToolMedium2015->accept(elOff);
            m_el_loosePP=m_LHToolLoose2015->accept(elOff);
          }
        } else {
          true_electron =  xAOD::TruthHelpers::getTruthParticle(*(*el_itr));
          m_el_tightPP=m_LHToolTight2015->accept(*el_itr);
          m_el_mediumPP=m_LHToolMedium2015->accept(*el_itr);
          m_el_loosePP=m_LHToolLoose2015->accept(*el_itr);
        }

        if (not true_electron) {
          //Error("execute()", "Failed to retrive true particle");


          m_el_truth_E=-999;
          m_el_truth_pt=-999;
          m_el_truth_eta=-999;
          m_el_truth_phi=-999;
          m_el_truth_type=-999;
          m_el_truth_parent_pdgId= -999;
          m_el_truth_matched=false;

        }
        else{
          m_el_truth_matched=true;
          m_el_truth_pt= true_electron->pt();
          m_el_truth_phi= true_electron->phi();
          m_el_truth_eta= true_electron->eta();
          m_el_truth_E= true_electron->e();
          m_el_truth_type= true_electron->pdgId();
          const xAOD::TruthParticle* true_parent= true_electron->parent();
          if(true_parent)
          m_el_truth_parent_pdgId= true_parent->pdgId();
          else  m_el_truth_parent_pdgId= -999;


        }





        if (FLAT && (N_particle_saved>10 || m_el_n==1)) outputTree->Fill() ;



        else if (!FLAT && (N_particle_saved>10 || m_el_n==1)){

          m_vec_el_cl_E->push_back(m_el_cl_E);
          m_vec_el_cl_etaCalo->push_back(m_el_cl_etaCalo);
          m_vec_el_cl_phi->push_back(m_el_cl_phi);
          m_vec_el_cl_phiCalo->push_back(m_el_cl_phiCalo);
          m_vec_el_author->push_back(m_el_author);
          m_vec_el_charge->push_back(m_el_charge);
          m_vec_el_cl_eta->push_back(m_el_cl_eta);
          // m_vec_el_deltaphi2->push_back(m_el_deltaphi2);
          //m_vec_el_deltaPhiFirstLast->push_back(m_el_deltaPhiFirstLast);
          m_vec_el_deltaPhiFromLast->push_back(m_el_deltaPhiFromLast);
          m_vec_el_fside->push_back(m_el_fside);
          // m_vec_el_isEM->push_back(m_el_isEM);
          m_vec_el_loosePP->push_back(m_el_loosePP);
          m_vec_el_mediumPP->push_back(m_el_mediumPP);
          // m_vec_el_p0->push_back(m_el_p0);
          // m_vec_el_pLast->push_back(m_el_pLast);
          // m_vec_el_refittedTrack_author->push_back(m_el_refittedTrack_author);
          // m_vec_el_refittedTrack_LMqoverp->push_back(m_el_refittedTrack_LMqoverp);
          m_vec_el_refittedTrack_qoverp->push_back(m_el_refittedTrack_qoverp);
          m_vec_el_E237->push_back(m_el_E237);
          m_vec_el_E233->push_back(m_el_E233);
          m_vec_el_E277->push_back(m_el_E277);
          m_vec_el_reta->push_back(m_el_reta);
          m_vec_el_rphi->push_back(m_el_rphi);
          m_vec_el_Ethad->push_back(m_el_Ethad);
          m_vec_el_Ethad1->push_back(m_el_Ethad1);
          m_vec_el_tightPP->push_back(m_el_tightPP);
          m_vec_el_rawcl_calibHitsShowerDepth->push_back(m_el_rawcl_calibHitsShowerDepth);
          m_vec_el_rawcl_Eacc->push_back(m_el_rawcl_Eacc);
          m_vec_el_rawcl_Es0->push_back(m_el_rawcl_Es0);
          m_vec_el_rawcl_Es1->push_back(m_el_rawcl_Es1);
          m_vec_el_rawcl_Es2->push_back(m_el_rawcl_Es2);
          m_vec_el_rawcl_Es3->push_back(m_el_rawcl_Es3);
          m_vec_el_rawcl_Et->push_back(m_el_rawcl_Et);
          m_vec_el_rawcl_f0->push_back(m_el_rawcl_f0);
          m_vec_el_tracketa->push_back(m_el_tracketa);
          m_vec_el_trackpt->push_back(m_el_trackpt);
          m_vec_el_trackz0->push_back(m_el_trackz0);
          m_vec_el_truth_pt->push_back(m_el_truth_pt);
          m_vec_el_truth_E->push_back(m_el_truth_E);
          m_vec_el_truth_eta->push_back(m_el_truth_eta);
          m_vec_el_truth_phi->push_back(m_el_truth_phi);
          m_vec_el_truth_type->push_back(m_el_truth_type);
          m_vec_el_truth_parent_pdgId->push_back(m_el_truth_parent_pdgId);
          m_vec_el_truth_matched->push_back(m_el_truth_matched);
          m_vec_el_weta2->push_back(m_el_weta2);
          m_vec_el_ws3->push_back(m_el_ws3);
          m_vec_el_wstot->push_back(m_el_wstot);
          m_vec_el_DeltaE->push_back(m_el_DeltaE);
          m_vec_el_Eratio->push_back(m_el_Eratio);
          m_vec_el_Rhad1->push_back(m_el_Rhad1);
          m_vec_el_Rhad->push_back(m_el_Rhad);
        }

        else{





          tmp_vec_el_cl_E->push_back(m_el_cl_E);
          tmp_vec_el_cl_etaCalo->push_back(m_el_cl_etaCalo);
          tmp_vec_el_cl_phi->push_back(m_el_cl_phi);
          tmp_vec_el_cl_phiCalo->push_back(m_el_cl_phiCalo);
          tmp_vec_el_author->push_back(m_el_author);
          tmp_vec_el_charge->push_back(m_el_charge);
          tmp_vec_el_cl_eta->push_back(m_el_cl_eta);
          // tmp_vec_el_deltaphi2->push_back(m_el_deltaphi2);
          //tmp_vec_el_deltaPhiFirstLast->push_back(m_el_deltaPhiFirstLast);
          tmp_vec_el_deltaPhiFromLast->push_back(m_el_deltaPhiFromLast);
          tmp_vec_el_fside->push_back(m_el_fside);
          // tmp_vec_el_isEM->push_back(m_el_isEM);
          tmp_vec_el_loosePP->push_back(m_el_loosePP);
          tmp_vec_el_mediumPP->push_back(m_el_mediumPP);
          // tmp_vec_el_p0->push_back(m_el_p0);
          // tmp_vec_el_pLast->push_back(m_el_pLast);
          // tmp_vec_el_refittedTrack_author->push_back(m_el_refittedTrack_author);
          // tmp_vec_el_refittedTrack_LMqoverp->push_back(m_el_refittedTrack_LMqoverp);
          tmp_vec_el_refittedTrack_qoverp->push_back(m_el_refittedTrack_qoverp);
          tmp_vec_el_E237->push_back(m_el_E237);
          tmp_vec_el_E233->push_back(m_el_E233);
          tmp_vec_el_E277->push_back(m_el_E277);
          tmp_vec_el_reta->push_back(m_el_reta);
          tmp_vec_el_rphi->push_back(m_el_rphi);
          tmp_vec_el_Ethad->push_back(m_el_Ethad);
          tmp_vec_el_Ethad1->push_back(m_el_Ethad1);
          tmp_vec_el_tightPP->push_back(m_el_tightPP);
          tmp_vec_el_rawcl_calibHitsShowerDepth->push_back(m_el_rawcl_calibHitsShowerDepth);
          tmp_vec_el_rawcl_Eacc->push_back(m_el_rawcl_Eacc);
          tmp_vec_el_rawcl_Es0->push_back(m_el_rawcl_Es0);
          tmp_vec_el_rawcl_Es1->push_back(m_el_rawcl_Es1);
          tmp_vec_el_rawcl_Es2->push_back(m_el_rawcl_Es2);
          tmp_vec_el_rawcl_Es3->push_back(m_el_rawcl_Es3);
          tmp_vec_el_rawcl_Et->push_back(m_el_rawcl_Et);
          tmp_vec_el_rawcl_f0->push_back(m_el_rawcl_f0);
          tmp_vec_el_tracketa->push_back(m_el_tracketa);
          tmp_vec_el_trackpt->push_back(m_el_trackpt);
          tmp_vec_el_trackz0->push_back(m_el_trackz0);
          tmp_vec_el_truth_pt->push_back(m_el_truth_pt);
          tmp_vec_el_truth_E->push_back(m_el_truth_E);
          tmp_vec_el_truth_eta->push_back(m_el_truth_eta);
          tmp_vec_el_truth_phi->push_back(m_el_truth_phi);
          tmp_vec_el_truth_type->push_back(m_el_truth_type);
          tmp_vec_el_truth_parent_pdgId->push_back(m_el_truth_parent_pdgId);
          tmp_vec_el_truth_matched->push_back(m_el_truth_matched);
          tmp_vec_el_weta2->push_back(m_el_weta2);
          tmp_vec_el_ws3->push_back(m_el_ws3);
          tmp_vec_el_wstot->push_back(m_el_wstot);
          tmp_vec_el_DeltaE->push_back(m_el_DeltaE);
          tmp_vec_el_Eratio->push_back(m_el_Eratio);
          tmp_vec_el_Rhad1->push_back(m_el_Rhad1);
          tmp_vec_el_Rhad->push_back(m_el_Rhad);

        }

      }

      delete caloclusters;

      if(N_particle_saved<10 && m_el_n>1){
        double pt=0;
        std::vector<int> index_pt(N_particle_saved,-999);
        std::vector<int>::iterator it;


        for (int k=0; k<N_particle_saved; k++){
          for(unsigned int i=0; i<tmp_vec_el_cl_E->size(); i++){
            if( (tmp_vec_el_cl_E->at(i)/cosh(tmp_vec_el_cl_eta->at(i)))>pt ){
              it = find (index_pt.begin(), index_pt.end(), i);
              if (it == index_pt.end()){
                pt=(tmp_vec_el_cl_E->at(i)/cosh(tmp_vec_el_cl_eta->at(i)));
                index_pt[k]=i;
              }
            }

          }
          pt=0;

        }

        if (FLAT) {

          for(unsigned int i=0; i<index_pt.size(); i++){
            if (index_pt[i]==-999) continue;

            m_el_cl_E=tmp_vec_el_cl_E->at(index_pt[i]);
            m_el_cl_eta=tmp_vec_el_cl_eta->at(index_pt[i]);
            m_el_author=tmp_vec_el_author->at(index_pt[i]);
            m_el_charge=tmp_vec_el_charge->at(index_pt[i]);
            m_el_cl_etaCalo=tmp_vec_el_cl_etaCalo->at(index_pt[i]);
            m_el_cl_phi=tmp_vec_el_cl_phi->at(index_pt[i]);
            m_el_cl_phiCalo=tmp_vec_el_cl_phiCalo->at(index_pt[i]);
            m_el_Ethad=tmp_vec_el_Ethad->at(index_pt[i]);
            m_el_Ethad1=tmp_vec_el_Ethad1->at(index_pt[i]);
            m_el_fside=tmp_vec_el_fside->at(index_pt[i]);
            m_el_deltaPhiFromLast=tmp_vec_el_deltaPhiFromLast->at(index_pt[i]);
            m_el_refittedTrack_qoverp=tmp_vec_el_refittedTrack_qoverp->at(index_pt[i]);
            m_el_loosePP=tmp_vec_el_loosePP->at(index_pt[i]);
            // m_el_materialTraversed=tmp_vec_el_materialTraversed->at(index_pt[i]);
            m_el_rawcl_calibHitsShowerDepth=tmp_vec_el_rawcl_calibHitsShowerDepth->at(index_pt[i]);
            //m_el_rawcl_Eacc=tmp_vec_el_rawcl_Eacc->at(index_pt[i]);
            m_el_rawcl_Es0=tmp_vec_el_rawcl_Es0->at(index_pt[i]);
            m_el_rawcl_Es1=tmp_vec_el_rawcl_Es1->at(index_pt[i]);
            m_el_rawcl_Es2=tmp_vec_el_rawcl_Es2->at(index_pt[i]);
            m_el_rawcl_Es3=tmp_vec_el_rawcl_Es3->at(index_pt[i]);
            m_el_rawcl_Et=tmp_vec_el_rawcl_Et->at(index_pt[i]);
            m_el_rawcl_f0=tmp_vec_el_rawcl_f0->at(index_pt[i]);
            m_el_E237=tmp_vec_el_E237->at(index_pt[i]);
            m_el_E233=tmp_vec_el_E233->at(index_pt[i]);
            m_el_E277=tmp_vec_el_E277->at(index_pt[i]);
            m_el_reta=tmp_vec_el_reta->at(index_pt[i]);
            m_el_rphi=tmp_vec_el_rphi->at(index_pt[i]);
            m_el_tightPP=tmp_vec_el_tightPP->at(index_pt[i]);
            m_el_tracketa=tmp_vec_el_tracketa->at(index_pt[i]);
            m_el_trackpt=tmp_vec_el_trackpt->at(index_pt[i]);
            m_el_trackz0=tmp_vec_el_trackz0->at(index_pt[i]);
            m_el_truth_pt=tmp_vec_el_truth_pt->at(index_pt[i]);
            m_el_truth_E=tmp_vec_el_truth_E->at(index_pt[i]);
            m_el_truth_eta=tmp_vec_el_truth_eta->at(index_pt[i]);
            m_el_truth_matched=tmp_vec_el_truth_matched->at(index_pt[i]);
            m_el_truth_phi=tmp_vec_el_truth_phi->at(index_pt[i]);
            m_el_truth_type=tmp_vec_el_truth_type->at(index_pt[i]);
            m_el_truth_parent_pdgId=tmp_vec_el_truth_parent_pdgId->at(index_pt[i]);
            m_el_weta2=tmp_vec_el_weta2->at(index_pt[i]);
            m_el_ws3=tmp_vec_el_ws3->at(index_pt[i]);
            m_el_wstot=tmp_vec_el_wstot->at(index_pt[i]);
            m_el_DeltaE=tmp_vec_el_DeltaE->at(index_pt[i]);
            m_el_Eratio=tmp_vec_el_Eratio->at(index_pt[i]);
            m_el_Rhad1=tmp_vec_el_Rhad1->at(index_pt[i]);
            m_el_Rhad=tmp_vec_el_Rhad->at(index_pt[i]);
            outputTree->Fill() ;
        }
      }
        else{


          for(int idx=0; idx<N_particle_saved; idx++){
            if (index_pt.at(idx)==-999) continue;



            m_vec_el_cl_E->push_back(tmp_vec_el_cl_E->at(index_pt.at(idx)));
            m_vec_el_cl_etaCalo->push_back(tmp_vec_el_cl_etaCalo->at(index_pt.at(idx)));
            m_vec_el_cl_phi->push_back(tmp_vec_el_cl_phi->at(index_pt.at(idx)));
            m_vec_el_cl_phiCalo->push_back(tmp_vec_el_cl_phiCalo->at(index_pt.at(idx)));
            m_vec_el_author->push_back(tmp_vec_el_author->at(index_pt.at(idx)));
            m_vec_el_charge->push_back(tmp_vec_el_charge->at(index_pt.at(idx)));
            m_vec_el_cl_eta->push_back(tmp_vec_el_cl_eta->at(index_pt.at(idx)));
            //m_vec_el_deltaphi2->push_back(tmp_vec_el_deltaphi2->at(index_pt.at(idx)));
            //m_vec_el_deltaPhiFirstLast->push_back(tmp_vec_el_deltaPhiFirstLast->at(index_pt.at(idx)));
            m_vec_el_deltaPhiFromLast->push_back(tmp_vec_el_deltaPhiFromLast->at(index_pt.at(idx)));
            m_vec_el_fside->push_back(tmp_vec_el_fside->at(index_pt.at(idx)));
            //m_vec_el_isEM->push_back(m_vec_el_isEM->at(index_pt.at(idx)));
            m_vec_el_loosePP->push_back(tmp_vec_el_loosePP->at(index_pt.at(idx)));
            m_vec_el_mediumPP->push_back(tmp_vec_el_mediumPP->at(index_pt.at(idx)));
            // m_vec_el_p0->push_back(tmp_vec_el_p0->at(index_pt.at(idx)));
            //m_vec_el_pLast->push_back(tmp_vec_el_pLast->at(index_pt.at(idx)));
            //m_vec_el_refittedTrack_author->push_back(tmp_vec_el_refittedTrack_author->at(index_pt.at(idx)));
            //m_vec_el_refittedTrack_LMqoverp->push_back(tmp_vec_el_refittedTrack_LMqoverp->at(index_pt.at(idx)));
            m_vec_el_refittedTrack_qoverp->push_back(tmp_vec_el_refittedTrack_qoverp->at(index_pt.at(idx)));
            m_vec_el_E237->push_back(tmp_vec_el_E237->at(index_pt.at(idx)));
            m_vec_el_E233->push_back(tmp_vec_el_E233->at(index_pt.at(idx)));
            m_vec_el_E277->push_back(tmp_vec_el_E277->at(index_pt.at(idx)));
            m_vec_el_reta->push_back(tmp_vec_el_reta->at(index_pt.at(idx)));
            m_vec_el_rphi->push_back(tmp_vec_el_rphi->at(index_pt.at(idx)));
            m_vec_el_tightPP->push_back(tmp_vec_el_tightPP->at(index_pt.at(idx)));
            m_vec_el_rawcl_calibHitsShowerDepth->push_back(tmp_vec_el_rawcl_calibHitsShowerDepth->at(index_pt.at(idx)));
            m_vec_el_rawcl_Eacc->push_back(tmp_vec_el_rawcl_Eacc->at(index_pt.at(idx)));
            m_vec_el_rawcl_Es0->push_back(tmp_vec_el_rawcl_Es0->at(index_pt.at(idx)));
            m_vec_el_rawcl_Es1->push_back(tmp_vec_el_rawcl_Es1->at(index_pt.at(idx)));
            m_vec_el_rawcl_Es2->push_back(tmp_vec_el_rawcl_Es2->at(index_pt.at(idx)));
            m_vec_el_rawcl_Es3->push_back(tmp_vec_el_rawcl_Es3->at(index_pt.at(idx)));
            m_vec_el_rawcl_Et->push_back(tmp_vec_el_rawcl_Et->at(index_pt.at(idx)));
            m_vec_el_rawcl_f0->push_back(tmp_vec_el_rawcl_f0->at(index_pt.at(idx)));
            m_vec_el_tracketa->push_back(tmp_vec_el_tracketa->at(index_pt.at(idx)));
            m_vec_el_trackpt->push_back(tmp_vec_el_trackpt->at(index_pt.at(idx)));
            m_vec_el_trackz0->push_back(tmp_vec_el_trackz0->at(index_pt.at(idx)));
            m_vec_el_truth_E->push_back(tmp_vec_el_truth_E->at(index_pt.at(idx)));
            m_vec_el_truth_pt->push_back(tmp_vec_el_truth_pt->at(index_pt.at(idx)));
            m_vec_el_truth_eta->push_back(tmp_vec_el_truth_eta->at(index_pt.at(idx)));
            m_vec_el_truth_phi->push_back(tmp_vec_el_truth_phi->at(index_pt.at(idx)));
            m_vec_el_truth_type->push_back(tmp_vec_el_truth_type->at(index_pt.at(idx)));
            m_vec_el_truth_parent_pdgId->push_back(tmp_vec_el_truth_parent_pdgId->at(index_pt.at(idx)));
            m_vec_el_truth_matched->push_back(tmp_vec_el_truth_matched->at(index_pt.at(idx)));
            m_vec_el_weta2->push_back(tmp_vec_el_weta2->at(index_pt.at(idx)));
            m_vec_el_ws3->push_back(tmp_vec_el_ws3->at(index_pt.at(idx)));
            m_vec_el_wstot->push_back(tmp_vec_el_wstot->at(index_pt.at(idx)));
            m_vec_el_DeltaE ->push_back(tmp_vec_el_DeltaE->at(index_pt.at(idx)));
            m_vec_el_Eratio ->push_back(tmp_vec_el_Eratio->at(index_pt.at(idx)));
            m_vec_el_Rhad1->push_back(tmp_vec_el_Rhad1->at(index_pt.at(idx)));
            m_vec_el_Rhad ->push_back(tmp_vec_el_Rhad->at(index_pt.at(idx)));
            m_vec_el_Ethad->push_back(tmp_vec_el_Ethad->at(index_pt.at(idx)));
            m_vec_el_Ethad1->push_back(tmp_vec_el_Ethad1->at(index_pt.at(idx)));



          }
        }

      }
    }
  }


  if(!FLAT && ((particleType==1 && m_el_n>0) || (particleType==0 && m_ph_n>0))) outputTree->Fill() ;

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode dumpxAODntuple::postExecute ()
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode dumpxAODntuple::finalize ()
{
  if(particleType == 0)
        /*std::cout << m_problems << " wrong photons out of "
	      << m_problems+ m_sane << " in total, "
	      << m_problems/(m_problems + m_sane)*100 << " % of the total"
	      << std::endl;*/


        delete m_LHToolTight2015;
        delete m_LHToolMedium2015;
        delete m_LHToolLoose2015;
        delete m_photonTightIsEMSelector;
        delete m_photonLooseIsEMSelector;

  if(particleType == 0) {
    if(N_particle_saved<10){
      delete tmp_vec_ph_CaloPointing_eta;
      delete tmp_vec_ph_cl_E;
      delete tmp_vec_ph_cl_eta;
      delete tmp_vec_ph_cl_etaCalo;
      delete tmp_vec_ph_cl_phi;
      delete tmp_vec_ph_cl_phiCalo;
      delete tmp_vec_ph_author;
      delete tmp_vec_ph_convFlag;
      delete tmp_vec_ph_convMatchDeltaPhi1;
      delete tmp_vec_ph_convMatchDeltaPhi2;
      delete tmp_vec_ph_convMatchDeltaEta1;
      delete tmp_vec_ph_convMatchDeltaEta2;
      delete tmp_vec_ph_convTrk1_DeltaPhi_track_calo;
      delete tmp_vec_ph_convtrk1nPixHits;
      delete tmp_vec_ph_convtrk1nSCTHits;
      delete tmp_vec_ph_convTrk2_DeltaPhi_track_calo;
      delete tmp_vec_ph_convtrk2nPixHits;
      delete tmp_vec_ph_convtrk2nSCTHits;
      delete tmp_vec_ph_etas1;
      delete tmp_vec_ph_etas2;
      delete tmp_vec_ph_Ethad;
      delete tmp_vec_ph_Ethad1;
      delete tmp_vec_ph_fside;
      delete tmp_vec_ph_HPV_zvertex;
      delete tmp_vec_ph_isEM;
      delete tmp_vec_ph_loose;
      delete tmp_vec_ph_materialTraversed;
      delete tmp_vec_ph_pt1conv;
      delete tmp_vec_ph_pt2conv;
      delete tmp_vec_ph_ptconv;
      delete tmp_vec_ph_raw_cl;
      delete tmp_vec_ph_rawcl_calibHitsShowerDepth;
      delete tmp_vec_ph_rawcl_Eacc;
      delete tmp_vec_ph_rawcl_Es0;
      delete tmp_vec_ph_rawcl_Es1;
      delete tmp_vec_ph_rawcl_Es2;
      delete tmp_vec_ph_rawcl_Es3;
      delete tmp_vec_ph_rawcl_Et;
      delete tmp_vec_ph_rawcl_f0;
      delete tmp_vec_ph_Rconv;
      delete tmp_vec_ph_E237;
      delete tmp_vec_ph_E233;
      delete tmp_vec_ph_E277;
      delete tmp_vec_ph_reta;
      delete tmp_vec_ph_rphi;
      delete tmp_vec_ph_tight;
      delete tmp_vec_ph_truth_E;
      delete tmp_vec_ph_truth_pt;
      delete tmp_vec_ph_truth_eta;
      delete tmp_vec_ph_truth_matched;
      delete tmp_vec_ph_truth_phi;
      delete tmp_vec_ph_truth_Rconv;
      delete tmp_vec_ph_truth_type;
      delete tmp_vec_ph_truth_parent_pdgId;
      delete tmp_vec_ph_weta2;
      delete tmp_vec_ph_ws3;
      delete tmp_vec_ph_wstot;
      delete tmp_vec_ph_zconv;
      delete tmp_vec_ph_DeltaE;
      delete tmp_vec_ph_Eratio;
      delete tmp_vec_ph_Rhad1;
      delete tmp_vec_ph_Rhad;}

      if(!FLAT){

        delete m_vec_ph_CaloPointing_eta;
        delete m_vec_ph_cl_E;
        delete m_vec_ph_cl_eta;
        delete m_vec_ph_cl_etaCalo;
        delete m_vec_ph_cl_phi;
        delete m_vec_ph_cl_phiCalo;
        delete m_vec_ph_author;
        delete m_vec_ph_convFlag;
        delete m_vec_ph_convMatchDeltaPhi1;
        delete m_vec_ph_convMatchDeltaPhi2;
        delete m_vec_ph_convMatchDeltaEta1;
        delete m_vec_ph_convMatchDeltaEta2;
        delete m_vec_ph_convTrk1_DeltaPhi_track_calo;
        delete m_vec_ph_convtrk1nPixHits;
        delete m_vec_ph_convtrk1nSCTHits;
        delete m_vec_ph_convTrk2_DeltaPhi_track_calo;
        delete m_vec_ph_convtrk2nPixHits;
        delete m_vec_ph_convtrk2nSCTHits;
        delete m_vec_ph_etas1;
        delete m_vec_ph_etas2;
        delete m_vec_ph_Ethad;
        delete m_vec_ph_Ethad1;
        delete m_vec_ph_fside;
        delete m_vec_ph_HPV_zvertex;
        delete m_vec_ph_isEM;
        delete m_vec_ph_loose;
        delete m_vec_ph_materialTraversed;
        delete m_vec_ph_pt1conv;
        delete m_vec_ph_pt2conv;
        delete m_vec_ph_ptconv;
        delete m_vec_ph_raw_cl;
        delete m_vec_ph_rawcl_calibHitsShowerDepth;
        delete m_vec_ph_rawcl_Eacc;
        delete m_vec_ph_rawcl_Es0;
        delete m_vec_ph_rawcl_Es1;
        delete m_vec_ph_rawcl_Es2;
        delete m_vec_ph_rawcl_Es3;
        delete m_vec_ph_rawcl_Et;
        delete m_vec_ph_rawcl_f0;
        delete m_vec_ph_Rconv;
        delete m_vec_ph_E237;
        delete m_vec_ph_E233;
        delete m_vec_ph_E277;
        delete m_vec_ph_reta;
        delete m_vec_ph_rphi;
        delete m_vec_ph_tight;
        delete m_vec_ph_truth_E;
        delete m_vec_ph_truth_pt;
        delete m_vec_ph_truth_eta;
        delete m_vec_ph_truth_matched;
        delete m_vec_ph_truth_phi;
        delete m_vec_ph_truth_Rconv;
        delete m_vec_ph_truth_type;
        delete m_vec_ph_truth_parent_pdgId;
        delete m_vec_ph_weta2;
        delete m_vec_ph_ws3;
        delete m_vec_ph_wstot;
        delete m_vec_ph_zconv;
        delete m_vec_ph_DeltaE;
        delete m_vec_ph_Eratio;
        delete m_vec_ph_Rhad1;
        delete m_vec_ph_Rhad; }
      }
      if (particleType == 1) {

        if(!FLAT){
          delete m_vec_el_cl_E;
          delete m_vec_el_cl_etaCalo;
          delete m_vec_el_cl_phi;
          delete m_vec_el_cl_phiCalo;
          delete m_vec_el_author;
          delete m_vec_el_charge;
          delete m_vec_el_cl_eta;
          delete m_vec_el_deltaphi2;
          delete m_vec_el_deltaPhiFirstLast;
          delete m_vec_el_deltaPhiFromLast;
          delete m_vec_el_fside;
          delete m_vec_el_isEM;
          delete m_vec_el_loosePP;
          delete m_vec_el_mediumPP;
          delete m_vec_el_p0;
          delete m_vec_el_pLast;
          delete m_vec_el_refittedTrack_author;
          delete m_vec_el_refittedTrack_LMqoverp;
          delete m_vec_el_refittedTrack_qoverp;
          delete m_vec_el_E237;
          delete m_vec_el_E233;
          delete m_vec_el_E277;
          delete m_vec_el_reta;
          delete m_vec_el_rphi;
          delete m_vec_el_Ethad;
          delete m_vec_el_Ethad1;
          delete m_vec_el_tightPP;
          delete m_vec_el_rawcl_calibHitsShowerDepth;
          delete m_vec_el_rawcl_Eacc;
          delete m_vec_el_rawcl_Es0;
          delete m_vec_el_rawcl_Es1;
          delete m_vec_el_rawcl_Es2;
          delete m_vec_el_rawcl_Es3;
          delete m_vec_el_rawcl_Et;
          delete m_vec_el_rawcl_f0;
          delete m_vec_el_tracketa;
          delete m_vec_el_trackpt;
          delete m_vec_el_trackz0;
          delete m_vec_el_truth_E;
          delete m_vec_el_truth_pt;
          delete m_vec_el_truth_eta;
          delete m_vec_el_truth_phi;
          delete m_vec_el_truth_type;
          delete m_vec_el_truth_matched;
          delete m_vec_el_weta2;
          delete m_vec_el_ws3;
          delete m_vec_el_wstot;
          delete m_vec_el_DeltaE;
          delete m_vec_el_Eratio;
          delete m_vec_el_Rhad1;
          delete m_vec_el_Rhad;
          delete m_vec_el_truth_parent_pdgId;}

          if(N_particle_saved<10){
            delete tmp_vec_el_cl_E;
            delete tmp_vec_el_cl_etaCalo;
            delete tmp_vec_el_cl_phi;
            delete tmp_vec_el_cl_phiCalo;
            delete tmp_vec_el_author;
            delete tmp_vec_el_charge;
            delete tmp_vec_el_cl_eta;
            delete tmp_vec_el_deltaphi2;
            delete tmp_vec_el_deltaPhiFirstLast;
            delete tmp_vec_el_deltaPhiFromLast;
            delete tmp_vec_el_fside;
            delete tmp_vec_el_isEM;
            delete tmp_vec_el_loosePP;
            delete tmp_vec_el_mediumPP;
            delete tmp_vec_el_p0;
            delete tmp_vec_el_pLast;
            delete tmp_vec_el_refittedTrack_author;
            delete tmp_vec_el_refittedTrack_LMqoverp;
            delete tmp_vec_el_refittedTrack_qoverp;
            delete tmp_vec_el_E237;
            delete tmp_vec_el_E233;
            delete tmp_vec_el_E277;
            delete tmp_vec_el_reta;
            delete tmp_vec_el_rphi;
            delete tmp_vec_el_Ethad;
            delete tmp_vec_el_Ethad1;
            delete tmp_vec_el_tightPP;
            delete tmp_vec_el_rawcl_calibHitsShowerDepth;
            delete tmp_vec_el_rawcl_Eacc;
            delete tmp_vec_el_rawcl_Es0;
            delete tmp_vec_el_rawcl_Es1;
            delete tmp_vec_el_rawcl_Es2;
            delete tmp_vec_el_rawcl_Es3;
            delete tmp_vec_el_rawcl_Et;
            delete tmp_vec_el_rawcl_f0;
            delete tmp_vec_el_tracketa;
            delete tmp_vec_el_trackpt;
            delete tmp_vec_el_trackz0;
            delete tmp_vec_el_truth_E;
            delete tmp_vec_el_truth_pt;
            delete tmp_vec_el_truth_eta;
            delete tmp_vec_el_truth_phi;
            delete tmp_vec_el_truth_type;
            delete tmp_vec_el_truth_matched;
            delete tmp_vec_el_weta2;
            delete tmp_vec_el_ws3;
            delete tmp_vec_el_wstot;
            delete tmp_vec_el_DeltaE;
            delete tmp_vec_el_Eratio;
            delete tmp_vec_el_Rhad1;
            delete tmp_vec_el_Rhad;
            delete tmp_vec_el_truth_parent_pdgId; }


          }


          return EL::StatusCode::SUCCESS;
        }



        EL::StatusCode dumpxAODntuple::histFinalize ()
        {
          return EL::StatusCode::SUCCESS;
        }



        float dumpxAODntuple::getPtAtFirstMeasurement( const xAOD::TrackParticle* tp) const
        {
          if (!tp) return 0;
          for (unsigned int i = 0; i < tp->numberOfParameters(); ++i)
          if (tp->parameterPosition(i) == xAOD::FirstMeasurement)
          return hypot(tp->parameterPX(i), tp->parameterPY(i));

          return tp->pt();
        }
