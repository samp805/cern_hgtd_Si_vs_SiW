# python plot_shift2.py -r  /afs/cern.ch/user/b/blenzi/outputs/MVACalib/photon_newShowerDepth_etaPhiCalo_convR_convPtRatiosB_95.v10_Eaccordion/ -p convertedPhoton

#python plot_shift2.py -r /afs/cern.ch/user/b/blenzi/outputs/MVACalib/electron_newShowerDepth_etaPhiCalo_95.v10tmp_Eaccordion/ -p electron

from stat import S_ISREG, ST_CTIME, ST_MODE
import re
import os
import logging
import sys
import numpy as np
from itertools import tee, izip

import numpy as np

from array import array
import ROOT

logging.basicConfig(level=logging.INFO)

colors = [ ROOT.kRed,
           ROOT.kBlue,
           ROOT.kBlack,
           ROOT.kGreen,
           ROOT.kSpring + 7,
           ROOT.kYellow,
           ROOT.kOrange,
           ROOT.kCyan,
           ROOT.kTeal - 6,
           ROOT.kAzure + 2,
           ROOT.kMagenta + 3 ]

colors = colors + map(lambda x: x +3, colors)
           

def remove_zeros(graph):
    x = graph.GetX()
    y = graph.GetY()
    x.SetSize(graph.GetN())
    y.SetSize(graph.GetN())
    newx = []
    newy = []
    for x, y, in zip(x, y):
        if y != 0:
            newx.append(x)
            newy.append(y)
    newx = array('f', newx)
    newy = array('f', newy)
    newgraph = ROOT.TGraph(len(newx), newx, newy)
    newgraph.SetLineColor(graph.GetLineColor())
    newgraph.SetMarkerColor(graph.GetMarkerColor())
    return newgraph
        

def group_filenames_eta(filenames):
    regex = re.compile(r'MVACalib_(?P<particle>\w+)_Et(?P<Etrange>[0-9\-\.]+)_eta(?P<etarange>[0-9\-\.]+)_(?P<calibType>\w+)')
    result = { }
    logging.info('finding binning from %d files', len(filenames))
    for f in filenames:
        m = regex.search(f)
        if not m:
            raise ValueError('cannot understand %s', f)
        regex_result = m.groupdict()
        Et_range = tuple(map(float, regex_result['Etrange'].split('-')))
        eta_range = tuple(map(float, regex_result['etarange'].split('-')))
        result.setdefault(eta_range, {}).update({Et_range: f})
    return result


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


def plot_shift(root_file_grouped, particle):
    canvas_shift = ROOT.TCanvas()
    canvas_shift.mem = []
    canvas_shift_profile = ROOT.TCanvas()
    canvas_shift_profile.mem = []
    legend = ROOT.TLegend(0.26, 0.2, 0.89, 0.4)
    legend.SetNColumns(3)
    xbins = np.concatenate((np.arange(2, 20, 0.1),  np.arange(20, 50, 0.5), np.arange(50, 300, 2), np.arange(300, 3500, 50)))
    xbins = array('d', list(xbins))
    iters = list(root_file_grouped.iteritems())
    iters = sorted(iters, key=lambda x: x[0])
    for i, (eta, g) in enumerate(iters):
        if eta[0] < 1.54 < eta[1]: # skip the crack
            continue
        chain_eta = ROOT.TChain("TrainTree")
        logging.info("plotting weight for eta bin (%f, %f)", *eta)
        for etraw, r in g.iteritems():
            chain_eta.Add(r)
#        chain_eta.SetProof()
        histo_name = "histo_shift_eta%s-%s" % eta
        histo = ROOT.TH2F(histo_name,  "(%s, %s)" % eta,
                          len(xbins) - 1, xbins, 1000, 0.9, 1.1)
        if particle == "electron":
            chain_eta.Draw("Mean10:(BDTG*(el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3)/cosh(el_cl_eta)/1e3)>>%s" % histo_name, "", "goff")
        else:
            chain_eta.Draw("Mean10:(BDTG*(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta)/1e3)>>%s" % histo_name, "", "goff")
        histo.SetMarkerColor(colors[i])
        histo.SetLineColor(colors[i])
        canvas_shift.cd()
        histo.GetXaxis().SetRangeUser(1, 3E3)
        histo.GetXaxis().SetTitle("p_{T} [GeV]")
        histo.GetYaxis().SetTitle("mean10")
        histo.Draw("same" if i != 0 else "")
        canvas_shift.mem.append(histo)
        legend.AddEntry(histo)

        profile = histo.ProfileX()
        profile.GetYaxis().SetRangeUser(0.9, 1.1)
        profile.GetXaxis().SetRangeUser(1, 3E3)
        profile.SetLineColor(colors[i])
        profile.SetLineWidth(2)
        graph = ROOT.TGraph(profile)
        canvas_shift_profile.cd()
        graph = remove_zeros(graph)
        graph.SetLineWidth(2)
        graph.GetXaxis().SetTitle("p_{T} [GeV]")
        graph.GetYaxis().SetTitle("mean10")
        graph.GetYaxis().SetLimits(0.95, 1.05)
        graph.GetYaxis().SetRangeUser(0.95, 1.05)
        graph.SetTitle("")
        graph.Draw("Lsame" if i != 0 else "AL")
        canvas_shift_profile.mem.append(graph)

    canvas_shift.cd()
    canvas_shift.SetLogx()
    legend.Draw()
    canvas_shift.SaveAs("weights.png")
    canvas_shift.Write()

    canvas_shift_profile.cd()
    canvas_shift_profile.SetLogx()
    legend.Draw()
    canvas_shift_profile.SaveAs("weights_profile.png")
    canvas_shift_profile.Write()


