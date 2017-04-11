import ROOT
import logging
logging.basicConfig(level=logging.INFO)
from optparse import OptionParser





parser = OptionParser()
parser.add_option("--sample", help="sample/samples to be seaarched")
parser.add_option("--output", help="sampple handler directory file name")
parser.add_option("--griddirect", help="make grid direct, if necessary, modify local site",action='store_true', default=False)
(options, args) = parser.parse_args()

import atexit
@atexit.register
def quite_exit():
    ROOT.gSystem.Exit(0)

logging.info("loading packages")
ROOT.gROOT.ProcessLine(".x $ROOTCOREDIR/scripts/load_packages.C")



sh = ROOT.SH.SampleHandler()
#sh1 = ROOT.SH.SampleHandler()

print options.sample
ROOT.SH.scanDQ2 (sh, options.sample);

#ROOT.SH.scanDir (sh1, "/gpfs/storage_6/storage_tmp/atlas/smanzoni/MVACalib");
#sample = sh1.get("mc14_13TeV.184001.ParticleGenerator_gamma_ETspectrumMVAcalib.recon.AOD.e3145_s1982_s2008_r5721_tid01529531_00")
#sh.add(sample)
sh.printContent()

if(options.griddirect):
        local_site="INFN-MILANO-ATLASC_PERF-EGAMMA"
	ROOT.SH.makeGridDirect(sh,local_site,"srm://t2cmcondor.mi.infn.it/","/gpfs/storage_2/", False);
	sh.printContent()

sh.save(options.output)


