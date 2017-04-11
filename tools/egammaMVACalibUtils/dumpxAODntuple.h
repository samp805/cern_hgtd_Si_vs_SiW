#ifndef dumpxAODntuple_dumpxAODntuple_H
#define dumpxAODntuple_dumpxAODntuple_H

#include <TString.h>
#include <TTree.h>
#include <EventLoop/Algorithm.h>
#include <ElectronPhotonSelectorTools/AsgPhotonIsEMSelector.h>
#include <xAODRootAccess/Init.h>
#include <xAODRootAccess/TEvent.h>
#include "ElectronPhotonSelectorTools/AsgElectronIsEMSelector.h"
#include "ElectronPhotonSelectorTools/AsgElectronLikelihoodTool.h"
#include "xAODTracking/TrackParticleFwd.h"
//#include "IsolationCorrections/IsolationCorrectionTool.h"
class dumpxAODntuple : public EL::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
 public:
  // float cutValue;
  xAOD::TEvent *m_event;  //!
  int m_eventCounter; //!
  int m_problems;//!
  int m_sane;//!

 private:
  TH1* histo_truthnumberPV; //!
  TH1* histo_matchnumberPV; //!
  TH1* histo_truthnumberETA; //!
  TH1* histo_matchnumberETA; //!
  TH1* histo_truthnumberPT; //!
  TH1* histo_matchnumberPT; //!
  TH1* histo_truthnumberAIX; //!
  TH1* histo_matchnumberAIX; //!
  float getPtAtFirstMeasurement(const xAOD::TrackParticle* ) const;
  // variables that don't get filled at submission time should be
  // protected from being send from the submission node to the worker
  // node (done by the //!)
 public:

  TFile *outputFile; //!
  TTree *outputTree; //!

  TString outputStreamName;
  bool FLAT;
  bool doOnline;
  int particleType;
  int N_particle_saved;

  AsgElectronLikelihoodTool* m_LHToolTight2015; //!
  AsgElectronLikelihoodTool* m_LHToolMedium2015; //!
  AsgElectronLikelihoodTool* m_LHToolLoose2015; //!

  //CP::IsolationCorrectionTool* isoCorr_tool_20;//!

  AsgPhotonIsEMSelector* m_photonTightIsEMSelector; //!
  AsgPhotonIsEMSelector* m_photonLooseIsEMSelector; //!

  float m_ph_E;//!
  float m_ph_eta;//!
  float m_ph_phi;//!
  float m_ph_CaloPointing_eta;//!
  float m_ph_cl_E;//!
  float m_ph_cl_eta;//!
  float m_ph_cl_etaCalo;//!
  float m_ph_cl_etaS1Calo;//!
  float m_ph_cl_etaS2Calo;//!
  float m_ph_cl_phi;//!
  float m_ph_cl_phiCalo;//!
  float m_ph_cl_phiS1Calo;//!
  float m_ph_cl_phiS2Calo;//!
  int m_ph_author;//!
  int m_ph_convFlag;//!
  float m_ph_convMatchDeltaPhi1;//!
  float m_ph_convMatchDeltaPhi2;//!
  float m_ph_convMatchDeltaEta1;//!
  float m_ph_convMatchDeltaEta2;//!
  float m_ph_convTrk1_DeltaPhi_track_calo;//!
  int m_ph_convtrk1nPixHits;//!
  int m_ph_convtrk1nSCTHits;//!
  float m_ph_convTrk2_DeltaPhi_track_calo;//!
  int m_ph_convtrk2nPixHits;//!
  int m_ph_convtrk2nSCTHits;//!
  float m_ph_etas1;//!
  float m_ph_etas2;//!
  float m_ph_Ethad;//!
  float m_ph_Ethad1;//!
  float m_ph_fside;//!
  float m_ph_HPV_zvertex;//!
  int m_ph_isEM;//!
  bool m_ph_loose;//!
  float m_ph_materialTraversed;//!
  int m_ph_n;//!
  int m_ph_truth_n;//!
  float m_ph_pt1conv;//!
  float m_ph_pt2conv;//!
  float m_ph_ptconv;//!
  float m_ph_raw_cl;//!
  float m_ph_rawcl_calibHitsShowerDepth;//!
  float m_ph_rawcl_Eacc;//!
  float m_ph_rawcl_Es0;//!
  float m_ph_rawcl_Es1;//!
  float m_ph_rawcl_Es2;//!
  float m_ph_rawcl_Es3;//!
  float m_ph_rawcl_Et;//!
  float m_ph_rawcl_f0;//!
  float m_ph_Rconv;//!
  float m_ph_E237;//!
  float m_ph_E233;//!
  float m_ph_E277;//!
  float m_ph_reta;//!
  float m_ph_rphi;//!
  bool m_ph_tight;//!
  float m_ph_truth_E;//!
  float m_ph_truth_pt;//!
  float m_ph_truth_eta;//!
  bool m_ph_truth_matched;//!
  float m_ph_truth_phi;//!
  float m_ph_truth_Rconv;//!
  int m_ph_truth_type;//!
  int m_ph_truth_parent_pdgId;//!
  float m_ph_weta2;//!
  float m_ph_ws3;//!
  float m_ph_wstot;//!
  float m_ph_zconv;//!
  float m_ph_DeltaE;//!
  float m_ph_Eratio;//!
  float m_ph_Rhad1;//!
  float m_ph_Rhad;//!
  float m_ph_emaxs1;//!
  float m_ph_e2tsts1;//!
  float m_ph_emins1;//!
  float m_ph_topoetcone40; //!
  float m_ph_topoetcone30; //!
  float m_ph_topoetcone20; //!
  float m_ph_topoetcone40ptCorrection; //!
  float m_ph_topoetcone30ptCorrection; //!
  float m_ph_topoetcone20ptCorrection; //!
  float m_ph_topoetcone40pileupCorrection; //!
  float m_ph_topoetcone30pileupCorrection; //!
  float m_ph_topoetcone20pileupCorrection; //!
  float m_ph_etcone40; //!
  float m_ph_etcone30; //!
  float m_ph_etcone20; //!
  float m_ph_topoetcone40coreconeCorrection; //!
  float m_ph_topoetcone30coreconeCorrection; //!
  float m_ph_topoetcone20coreconeCorrection; //!
  float m_ph_topoetcone40core57Correction; //!
  float m_ph_topoetcone30core57Correction; //!
  float m_ph_topoetcone20core57Correction; //!
  float m_ph_neflowisol40; //!
  float m_ph_neflowisol30; //!
  float m_ph_neflowisol20; //!

  float m_ph_topoetcone40coreconeCorrected; //!
  float m_ph_topoetcone30coreconeCorrected; //!
  float m_ph_topoetcone20coreconeCorrected; //!
  float m_ph_topoetcone40noCorrected; //!
  float m_ph_topoetcone30noCorrected; //!
  float m_ph_topoetcone20noCorrected; //!
  float m_ph_topoetcone40toolCorrected; //!
  float m_ph_topoetcone30toolCorrected; //!
  float m_ph_topoetcone20toolCorrected; //!
  float m_ph_topoetcone40toolCorrection; //!
  float m_ph_topoetcone30toolCorrection; //!
  float m_ph_topoetcone20toolCorrection; //!

  float m_ph_cl_E_TileGap3;//!
  float m_ph_cl_E_TileGap2;//!
  float m_ph_cl_E_TileGap1;//!


  float m_el_E;//!
  float m_el_eta;//!
  float m_el_phi;//!
  float m_el_cl_E;//!
  float m_el_cl_etaCalo;//!
  float m_el_cl_etaS1Calo;//!
  float m_el_cl_etaS2Calo;//!
 float m_el_cl_phi;//!
  float m_el_cl_pt;//!
 float m_el_cl_m;//!
  float m_el_m;//!
  float m_el_cl_phiCalo;//!
  float m_el_cl_phiS1Calo;//!
  float m_el_cl_phiS2Calo;//!
  int m_el_author;//!
  int m_el_charge;//!
  int m_el_n;//!
  float m_el_cl_eta;//!
  float m_el_etas1;//!
  float m_el_etas2;//!
  float m_el_deltaphi2;//!
  float m_el_deltaPhiFirstLast;//!
  float m_el_deltaPhiFromLast;//!
  float m_el_fside;//!
  int m_el_isEM;//!
  bool m_el_loosePP;//!
  bool m_el_mediumPP;//!
  float m_el_p0;//!
  float m_el_pLast;//!
  float m_el_refittedTrack_author;//!
 float m_el_refittedTrack_LMqoverp;//!
  float m_el_refittedTrack_qoverp;//!
  float m_el_trackqoverp;//!
  float m_el_trackcov_qoverp;//!
  float m_el_E237;//!
  float m_el_E233;//!
  float m_el_E277;//!
  float m_el_reta;//!
  float m_el_rphi;//!
  float m_el_Ethad;//!
  float m_el_Ethad1;//!
  bool m_el_tightPP;//!
  float m_el_rawcl_calibHitsShowerDepth;//!
  float m_el_rawcl_Eacc;//!
  float m_el_rawcl_Es0;//!
  float m_el_rawcl_Es1;//!
  float m_el_rawcl_Es2;//!
  float m_el_rawcl_Es3;//!
  float m_el_rawcl_Et;//!
  float m_el_rawcl_f0;//!
  float m_el_tracketa;//!
  float m_el_trackphi;//!
