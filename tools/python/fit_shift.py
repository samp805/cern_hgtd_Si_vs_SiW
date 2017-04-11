#!/usr/bin/env python

# --> python fit_shift.py ~turra/public/electron_simple_etaPhiCalo.v10tmp_Eaccordion_bettershift/\*1.74\*.root\* TrainTree


import ROOT

# Workaroud to fix import keywork collision
ROOT.RooWorkspace.rfimport = getattr(ROOT.RooWorkspace, 'import')
# Workaround to fix threadlock issues with GUI
ROOT.PyConfig.StartGuiThread = False
# suppress ROOT command line, use python optparse
ROOT.PyConfig.IgnoreCommandLineOptions = True
import logging
logging.basicConfig(level=logging.INFO)
import re



def group_filenames_eta(filenames):
    regex = re.compile(r'MVACalib_(?P<particle>\w+)_Et(?P<Etrange>[\w\-\.]+)_eta(?P<etarange>[\w\-\.]+)_(?P<calibType>\w+)')
    result = { }
    logging.info('finding binning from %d files', len(filenames))
    for f in filenames:
        m = regex.search(f)
        if not m:
            raise ValueError('cannot understand %s', f)
        regex_result = m.groupdict()
        eta_range = tuple(map(float, regex_result['etarange'].split('-')))
        result.setdefault(eta_range, []).append(f)
    return result


def create_model(ws):
    ratio = ws.var('ratio')

    shift = ROOT.RooRealVar('shift', 'shift', 0, -1, 1)
    sigma_CB = ROOT.RooRealVar('sigma_CB', 'sigma_CB', 0.1, 0.001, 2)
    sigma_GA = ROOT.RooRealVar('sigma_GA', 'sigma_GA', 0.1, 0.001, 2)
    max_CB = ROOT.RooFormulaVar('max_CB', 'max_CB', '@0 + 1', ROOT.RooArgList(shift))
    alpha_CB1 = ROOT.RooRealVar('alpha_CB1', 'alpha_CB1', 2, 0.01, 5)
    alpha_CB2 = ROOT.RooRealVar('alpha_CB2', 'alpha_CB2', 2, 0.01, 5)
    n_CB = ROOT.RooRealVar('n_CB', 'n_CB', 10)
    n_CB.setConstant(True)
    CB1 = ROOT.RooCBShape('CB1', 'CB1', ratio, max_CB, sigma_CB, alpha_CB1, n_CB)
    inv_ratio = ROOT.RooFormulaVar('inv_ratio', 'inv_ratio', '2. * @0 - @1', ROOT.RooArgList(max_CB, ratio));
    CB2 = ROOT.RooCBShape('CB2', 'CB2', inv_ratio, max_CB, sigma_CB, alpha_CB2, n_CB)
    NOVO = ROOT.RooNovosibirsk('NOVO', 'NOVO', inv_ratio, max_CB, sigma_CB, alpha_CB1)
    BW = ROOT.RooBreitWigner('BW', 'BW', ratio, max_CB, sigma_CB)

    GA = ROOT.RooGaussian('GA', 'GA', ratio, max_CB, sigma_GA)
    f = ROOT.RooRealVar('f', 'f', 0.5, 0, 1)
    model = ROOT.RooAddPdf("model", "model", BW, CB1, f)
#    model = ROOT.RooAddPdf("model", "model", CB1, GA, f)
#    model = ROOT.RooAddPdf("model", "model", NOVO, GA, f)
#    model = ROOT.RooAddPdf("model", "model", CB1, CB2, f)

    ws.rfimport(model)


def autofit(ws): 
    model = ws.pdf('model')
    ratio = ws.var('ratio')
    ROOT.RooArgSet(ratio)
    generated_data = model.generate(ROOT.RooArgSet(ratio), 10000, ROOT.RooFit.Name('generated_dataset'))
    frame = ratio.frame()
    generated_data.plotOn(frame)
    canvas = ROOT.TCanvas()
    frame.Draw()
    canvas.SaveAs("c.png")


def single_fit(ws, data, name=""):
    model = ws.pdf('model')
    fit_result = model.fitTo(data, ROOT.RooFit.NumCPU(4), ROOT.RooFit.Hesse(False), ROOT.RooFit.Save())

    ratio = ws.var('ratio')
    frame = ratio.frame()
    data.plotOn(frame)
    model.plotOn(frame)
    canvas = ROOT.TCanvas()
    frame.Draw()
    canvas.SaveAs("cc_%s.png" % name)
    return fit_result

