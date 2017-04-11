import numpy as np
N, nbins1, nbins2 = 1e5, 50, 20

data = np.random.random(N)
binning = np.linspace(0, 2.5, nbins1+1), np.linspace(0, 120, nbins2+1)
bins = np.random.randint(0, nbins1+2, N),  np.random.randint(0, nbins2+2, N)

#import timeit, performanceTools as pT, test
# b = pT.binData2(test.data, test.binning, test.bins)
# Test 1D binning:
# b = pT.binData2(test.data, test.binning[:1], test.bins[:1])

#timeit.timeit('b = pT.binData1(test.data, test.binning, test.bins)', 'import performanceTools as pT, test', number=2)
#timeit.timeit('b = pT.binData2(test.data, test.binning, test.bins)', 'import performanceTools as pT, test', number=2)
#timeit.timeit('b = pT.binData1b(test.data, test.binning, test.bins)', 'import performanceTools as pT, test', number=2)
# [timeit.timeit('b = pT.binData%s(test.data, test.binning, test.bins)' % i, 'import performanceTools as pT, test', number=100) for i in range(1,4)]

