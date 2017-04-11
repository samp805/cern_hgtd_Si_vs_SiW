#!/usr/bin/env python

try:
    import colorer
except ImportError:
    print "mmm... you don't have the colorer module, well... no colors for you"
import logging
import numpy as np
import scipy
# from scipy.optimize import minimize_scalar # only in scipy 0.11
from functools import wraps
import ROOT


def resample(data):
    return np.random.choice(data, len(data))


def bootstrap(data, estimator, repetitions=100):
    results = []
    for i in xrange(repetitions):
        new_data = resample(data)
        result = estimator(new_data)
        results.append(result)
    return np.rms(results)

use_bootstrap = False


def errorize(f):
    """
    use this decorator when defining function on data (the mean, the rms, the guassian fit), ...
    to be sure that the output has 2 arguments: the value and the error as a tuple
    if the output is not a tuple of two object, with this decorator the function will
    return (value, 0)
    """
    @wraps(f)  # wraps decorator is needed to preserve function name
    def function(*args, **kwargs):
        result = f(*args, **kwargs)
        if isinstance(result, (list, tuple)) and len(result) == 2:
            if type(result[1]) is not float:
                result = result[0], float(result[1])
            if type(result[0]) is not float:
                result = float(result[0]), result[1]
            return result
        else:
            if use_bootstrap:
                return result, bootstrap(args[0], f)
            else:
                return (result, 0.)
    return function


class caller:
  """Wrapper class to call a function with default arguments, e.g.:
  x = caller( quantiles, prob=[0.25])
  x(data, None) # equivalent to quantiles(data, None, prob=[0.25])
  Special argument __name__ might be passed to set the function name
  """
  def __init__(self, fcn, *args, **kw):
    self.__name__ = kw.pop('__name__', fcn.__name__)
    self.__doc__ = fcn.__doc__
    self.fcn = fcn
    self.args = args
    self.kw = kw

  def __call__(self, *args, **kw):
    return self.fcn(*self.args+args, **dict(self.kw, **kw) )


@errorize
def mean(data, w=None):
    "mean(data, w = None)"
    old_option = np.seterr(all='raise')
    N = len(data)
    if not N:
        np.seterr(**old_option)
        return np.nan, 0.
    if w is not None:
        value, sumW = np.average(data, weights=w, returned=True)
        N = 1. * sumW ** 2 / (w ** 2).sum()  # effective entries
    else:
      try:
          value = np.mean(data)
      except FloatingPointError:
          np.seterr(**old_option)
          if len(data) == 0:
              np.seterr(**old_option)
              return np.nan, 0.
          else:
              logging.error("problem computing mean for data: %s", data)
              raise
    np.seterr(**old_option)
    if np.isnan(value):
        return np.nan, 0.
    return value, rms(data, w)[0] / np.sqrt(N)


@errorize
def rms(data, w=None):
    "rms(data, w=None)"
    N = len(data)
    if N < 3:
        return np.nan
    if w is None:
        std = np.std(data)
    else:
        mean, sumW = np.average(data, weights=w, returned=True)
        mean2 = np.average(data ** 2, weights=w)
        std = np.sqrt(mean2 - mean ** 2)
        N = 1. * sumW ** 2 / (w ** 2).sum()  # effective entries
    return std, std / np.sqrt(2 * N)


@errorize
def stat(data, w=None):
    "stat(data, w=None)"
    try:
        result = len(data)
    except TypeError:
        result = sum(1 for _ in data)
    return result, np.sqrt(result)


@errorize
def sumw(data, w=None):
    "sumw(data, w=None)"
    if w is None:
        return stat(data)
    return np.sum(w), np.sqrt(np.square(w).sum())


@errorize
def median(data, w=None):
    "median(data, w=None)"
    if len(data) == 0:
        return np.nan
    if w is None:
        return np.median(data), np.std(data) / np.sqrt(len(data)) * 1.253
    # Find the point that divides the sum of weights in 2
    sort_index = np.argsort(data)
    wSum = np.cumsum(w[sort_index])
    m = 0.5 * wSum[-1]  # sum of weights / 2
    N = 1. * wSum[-1] ** 2 / (w ** 2).sum()  # effective entries
    for i, j in enumerate(wSum):
        if j > m:
            med = 0.5 * (data[sort_index[i]] + data[sort_index[i-1]])
            return med, rms(data, w)[0] / np.sqrt(N) * 1.253