if __name__ == "__main__":
    ROOT.gROOT.SetBatch()

    ATLASSTYLEDIR = "."
    ROOT.gROOT.LoadMacro(ATLASSTYLEDIR + "/AtlasStyle.C")
    ROOT.gROOT.LoadMacro(ATLASSTYLEDIR + "/AtlasLabels.C")

    try:
#        ROOT.SetAtlasStyle()
        ROOT.ATLASLabel
    except AttributeError:
        logging.error("you must copy the AtlasStyle.{h,C} AtlasLabels.C from https://twiki.cern.ch/twiki/pub/AtlasProtected/PubComTemplates/atlasstyle-00-03-05.tar.gz to %s", ATLASSTYLEDIR)
        exit()
    ROOT.gStyle.SetMarkerSize(0.8)
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetNumberContours(256)
    ROOT.gStyle.SetOptTitle(1)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetLegendFillColor(0)


    from optparse import OptionParser

    parser = OptionParser(epilog='''example:
python plot_shift2.py -r  /afs/cern.ch/user/b/blenzi/outputs/MVACalib/photon_newShowerDepth_etaPhiCalo_convR_convPtRatiosB_95.v10_Eaccordion/ -p convertedPhoton''')
    parser.add_option("-r", "--root-directory",
                      help="directory with the associated ROOT files (TMVA outputs)")
    parser.add_option("-p", "--particle",
                      help="particle type (electron or unconvertedPhoton or convertedPhoton or convertedSiSi)", choices=["electron", "unconvertedPhoton", "convertedPhoton", "convertedSiSiPhoton"])
    (options, args) = parser.parse_args()


    output_file = ROOT.TFile("weights2.root", "recreate")

    logging.info("finding ROOT files")
    root_files = list_rootfiles(options.root_directory, options.particle)

    root_file_grouped = group_filenames_eta(root_files)
    
