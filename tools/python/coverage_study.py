import numpy as np
from scipy import stats
import scipy.optimize

from choice import choice # because of old numpy

def mean(data):
    return np.mean(data), np.std(data) / np.sqrt(len(data))

def resample(data):
    return choice(data, len(data))

def bootstrap(data, estimator, repetitions):
    results = []
    for i in xrange(repetitions):
        new_data = resample(data)
        result = estimator(new_data)[0]
        results.append(result)
    return results

def coverage(data_generator, estimator, repetitions, true):
    results = []
    errors = []
    for i in xrange(repetitions):
        data = data_generator()
        result, error = estimator(data)
        results.append(result)
        errors.append(error)
    results = np.array(results)
    errors = np.array(errors)
    return np.mean(results), np.std(results) / np.sqrt(len(results)), len(results[(results > (true - errors)) & (results < (true + errors))]) / float(len(results))

def data_generator(random_variable, size):
    def f():
        return random_variable.rvs(size)
    return f

import Estimators

def main():
#    random_variable = stats.uniform()
    random_variable = stats.norm(10, 2)

    data = random_variable.rvs(100)
    estimators = [(Estimators.skew, lambda rv: rv.stats('s')),
                  (Estimators.truncated_mean, lambda x: x.mean()),
                  (Estimators.modeHistogram, lambda rv: scipy.optimize.brent(lambda x: -rv.pdf(x))),
                  (Estimators.EPDFM, lambda rv: scipy.optimize.brent(lambda x: -rv.pdf(x))),
                  (Estimators.interquartile, lambda x: x.ppf(0.75) - x.ppf(0.25)),
                  (Estimators.HSM, lambda rv: scipy.optimize.brent(lambda x: -rv.pdf(x))),
                  (Estimators.median, lambda x: x.median()),
                  (Estimators.truncated_median, lambda x: x.median()),
                  (Estimators.madEff, lambda x: x.std()),
                  (Estimators.interquartileEff, lambda x: x.std()),
                  (Estimators.truncated_effective_rms, lambda x: x.std()),
                  (Estimators.mean, lambda x: x.mean()),
                  (Estimators.rms, lambda x: x.std()),
                  (Estimators.truncated_rms, lambda x: x.std()),
                  ]
    dg = data_generator(random_variable, 1000)
    for estimator, true in estimators:
        print "=" * 80
        print "Estimator: ", estimator.func_name
        result = bootstrap(data, estimator, repetitions=1000)
        print "error from bootstrap: ", np.std(result), "error from formula: ", estimator(data)[1]
        coverage_result = coverage(dg, estimator, 10000, true(random_variable))
        true_value = true(random_variable)
        print "average of estimator: %.4f +/- %.4f true value: %.4f" % (coverage_result[0], coverage_result[1], true_value),
        if true_value != 0.:
            print "bias: {0} ({1} %)".format(coverage_result[0] - true_value, (coverage_result[0] / true_value - 1. )* 100.)
        else:
            print "bias: {0}".format(coverage_result[0] - true_value)
        print "coverage: ", coverage_result[2], "coverage / 0.6827: ", coverage_result[2] / 0.6827
    
if __name__ == "__main__":
    main()
