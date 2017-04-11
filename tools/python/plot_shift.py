from stat import S_ISREG, ST_CTIME, ST_MODE
import re
import os
import logging
import sys
import numpy as np
from itertools import tee, izip

from array import array
import ROOT

logging.basicConfig(level=logging.INFO)

def eval_formulas(tree, formulas, cut):
    entries = tree.GetEntries()
    values = { }
    formula_cut = ROOT.TTreeFormula("formula_cut", cut, tree)
    for i in xrange(entries):
        tree.GetEntry(i)
        if float(formula_cut.EvalInstance()) == 0: continue
        for k, v in formulas.iteritems():
            values.setdefault(k, []).append(float(v.EvalInstance()))
    for v in values:
        values[v] = np.array(values[v])
    for k,v in values.iteritems():
        if (len(np.unique(v)) != 1):
            logging.warning("more than one values for %s: %s, with cut: %s, returning the mean", k, np.unique(v), cut)
    for v in values:
        values[v] = np.mean(values[v])
    return values


def list_extfiles(dirpath, ext):
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    # leave only regular ext files
    entries = (path for path in entries if (S_ISREG(os.stat(path)[ST_MODE]) and os.path.splitext(path)[1] == ("." + ext)))
    return entries

def list_xmlfiles(dirpath, particle):
    full_list = list(list_extfiles(dirpath, "xml"))
    if len(full_list) == 0:
        logging.warning("cannon find any xml in %s", dirpath)
    particle_list = [filename for filename in full_list if (("_" + particle + "_") in filename)]
    return particle_list

def list_rootfiles(dirpath, particle):
    full_list = list_extfiles(dirpath, "root")
    particle_list = [filename for filename in full_list if (("_" + particle + "_") in filename)]
    return particle_list

def extract_info(xml_filename):
    import xml.etree.ElementTree as ET
    tree = ET.parse(xml_filename)
    elements = tree.findall("UserInfo/Info")
    result = {}
    for el in elements:
        v = dict(el.items())
        result[v['name']] = v['value']
    return result

def get_energy_histo(tree, particle, nbins=200, cut=""):
    histo = ROOT.TH1F("histo" + root_filename.replace("/", "_"), "energy / true energy", nbins, 0.7, 1.2)
    if particle == "electron":
        tree.Draw("BDTG*el_rawcl_Eacc/el_truth_E>>" + "histo" + root_filename.replace("/", "_"), cut, "GOFF")
    elif particle in ("unconvertedPhoton", "convertedPhoton", "convertedSiSiPhoton"):
        tree.Draw("BDTG*ph_rawcl_Eacc/ph_truth_E>>" + "histo" + root_filename.replace("/", "_"), cut, "GOFF")
    else:
        logging.error("particle not valid")
    histo.SetDirectory(0)
    return histo

        
