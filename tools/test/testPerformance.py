import sys
sys.path += ["../python"]

import numpy, ROOT, RootTools, performance, Estimators as E
data = numpy.random.random(1e4)
from math import pi

def doTest(Ndim = 1):
  if Ndim == 1: # 1D case
    nbins = 30
    binnedData = numpy.array( map(numpy.random.random, numpy.random.poisson(1e4, nbins+2) ), dtype=object)
    binVarName = ("eta",)
    binning = (dict(min=0, max=2.5, nbins=nbins), )
  elif Ndim == 2: # 2D case
    binnedData = numpy.array( map(numpy.random.random, numpy.random.poisson(1e4, 7*8) ), dtype=object).reshape(7,8)
    binVarName = ("eta", "Et")
    binning = dict(min=0, max=2.5, nbins=5), [0,20,40,60,80,100,200]
  elif Ndim == 3: # 3D case
    binnedData = numpy.array( map(numpy.random.random, numpy.random.poisson(1e4, 7*8*5) ), dtype=object).reshape(7,8,5)
    binVarName = ("eta", "Et", "f3")
    binning = dict(min=0, max=2.5, nbins=5), [0,20,40,60,80,100,200], [0, 0.4, 0.8, 1.]
  elif Ndim == 4: # 4D case, uhhh
    binnedData = numpy.array( map(numpy.random.random, numpy.random.poisson(1e4, 7*8*5*4) ), dtype=object).reshape(7,8,5,4)
    binVarName = ("eta", "Et", "f3", "phi")
    binning = dict(min=0, max=2.5, nbins=5), [0,20,40,60,80,100,200], [0, 0.4, 0.8, 1.], [-pi, 0, pi]
  else:
    raise ValueError('Not implemented: D = %s' % Ndim)
  
  weights = None
  histoBinning = numpy.arange(0, 1.01, 0.1)
  dataVarName = "x"
  estimators = numpy.vectorize(E.mean), numpy.vectorize(E.rms)

  fixedBinning = map(RootTools.binning2array, binning)
  variables = [bin[0] + bin[-1] * numpy.random.random(len(data)) for bin in fixedBinning]
  bins = [numpy.digitize(variable, bin) for variable, bin in zip(variables, fixedBinning)] 
  
  P = performance.PerformanceWorker(data, weights, bins, estimators, binning, dataVarName, binVarName, histoBinning)
  return P


ROOT.gROOT.SetBatch()

from superimposer import SuperImposer
import logging
logging.basicConfig(level=logging.INFO)
P1 = doTest(2)
P2 = doTest(2)
values1, histograms1, graphs1, graphs2d1 = P1()
values2, histograms2, graphs2, graphs2d2 = P2()
print graphs1

histos_dict = {"worker1": histograms1, "worker2": histograms2}
graphs_dict = {}
for title, graphs in zip(("worker1", "worker2"), (graphs1, graphs2)):
  for k,v in graphs.iteritems():
    key = (title,) + k
    graphs_dict[key] = v
values_dict = {}
for title, values in zip(("worker1", "worker2"), (values1, values2)):
  for k,v in values.iteritems():
    key = (title,) + (k,)
    values_dict[key] = v

f = ROOT.TFile("test_output.root", "recreate")
print P1.bin_description
print graphs_dict
print values_dict
super_imposer = SuperImposer(P1.bin_description, "foo_quantity", f, values_dict, histos_dict, graphs_dict)
super_imposer.draw_values()
super_imposer.draw_histos()
super_imposer.draw_graphs()

## Test binning the data
# import performanceTools as pT
# bd = pT.binData2(data, fixedBinning, bins)
# 
# # vectorized version
# H = RootTools.RootHistoGetter(histoBinning)(binnedData)
# # non-vectorized version
# H = map(RootTools.RootHistoGetter(histoBinning), binnedData)
# 
# 
# 
# P.graphs[('Et', ('eta',), themean)][0].Print()
# # value
# pT.sliceUnderOverflows(P.values[themean][0])[:,0]
# # error
# pT.sliceUnderOverflows(P.values[themean][1])[:,0]
# 
# for i,j in enumerate(P.graphs.values()[0]):
#   j.SetLineColor(i+1)
# 
# mg = ROOT.TMultiGraph()
# map(mg.Add, P.graphs.values()[0])
# mg.Draw('APL')
# 
# 
# print timeit.Timer('ha = RootTools.RootHistoGetter(numpy.arange(0,1.01,10), filler=RootTools.fillHisto)(numpy.random.random(1e4))', 'import RootTools,numpy').timeit(100)