float m_el_trackpt;//!
  float m_el_trackz0;//!
  float m_el_truth_E;//!
  float m_el_truth_eta;//!
  float m_el_truth_phi;//!
  float m_el_truth_pt;//!
  int m_el_truth_type;//!
  int m_el_truth_parent_pdgId;//!
  bool m_el_truth_matched;//!
  float m_el_weta2;//!
  float m_el_ws3;//!
  float m_el_wstot;//!
  float m_PV_zvertex;//!
  float m_averageIntPerXing;//!
  float m_actualIntPerXing;//!
  int m_RunNumber;//!
  int m_EventNumber;//!
  int m_PhotonPV_n;//!
  int m_bcid;//!
  int m_el_truth_n;//!
  float m_el_DeltaE;//!
  float m_el_Eratio;//!
  float m_el_Rhad1;//!
  float m_el_Rhad;//!
  float m_el_topoetcone40; //!
  float m_el_topoetcone30; //!
  float m_el_topoetcone20; //!
  float m_el_topoetcone40ptCorrection; //!
  float m_el_topoetcone30ptCorrection; //!
  float m_el_topoetcone20ptCorrection; //!
  float m_el_topoetcone40pileupCorrection; //!
  float m_el_topoetcone30pileupCorrection; //!
  float m_el_topoetcone20pileupCorrection; //!
  float m_el_etcone40; //!
  float m_el_etcone30; //!
  float m_el_etcone20; //!
  float m_el_topoetcone40coreconeCorrection; //!
  float m_el_topoetcone30coreconeCorrection; //!
  float m_el_topoetcone20coreconeCorrection; //!
  float m_el_topoetcone40core57Correction; //!
  float m_el_topoetcone30core57Correction; //!
  float m_el_topoetcone20core57Correction; //!
  float m_el_neflowisol40; //!
  float m_el_neflowisol30; //!
  float m_el_neflowisol20; //!

  float m_el_topoetcone40coreconeCorrected; //!
  float m_el_topoetcone30coreconeCorrected; //!
  float m_el_topoetcone20coreconeCorrected; //!
  float m_el_topoetcone40noCorrected; //!
  float m_el_topoetcone30noCorrected; //!
  float m_el_topoetcone20noCorrected; //!
  float m_el_topoetcone40toolCorrected; //!
  float m_el_topoetcone30toolCorrected; //!
  float m_el_topoetcone20toolCorrected; //!
  float m_el_topoetcone40toolCorrection; //!
  float m_el_topoetcone30toolCorrection; //!
  float m_el_topoetcone20toolCorrection; //!
  int m_el_FTFseed; //!
  float m_el_cl_E_TileGap3;//!
  float m_el_cl_E_TileGap2;//!
  float m_el_cl_E_TileGap1;//!

  std::vector<float>* m_vec_ph_CaloPointing_eta;//!
  std::vector<float>* m_vec_ph_cl_E;//!
  std::vector<float>* m_vec_ph_cl_eta;//!
  std::vector<float>* m_vec_ph_cl_etaCalo;//!
  std::vector<float>* m_vec_ph_cl_phi;//!
  std::vector<float>* m_vec_ph_cl_phiCalo;//!
  std::vector<int>* m_vec_ph_author;//!
  std::vector<int>* m_vec_ph_convFlag;//!
  std::vector<float>* m_vec_ph_convMatchDeltaPhi1;//!
  std::vector<float>* m_vec_ph_convMatchDeltaPhi2;//!
  std::vector<float>* m_vec_ph_convMatchDeltaEta1;//!
  std::vector<float>* m_vec_ph_convMatchDeltaEta2;//!
  std::vector<float>* m_vec_ph_convTrk1_DeltaPhi_track_calo;//!
  std::vector<int>* m_vec_ph_convtrk1nPixHits;//!
  std::vector<int>* m_vec_ph_convtrk1nSCTHits;//!
  std::vector<float>* m_vec_ph_convTrk2_DeltaPhi_track_calo;//!
  std::vector<int>* m_vec_ph_convtrk2nPixHits;//!
  std::vector<int>* m_vec_ph_convtrk2nSCTHits;//!
  std::vector<float>* m_vec_ph_etas1;//!
  std::vector<float>* m_vec_ph_etas2;//!
  std::vector<float>* m_vec_ph_Ethad;//!
  std::vector<float>* m_vec_ph_Ethad1;//!
  std::vector<float>* m_vec_ph_fside;//!
  std::vector<float>* m_vec_ph_HPV_zvertex;//!
  std::vector<int>* m_vec_ph_isEM;//!
  std::vector<bool>* m_vec_ph_loose;//!
  std::vector<float>* m_vec_ph_materialTraversed;//!
  std::vector<int>* m_vec_ph_n;//!
  std::vector<float>* m_vec_ph_pt1conv;//!
  std::vector<float>* m_vec_ph_pt2conv;//!
  std::vector<float>* m_vec_ph_ptconv;//!
  std::vector<float>* m_vec_ph_raw_cl;//!
  std::vector<float>* m_vec_ph_rawcl_calibHitsShowerDepth;//!
  std::vector<float>* m_vec_ph_rawcl_Eacc;//!
  std::vector<float>* m_vec_ph_rawcl_Es0;//!
  std::vector<float>* m_vec_ph_rawcl_Es1;//!
  std::vector<float>* m_vec_ph_rawcl_Es2;//!
  std::vector<float>* m_vec_ph_rawcl_Es3;//!
  std::vector<float>* m_vec_ph_rawcl_Et;//!
  std::vector<float>* m_vec_ph_rawcl_f0;//!
  std::vector<float>* m_vec_ph_Rconv;//!
  std::vector<float>* m_vec_ph_E237;//!
  std::vector<float>* m_vec_ph_E233;//!
  std::vector<float>* m_vec_ph_E277;//!
  std::vector<float>* m_vec_ph_reta;//!
  std::vector<float>* m_vec_ph_rphi;//!
  std::vector<bool>* m_vec_ph_tight;//!
  std::vector<float>* m_vec_ph_truth_E;//!
  std::vector<float>* m_vec_ph_truth_pt;//!
  std::vector<float>* m_vec_ph_truth_eta;//!
  std::vector<bool>* m_vec_ph_truth_matched;//!
  std::vector<float>* m_vec_ph_truth_phi;//!
  std::vector<float>* m_vec_ph_truth_Rconv;//!
  std::vector<int>* m_vec_ph_truth_type;//!
  std::vector<int>* m_vec_ph_truth_parent_pdgId;//!
  std::vector<float>* m_vec_ph_weta2;//!
  std::vector<float>* m_vec_ph_ws3;//!
  std::vector<float>* m_vec_ph_wstot;//!
  std::vector<float>* m_vec_ph_zconv;//!
  std::vector<float>* m_vec_ph_DeltaE;//!
  std::vector<float>* m_vec_ph_Eratio;//!
  std::vector<float>* m_vec_ph_Rhad1;//!
  std::vector<float>* m_vec_ph_Rhad;//!
  std::vector<float>* m_vec_ph_topoetcone40; //!
  std::vector<float>* m_vec_ph_topoetcone30; //!
  std::vector<float>* m_vec_ph_topoetcone20; //!
  std::vector<float>* m_vec_ph_etcone40; //!
  std::vector<float>* m_vec_ph_etcone30; //!
  std::vector<float>* m_vec_ph_etcone20; //!



  std::vector<float>* m_vec_el_cl_E;//!
  std::vector<float>* m_vec_el_cl_etaCalo;//!
  std::vector<float>* m_vec_el_cl_phi;//!
  std::vector<float>* m_vec_el_cl_phiCalo;//!
  std::vector<int>* m_vec_el_author;//!
  std::vector<int>* m_vec_el_charge;//!
  std::vector<float>* m_vec_el_cl_eta;//!
  std::vector<float>* m_vec_el_etas1;//!
  std::vector<float>* m_vec_el_etas2;//!
  std::vector<float>* m_vec_el_deltaphi2;//!
  std::vector<float>* m_vec_el_deltaPhiFirstLast;//!
  std::vector<float>* m_vec_el_deltaPhiFromLast;//!
  std::vector<float>* m_vec_el_fside;//!
  std::vector<int>* m_vec_el_isEM;//!
  std::vector<bool>* m_vec_el_loosePP;//!
  std::vector<bool>* m_vec_el_mediumPP;//!
  std::vector<float>* m_vec_el_p0;//!
  std::vector<float>* m_vec_el_pLast;//!
  std::vector<float>* m_vec_el_refittedTrack_author;//!
  std::vector<float>* m_vec_el_refittedTrack_LMqoverp;//!
  std::vector<float>* m_vec_el_refittedTrack_qoverp;//!
  std::vector<float>* m_vec_el_trackqoverp;//!
  std::vector<float>* m_vec_el_trackcov_qoverp;//!
  std::vector<float>* m_vec_el_E237;//!
  std::vector<float>* m_vec_el_E233;//!
  std::vector<float>* m_vec_el_E277;//!
  std::vector<float>* m_vec_el_reta;//!
  std::vector<float>* m_vec_el_rphi;//!
  std::vector<float>* m_vec_el_Ethad;//!
  std::vector<float>* m_vec_el_Ethad1;//!
  std::vector<bool>* m_vec_el_tightPP;//!
  std::vector<float>* m_vec_el_rawcl_calibHitsShowerDepth;//!
  std::vector<float>* m_vec_el_rawcl_Eacc;//!
  std::vector<float>* m_vec_el_rawcl_Es0;//!
  std::vector<float>* m_vec_el_rawcl_Es1;//!
  std::vector<float>* m_vec_el_rawcl_Es2;//!
  std::vector<float>* m_vec_el_rawcl_Es3;//!
  std::vector<float>* m_vec_el_rawcl_Et;//!
  std::vector<float>* m_vec_el_rawcl_f0;//!
  std::vector<float>* m_vec_el_tracketa;//!
  std::vector<float>* m_vec_el_trackpt;//!
  std::vector<float>* m_vec_el_trackz0;//!
  std::vector<float>* m_vec_el_truth_E;//!
  std::vector<float>* m_vec_el_truth_pt;//!
  std::vector<float>* m_vec_el_truth_eta;//!
  std::vector<float>* m_vec_el_truth_phi;//!
  std::vector<int>* m_vec_el_truth_type;//!
  std::vector<int>* m_vec_el_truth_parent_pdgId;//!
  std::vector<bool>* m_vec_el_truth_matched;//!
  std::vector<float>* m_vec_el_weta2;//!
  std::vector<float>* m_vec_el_ws3;//!
  std::vector<float>* m_vec_el_wstot;//!
  std::vector<float>* m_vec_el_DeltaE;//!
  std::vector<float>* m_vec_el_Eratio;//!
  std::vector<float>* m_vec_el_Rhad1;//!
  std::vector<float>* m_vec_el_Rhad;//!
  std::vector<float>* m_vec_el_topoetcone40; //!
  std::vector<float>* m_vec_el_topoetcone30; //!
  std::vector<float>* m_vec_el_topoetcone20; //!
  std::vector<float>* m_vec_el_etcone40; //!
  std::vector<float>* m_vec_el_etcone30; //!
  std::vector<float>* m_vec_el_etcone20; //!


  std::vector<float>* tmp_vec_ph_CaloPointing_eta;//!
  std::vector<float>* tmp_vec_ph_cl_E;//!
  std::vector<float>* tmp_vec_ph_cl_eta;//!
  std::vector<float>* tmp_vec_ph_cl_etaCalo;//!
  std::vector<float>* tmp_vec_ph_cl_phi;//!
  std::vector<float>* tmp_vec_ph_cl_phiCalo;//!
  std::vector<int>* tmp_vec_ph_author;//!
  std::vector<int>* tmp_vec_ph_convFlag;//!
  std::vector<float>* tmp_vec_ph_convMatchDeltaPhi1;//!
  std::vector<float>* tmp_vec_ph_convMatchDeltaPhi2;//!
  std::vector<float>* tmp_vec_ph_convMatchDeltaEta1;//!
  std::vector<float>* tmp_vec_ph_convMatchDeltaEta2;//!
  std::vector<float>* tmp_vec_ph_convTrk1_DeltaPhi_track_calo;//!
  std::vector<int>* tmp_vec_ph_convtrk1nPixHits;//!
  std::vector<int>* tmp_vec_ph_convtrk1nSCTHits;//!
  std::vector<float>* tmp_vec_ph_convTrk2_DeltaPhi_track_calo;//!
  std::vector<int>* tmp_vec_ph_convtrk2nPixHits;//!
  std::vector<int>* tmp_vec_ph_convtrk2nSCTHits;//!
  std::vector<float>* tmp_vec_ph_etas1;//!
  std::vector<float>* tmp_vec_ph_etas2;//!
  std::vector<float>* tmp_vec_ph_Ethad;//!
  std::vector<float>* tmp_vec_ph_Ethad1;//!
  std::vector<float>* tmp_vec_ph_fside;//!
  std::vector<float>* tmp_vec_ph_HPV_zvertex;//!
  std::vector<int>* tmp_vec_ph_isEM;//!
  std::vector<bool>* tmp_vec_ph_loose;//!
  std::vector<float>* tmp_vec_ph_materialTraversed;//!
  std::vector<int>* tmp_vec_ph_n;//!
  std::vector<float>* tmp_vec_ph_pt1conv;//!
  std::vector<float>* tmp_vec_ph_pt2conv;//!
  std::vector<float>* tmp_vec_ph_ptconv;//!
  std::vector<float>* tmp_vec_ph_raw_cl;//!
  std::vector<float>* tmp_vec_ph_rawcl_calibHitsShowerDepth;//!
  std::vector<float>* tmp_vec_ph_rawcl_Eacc;//!
  std::vector<float>* tmp_vec_ph_rawcl_Es0;//!
  std::vector<float>* tmp_vec_ph_rawcl_Es1;//!
  std::vector<float>* tmp_vec_ph_rawcl_Es2;//!
  std::vector<float>* tmp_vec_ph_rawcl_Es3;//!
  std::vector<float>* tmp_vec_ph_rawcl_Et;//!
  std::vector<float>* tmp_vec_ph_rawcl_f0;//!
  std::vector<float>* tmp_vec_ph_Rconv;//!
  std::vector<float>* tmp_vec_ph_E237;//!
  std::vector<float>* tmp_vec_ph_E233;//!
  std::vector<float>* tmp_vec_ph_E277;//!
  std::vector<float>* tmp_vec_ph_reta;//!
  std::vector<float>* tmp_vec_ph_rphi;//!
  std::vector<bool>* tmp_vec_ph_tight;//!
  std::vector<float>* tmp_vec_ph_truth_E;//!
  std::vector<float>* tmp_vec_ph_truth_pt;//!
  std::vector<float>* tmp_vec_ph_truth_eta;//!
  std::vector<bool>* tmp_vec_ph_truth_matched;//!
  std::vector<float>* tmp_vec_ph_truth_phi;//!
  std::vector<float>* tmp_vec_ph_truth_Rconv;//!
  std::vector<int>* tmp_vec_ph_truth_type;//!
  std::vector<int>* tmp_vec_ph_truth_parent_pdgId;//!
  std::vector<float>* tmp_vec_ph_weta2;//!
  std::vector<float>* tmp_vec_ph_ws3;//!
  std::vector<float>* tmp_vec_ph_wstot;//!
  std::vector<float>* tmp_vec_ph_zconv;//!
  std::vector<float>* tmp_vec_ph_DeltaE;//!
  std::vector<float>* tmp_vec_ph_Eratio;//!
  std::vector<float>* tmp_vec_ph_Rhad1;//!
  std::vector<float>* tmp_vec_ph_Rhad;//!
  std::vector<float>* tmp_vec_ph_topoetcone40; //!
  std::vector<float>* tmp_vec_ph_topoetcone30; //!
  std::vector<float>* tmp_vec_ph_topoetcone20; //!
  std::vector<float>* tmp_vec_ph_etcone40; //!
  std::vector<float>* tmp_vec_ph_etcone30; //!
  std::vector<float>* tmp_vec_ph_etcone20; //!



  std::vector<float>* tmp_vec_el_cl_E;//!
  std::vector<float>* tmp_vec_el_cl_etaCalo;//!
  std::vector<float>* tmp_vec_el_cl_phi;//!
  std::vector<float>* tmp_vec_el_cl_phiCalo;//!
  std::vector<int>* tmp_vec_el_author;//!
  std::vector<int>* tmp_vec_el_charge;//!
  std::vector<float>* tmp_vec_el_cl_eta;//!
  std::vector<float>* tmp_vec_el_etas1;//!
  std::vector<float>* tmp_vec_el_etas2;//!
  std::vector<float>* tmp_vec_el_deltaphi2;//!
  std::vector<float>* tmp_vec_el_deltaPhiFirstLast;//!
  std::vector<float>* tmp_vec_el_deltaPhiFromLast;//!
  std::vector<float>* tmp_vec_el_fside;//!
  std::vector<int>* tmp_vec_el_isEM;//!
  std::vector<bool>* tmp_vec_el_loosePP;//!
  std::vector<bool>* tmp_vec_el_mediumPP;//!
  std::vector<float>* tmp_vec_el_p0;//!
  std::vector<float>* tmp_vec_el_pLast;//!
  std::vector<float>* tmp_vec_el_refittedTrack_author;//!
  std::vector<float>* tmp_vec_el_refittedTrack_LMqoverp;//!
  std::vector<float>* tmp_vec_el_refittedTrack_qoverp;//!
  std::vector<float>* tmp_vec_el_E237;//!
  std::vector<float>* tmp_vec_el_E233;//!
  std::vector<float>* tmp_vec_el_E277;//!
  std::vector<float>* tmp_vec_el_reta;//!
  std::vector<float>* tmp_vec_el_rphi;//!
  std::vector<float>* tmp_vec_el_Ethad;//!
  std::vector<float>* tmp_vec_el_Ethad1;//!
  std::vector<bool>* tmp_vec_el_tightPP;//!
  std::vector<float>* tmp_vec_el_rawcl_calibHitsShowerDepth;//!
  std::vector<float>* tmp_vec_el_rawcl_Eacc;//!
  std::vector<float>* tmp_vec_el_rawcl_Es0;//!
  std::vector<float>* tmp_vec_el_rawcl_Es1;//!
  std::vector<float>* tmp_vec_el_rawcl_Es2;//!
  std::vector<float>* tmp_vec_el_rawcl_Es3;//!
  std::vector<float>* tmp_vec_el_rawcl_Et;//!
  std::vector<float>* tmp_vec_el_rawcl_f0;//!
  std::vector<float>* tmp_vec_el_tracketa;//!
  std::vector<float>* tmp_vec_el_trackpt;//!
  std::vector<float>* tmp_vec_el_trackz0;//!
  std::vector<float>* tmp_vec_el_truth_E;//!
  std::vector<float>* tmp_vec_el_truth_pt;//!
  std::vector<float>* tmp_vec_el_truth_eta;//!
  std::vector<float>* tmp_vec_el_truth_phi;//!
  std::vector<int>* tmp_vec_el_truth_type;//!
  std::vector<int>* tmp_vec_el_truth_parent_pdgId;//!
  std::vector<bool>* tmp_vec_el_truth_matched;//!
  std::vector<float>* tmp_vec_el_weta2;//!
  std::vector<float>* tmp_vec_el_ws3;//!
  std::vector<float>* tmp_vec_el_wstot;//!
  std::vector<float>* tmp_vec_el_DeltaE;//!
  std::vector<float>* tmp_vec_el_Eratio;//!
  std::vector<float>* tmp_vec_el_Rhad1;//!
  std::vector<float>* tmp_vec_el_Rhad;//!
  std::vector<float>* tmp_vec_el_topoetcone40; //!
  std::vector<float>* tmp_vec_el_topoetcone30; //!
  std::vector<float>* tmp_vec_el_topoetcone20; //!
  std::vector<float>* tmp_vec_el_etcone40; //!
  std::vector<float>* tmp_vec_el_etcone30; //!
  std::vector<float>* tmp_vec_el_etcone20; //!



  // this is a standard constructor
  dumpxAODntuple ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);
  virtual EL::StatusCode fileExecute ();
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode changeInput (bool firstFile);
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode postExecute ();
  virtual EL::StatusCode finalize ();
  virtual EL::StatusCode histFinalize ();

  // this is needed to distribute the algorithm to the workers
  ClassDef(dumpxAODntuple, 1);
};

#endif
