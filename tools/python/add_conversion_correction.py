import os, os.path, sys, RootTools
from glob import glob
from array import array

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


try:
    ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C+")
except RuntimeError:
    print """you have to compile all the libraries first:
cd ..
cd RootCore
./configure
cd scripts
source setup.sh
cd ../..
$ROOTCOREDIR/scripts/find_packages.sh
$ROOTCOREDIR/scripts/compile.sh
"""

def CorrectionGenerator(input_tree, tool=None,
                        ph_cl_eta = 'ph_cl_eta', ph_cl_E='ph_cl_E', ph_Rconv='ph_Rconv'):
    if tool is None:
        conv_path = os.path.expandvars('$ROOTCOREDIR/data/egammaAnalysisUtils/conversion.root')
        tool = ROOT.ConvertedPhotonScaleTool(conv_path)
    entries = tree.GetEntries()
    for i in xrange(entries):
        input_tree.GetEntry(i)
        try:
            eta = input_tree.__getattr__(ph_cl_eta)
            energy = input_tree.__getattr__(ph_cl_E)
            radius = input_tree.__getattr__(ph_Rconv)
        except AttributeError:
            radius = -1
        if radius <= 0:
            yield 1.
        else:
            yield conv_tool.Scale(eta, energy, radius)


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-i", "--input", help="input file or directory with ROOT files")
    parser.add_option("-t", "--tree", help="input tree name")
    parser.add_option("-o", "--output-file", 
      help="output file name (use input file if not given)")
    parser.add_option("--output-tree", default="convTree",
      help="output tree name (default: %default)")

    (options, args) = parser.parse_args()
    
    if os.path.isdir(options.input):
        input_filenames = glob(os.path.join(options.input, "*.root*") )
    else:
        input_filenames = [options.input]
    if not input_filenames:
        print "ERROR: no files found"
    
    conv_path = os.path.expandvars('$ROOTCOREDIR/data/egammaAnalysisUtils/conversion.root')
    conv_tool = ROOT.ConvertedPhotonScaleTool(conv_path)

    for filename in input_filenames:
        print "patching file %s" % filename
        
        f = ROOT.TFile.Open(filename, "update")
        tree = f.Get(options.tree)

        if options.output_file:
            fout = ROOT.TFile(options.output_file, 'update')
        newtree = ROOT.TTree(options.output_tree, options.output_tree)
        branchName = 'conv_correction'
        
        isVector = 'vector' in tree.GetLeaf('ph_cl_eta').GetTypeName()
        if isVector:
            correction = ROOT.vector(float)()
            newtree.Branch(branchName, correction)
        else:
            correction = array('f', [0.])
            newtree.Branch(branchName, correction, branchName + '/F')
        
        branches = 'ph_cl_eta', 'ph_cl_E', 'ph_Rconv'
        for value in RootTools.correctionGenerator(tree, conv_tool.Scale, branches, 1.):
            value = 1. if value < 0 else value
            if isVector:
                correction.clear()
                map(correction.push_back, value)
            else:
                correction[0] = value
            newtree.Fill()
        
        if not options.output_file:
            tree.AddFriend(newtree)
            tree.Write("", ROOT.TObject.kOverwrite)
            newtree.Write("", ROOT.TObject.kOverwrite)
        else:
            fout.cd()
            newtree.Write("", ROOT.TObject.kOverwrite)
            fout.Close()
        
        f.Close()
        
