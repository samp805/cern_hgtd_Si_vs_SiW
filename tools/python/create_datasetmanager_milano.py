import ROOT

manager = ROOT.TDataSetManagerFile("dir:milano_datasets")


common_path = "/gpfs/storage_2/atlas/atlasgroupdisk/perf-egamma/mc12_8TeV/NTUP_EGAMMA/"
common_path_p1005 = common_path + "e1173_s1479_s1470_r3586_r3549_p1005/"

# name, filenames, tree name
data = [
    ("mc12_8TeV_e_Et7to80_p1005",
     common_path_p1005 + "mc12_8TeV.159010.ParticleGenerator_e_Et7to80.merge.NTUP_EGAMMA.e1173_s1479_s1470_r3586_r3549_p1005_tid793927_00/*.root*",
     "egamma"),
    ("mc12_8TeV_e_Et80to500_p1005",
     common_path_p1005 + "mc12_8TeV.159011.ParticleGenerator_e_Et80to500.merge.NTUP_EGAMMA.e1173_s1479_s1470_r3586_r3549_p1005_tid793928_00/*.root*",
     "egamma"),
    ("mc12_8TeV_e_Et1000_p1005",
     common_path_p1005 + "mc12_8TeV.159012.ParticleGenerator_e_Et1000.merge.NTUP_EGAMMA.e1173_s1479_s1470_r3586_r3549_p1005_tid793929_00/*.root*",
     "egamma"),
    ("mc12_8TeV_gamma_Et7to80_p1005",
     common_path_p1005 + "mc12_8TeV.159020.ParticleGenerator_gamma_Et7to80.merge.NTUP_EGAMMA.e1173_s1479_s1470_r3586_r3549_p1005_tid793930_00/*.root*",
     "egamma"),
    ("mc12_8TeV_gamma_Et80to500_p1005",
     common_path_p1005 + "mc12_8TeV.159021.ParticleGenerator_gamma_Et80to500.merge.NTUP_EGAMMA.e1173_s1479_s1470_r3586_r3549_p1005_tid793931_00/*.root*",
     "egamma"),
    ("mc12_8TeV_gamma_Et1000_p1005",
     common_path_p1005 + "mc12_8TeV.159022.ParticleGenerator_gamma_Et1000.merge.NTUP_EGAMMA.e1173_s1479_s1470_r3586_r3549_p1005_tid793932_00/*.root*",
     "egamma"),
    ("diphoton1",
     ("/gpfs/storage_2/atlas/atlasgroupdisk/phys-sm/mc11_7TeV/NTUP_PHOTON/e901_s1310_s1300_r3043_r2993_p868/mc11_7TeV.128490.AlpgenJimmyGamGamWithAAMass50GeVNp0.merge.NTUP_PHOTON.e901_s1310_s1300_r3043_r2993_p868_tid735987_00/*.root*",
      "/gpfs/storage_2/atlas/atlasgroupdisk/phys-sm/mc11_7TeV/NTUP_PHOTON/e901_s1310_s1300_r3043_r2993_p868/mc11_7TeV.128491.AlpgenJimmyGamGamWithAAMass50GeVNp1.merge.NTUP_PHOTON.e901_s1310_s1300_r3043_r2993_p868_tid735988_00/*.root*",
      "/gpfs/storage_2/atlas/atlasgroupdisk/phys-sm/mc11_7TeV/NTUP_PHOTON/e901_s1310_s1300_r3043_r2993_p868/mc11_7TeV.128492.AlpgenJimmyGamGamWithAAMass50GeVNp2.merge.NTUP_PHOTON.e901_s1310_s1300_r3043_r2993_p868_tid735989_00/*.root*",
      "/gpfs/storage_2/atlas/atlasgroupdisk/phys-sm/mc11_7TeV/NTUP_PHOTON/e901_s1310_s1300_r3043_r2993_p868/mc11_7TeV.128493.AlpgenJimmyGamGamWithAAMass50GeVNp3.merge.NTUP_PHOTON.e901_s1310_s1300_r3043_r2993_p868_tid735990_00/*.root*"),
     "photon"),
    ("mc12_8TeV.e_Et7to80.p1005_flat", "/storage/turra/data_MVA/flatten_input/mc12_8TeV.e_Et7to80.merge.NTUP_EGAMMA_p1005.root", "egamma"),
    ("mc12_8TeV.e_Et80to500.p1005_flat", "/storage/turra/data_MVA/flatten_input/mc12_8TeV.e_Et80to500.merge.NTUP_EGAMMA_p1005.root", "egamma"),
    ]    

for datum in data:
    print ".",
    dataset = ROOT.TFileCollection()
    file_list = datum[1]
    if type(file_list) is str:
        file_list = (file_list,)
    for f in file_list:
        dataset.Add(f)
    dataset.SetDefaultTreeName(datum[2])
    manager.RegisterDataSet(datum[0], dataset, "")



manager.ShowDataSets()
