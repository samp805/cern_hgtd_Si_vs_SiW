import logging, itertools, RootTools, numpy as np
from itertools import imap
from performanceTools import binDataAndWeights as binData, \
  sliceUnderOverflows, getFcnName, getMidPoint, BinningDescription


class BasePerformance(object):
  def __init__(self, data, binning, dataVarName, binVarName, histoBinning, actions, histo_max_depth, values_max_depth):
    self.binning = binning # tuple or ndarray ?
    self.dataVarName = dataVarName # string
    self.binVarName = binVarName # list of strings
    self.histoBinning = histoBinning # list, array, ndarray or dict(min, max, bins)
    self.bin_description = BinningDescription(binning, binVarName)
    self.actions = actions
    self.histo_max_depth = histo_max_depth 
    self.values_max_depth = values_max_depth 


class PerformanceWorker(BasePerformance):
  """Creates histogram of a variable (e.g. E/Etrue) and calls PerformanceEstimators to 
  calculate and plot the dependence of the variable with some quantities
  (e.g. mean of E/Etrue vs eta)"""
  histoGetter = staticmethod(RootTools.RootHistoGetter) # BRUNO: Getter -> Builder
  graphGetter = staticmethod(RootTools.getGraph)
  graph2dGetter = staticmethod(RootTools.Root2DHistoGetter)
  
  def __init__(self, data, weights, bins, estimators, binning, dataVarName, binVarName, histoBinning, actions=[], histo_max_depth=1, values_max_depth=1, min_stat_bin=None, do2d=True, **kw):
    """
    data -- the data, flat iterable (or np.array for binned data if bins = None)
    weights -- weights, None or flat iterable (or np.array for binned data if bins = None)
    bins -- a list of bin index, the result of digitize for example
    estimators -- a list of vectorized functions
    binning -- the general binning, a list of items, every item
               should be an iterable like (0, 0.6, ...) or a dictionary
               with keys 'min', 'max' and 'nbins'
    binVarName -- the name of every axis of the binning as a tuple, for example
                  ('eta', 'ph_cl_E')
    histoBinning -- the binning for the axis of the histograms
    actions -- a list with the actions to execute with each variable 
    (0=plotting and binning, 1=binning, 2=plotting)
    histo-max-depth
    values-max-depth
    """
    
    super(PerformanceWorker, self).__init__(data, binning, dataVarName, binVarName, histoBinning, actions, histo_max_depth, values_max_depth)
#     logging.info("/".join(map(repr, (data, weights, binning, dataVarName, binVarName, histoBinning, actions, histo_max_depth, values_max_depth))))
    # Bin the data if needed
    binning = map(RootTools.binning2array, binning)
    if bins is not None:
      logging.info('Binning data (shape = %s, nbins = %s)', data.shape, [len(i)-1 for i in binning])
      binnedData, binnedWeights = binData(data, binning, bins, weights)
    elif data.dtype != object and len(data.shape) == 1: # no independent variable but wrong format
      binnedData = np.zeros(1, dtype=object)
      binnedData[0] = data
      binnedWeights = np.zeros(1, dtype=object)
      binnedWeights[0] = weights
    else: # data is already binned
      binnedData = data
      binnedWeights = weights
    logging.info("Shape of binnedData: %s. Type of first element: %s", binnedData.shape, type(binnedData.flat.next()))
    # TODO: No need to keep binned data ?
    self.binnedData = binnedData
    self.binnedWeights = binnedWeights
    self.values, self.histograms, self.graphs, self.graphs2d = self.run(binnedData, binnedWeights, estimators,
                                                                        binning, dataVarName,
                                                                        binVarName, histoBinning, min_stat_bin, do2d)
  
  def __call__(self):
    return self.values, self.histograms, self.graphs, self.graphs2d
  
  def run(self, binnedData, binnedWeights, estimators, binning, dataVarName, binVarName, histoBinning, min_stat_bin=None, do2d=True):
    
    Ndim = len(binning)
    # Create histograms of the variable, the result is a structure with the same
    # shape of the input binnedData
