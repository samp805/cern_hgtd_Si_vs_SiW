import ROOT
import logging
import os
logging.basicConfig(level=logging.INFO)
from optparse import OptionParser


def getChain(tree_name, inputFiles, readFromFile = False):
    import os
    expanded_path = os.path.expanduser(os.path.expandvars(inputFiles))
    print expanded_path
    chain = ROOT.TChain(tree_name)
    if readFromFile:
      file_list = filter(bool, (i.strip('\n') for i in open(inputFiles)))
      map(chain.Add, file_list)
    else:
       chain.Add(expanded_path)
    if len(list(chain.GetListOfFiles())) == 0:
        logging.error("Cannot find any file from %s", str(inputFiles))
    return chain




parser = OptionParser()
parser.add_option("--input", help="input file/files. If single file add option --singleFile")
parser.add_option("--sampleHandler", help="sample handler directory")
parser.add_option("--outputsample", help='output file name, if grid/prun driver it has to be like: "user.<your grid id>.<whatever you want>')
parser.add_option("--submitDir", help="dir to store the output", default="submit_dir")
parser.add_option("--driver", help="select where to run", choices=("direct", "prooflite", "grid", "prun"), default="direct")
parser.add_option("--nevents", type=int, help="number of events to process for all the datasets")
parser.add_option("--particleType", type=int, help="0 for photons, 1 for electrons", default =0)
parser.add_option("--skip-events", type=int, help="skip the first n events")
parser.add_option("-w", "--overwrite", action='store_true', default=False, help="overwrite previous submitDir")
parser.add_option("--readFromFile", default=False, action="store_true", 
                             help="Read input files from text file")
parser.add_option("--flat", default=False, action="store_true", 
                             help="Fill a flat tree, one particle -> one entry")
parser.add_option("--download", default=False, action="store_true", 
                             help="download the samples")
parser.add_option("--doOnline", default=False, action="store_true", 
                             help="use Online objects")
parser.add_option("--nparticles", type=int, help="number of particles to be saved. From 1 to 10, over 10 all particles are saved. The particles are saved starting from the one with high pt", default=11)

(options, args) = parser.parse_args()

import atexit
@atexit.register
def quite_exit():
    ROOT.gSystem.Exit(0)

logging.info("loading packages")
ROOT.gROOT.ProcessLine(".x $ROOTCOREDIR/scripts/load_packages.C")

if options.overwrite:
    import shutil
    shutil.rmtree(options.submitDir, True)

if (options.particleType==0):
   particle="Photon";
else :
   particle="Electron";

ROOT.xAOD.Init().ignore()
sh = ROOT.SH.SampleHandler()

if (options.input):
	
	chain = getChain("CollectionTree", options.input, options.readFromFile )
        #chain =ROOT.TChain("CollectionTree")
        #chain.Add("/gpfs/storage_2/atlas/atlasgroupdisk/perf-egamma/rucio/mc14_13TeV/17/d8/AOD.01529530._000103.pool.root.1")
	sample=ROOT.SH.makeFromTChain(options.outputsample, chain)
	sample.setMetaString ("nc_tree", "CollectionTree");

	sh.add(sample)

if (options.sampleHandler):
	sh.load(options.sampleHandler)
	sh.setMetaString ("nc_tree", "CollectionTree");



#ROOT.SH.scanDir(sh, options.directory)
sh.printContent()

job=ROOT.EL.Job()
job.sampleHandler(sh)

if options.nevents:
    logging.info("processing only %d events", options.nevents)
    job.options().setDouble(ROOT.EL.Job.optMaxEvents, options.nevents)

if options.skip_events:
    logging.info("skipping first %d events", options.skip_events)
    job.options().setDouble(ROOT.EL.Job.optSkipEvents, options.skip_events)

alg=ROOT.dumpxAODntuple()

alg.outputStreamName = "output"
alg.particleType = options.particleType
alg.N_particle_saved = options.nparticles

if (options.doOnline):
   alg.doOnline=True

if options.flat:
   alg.FLAT=True



job.algsAdd(alg)


driver=None
if (options.driver == "direct"):
    logging.info("running on direct")
    driver = ROOT.EL.DirectDriver()
    job.options().setDouble (ROOT.EL.Job.optCacheSize, 10*1024*1024)
elif (options.driver == "prooflite"):
    logging.info("running on prooflite")
    driver = ROOT.EL.ProofDriver()
elif (options.driver == "prun"):
    logging.info("running on Prun")
    driver = ROOT.EL.PrunDriver()
    driver.options().setString("nc_outputSampleName", options.outputsample + ".%in:name[2]%")
    driver.options().setDouble("nc_mergeOutput", 1)
    job.options().setDouble (ROOT.EL.Job.optCacheSize, 10*1024*1024);
elif (options.driver == "grid"):
    logging.info("running on Grid")
    driver = ROOT.EL.GridDriver()
    driver.outputSampleName = options.outputsample +".%in:name[2]%"
    driver.mergeOutput=True
    job.options().setDouble (ROOT.EL.Job.optCacheSize, 10*1024*1024);


logging.info("submit job")
driver.submit (job, options.submitDir);

if options.download:
	logging.info("download sample")
        os.chdir(options.submitDir)
        os.mkdir("data-output")
        sh_out = ROOT.SH.SampleHandler()
        sh_out.load(options.submitDir+"/output-output/")
        sh_out.printContent()
        os.chdir(options.submitDir+"/data-output/")
        for sample in sh_out:
           samplename=sample.getMetaString("nc_grid")
           print samplename
           os.system("dq2-get "+samplename)