def fit_allenergies(ws, data):
    energy_bins = (0, 4E3, 7E3, 10E3, 15E3, 20E3, 30E3, 40E3, 50E3, 75E3, 100E3, 200E3)
    raw_pt = ws.var('raw_pt')
    print raw_pt

    graph_shift = ROOT.TGraph()

    for i in range(len(energy_bins) - 1):
        lo, hi = energy_bins[i], energy_bins[i + 1]
        logging.info('fitting for %f - %f', lo, hi)
        range_name = 'range_%f_%f' % (lo, hi)
        raw_pt.setRange(range_name, lo, hi)
        sub_data = data.reduce(ROOT.RooFit.CutRange(range_name))
        sub_data.SetName("sub_data%s" % range_name)
        fit_result = single_fit(ws, sub_data, range_name)
        shift = fit_result.floatParsFinal().find('shift').getVal()
        graph_shift.SetPoint(i, 0.5 * (lo + hi), shift)
    canvas = ROOT.TCanvas()
    graph_shift.Draw("APL")
    canvas.SaveAs("canvas_shift.png")
        

    
def main(inputs, treename):
    chain = ROOT.TChain(treename)
    chain.Add(inputs)
    if len(list(chain.GetListOfFiles())) == 0:
        logging.error('Cannot find any file from %s', str(inputs))

    file_partitioned = group_filenames_eta([f.GetTitle() for f in chain.GetListOfFiles()])
    logging.info('files partitioned: %s', file_partitioned)

    
    ws = ROOT.RooWorkspace('workspace')
    

    raw_energy = ROOT.RooRealVar('el_rawcl_Eacc', 'el_rawcl_Eacc', 0 , 1E20)
    cl_eta = ROOT.RooRealVar('el_cl_eta', 'el_cl_eta', -2.5, 2.5)  # TODO: check eta definition
    true_energy = ROOT.RooRealVar('el_truth_E', 'el_truth_E', 0, 1E20)
    MVA = ROOT.RooRealVar('BDTG', 'BDTG', 0, 1E20)
    ratio_formula = ROOT.RooFormulaVar('ratio', 'ratio', '@0 * @1 / @2', ROOT.RooArgList(raw_energy, MVA, true_energy))
    raw_pt_formula = ROOT.RooFormulaVar('raw_pt', 'raw_pt', '@0 / cosh(@1)', ROOT.RooArgList(raw_energy, cl_eta))

    for eta_range, files in file_partitioned.iteritems():
        logging.info('creating dataset for eta [%f, %f]', eta_range[0], eta_range[1])

        chain = ROOT.TChain(treename)
        for f in files:
            chain.Add(f)

        logging.info('found %d files', len(list(chain.GetListOfFiles())))

        eta_suffix = '%f-%f' % (eta_range[0], eta_range[1])
        dataset = ROOT.RooDataSet('data_%s' % eta_suffix,
                                  'data_%s' % eta_suffix,
                                  ROOT.RooArgSet(raw_energy, true_energy, MVA, cl_eta), ROOT.RooFit.Import(chain))
        logging.info('computing ratio')
        ratio = dataset.addColumn(ratio_formula)
        ratio.setMin(0.8)
        ratio.setMax(1.2)
        logging.info('computing raw-pt')
        raw_pt = dataset.addColumn(raw_pt_formula)
        raw_pt.setMin(0)
        raw_pt.setMax(4000E3)

        ws.rfimport(dataset)

    logging.info('dataset imported')

    create_model(ws)
    ws.Print()

    fit_allenergies(ws, ws.allData().front())

    ws.writeToFile('workspace.root')




if __name__ == '__main__':
    ROOT.PyConfig.IgnoreCommandLineOptions = True

    from optparse import OptionParser
    parser = OptionParser('%prog [options] <inputfiles> <treename>')
    doc = 'example: python fit_shift.py ~/public/electron_simple_etaPhiCalo.v10tmp_Eaccordion_bettershift/\*.root\* TrainTree'
    parser.description = doc

 

    (options, args) = parser.parse_args()

    print args

    main(inputs=args[0],
         treename=args[1])
