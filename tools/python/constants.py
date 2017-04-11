class Constants():
    
    anal_dir = "~/workspace/hgtd/rootfiles/analysis_results/"
    root_dir = "~/workspace/hgtd/rootfiles/"
    regr_dir = "~/workspace/hgtd/rootfiles/regression_results/"
    energys = ["max_energy", "combined2_energy", "combined4_energy", "combined9_energy"]
    
    
    @classmethod
    def analDir(cls):
        return cls.anal_dir
    
    @classmethod
    def rootDir(cls):
        return cls.root_dir

    @classmethod
    def regrDir(cls):
        return cls.regr_dir

    @classmethod
    def energies(cls):
        return cls.energys

    