@errorize
def skew(data, w=None):
    "skew(data, w=None)"
    n = len(data)
    if not n:
        return np.nan, 0.
    skew_error = 0
    if n > 8:
        skew_error = np.sqrt(6.*n*(n-1) / (n-2) / (n+1) / (n+3))
    try:
        from scipy.stats import skew as scipy_skew
    except ImportError:
        mean = np.mean(data)
        try:
            return ( np.sum((data - mean)**3) / n ) / ( np.power(( np.sum((data - mean)**2) / n ), 3./2.) ), skew_error
        except FloatingPointError:
            return np.nan
    else:
        return scipy_skew(data), skew_error


def get_truncated_data_OLD(data, w=None, fraction=0.9):
    if type(data) != np.ndarray:
        data = np.array(data)
    smallest_interval = smallestInterval(data, w, fraction)
    if smallest_interval is None:
        return [], None
    indices = np.logical_and(data > smallest_interval[0], data < smallest_interval[1])
    if w is None:
        return data[indices], None
    return data[indices], w[indices]

# FIXME: this is not correct for weighted data
def get_truncated_data(data, w=None, integral=0.9):
    if type(data) is not np.ndarray:
        data = np.array(data)
    index_sorted = np.argsort(data)
    xsorted = data[index_sorted]
    N = len(data)
    D = np.floor(integral * N)
    if D == 0:
        logging.warning("not enought statistics (%d) to compute smallestInterval, data: %s", len(data), str(data))
        return None
    first_index = (xsorted[D:] - xsorted[:-D]).argmin()
    if w is None:
        return xsorted[first_index:D + first_index], None
    else:
        return xsorted[first_index:D + first_index], w[index_sorted[first_index:D + first_index]]


def get_truncated_data_simmetric(data, w=None, fraction=0.9):
    if type(data) != np.ndarray:
        data = np.array(data)
    ordered_indices = data.argsort()
    start = int((1 - fraction) / 2. * len(data))
    end = int((1 + fraction) / 2. * len(data))
    selected_indices = ordered_indices[start:end]
    if w is None:
        return data[selected_indices], None
    else:
        return data[selected_indices], data[selected_indices]


def get_winsorized_data(data, w=None, fraction=0.9):
    if type(data) != np.ndarray:
        data = np.array(data)
    smallest_interval = smallestInterval(data, w, fraction)
    if smallest_interval is None:
        return [], None
    return np.clip(data, smallest_interval[0], smallest_interval[1])


@errorize
def winsorized_rms(data, w=None, fraction=0.9):
    newdata = get_winsorized_data(data, w, fraction)
    return rms(newdata, w)


@errorize
def truncated_mean(data, w=None, fraction=0.9):
    "truncated_mean(data, w=None, fraction=0.9)"
    r = get_truncated_data(data, w, fraction)
    if r is None:
        return np.nan
    newdata, w = r
    #    return mean(newdata, w)[0], winsorized_rms(data, w, fraction)[0] / (fraction * np.sqrt(len(data)))
    return mean(newdata, w)


@errorize
def truncated_mean20(data, w=None):
    return truncated_mean(data, w, 0.2)


@errorize
def truncated_mean10(data, w=None):
    return truncated_mean(data, w, 0.1)


@errorize
def truncated_rms(data, w=None, fraction=0.9):
    "truncated_rms(data, w=None, fraction=0.9)"
    r = get_truncated_data(data, w, fraction)
    if r is None:
        return np.nan, 0
    data, w = r
    return rms(data, w)


@errorize
def truncated_effective_rms(data, w=None, fraction=0.9):
    erfinv = scipy.special.erfinv
    ratio = np.sqrt(np.sqrt(np.pi)*fraction - 2 * np.exp(-pow(erfinv(fraction), 2))*erfinv(fraction))/pow(np.pi, 1./4.)
    r = truncated_rms(data, w, fraction)
    return r[0] / ratio, r[1] / ratio


@errorize
def truncated_median(data, w=None, fraction=0.9):
    "truncated_median(data, w=None, fraction=0.9)"
    data, w = get_truncated_data(data, w, fraction)
    return median(data, w)