#     if not self.actions or not any(i in [1,2] for i in self.actions):
    if Ndim <= self.histo_max_depth: 
      try:
        histograms = np.vectorize(self.histoGetter(histoBinning))(binnedData, binnedWeights) # TODO: pass options to c-tor
      except ValueError:
        h = self.histoGetter(histoBinning)
        histograms = np.zeros(binnedData.shape, dtype=object)
        for indices,_ in np.ndenumerate(histograms):
          if binnedWeights is not None:
            histograms[indices] = h(binnedData[indices], binnedWeights[indices])
          else:
            histograms[indices] = h(binnedData[indices], None)
    else: 
      histograms = None
    
    # Calculate quantities (like mean, median, etc) and 
    # call graphers to plot the dependences
    graphs = {}
    graphs2d = {}
    
    logging.info('Getting values (including under/overflows)')
    values = { }
    if min_stat_bin is not None:
      mask_minstat = np.array([len(x) for x in binnedData]) < min_stat_bin
    for f in estimators:
      logging.debug('Getting values for %s', getFcnName(f))
      v = f(binnedData, binnedWeights)
      if min_stat_bin is not None:
        v[0][mask_minstat] = np.nan
        v[1][mask_minstat] = 0
      values[getFcnName(f)] = v

    logging.debug("got values for %s estimators", len(estimators))

    # TODO: Convert each binning to ndarray
    for f, (value, error) in values.iteritems():
      if Ndim == 0: # fully inclusive case, no graph
        break
      logging.info('Getting graphs for "%s"', f)
      # value (and error) is a ndarray and its shape corresponds to the the binning
      # + under / overflows.
      # e.g.: (4, 5) if binning (eta, Et) = (0, 1.4, 2.5), (0, 20, 40, 60)
      # Remove the under/overflows of all dimensions
      valueC = sliceUnderOverflows(value)
      errorC = sliceUnderOverflows(error)
      
      # get graphs by transforming the array in a 2D array
      # where the dimension we want to plot is the last one and the others are merged
      # (this is done in order to iterate easily over the array)
      # e.g. if shape = (2,3,5) becomes (15, 2) or (10, 3) or (6, 5)
      for axis in range(Ndim):
        # Skip the configuration if the action associated to variable used for plotting
        # (axis) is 1 (binning only) or if the action associated to any of the variables
        # used for binning is 2 (plotting only)
        if self.actions and self.actions[axis] == 1: 
          logging.info('Skipping plots vs. %s' % binVarName[axis])
          continue
        if self.actions and any(a == 2 and i != axis for i,a in enumerate(self.actions)):
          logging.info('Skipping plots...')
          continue
        if Ndim == 1:
          rolledShape = (1,)
        else:
          rolledShape = [j for i,j in enumerate(valueC.shape) if i != axis]
        ngraphs = np.prod(rolledShape)
        #print valueC.shape, ngraphs, rolledShape
        # np.rollaxis(value, axis=i, Ndim) sends the ith axis to the back
        # and keeps the order of the others
        # e.g.: v.shape = (2,3,5) np.rollaxis(v, 1, 3).shape = (2, 5, 3)
        # Determine the shape after rolling, excluding the last dimension            
        newShape = ngraphs, valueC.shape[axis]
        #print "axis = %s / org shape = %s / newShape = %s / ngraphs = %s / rolledShape = %s" % (axis, valueC.shape, newShape, ngraphs, rolledShape)
        vRoll = np.rollaxis(valueC, axis, Ndim).reshape(newShape)
        eRoll = np.rollaxis(errorC, axis, Ndim).reshape(newShape)
        axisVar = binVarName[axis]
        # cannot use subtract as it might change the order:
        binnedVars = tuple(j for i,j in enumerate(binVarName) if i != axis)
        key = (axisVar, binnedVars, f)
        #print axisVar, binnedVars, vRoll.shape, key, binning[axis]
        # Values in the x axis
        x = itertools.repeat(getMidPoint(binning[axis]), ngraphs)
        #print x.next()
        sx = itertools.repeat( np.diff(binning[axis])/2, ngraphs )
        g = np.array(map(self.graphGetter, x, vRoll, sx, eRoll )).reshape(rolledShape)
        try:
          graphs[key] = g
        except ValueError:
          print "Graphs shape = %s / g = %s" % (g.shape, g)
        
      # get 2D graphs for all the combinations of 2 axis
      for axes in itertools.combinations( range(len(binning)), 2 ):
        if not do2d: break
        xaxis, yaxis = axes
        binnedVars = tuple(j for i,j in enumerate(binVarName) if i not in axes)
        key = ((binVarName[xaxis], binVarName[yaxis]), binnedVars, f)
        #print key
        #if self.actions and (self.actions[xaxis] == 1 or self.actions[yaxis] == 1):
        # Skip the plots if the action associated to any of the axis is "bin only" (1) 
        # or the one associated to any other variable is "plot only" (2) 
        if any(self.actions[i] == [1,2][i not in axes] for i in range(Ndim)): 
          logging.info('Skipping plots vs. %s,%s' % (binVarName[xaxis], binVarName[yaxis]) )
          continue
        
        if Ndim == 2:
          rolledShape = (1,)
        else:
          rolledShape = [j for i,j in enumerate(valueC.shape) if i not in axes]
        ngraphs = np.prod(rolledShape)
        newShape = ngraphs, valueC.shape[xaxis], valueC.shape[yaxis]
        #print "axes = %s / org shape = %s / newShape = %s / ngraphs = %s / rolledShape = %s" % (axes, valueC.shape, newShape, ngraphs, rolledShape)
        
        # Roll x and y axes to make them the last 2 ones
        vRoll = np.rollaxis(np.rollaxis(valueC, xaxis, Ndim - 1 ), yaxis, Ndim).reshape(newShape)
        x, y = map(binning.__getitem__, axes)
        # NB: np.array( ... ) does not work...
        g2d = np.zeros(len(vRoll), dtype=object)
        for i,j in enumerate( imap(self.graph2dGetter(x, y), vRoll) ):
          g2d[i] = j
        try:
          graphs2d[key] = g2d.reshape(rolledShape)
        except:
          print 'Reshape failed: %s %s' % (graphs, graphs.shape)
    
    if Ndim > self.values_max_depth or any(i in [1,2] for i in self.actions): 
      values = dict( (getFcnName(f), None) for f in estimators) 
    return values, histograms, graphs, graphs2d
    
