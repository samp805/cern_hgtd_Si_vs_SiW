from glob import glob
import os.path
import os
from array import array
import sys
from math import cosh

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

try:
    ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C+")
except RuntimeError:
    print """you have to compile all the libraries first:
cd ..
cd externals
cd RootCore
./configure
cd scripts
source setup.sh
cd ../..
$ROOTCOREDIR/scripts/find_packages.sh
$ROOTCOREDIR/scripts/compile.sh
"""

# python add_fudged.py -o ~/prova2 -t photon -f -i ~/eos/atlas/user/b/blenzi/egammaMVACalibD3PD/user.blenzi.MiniPhotonD3PD.v3muB.mc12_8TeV.159020.ParticleGenerator_gamma_Et7to80.merge.AOD.e1173_s1479_s1470_r3586_r3549.120824140852/


conv_path = os.path.expandvars('$ROOTCOREDIR/data/egammaAnalysisUtils/conversion.root')
conv_tool = ROOT.ConvertedPhotonScaleTool(conv_path)

def compute_correction(tree):
    eta = tree.ph_cl_eta
    energy = tree.ph_cl_E
    radius = tree.ph_Rconv
    if type(eta) == ROOT.vector("float"):
        result = []
        for i in range(eta.size()):
            if radius[i] <= 0: # TODO: better
                result.append(1)
            else:
                result.append(conv_tool.Scale(eta[i], energy[i], radius[i]))
        return result
    else:
        if radius <= 0: # TODO: better
            return 1.
        else:
            return conv_tool.Scale(eta, energy, radius)

def fudge_one_event(isflat, tune, **kwargs):
    if isflat:
        return fudge_one_particle(tune, kwargs)
    else:
        results = {}
        for k in kwargs:
            results[k] = ROOT.vector("float")()
        newkwargs = {}
        for i in range(kwargs["pt"].size()):
            for k in kwargs:
                newkwargs[k] = kwargs[k][i]
            fudged = fudge_one_particle(tune, **newkwargs)
            for k,v in fudged.iteritems():
                results[k].push_back(v)
    return results

def fudge_one_particle(tune, **kwargs):
    kwargs["reta"]   = fudge_mc_tool.Fudge_Reta(kwargs["reta"],   kwargs["pt"], kwargs["ph_etas2"], kwargs["conv"], tune)
    kwargs["rphi"]   = fudge_mc_tool.Fudge_Rphi(kwargs["rphi"],   kwargs["pt"], kwargs["ph_etas2"], kwargs["conv"], tune)
    kwargs["weta2"]  = fudge_mc_tool.Fudge_Weta2(kwargs["weta2"], kwargs["pt"], kwargs["ph_etas2"], kwargs["conv"], tune)
    kwargs["fside"]  = fudge_mc_tool.Fudge_Fside(kwargs["fside"], kwargs["pt"], kwargs["ph_etas2"], kwargs["conv"], tune)
    kwargs["wtot"]   = fudge_mc_tool.Fudge_Wtot(kwargs["wtot"],   kwargs["pt"], kwargs["ph_etas2"], kwargs["conv"], tune)
    kwargs["w1"]     = fudge_mc_tool.Fudge_W1(kwargs["w1"],       kwargs["pt"], kwargs["ph_etas2"], kwargs["conv"], tune)
    return kwargs

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-i", "--input", help="input directory")
    parser.add_option("-o", "--output", help="output directory")
    parser.add_option("-t", "--tree", help="tree name")
    parser.add_option("-f", "--fudge", action="store_true", default=False, help="fudge shower shapes")
    parser.add_option("--fudge-tune", default=13, help="tune, default=13")
    parser.add_option("--entries", type=int, help="number of entries to process (default: all)")
    
    (options, args) = parser.parse_args()

    if options.input is None:
        parser.error("input not given")
    if options.output is None:
        parser.error("output not given")
    if options.tree is None:
        parser.error("tree not given")
    
    input_filenames = glob(os.path.join(options.input, "*.root*"))

    if not input_filenames:
        print "no ROOT files found in directory", options.input
        exit()
    
    if not os.path.exists(options.output):
        os.makedirs(options.output)
    else:
        exit("directory %s already exist" % options.output)    



    for filename in input_filenames:
        print "patching file %s" % filename,
        f = ROOT.TFile(filename)
        tree = f.Get(options.tree)
        newfile = ROOT.TFile(os.path.join(options.output, os.path.basename(filename)), "RECREATE")
        newfile.cd()
        newtree = tree.CloneTree(0)


        # check if input is flat
        isflat = True
        tree.GetEntry(0)
        if type(tree.ph_cl_E) == ROOT.vector("float"):
            print "not flat"
            isflat = False
        
        unconv = 'unconvertedPhoton' in filename
        if not unconv:  
          # declare new variables
          if isflat:
              correction = array('f', [0])
              newtree.Branch("conv_correction", correction, "conv_correction/F")
          else:
              correction = ROOT.vector("float")()
              newtree.Branch("conv_correction", correction)


        entries = options.entries or tree.GetEntries()
        dot_step = int(entries / 10.)
        fudge_mc_tool = ROOT.FudgeMCTool(0,0,0, options.fudge_tune)
        fudge_mc_tool.SetPreselection(options.fudge_tune)
        for i in xrange(entries):
            if (i % dot_step) == 0:
                print ".",
                sys.stdout.flush()
            tree.GetEntry(i)
            if not unconv:
              if isflat:
                  correction[0] = compute_correction(tree)
              else:
                  correction.clear()
                  for i in compute_correction(tree):
                      correction.push_back(i)

            if options.fudge:
                if isflat:
                    pt = tree.ph_cl_E / cosh(tree.ph_cl_eta)
                else:
                    pt = ROOT.vector("float")()
                    for i in range(tree.ph_cl_E.size()):
                        pt.push_back(tree.ph_cl_E[i] / cosh(tree.ph_cl_eta[i]))
                                     

                new_shw = fudge_one_event(isflat,
                                          tune = options.fudge_tune,
                                          pt = pt,
                                          ph_etas2 = tree.ph_etas2,
                                          conv = tree.ph_isConv,
                                          e277 = tree.ph_E277,
                                          reta = tree.ph_reta,
                                          rphi = tree.ph_rphi,
                                          weta2 = tree.ph_weta2,
                                          f1 = tree.ph_f1,
                                          fside = tree.ph_fside,
                                          wtot = tree.ph_wstot,
                                          w1 = tree.ph_ws3)
                
                if isflat:
                    tree.ph_E277 = new_shw["e277"]
                    tree.ph_reta = new_shw["reta"]
                    tree.ph_rphi = new_shw["rphi"]
                    tree.ph_weta2 = new_shw["weta2"]
                    tree.ph_f1 = new_shw["f1"]
                    tree.ph_fside = new_shw["fside"]
                    tree.ph_wstot = new_shw["wtot"]
                    tree.ph_ws3 = new_shw["w1"]
                else:
                    for i in range(tree.ph_cl_E.size()):
                        tree.ph_E277[i] = new_shw["e277"][i]
                        tree.ph_reta[i] = new_shw["reta"][i]
                        tree.ph_rphi[i] = new_shw["rphi"][i]
                        tree.ph_weta2[i] = new_shw["weta2"][i]
                        tree.ph_f1[i] = new_shw["f1"][i]
                        tree.ph_fside[i] = new_shw["fside"][i]
                        tree.ph_wstot[i] = new_shw["wtot"][i]
                        tree.ph_ws3[i] = new_shw["w1"][i]
            
            
            newtree.Fill()
        print "writing"
        newtree.Write()
        
        f.Close()

