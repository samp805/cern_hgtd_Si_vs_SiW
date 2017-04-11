import sys
sys.path += ["../python"]

import numpy as np
import ROOT
import RootTools
import performance
import Estimators as E
from performanceTools import BinningDescription

import unittest

class TestBinner(unittest.TestCase):
    def test_name_title(self):
        binner = BinningDescription(binnings=((0., 0.6, 1.4, 2.5), (10, 20, 30)),
                                   axis_names=['ph_cl_eta', 'ph_cl_E'])
        self.assertTupleEqual(binner.axis_titles, binner.axis_names)
    def test_get_range(self):
        binner = BinningDescription(binnings=((0., 0.6, 1.4, 2.5), (10, 20, 30)),
                                    axis_names=['ph_cl_eta', 'ph_cl_E'])
        self.assertTupleEqual(binner.get_range(0, 0), (-np.inf, 0.))
        self.assertTupleEqual(binner.get_range(0, 1), (0, 0.6))
        self.assertTupleEqual(binner.get_range(0, 2), (0.6, 1.4))
        self.assertTupleEqual(binner.get_range(1, 2), (20, 30))
        self.assertTupleEqual(binner.get_range(1, 3), (30, np.inf))
        self.assertTupleEqual(binner.get_range("ph_cl_E", 3), (30, np.inf))
        self.assertTupleEqual(binner.get_range("ph_cl_eta", 0), (-np.inf, 0.))
    def test_get_range2(self):
        binner = BinningDescription(binnings=((0., 0.6, 1.4, 2.5), (10, 20, 30)),
                                    axis_names=['ph_cl_eta', 'ph_cl_E'])
        self.assertTupleEqual(binner.get_range(0, None, inclusive_range=True), (0, 2.5))
        self.assertTupleEqual(binner.get_range(0, (1,2)), (0, 1.4)) # TODO: is this what we want?
        self.assertTupleEqual(binner.get_range(0, (0,2)), (-np.inf, 1.4))
        self.assertTupleEqual(binner.get_range(0, (0,5)), (-np.inf, np.inf))
        self.assertTupleEqual(binner.get_range("ph_cl_eta", (0,5)), (-np.inf, np.inf))
    def test_sub1(self):
        binner = BinningDescription(binnings=((0., 0.6, 1.4, 2.5), (10, 20, 30)),
                                    axis_names=['ph_cl_eta', 'ph_cl_E'])
        sub = binner.subBinningDescriptionFromAxis(('ph_cl_eta',))
        l = list(sub)
        self.assertEqual(sub.dim(),1)
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0]["name"], "ph_cl_eta")
        self.assertEqual(l[0]["title"], "ph_cl_eta")
        np.testing.assert_allclose(l[0]["binning"], [ 0. ,  0.6,  1.4,  2.5])
    def test_sub2(self):
        binner = BinningDescription(binnings=((0., 0.6, 1.4, 2.5), (10, 20, 30)),
                                    axis_names=['ph_cl_eta', 'ph_cl_E'])
        sub = binner.subBinningDescriptionFromAxis(())
        l = list(sub)
        self.assertEqual(sub.dim(), 0)
        self.assertEqual(len(l), 0)
        

class Test1D(unittest.TestCase):
    def setUp(self):
        self.data = np.random.random(1e4) # the main variable (the linearity)
        self.weights = None

        # the variable to be binned (eta, between 0 and 2.5 with 5 bins)
        self.nbins = 5
        self.binVarName = ("eta",)
        self.binnings = (dict(min=0, max=2.5, nbins=self.nbins), )
        self.fixed_binnings = map(RootTools.binning2array, self.binnings)
        variables = [np.random.uniform(bin[0], bin[-1], len(self.data)) for bin in self.fixed_binnings]

        self.bins = [np.digitize(variable, bin) for variable, bin in zip(variables, self.fixed_binnings)] 

        self.histoBinning = np.arange(0, 1.01, 0.1)
        self.dataVarName = "linearity"
        self.estimators = map(np.vectorize, [E.mean])

        self.P = performance.PerformanceWorker(self.data, self.weights, self.bins, self.estimators, self.binnings, self.dataVarName, self.binVarName, self.histoBinning)
        old = np.seterr(all="ignore")
        self.test_means = [np.mean(self.data[self.bins[0]==i]) for i in range(self.nbins+2)]
        self.test_lengths = [len(self.data[self.bins[0]==i]) for i in range(self.nbins+2)]
        np.seterr(**old)

        
    def test_values(self):
        values_result, errors_result = self.P.values.values()[0]
        # test the mean from the values
        self.assertTrue(np.allclose(np.nan_to_num(self.test_means), np.nan_to_num(values_result)))

    def test_histos(self):
        # test the number of entries for each bin
        self.assertTrue((self.test_lengths == [h.GetEntries() for h in self.P.histograms]))
        # test the mean from the histograms for every bin
        np.testing.assert_allclose(np.nan_to_num(self.test_means), [h.GetMean() for h in self.P.histograms])
        
    def test_graphs(self):
        graph = self.P.graphs.values()[0][0]
        x_values = [graph.GetX()[i] for i in range(graph.GetN())]
        y_values = [graph.GetY()[i] for i in range(graph.GetN())]
        np.testing.assert_allclose(y_values, self.test_means[1:-1])
        np.testing.assert_allclose(x_values, (np.array(self.fixed_binnings[0])[1:] + np.array(self.fixed_binnings[0])[:-1]) / 2.)

# class TestInclusiveWorker(unittest.TestCase):
#     def setUp(self):
#         self.data = np.random.random(1e4) # the main variable (the linearity)
#         self.data = np.array([self.data])
# 
#         # the variable to be binned (eta, between 0 and 2.5 with 5 bins)
#         self.binVarName = []
#         self.binnings = np.array([])
#         self.bins = None
# 
#         self.histoBinning = np.arange(0, 1.01, 0.1)
#         self.dataVarName = "linearity"
#         self.estimators = map(np.vectorize, [E.mean])
# 
#         self.P = performance.PerformanceWorker(self.data, self.bins, self.estimators, self.binnings, self.dataVarName, [], self.histoBinning)
#         old = np.seterr(all="ignore")
#         self.test_means = [np.mean(self.data[self.bins[0]==i]) for i in range(self.nbins+2)]
#         self.test_lengths = [len(self.data[self.bins[0]==i]) for i in range(self.nbins+2)]
#         np.seterr(**old)
# 
#         
#     def test_values(self):
#         values_result, errors_result = self.P.values.values()[0]
#         # test the mean from the values
#         self.assertTrue(np.allclose(np.nan_to_num(self.test_means), np.nan_to_num(values_result)))
# 
#     def test_histos(self):
#         # test the number of entries for each bin
#         self.assertTrue((self.test_lengths == [h.GetEntries() for h in self.P.histograms]))
#         # test the mean from the histograms for every bin
#         np.testing.assert_allclose(np.nan_to_num(self.test_means), [h.GetMean() for h in self.P.histograms])


if __name__ == "__main__":
    unittest.main()
