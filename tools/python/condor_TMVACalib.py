#!/usr/bin/env python

__doc__ = "Send jobs to run TMVACalib.py on lxbatch"

# Takes the same arguments as TMVACalib.py + options for the batch jobs
# Modify the inputs to accept "lists" (comma separated values)
# Loop over the possible arguments and launch the jobs

import os, itertools, inspect, string, time
from TMVACalib import getParser, particleNames, calibNames
from optparse import OptionGroup




def make_list(x):
  "Return an iterable object, i.e. the object itself or a list with a single element"
  if hasattr(x, '__iter__'):
    return x
  else:
    return [x]

def pairwise(iterable):
  "s -> (s0,s1), (s1,s2), (s2, s3), ..."
  from itertools import tee, izip
  a, b = tee(iterable)
  next(b, None)
  return izip(a, b)


def condor_TMVACalib(batch_command, inputfiles,
  etaRange, etRange, particleTypes, calibrationTypes, common_args = {}, noSubmit = False, Proxy = False):
  """condor_TMVACalib(batch_command, inputfiles,
  etaRange, etRange, particleTypes, calibrationTypes, common_args = {}, noSubmit=False):
  
  Send jobs to batch queue, using all the combinations of etaRange, etRange,
  particleTypes and calibrationTypes (which should be iterables).
  <common_args> is a dictionary containing arguments for all jobs"""
  
  #print etaRange, etRange, particleTypes, calibrationTypes
  
  # Convert eta and et ranges to pairs if needed
  if isinstance(etRange, (tuple, list)) and len(etRange) > 1:
    etRange = pairwise(etRange)
  # etaRange can also be the actual bin,
  # in which case should not be converted    
  if isinstance(etaRange, (tuple, list)) and len(etaRange) > 1 and \
    not all(isinstance(i, int) for i in etaRange):
    etaRange = pairwise(etaRange)

  args = dict(common_args) # copy common_args to modify it if needed
  #print 'common_args:', args, common_args
  if not isinstance(inputfiles, str):
    inputfiles = ' '.join(inputfiles)
  
  if not noSubmit:
    # cd to CODE_DIR/../scripts to launch the jobs  
    code_dir = os.path.abspath( os.path.dirname(inspect.stack()[0][1]) ) # location of the code
    os.chdir('%s/../scripts' % code_dir)
  
  # Loop over all combinations of etaRange, etRange, particleTypes, calibrationTypes
  # and submit jobs or print the command
  loop = list(itertools.product(etaRange, etRange, particleTypes, calibrationTypes))

  if Proxy:
        os.system("cp $X509_USER_PROXY proxy")
        os.environ['X509_USER_PROXY'] = os.getcwd()+"/proxy"
  
  #   print loop
  for eta, et, particle, calibType in loop:
    particleName = particleNames[particle]
    calibName = calibNames[int(calibType)]
    
    # Change the outputDir if there is more than one calibrationType
    if 'outputDir' in args and \
      isinstance(calibrationTypes, (list,tuple)) and len(calibrationTypes) > 1:
      args['outputDir'] = common_args['outputDir'] + '_%s' % calibName
    
    # Fix eta and et to TMVACalib.py format (comma separated)
    if isinstance(eta, (list,tuple)): 
      args['etaRange'] = '%s,%s' % (eta[0], eta[1])
      eta_string = '%s-%s' % (eta[0], eta[1])
    else: # can also be int for which no conversion is needed
      args['etaRange']  = eta
      eta_string = str(eta)
    if et is not None:
      args['etRange'] = '%s,%s' % (et[0], et[1])
      et_string='%s-%s' % (et[0], et[1])
 
    args['particleType'] = particle
    args['calibrationType'] = calibType
    runArgs = ' '.join("--%s '%s'" % (i,j) if j is not None else "'--%s'" % i  for i,j in args.iteritems())
    if et is not None:
      jobName = 'MVACalib_%s_eta'% (particleName)+eta_string+'_Et'+et_string+'_%s' % (calibName)
    else:
      jobName = 'MVACalib_%s_eta'% (particleName)+eta_string+'_%s' % (calibName)
   # try:
   #   jobArg = jobArgs % (jobName)
   # except:
   #   jobArg = jobArgs

    
   
    
    command = './run_condorTMVACalib.sh ' + jobName+".vanilla"
   
       
    cd_sub_script = []
    cd_sub_script.append("Executable= ../python/TMVACalib.py\nUniverse = vanilla")
    cd_sub_script.append("output = "+jobName+".out")                 
    cd_sub_script.append("error = "+jobName+".error") 
    cd_sub_script.append('arguments = "'+runArgs+" "+inputfiles+'"')     
    cd_sub_script.append("use_x509userproxy = TRUE\ngetenv = TRUE\nRequirements = (OpSysMajorVer == 6)\nqueue") 
    cd_sub_script = '\n'.join(cd_sub_script)
    if noSubmit:
         print "*" * 10
         print cd_sub_script
    else:
         f = open(jobName+".vanilla", 'w')
         f.write(cd_sub_script)
         f.close() 
    # Send jobs or print the command
         
         tmp = os.system(command)
         time.sleep(1)
     
  

if __name__ == '__main__':
  parser = getParser(__doc__)
  
  # Convert int types to str to allow multiple values
  parser.get_option('--calibrationType').type = "str"
  parser.get_option('--particleType').type = "str"
  
  # Convert actions to append to allow multiple values --> does not work
  # for i in 'calibrationType','particleType','etaRange','etRange':
  #   parser.get_option('--%s' % i).action = 'append'
  
  # Add options for batch jobs
  group = OptionGroup(parser, "Batch job options")
  group.add_option("--noSubmit", help="Do not submit the jobs, only print the commands", default=False, action="store_true")
  group.add_option("--Proxy", help="If you need to use an already active proxy in order to read remote file", default=False, action="store_true")
  #group.add_option("-q", "--queue", help="Batch queue (default: %default)", default='1nd')
  #group.add_option("-u", "--urgent", help="Urgent priority", default=False, action="store_true")
  parser.add_option_group(group)
  (options, inputfiles) = parser.parse_args()
  
  #if options.urgent:
  #  options.queue += ' -m g_atlascaturgent'

  # Eval strings and make sure we have iterables
  iter_options = 'calibrationType','particleType','etaRange','etRange'
  for i in iter_options:
    value = getattr(options, i)
    try:
      value = eval(value)
    except TypeError: # not a string
      pass
    # Make sure it is iterable
    setattr(options, i, make_list(value))
    
  # Define common arguments for all jobs
  # Construct a dictionary looping over the common variables
  common_variables = parser.option_groups[0].option_list + parser.option_groups[2].option_list + [parser.get_option('--methods')]
  common_args = {}
  for v in common_variables:
    value = getattr(options, v.dest)
    if value != v.default and (v.default != ('NO', 'DEFAULT') or value is not None):
      if isinstance(value, bool): # argument does not take a value
        common_args[v.dest] = None
      else:
        common_args[v.dest] = value
  print common_args
  
  batch_command = 'submit_batch '
  
 
  condor_TMVACalib(batch_command, inputfiles,
    options.etaRange, options.etRange, options.particleType, options.calibrationType,
    common_args, options.noSubmit, options.Proxy)