#    proof = ROOT.TProof.Open("")

    plot_shift(root_file_grouped, options.particle)


    for i, (eta, g) in enumerate(root_file_grouped.iteritems()):
        chain_eta = ROOT.TChain("TrainTree")
        logging.info("plotting distributions for eta bin (%f, %f)", *eta)
        for etraw, r in g.iteritems():
            chain_eta.Add(r)
        MVA_bins = [3, 5, 7, 10, 15, 20, 30, 50, 80]
        for ibin in range(len(MVA_bins) - 1):
            minE = MVA_bins[ibin]
            maxE = MVA_bins[ibin + 1]
            minbin, maxbin = 0.9, 1.1
            if minE < 15: minbin, maxbin = 0.7, 1.3
            if minE < 7: minbin, maxbin = 0.3, 1.7
            logging.info("plotting distribution for eta %s-%s, pt %s-%s", eta[0], eta[1], minE, maxE)
            canvas_name = "canvas_histo_pt%d-%d_eta%f-%f" % (minE, maxE, eta[0], eta[1])
            canvas = ROOT.TCanvas(canvas_name)
            legend = ROOT.TLegend(0.65, 0.55, 0.85, 0.85)
            if options.particle == "electron":
                selection = "BDTG*(el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3)/cosh(el_cl_eta) > %s && BDTG*(el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3)/cosh(el_cl_eta) < %s" % (minE*1000., maxE*1000.)
            else:
                selection = "BDTG*(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta) > %s && BDTG*(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/cosh(ph_cl_eta) < %s" % (minE*1000., maxE*1000.)

            histo_energy_name = "histo_pt_%d-%d_eta%f-%f" % (minE, maxE, eta[0], eta[1])
            histo_title = "|#eta|: [%.2f, %.2f]" % eta + "  E_{T}^{MVA}: [%.2f, %.2f] GeV" % (minE, maxE)
            histo_energy = ROOT.TH1F(histo_energy_name, histo_title, 100, minbin, maxbin)
            histo_energy.SetLineWidth(2)
            if options.particle == "electron":
                chain_eta.Draw("BDTG*(el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3)/el_truth_E>>%s" % histo_energy_name, selection, "goff")
            else:
                chain_eta.Draw("BDTG*(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/ph_truth_E>>%s" % histo_energy_name, selection, "goff")
            histo_energy.GetXaxis().SetTitle("E / E_{true}")
            histo_weight_name = "histo_weight_%d-%d_eta%f-%f" % (minE, maxE, eta[0], eta[1])
            histo_weight = ROOT.TH1F(histo_weight_name, histo_weight_name, 500, 0.9, 1.1)
            chain_eta.Draw("Mean10>>%s" % histo_weight_name, selection, "goff")
            histo_energystd_name = "histo_std_pt_%d-%d_eta%f-%f" % (minE, maxE, eta[0], eta[1])
            histo_energystd = ROOT.TH1F(histo_energystd_name, histo_title, 100, minbin, maxbin)
            histo_energystd.SetLineWidth(2)
            conv_correction = "conv_correction" if options.particle in ("convertedPhoton", "convertedSiSiPhoton") else 1
            if options.particle == "electron":
                chain_eta.Draw("el_cl_E/el_truth_E*%s>>%s" % (conv_correction, histo_energystd_name), selection, "goff")
            else:
                chain_eta.Draw("ph_cl_E/ph_truth_E*%s>>%s" % (conv_correction, histo_energystd_name), selection, "goff")
            histo_energyshifted_name = "histo_shifted_pt_%d-%d_eta%f-%f" % (minE, maxE, eta[0], eta[1])
            histo_energyshifted = ROOT.TH1F(histo_energyshifted_name, histo_title, 100, minbin, maxbin)
            if options.particle == "electron":
                chain_eta.Draw("BDTG*(el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3)/el_truth_E/Mean10>>%s" % histo_energyshifted_name, selection, "goff")
            else:
                chain_eta.Draw("BDTG*(ph_rawcl_Es1 + ph_rawcl_Es2 + ph_rawcl_Es3)/ph_truth_E/Mean10>>%s" % histo_energyshifted_name, selection, "goff")

            histo_energyshifted.SetLineWidth(2)

            histo_energy.SetLineColor(ROOT.kBlack)
            histo_weight.SetLineColor(ROOT.kBlue)
            histo_energystd.SetLineColor(ROOT.kRed)
            histo_energyshifted.SetLineColor(ROOT.kBlue)

            histo_energy.SetMarkerColor(ROOT.kBlack)
            histo_weight.SetMarkerColor(ROOT.kBlue)
            histo_energystd.SetMarkerColor(ROOT.kRed)
            histo_energyshifted.SetMarkerColor(ROOT.kBlue)

            legend.AddEntry(histo_energyshifted, "MVA")
            legend.AddEntry(histo_energy, "MVA no shift")
            legend.AddEntry(histo_energystd, "std")
#            legend.AddEntry(histo_weight, "weights")


            histo_energy.Draw()
            if histo_weight.GetMaximum() != 0:
                histo_weight.Scale(histo_energy.GetMaximum() / histo_weight.GetMaximum())
            mean_weight = histo_weight.GetMean()
            vline_weight = ROOT.TLine(mean_weight, 0, mean_weight, histo_energy.GetMaximum())
            vline_weight.SetLineWidth(2)
            vline_weight.SetLineColor(ROOT.kBlack)
#            histo_weight.Draw("same")
            histo_energystd.Draw("same")
            histo_energyshifted.Draw("same")
            canvas.Update()
            canvas.Modified()
            frame = canvas.GetFrame()
            vline = ROOT.TLine(1, canvas.GetUymin(), 1, canvas.GetUymax())
            vline.SetLineStyle(2)
            vline.Draw()
            vline_weight.Draw()
            canvas.vline = vline
            canvas.vline_weight = vline_weight

            legend.SetFillColor(0)
            legend.Draw()

            ROOT.ATLASLabel(0.15, 0.8, "Internal")
            latex_particle = ROOT.TLatex(0.15, 0.73, {"convertedPhoton": "converted photons",
                                                      "unconvertedPhoton": "unconverted photons",
                                                      "electron": "electron"}[options.particle])
            latex_particle.SetTextSizePixels(11)
            latex_particle.SetNDC()
            latex_particle.Draw()
            canvas.label = latex_particle


            canvas.SaveAs(canvas_name + ".png")
            canvas.Write()
            