if __name__ == "__main__":
    ROOT.gROOT.SetBatch()
    from optparse import OptionParser

    parser = OptionParser(epilog='''example:
plot_shift.py -d /afs/cern.ch/user/b/blenzi/outputs/MVACalib/electron_flatEt_simple_etaPhiCalo.v4low_95_Eaccordion/weights \
   -r /afs/cern.ch/user/b/blenzi/outputs/MVACalib/electron_flatEt_simple_etaPhiCalo.v4low_95_Eaccordion \
   -p electron --bin-formula "el_rawcl_Eacc/cosh(el_cl_eta)/1e3" --bin-values "0, 4, 8, 12, 16, 20"''')
    parser.add_option("-d", "--directory",
                      help="directory with xml files")
    parser.add_option("-r", "--root-directory",
                      help="directory with the associated ROOT files (TMVA outputs)")
    parser.add_option("-p", "--particle",
                      help="particle type (electron or unconvertedPhoton or convertedPhoton or convertedSiSi)", choices=["electron", "unconvertedPhoton", "convertedPhoton", "convertedSiSiPhoton"])
    parser.add_option("--binning", help="number of binning for the histograms", default=200)
    parser.add_option("--bin-formula", help="formula to define bins inside a file")
    parser.add_option("--bin-values", help="bin edge to define bins inside a file")
    (options, args) = parser.parse_args()

    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        return izip(a, b)
    
    pt_bins_lowE = []
    
    if options.bin_values is not None:
        pt_bins_lowE = list(pairwise(map(float, options.bin_values.split(','))))
    logging.info("bin formula: %s", str(options.bin_formula))
    logging.info("pt low E: %s", str(pt_bins_lowE))

    xml_files = list_xmlfiles(options.directory, options.particle)

    regex = re.compile(r"_Et(?P<Et1>[0-9\.]+)-(?P<Et2>[0-9\.]+)_eta(?P<eta1>[0-9\.]+)-(?P<eta2>[0-9\.]+)_")

    result = {}
    logging.info("reading")
    if len(xml_files)==0: logging.error("no xml files")
    for i,xml_filename in enumerate(xml_files):
        print ".",
        sys.stdout.flush()
        m = regex.search(xml_filename)
        if m is None:
            logging.error("fail on %s", xml_filename)
            continue

        meta_info = dict([(k,float(v)) for k,v in m.groupdict().iteritems()])
        logging.debug("Et: %.2f-%.2f, eta: %.2f-%.2f", *[meta_info[x] for x in ("Et1", "Et2", "eta1", "eta2")])
        info = extract_info(xml_filename)
        result[(meta_info["Et1"], meta_info["Et2"], meta_info["eta1"], meta_info["eta2"])] = info
    print
    logging.info("found %d xml files", (i+1))

    type_of_data = result.values()[0].keys()
    logging.info("shifts found (in the first file): %s", str(type_of_data))

    # looping over ROOT files
    if options.root_directory is not None:
        root_files = list_rootfiles(options.root_directory, options.particle)
        logging.info("adding ROOT files")
        for i,root_filename in enumerate(root_files, 1):
            print ".",
            sys.stdout.flush()
            m = regex.search(root_filename)
            if m is None:
                logging.error("fail on %s", root_filename)
                continue
            
            meta_info = dict([(k,float(v)) for k,v in m.groupdict().iteritems()])
            logging.debug("Et: %.2f-%.2f, eta: %.2f-%.2f", *[meta_info[x] for x in ("Et1", "Et2", "eta1", "eta2")])
            result[(meta_info["Et1"], meta_info["Et2"], meta_info["eta1"], meta_info["eta2"])].update({"root_filename": root_filename})
        logging.info("found %d ROOT files", i)

    output_file = ROOT.TFile("shift_histos_%s.root" % options.particle, "RECREATE")
    ROOT.gStyle.SetPaintTextFormat(".3f")
    
    logging.info("plotting")
    histos = dict([(t, ROOT.TH2Poly()) for t in type_of_data])
    graphs1D = {}
    for k,v in result.iteritems():
        print ".",
        sys.stdout.flush()
        eta_edges = (k[2], k[3])
        Et_edges =  (k[0], k[1])
        canvas_histo = ROOT.TCanvas()
        
        if "root_filename" in v:
            f = ROOT.TFile(v["root_filename"])
            tree = f.Get("TrainTree")
            canvas_histo.SetName("canvas_histo_%.2f-%.2f_%.2f-%.2f" % (eta_edges[0], eta_edges[1], Et_edges[0], Et_edges[1]))
            bins = []
            canvas_histo.mem = []
            legend = ROOT.TLegend(0.15, 0.7, 0.35, 0.9)
            formulas = {}
            all_float = True
            for kk,vv in v.iteritems():
                if kk in ("Median", "Peak", "Mean10", "Median10", "Mean20", "Median20", "Mean"):
                    formulas[kk] = ROOT.TTreeFormula("formula", vv, tree)
                    try:
                        float(str(vv))
                    except:
                        all_float = False
            if all_float:
                bins = ((Et_edges[0], Et_edges[1]),)
            else:
                if not pt_bins_lowE:
                    bins = ((Et_edges[0], Et_edges[1]),)
                else:
                    bins = [(a, b) for (a, b) in pt_bins_lowE if (a >= Et_edges[0] and b <= Et_edges[1])]
            # draw the histograms
            hstack = ROOT.THStack()
            legend_histos = ROOT.TLegend(0.15, 0.5, 0.35, 0.7)
            histo_energies = {}
            for ibin, (a, b) in enumerate(bins):
                cut_bin = "%s > %f && %s < %f" % (options.bin_formula, a, options.bin_formula, b)
                histo_energy = get_energy_histo(tree, options.particle, nbins=options.binning, cut=cut_bin)
                if histo_energy.GetEntries() == 0:
                    logging.warning("histo empty with cut %s from file %s", cut_bin, v["root_filename"])
                canvas_histo.mem.append(histo_energy)
                histo_energies[(a,b)] = histo_energy
                legend_histos.AddEntry(histo_energy, "(%.1f, %.1f) GeV" % (a, b))
                histo_energy.SetLineColor(ibin+1)
                hstack.Add(histo_energy)
            hstack.Draw("nostack")
            # draw lines
            for a,b in bins:
                cut_bin = "%s > %f && %s < %f" % (options.bin_formula, a, options.bin_formula, b)
                histo_energy = histo_energies[(a,b)]
                histo_energy.lines = {}
                if all_float:
                    for k, formula in formulas.iteritems():
                        histo_energy.lines[k] = float(str(formula.GetTitle()))
                else:
                    line_values = eval_formulas(tree, formulas, cut_bin)
                    for k, v in line_values.iteritems():
                        histo_energy.lines[k] = v

                for iline, (kk,vv) in enumerate(histo_energy.lines.iteritems()):
                    yupline = histo_energy.GetBinContent(histo_energy.FindBin(vv))
                    if yupline == 0:
                        yupline = canvas_histo.GetFrame().GetY2()
                    line = ROOT.TLine(vv, 0, vv, yupline)
                    line.SetLineColor(iline+1)
                    line.Draw()
                    if kk not in [ll.GetLabel() for ll in legend.GetListOfPrimitives()]:
                        legend.AddEntry(line, kk)
                    canvas_histo.mem.append(line)

                    ibin2d = histos[kk].AddBin(eta_edges[0], a, eta_edges[1], b)
                    histos[kk].SetBinContent(ibin2d, vv)
                    
                    graph1D = None
                    if (kk, eta_edges[0], eta_edges[1]) not in graphs1D:
                        graph1D = graphs1D[(kk, eta_edges[0], eta_edges[1])] = ROOT.TGraph()
                        graph1D.SetName("graph_%s_%f_%f" % (kk, eta_edges[0], eta_edges[1]))
                    else:
                        graph1D = graphs1D[(kk, eta_edges[0], eta_edges[1])]
                    graph1D.SetPoint(graph1D.GetN(), 0.5 * (a + b), vv)

            legend.Draw()
            legend_histos.Draw()
            output_file.cd()
            canvas_histo.Write()

    for title, histo in histos.iteritems():
        canvas = ROOT.TCanvas(title, title)
        histo.SetTitle(title)
        histo.SetName(title)
        histo.SetStats(0)
        histo.GetXaxis().SetTitle("|#eta|")
        histo.GetYaxis().SetTitle("E_{T}")
        histo.Draw("colztextbox")
        canvas.Write()

    for k, gr in graphs1D.iteritems():
        title = "%s_eta%f_%f" % k
        canvas = ROOT.TCanvas(title, title)
        gr.Draw("AP")
        gr.SetMarkerStyle(20)
        canvas.Write()




