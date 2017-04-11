#!/usr/bin/env python
__doc__ = "To compute the shower depth using raw energies"

from glob import glob
import os.path
import os
from array import array
import sys
from itertools import izip

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


try:
    ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")
except RuntimeError:
    print """you have to compile all the egammaMVACalib library first:
rc find_packages
rc compile
"""


def CorrectionGenerator(input_tree, branches):
    ""
    fcn = ROOT.egammaMVACalib.get_shower_depth
    entries = tree.GetEntries()
    for i in xrange(entries):
        if i % 10000 == 0:
            print i,
        input_tree.GetEntry(i)
        try:
            inputs = map(input_tree.__getattr__, branches)
        except AttributeError:
            yield None
        try:
            yield fcn(*inputs)
        except TypeError:
            yield [fcn(*i) for i in izip(*inputs)]


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-i", "--input", help="input directory with ROOT files")
    parser.add_option("-t", "--tree", help="tree name")

    (options, args) = parser.parse_args()

    input_filenames = glob(os.path.join(options.input, "*.root*"))
    if not input_filenames:
        print "ERROR: no files found"

    try:
        hasattr(ROOT.egammaMVACalib, 'get_shower_depth')
    except:
        raise AttributeError('You have to load egammaMVACalib package')

    for filename in input_filenames:
        print "patching file %s" % filename

        f = ROOT.TFile(filename, "update")
        tree = f.Get(options.tree)
        newtree = ROOT.TTree("showerDepthTree", "showerDepthTree")

        for prefix in 'el_', 'ph_':
            branches = [prefix + 'cl_eta'] + [prefix + 'rawcl_Es%d' % i for i in range(4)]
            if not all(tree.GetBranch(i) for i in branches):
                continue

            # Disable all branches but the needed ones
            tree.SetBranchStatus('*', 0)
            for br in branches:
                tree.SetBranchStatus(br, 1)

            # Create new branch, the same type as the old one
            branchName = prefix + 'rawcl_calibHitsShowerDepth'
            isVector = 'vector' in tree.GetLeaf(prefix + 'rawcl_Es0').GetTypeName()
            if isVector:
                showerDepth = ROOT.vector(float)()
                newtree.Branch(branchName, showerDepth)
            else:
                showerDepth = array('f', [0.])
                newtree.Branch(branchName, showerDepth, branchName + '/F')

            for value in CorrectionGenerator(tree, branches):
                if isVector:
                    showerDepth.clear()
                    map(showerDepth.push_back, value)
                else:
                    showerDepth[0] = value or -999.
                newtree.Fill()

        tree.SetBranchStatus('*', 1)
        tree.AddFriend(newtree)
        tree.Write("", ROOT.TObject.kOverwrite)
        if f.Get("showerDepthTree"):
            newtree.Write("", ROOT.TObject.kOverwrite)
        else:
            newtree.Write()
        f.Close()