@errorize
def truncated_rms_rel(data, w=None, fraction=0.9):
    "truncated_rms_rel(data, w=None, fraction=0.9)"
    rms, rmse = truncated_rms(data, w, fraction)
    m, me = truncated_mean(data, w, fraction)
    value = rms / m
    error = np.sqrt((rmse / rms) ** 2 + (me / m) ** 2) * value
    return value, error


@errorize
def truncated_skew(data, w=None, fraction=0.9):
    "truncated_skew(data, w=None, fraction=0.9)"
    data, w = get_truncated_data(data, w, fraction)
    return skew(data, w)


@errorize
def tail_one_sigma(data, w=None):
    mean = truncated_mean(data, w, fraction=0.2)
    rms = truncated_rms(data, w, fraction=0.9)
    cut = mean[0] - rms[0]
    try:
        tail = len(data[data < cut])
        return tail / float(len(data))
    except (ZeroDivisionError, FloatingPointError) as e:
        return np.nan


def get_CB_fit(data, w=None):
    m = np.min(data)
    M = np.max(data)
    x = ROOT.RooRealVar('x', 'x', m, M)
    # TODO: implement


# TODO: memoize this function
def get_gaussian_fit(data, w=None):
    "get_gaussian_fit(data, w=None) --> returns parameters and errors"
    if len(data) == 0:
        return None
    data = sorted(data)
    min_value = data[max(0, int(len(data) * 0.01))]
    max_value = data[min(int(len(data) * 0.98) - 1, len(data) - 1)]
    nbins = max(20, len(data) / 100)
    histo = ROOT.TH1F("histofit", "histofit", nbins, min_value, max_value)
    if w is not None:
      map(histo.Fill, data, w)
    else:
      map(histo.Fill, data)
    center = histo.GetMean()
    sigma = histo.GetRMS()

    fitmin = sigma * (-3) + center
    fitmax = sigma * (+2) + center

    fitsf1 = ROOT.TF1("gaus", "gaus", fitmin, fitmax)

    for i in range(6):
        histo.Fit(fitsf1, "0Q", "", fitmin, fitmax)
        center = fitsf1.GetParameter(1)
        sigma = fitsf1.GetParameter(2)
        fitmin = sigma * (-1.) + center
        fitmax = sigma * (+2.5) + center

    if fitsf1 is None:
        return None
    return [fitsf1.GetParameter(i) for i in (0, 1, 2)], [fitsf1.GetParError(i) for i in (0, 1, 2)]


def convoluted_gaussian(data, w=None):
    "convoluted_gaussian(data, w=None)"
    if len(data) == 0: return None
    data = sorted(data)
    min_value = data[max(0, int(len(data) * 0.01)) ]
    max_value = data[min(int(len(data) * 0.98) - 1, len(data)-1)]
    nbins = max(20, len(data) / 100)
    histo = ROOT.TH1F("histofit", "histofit", nbins, min_value, max_value)
    if w is not None:
        map(histo.Fill, data, w)
    else:
        map(histo.Fill, data)
    center = histo.GetMean()
    sigma = histo.GetRMS()
    fitmin = sigma * (-3) + center
    fitmax = sigma * (+2) + center
    fitsf1 = ROOT.TF1("fitfg","[3]*( ( exp( ([1]*[1] + 2*[0]*[2]*x)/(2*[0]*[0]*[2]*[2])) * (-1 + sqrt(1/([1]*[1]))*[1]+ TMath::Erfc(([1]*[1] + [0] * [2] * ((-1)*[0] + x))/(sqrt(2) * [0] * [1] * [2]))))/(2*(-1 + exp(1/[2]) ) * [2] ) )", fitmin, fitmax)
    fitsf1.SetParameter(0, 1)
    fitsf1.SetParameter(1, 0.005)
    fitsf1.SetParameter(2, 0.003)
    fitsf1.SetParameter(3, 6.5)
    histo.Fit(fitsf1, "0Q", "", fitmin, fitmax)

    if fitsf1 is None: return None
    return [fitsf1.GetParameter(i) for i in (0,1,2)], [fitsf1.GetParError(i) for i in (0,1,2)]


@errorize
def peak_convolution(data, w=None):
    "peak_convolution(data, w=None)"
    try:
        result = convoluted_gaussian(data, w)
        if not result: return None
        (peak, sigma, tau), (peak_err, sigma_err, tau_err) = result
        return peak, peak_err
    except FloatingPointError:
        return np.nan


