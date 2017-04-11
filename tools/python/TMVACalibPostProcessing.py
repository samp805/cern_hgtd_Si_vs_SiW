#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """To write info about the calibration on TMVA output xml files, 
such as the position of the mean, median and peak of E/Etrue""" 

import os, re, ROOT, numpy as np
from xml.dom.minidom import parse
from TMVACalib import particleNames, calibNames
import logging

regex_file = "MVACalib_(?P<particle>\w+)_Et(?P<Etrange>[\w\-\.]+)_eta(?P<etarange>[\w\-\.]+)_(?P<calibType>\w+)_(?P<method>\w+)\.weights\.xml"
regex = re.compile(regex_file)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    from itertools import tee, izip
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def group_filenames_eta(filenames):
    regex = re.compile(r'MVACalib_(?P<particle>\w+)_Et(?P<Etrange>[\w\-\.]+)_eta(?P<etarange>[\w\-\.]+)_(?P<calibType>\w+)')
    result = {}
    logging.info('finding binning from %d files', len(filenames))
    for f in filenames:
        m = regex.search(f)
        if not m:
            raise ValueError('cannot understand %s', f)
        regex_result = m.groupdict()
        eta_range = tuple(map(float, regex_result['etarange'].split('-')))
        result.setdefault(eta_range, []).append(f)
    return result


def add_user_information_to_dom(dom, user_information):
  top_element = dom.documentElement
  for previous in top_element.getElementsByTagName("UserInfo"):
      top_element.removeChild(previous)
  userinfo_element = top_element.appendChild(dom.createElement("UserInfo"))
  #   userinfo_element = top_element.replaceChild(previous, dom.createElement("UserInfo"))
  for k, v in user_information.iteritems():
      element = userinfo_element.appendChild(dom.createElement("Info"))
      element.setAttribute("name", k)
      if type(v) is str:
          element.setAttribute("value", v)
      elif type(v) is tuple and len(v) == 2:
          element.setAttribute("value", "%f" % v[0])
          element.setAttribute("error", "%f" % v[1])
      elif np.isreal(v):
          element.setAttribute("value", "%f" % v)
      else:
          raise NotImplementedError("only float or string or float[2] can be written, %s it not valid" % v)
  return dom




def add_user_information_to_xmlfile(xmlfilename, user_information):
  dom = parse(xmlfilename)
  newdom = add_user_information_to_dom(dom, user_information)
  with open(xmlfilename, 'w') as xmlfile:
    newdom.writexml(xmlfile)

def add_variablesname_to_dom(dom, user_information):
  top_element = dom.documentElement
  for previous in top_element.getElementsByTagName("VariablesName"):
      top_element.removeChild(previous)
  userinfo_element = top_element.appendChild(dom.createElement("VariablesName"))
  #   userinfo_element = top_element.replaceChild(previous, dom.createElement("UserInfo"))
  for k, v in user_information.iteritems():
      element = userinfo_element.appendChild(dom.createElement("Info"))
      if  type(v) is list:
	  element.setAttribute("Name", "%s" % ','.join(v))
      else:
          raise NotImplementedError("only list can be written, %s it not valid" % v)
  return dom

def add_variablesname_to_xmlfile(xmlfilename, user_information):
  dom = parse(xmlfilename)
  newdom = add_variablesname_to_dom(dom, user_information)
  with open(xmlfilename, 'w') as xmlfile:
    newdom.writexml(xmlfile)

def compute_quantities_fromROOTfile(variable, ROOTfilename, et, cuts=None, method='step'):
    import ROOT
    from RootTools import GetValuesFromTree
    from Estimators import truncated_mean, truncated_median

    def join_cut_value(cut, value):
        value = str(value)
        if not cut:
            return value
        return "(" + cut + ") * (" + value + ")"

    cuts = cuts or [""]
    try:
      float_cuts = map(float, cuts) # all cuts are floats, replace by "real" cuts
      cuts = ['abs(%s - %s) < %s' % (et, 0.5*(c0+c1), 0.5*(c1-c0)) \
        for c0,c1 in pairwise(float_cuts)] + ['%s > %s' % (et, float_cuts[-1])]
    except ValueError:
      pass


    try:
      f = ROOT.TFile(ROOTfilename)
      tree = f.TrainTree
    except TypeError: # a list was passed
      tree = ROOT.TChain('TrainTree')
      map(tree.Add, ROOTfilename)
    
    valid_cuts, medians, means, peaks, means10, means20, medians10, medians20 = \
      [], [], [], [], [], [], [], []
    mean_et = []
    for cut in cuts:
        data = np.fromiter(GetValuesFromTree(tree, variable, cut), dtype=float)
        weight = np.fromiter(GetValuesFromTree(tree, "weight", cut), dtype=float)
        data_energy = np.fromiter(GetValuesFromTree(tree, et, cut),
                                  dtype=float)
        median = np.median(data)
        mean = data.mean()
        # mean-mode ~ 3(mean-median), from http://mathworld.wolfram.com/StatisticalMedian.html
        peak = mean - 3*(mean-median)
        mean10 = truncated_mean(data, weight, 0.1)
        mean20 = truncated_mean(data, weight, 0.2)
        median10 = truncated_median(data, weight, 0.1)
        median20 = truncated_median(data, weight, 0.2)
        values = median, mean, peak, mean10[0], mean20[0], median10[0], median20[0]
        print "cut: %s Mean: %.3f / Median: %.3f / Peak: %.3f / Mean10: %.3f +/- %.3f / Mean20: %.3f +/- %.3f / Median10: %.3f +/- %.3f / Median20: %.3f +/- %.3f" % (cut, mean, median, peak, mean10[0], mean10[1], mean20[0], mean20[1], median10[0], median10[1], median20[0], median20[1])
        if np.any(np.isnan(values)):
            print "skipping NaN value(s)"
            continue
        valid_cuts.append(cut)
        mean_et.append(np.mean(data_energy))        
        medians.append(median)
        means.append(mean)
        peaks.append(peak)
        means10.append(mean10[0])
        means20.append(mean20[0])
        medians10.append(median10[0])
        medians20.append(median20[0])

    values = (medians, means, peaks, means10, means20, medians10, medians20)
    values_names = ("Median", "Mean", "Peak", "Mean10", "Mean20", "Median10", "Median20")


    if method == 'spline1':
        result = { }
        for value, value_name in zip(values, values_names):
            zs = []
            for i in range(len(means) - 1):
                zs.append("%.20f + %.20f * (..x.. - %f)" % (value[i+1], (value[i+1] - value[i]) / (mean_et[i+1] - mean_et[i]), mean_et[i+1]))
            formula = ["((%s) * (..x.. < %f))" % (zs[0], mean_et[0])]
            for i in range(len(zs)):
                formula.append("((%s) * (..x.. >= %f && ..x.. < %f))" % (zs[i], mean_et[i], mean_et[i+1]))
            formula.append("((%s) * (..x.. >= %f))" % (zs[-1], mean_et[-1]))
            formula = ' + '.join(formula)
            formula = formula.replace('..x..', et)
            
            result[value_name] = formula
        return result
    
    elif method == 'step':
        values_step = ["+".join(join_cut_value(cut, value) \
          for cut, value in zip(valid_cuts, V)) for V in values]
        return dict(zip(values_names, values_step))

def create_friendtree(additional_info, original_tree):
  entries = original_tree.GetEntries()
  from array import array
  name = original_tree.GetName() + "Friend"
  print 'Adding friend tree %s' % name
  friend_tree = ROOT.TTree(name, name)
  dict_for_friend = { }
  formulas = { }
  for k,v in additional_info.iteritems():
    v = "%s" % v
    if k == "CalibrationType": continue
    formula = ROOT.TTreeFormula("formula_" + k, v, original_tree)
    if formula.GetNdim() != 1:
      print "formula %s not valid" % k
      continue
    formulas[k] = formula
    dict_for_friend[k] = array('f', [-999])
    friend_tree.Branch(k, dict_for_friend[k], "%s/F" % k)

  for ievent in xrange(entries):
    original_tree.GetEntry(ievent)
    for k, formula in formulas.iteritems():
#       value = formula.EvalInstance(0)
      dict_for_friend[k][0] = formula.EvalInstance(0)
    friend_tree.Fill()

  return friend_tree

def get_info_from_filename(xmlfile, regex=regex):
  """parse the xml filename to extract all the information about eta and Et ranges, 
     ROOTfile, peak definition, etc"""
  if not os.path.exists(xmlfile):
    raise IOError('xml file %s does not exist' % xmlfile)
  
  directory, filename = os.path.split(xmlfile)
  directory = directory.replace('weights', '')
  
  match = regex.match(filename)
  if match is None:
    print "ERROR: problem parsing filename %s, skipping" % filename
    return {}
  infos = match.groupdict()
  
  ROOTfile = "MVACalib_" + infos["particle"] + "_Et" + infos["Etrange"] + "_eta" + infos["etarange"] + "_" + infos["calibType"] + ".root"
  ROOTfile = os.path.join(directory, ROOTfile)
  if not os.path.isfile(ROOTfile):
    print "ERROR: root file not found: %s" % ROOTfile
    return {}
  
  prefixes = {"electron": "el", 
            "photon": "ph", 
            "unconvertedPhoton": "ph", 
            "convertedPhoton": "ph", 
            "convertedSiSiPhoton": "ph"}
  prefix = prefixes[infos["particle"]]
  calibrationType = calibNames.index(infos["calibType"])
  if not type(calibrationType) is int:
    print "calibrationType parameter must be int"
    return {}
  
  if calibrationType == 0: # correction to cluster
    value = infos['method'] + '/K'
  elif  calibrationType == 1: # correction to Eacc
    value = infos['method'] + '/Kacc'
  else: # full calib
    value = infos['method'] + '/ph_truth_E'.replace('ph', prefix)
  
  infos.update( dict(ROOTfile = ROOTfile, prefix = prefix, value = value, 
    calibrationType = calibrationType) )
  return infos


def TMVACalibPostProcessing(xmlfile, regex=regex, cuts=None, doTrainTreeFriend=False,
  value_method='step', useCalibratedEt=False, **kw):
  """(xmlfile, regex=regex, cuts=None, doTrainTreeFriend=False,
  value_method='step', useCalibratedEt=False, **kw) --> 
  Write info about the optimization in xmlfile, including the calibration type,
  etaBin and energyBin definitions and the positions of the mean, median and peak"""  

  if not os.path.exists(xmlfile):
    raise IOError('xml file %s does not exist' % xmlfile)
  
  info = get_info_from_filename(xmlfile, regex)
  if not info:
    return
  ROOTfile = info['ROOTfile']
  
  # --------------------------------------------------------------
  # Compute the position of the mean, median and peak
  # --------------------------------------------------------------
  
  et = "(el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3)/cosh(el_cl_eta)/1e3"
  et = et.replace("el_", info['prefix'] + "_")
  if useCalibratedEt:
    et = "%s*%s" % (info['method'], et)  
  
  try:
    additional_info = kw.pop("Quantities")
  except KeyError:
    additional_info = compute_quantities_fromROOTfile(info['value'], ROOTfile, et, 
                                                      cuts, value_method)
  
  # ----------------------------------------------------------------
  # Write additional info about the optimization
  # ----------------------------------------------------------------
  
  additional_info.update({"CalibrationType": calibNames[info['calibrationType']]})
  additional_info.update(kw)

  add_user_information_to_xmlfile(xmlfile, additional_info)
  
  # ----------------------------------------------------------------
  # Add friend tree with all the shifts event by event
  # ----------------------------------------------------------------
  
  f = ROOT.TFile(ROOTfile, "UPDATE")
  TestFriendTree = create_friendtree(additional_info, f.TestTree)
  f.TestTree.AddFriend(TestFriendTree)
  f.TestTree.Write("", ROOT.TObject.kOverwrite)
  TestFriendTree.Write("", ROOT.TObject.kOverwrite)
  f.Close()
  
  # Crashes if the file is not re-opened, no idea why...
  if doTrainTreeFriend:
    f = ROOT.TFile(ROOTfile, "UPDATE")
    TrainTreeFriend = create_friendtree(additional_info, f.TrainTree)
    f.TrainTree.AddFriend(TrainTreeFriend)
    f.TrainTree.Write("", ROOT.TObject.kOverwrite)
    TrainTreeFriend.Write("", ROOT.TObject.kOverwrite)
    f.Close()


if __name__ == "__main__":
  from optparse import OptionParser
  parser = OptionParser()
  parser.description = __doc__
  parser.epilog = "\n"
  parser.add_option("-d", "--directory",
                    help="directory containing the weights subdirectory")
  parser.add_option("-r", "--regex-file",
                    default="MVACalib_(?P<particle>\w+)_Et(?P<Etrange>[\w\-\.]+)_eta(?P<etarange>[\w\-\.]+)_(?P<calibType>\w+)_(?P<method>\w+)\.weights\.xml",
                    help="regex to define the xml files, default: %default")
  parser.add_option("-c", "--cuts", default="",
                    help="cuts to be applied to every files (not very useful from command line)")
  parser.add_option("--overwrite", 
                    help="Overwrite UserInfo", default=False, action="store_true")
  parser.add_option("--filter-files", default="",
                    help="Regex to filter the xml files (e.g.: *0-20*)")
  parser.add_option("--method", default="step", help="method to compute shift", choices=("step", "spline1"))
  parser.add_option("--doTrainTreeFriend", 
                    help="Create friend of TrainTree", default=False, action="store_true")
  parser.add_option("--userDefined", 
                    help="User defined info (dictionary)", default="{}")
  parser.add_option("--doGlobal", default=False, action="store_true",
                    help="Compute quantities (shifts) using all files at once")
  parser.add_option("--useCalibratedEt", default=False, action="store_true",
                    help="Use calibrated Et (instead of raw) for splines and cuts")
    
  (options, args) = parser.parse_args()
  directory = os.path.expanduser(os.path.expandvars(options.directory))
  kw = eval(options.userDefined)
  cuts = options.cuts.split(",")
  value_method = options.method
  
  import os
  import os.path
  import re

  weights_dir = os.path.join(directory, "weights")
  regex =  re.compile(options.regex_file)
  weight_files = filter(lambda ff: ff[-4:]==".xml", os.listdir(weights_dir))
  if options.filter_files:
    import fnmatch
    weight_files = fnmatch.filter(weight_files, options.filter_files)
  
  weight_files_full = [os.path.join(weights_dir, filename) for filename in weight_files]
  
  # Pre-compute quantities using all files if requested (assume their info is the same)
  if options.doGlobal:
    print 'Calculating global quantities'
    info_files = filter(bool, [get_info_from_filename(os.path.join(weights_dir, filename), regex) \
      for filename in weight_files] )
    ROOTfiles = [ info['ROOTfile'] for info in info_files ]
    et = "(el_rawcl_Es1 + el_rawcl_Es2 + el_rawcl_Es3)/cosh(el_cl_eta)/1e3"
    et = et.replace("el_", info['prefix'] + "_")
    if options.useCalibratedEt:
      et = "%s*%s" % (info['method'], et)
    kw["Quantities"] = compute_quantities_fromROOTfile(info['value'], ROOTfiles, et,
                                                       cuts, value_method)
  
  for filename in weight_files:
    filename_full = os.path.join(weights_dir, filename)

    # check if the file was already patched
    with open(filename_full) as f:
      if "<UserInfo>" in f.read():
        if options.overwrite:
          print "Overwriting UserInfo in %s" % filename
        else:  
          print "UserInfo already present in %s, skipping" % filename
          continue
    
    TMVACalibPostProcessing(filename_full,
                            regex,
                            cuts,
                            options.doTrainTreeFriend,
                            value_method,
                            options.useCalibratedEt,
                            **kw )