@errorize
def sigma_convolution(data, w=None):
    "sigma_convolution(data, w=None)"
    try:
        result = convoluted_gaussian(data, w)
        if not result: return None
        (peak, sigma, tau), (peak_err, sigma_err, tau_err) = result
        return sigma, sigma_err
    except FloatingPointError:
        return np.nan


@errorize
def tau_convolution(data, w=None):
    "tau_convolution(data, w=None)"
    try:
        result = convoluted_gaussian(data, w)
        if not result: return None
        (peak, sigma, tau), (peak_err, sigma_err, tau_err) = result
        return tau, tau_err
    except FloatingPointError:
        return np.nan


@errorize
def peak_gaussian(data, w=None):
    "peak_gaussian(data, w=None)"
    gaussian_fit = get_gaussian_fit(data, w)
    if gaussian_fit is None: return np.nan
    fit_parameters, fit_parameter_errors = gaussian_fit
    return fit_parameters[1], fit_parameter_errors[1]


@errorize
def peak_gaussian_minus_one_over_interquartileEff(data, w=None):
    peak, err_peak = peak_gaussian(data, w)
    width, err_width = interquartileEff(data, w)
    if width == 0:
        return 0
    return (peak - 1) / width


@errorize
def width_gaussian(data, w=None):
    "width_gaussian(data, w=None)"
    try:
        fit_parameters, fit_parameter_errors = get_gaussian_fit(data, w)
    except TypeError:
        return np.nan
    return fit_parameters[2], fit_parameter_errors[2]


def smallestInterval(data, w=None, integral=0.9):
    """smallestInterval(data, w = none, integral = 0.9) -->
      return the endpoints of the smallest interval
      that contains the given integral (90%) using weights w if given"""
    N = len(data)
    if not N:
       return None
    if w is not None:
        return min(endpointsForFraction(data, w, integral), key = lambda x: x[1] - x[0])
    xsorted = np.sort(data)
    D = np.floor(integral * N)
    if D == 0:
        logging.warning("not enought statistics (%d) to compute smallestInterval, data: %s", len(data), str(data))
        return None
    first_index = (xsorted[D:] - xsorted[:-D]).argmin()
    return xsorted[first_index], xsorted[D + first_index]


@errorize
def width_smallest_interval(data, w=None, integral=0.9):
    "width_smallest_interval(data, w=None, integral=0.9)"
    si = smallestInterval(data, w, integral)
    if si is None:
        return np.nan
    width = si[1] - si[0]
    return width


@errorize
def width_smallest_interval_eff(data, w=None, integral=0.9):
    """width_smallest_interval_eff(data, w=None, integral=0.9) -> 
       width_smallest_interval divided by the equivalent number of sigmas"""
    width = width_smallest_interval(data, w, integral)[0]
    # Divide by the number of sigmas (i.e 1 for 0.683, 2 for 0.954, ...)
    Nsigma = ROOT.TMath.ErfInverse(integral) * np.sqrt(2)
    width /= (2 * Nsigma)
    return width, width / np.sqrt(2 * np.floor(integral * len(data)) - 1)


@errorize
def width_smallest_interval_eff90(data, w=None):
    return width_smallest_interval_eff(data, 0.9)


@errorize
def width_smallest_interval_eff80(data, w=None):
    return width_smallest_interval_eff(data, 0.8)


def quantile(data, w, prob):
    "quantile(data, w, prob) -> return the quantiles for a (weighted) data array"
    if w is None:
        from scipy.stats.mstats import mquantiles
        return mquantiles(data, prob)
    else:
        # from https://github.com/nudomarinero/wquantiles/blob/master/weighted.py
        ind_sorted = np.argsort(data)
        sorted_data = data[ind_sorted]
        sorted_weights = w[ind_sorted]
        # Compute the auxiliary arrays
        Sn = np.cumsum(sorted_weights)
        # TODO: Check that the weights do not sum zero
        Pn = (Sn - 0.5 * sorted_weights) / np.sum(sorted_weights)
        return np.fromiter( (np.interp(i, Pn, sorted_data) for i in prob), dtype=float)

@errorize
def interquartile(data, w=None):
    "interquartile(data, w=None) -> interquartile range"
    N = len(data)
    if not N:
        return np.nan, 0.
    iqr = np.diff( quantile(data, w, [0.25, 0.75]) )
    if w is not None:
        N = 1. * w.sum() ** 2 / (w ** 2).sum()  # effective entries
    return iqr, 1.166 * iqr / np.sqrt(N)  # 1.166 = 1.573 / 1.349, http://stats.stackexchange.com/questions/110902/error-on-interquartile-range


@errorize
def interquartileEff(data, w=None):
    """interquartileEff(data, w=None) -> interquartile range divided by 1.349 
       (to convert to sigma for a gaussian)"""
    iqr = interquartile(data, w)
    return iqr[0] / 1.349, iqr[1] / 1.349


@errorize
def mad(data, w=None):
    med = np.median(data)
    return np.median(np.abs(data - med))


@errorize
def madEff(data, w=None):
    return mad(data, w)[0] * 1.4826


def endpointsForFraction(x, w=None, fraction=0.683, isSorted=False):
  """endpointsForFraction(x, w=None, fraction = 0.683) -->
  Return the endpoints of the intervals that contains at least the given fraction (68.3%)
  of events or weights w if given"""
  # Loop over the sorted values of x with two iterators: for each point x1 in x,
  # the 2nd iterator <it> stops when it reaches the requested fraction
  from itertools import izip
  if w is None:  # set all weights to 1 if not given
    w = [1 for i in x]
  I0 = fraction * sum(w)  # the total fraction
  assert fraction > 0, 'Invalid fraction'
  I = 0  # the fraction between x1 and x2
  if isSorted:
    sorted_values = izip(x, w)
  else:
    sorted_values = sorted(izip(x, w))
  it = iter(sorted_values)
  for x1, w1 in sorted_values:
    while I < I0:
      x2, w2 = it.next()
      I += w2
    yield x1, x2  # I --> yield the fraction for debugging
    I -= w1  # remove the last value for the next iteration


def _HSM(data):
    N = len(data)
    if N == 1:
        return data[0]
    elif N == 2:
        return 0.5 * (data[0] + data[1])
    elif N == 3:
        if abs(data[0] - data[1]) < abs(data[1] - data[2]):
            return 0.5 * (data[0] + data[1])
        else:
            return 0.5 * (data[1] + data[2])
    else:
        new_data = get_truncated_data(data, integral=0.5)[0]
        return _HSM(new_data)


@errorize
def HSM(data, w=None):
    """ Half Sample Mode """
    # see http://arxiv.org/pdf/math/0505419.pdf
    if len(data) == 0:
        return np.nan, 0.
    return _HSM(data)


@errorize
def modeHistogram(data, w=None):
    # experimental
    MINBINGOAL = 50  # minimum entries per bin
    if len(data) < MINBINGOAL:
        return np.nan, 0.
    a, b = smallestInterval(data, w, 0.9)
    data = data[(data >= a) & (data <= b)]

    if len(data) < MINBINGOAL:
        return np.nan, 0.
    minbin = int(np.round(len(data) / (len(data) / float(MINBINGOAL))))
    nbins = len(data) / minbin

    data = np.sort(data)
    edges = [data[i * minbin] for i in range(nbins)] + [data[-1]]
    histo, edges = np.histogram(data, edges)
    density = histo / np.diff(edges)
    idx_max = np.argmax(density)
    left, right = edges[idx_max], edges[idx_max + 1]
    ind = (data > left) & (data < right)
    data_in_bin = data[ind]
    if w is not None:
        w = w[ind]
    return mean(data_in_bin, w)[0], 0.5 * (right - left)


@errorize
def EPDFM(data, w=None):
    from scipy.optimize import brent
    # Empirical Probability Densitify Function Mode
    # http://arxiv.org/pdf/math/0505419.pdf
    # (a sort of kernel density function)
    if len(data) == 0:
        return np.nan
    rms = np.std(data, w)
    mad = madEff(data, w)[0]
    sigma = min(rms, mad)
    if sigma == 0:
        return np.nan
    n = len(data)
    h = 0.9 * sigma / n ** (1. / 5.)
    k = 1. / (n * h * np.sqrt(2 * np.pi))
    fun = lambda x: -k * np.sum(np.exp(-0.5 * ((x - data) / h) ** 2))
    res = brent(fun)
    return res
