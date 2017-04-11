#!/usr/bin/env python

__doc__ = "Send jobs to run TMVACalib.py on queue (LSF, PBS, Condor)"

# Takes the same arguments as TMVACalib.py + options for the batch jobs
# Modify the inputs to accept "lists" (comma separated values)
# Loop over the possible arguments and launch the jobs

import os
import itertools
import inspect
import stat
import datetime
import time
import logging
logging.basicConfig(level=logging.DEBUG)

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


class Submitter(object):
  def __init__(self, job_arg=None, do_submit=True):
    self.do_submit = do_submit
    if job_arg is None:
      self.job_arg = []
    elif type(job_arg) is str:
      self.job_arg = [job_arg]
    else:
      self.job_arg = job_arg

  def copy_proxy(self):
    # copy the proxy and change env var
    logging.info("setting proxy to local folder")
    os.system("cp $X509_USER_PROXY proxy")
    os.environ['X509_USER_PROXY'] = os.getcwd() + "/proxy"

  def submit(self, job_name, args):
    raise NotImplementedError


class SubmitterSimple(Submitter):
  def __init__(self, job_arg, batch_command, job_name_key, do_submit=True):
    super(SubmitterSimple, self).__init__(job_arg, do_submit)
    self.batch_command = batch_command
    self.job_name_key = job_name_key  # -J or -N

  def prepare_script(self, args, inputfiles):
    time.sleep(0.05)
    now = str(datetime.datetime.now()).replace(' ', '_')
    script_name = 'run_TMVACalib_%s.sh' % now

    full_script_name = os.path.join('../scripts/', script_name)
    runArgs = ' '.join('--%s "%s"' % (i, j) if j is not None else "--%s" % i for i, j in args.iteritems())

    with open('../scripts/run_TMVACalib.sh.template') as f:
      text = f.read().format(path=os.getcwd(), args=runArgs, inputfiles=inputfiles)
    with open(full_script_name, 'w') as f:
      f.write(text)
    os.chmod(full_script_name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)

    return full_script_name

  def submit(self, job_name, args, inputfiles):
    logging.info("submitting on lsf %s", job_name)
    full_script_name = self.prepare_script(args, inputfiles)
    path, script_name = os.path.split(full_script_name)
    os.chdir(path)

    command = '{command} {job_name_key} {job_name} {job_args} {script_name}'.format(command=self.batch_command, job_name=job_name,
                                                                                    job_name_key=self.job_name_key,
                                                                                    job_args=' '.join(self.job_arg),
                                                                                    script_name=script_name)
    # Send jobs or print the command
    if not self.do_submit:
      os.system('pwd')
      print os.getcwd()
      print command, '\n'
    else:
      os.system(command)


class SubmitterLSF(SubmitterSimple):
  def __init__(self, job_arg=None, do_submit=True):
    super(SubmitterLSF, self).__init__(job_arg, "bsub", "-J", do_submit)


class SubmitterPBS(SubmitterSimple):
  def __init__(self, job_arg=None, do_submit=True):
    super(SubmitterPBS, self).__init__(job_arg, "qsub", "-N", do_submit)


class SubmitterCondor(Submitter):
  def __init__(self, job_arg=None, do_submit=True):
    super(SubmitterCondor, self).__init__(job_arg, do_submit)
    self.copy_proxy()

  def prepare_script(self, job_name, args, inputfiles):
    time.sleep(0.05)
    now = str(datetime.datetime.now()).replace(' ', '_')
    script_name = 'run_TMVACalib_%s.vanilla' % now

    full_script_name = os.path.join('../scripts/', script_name)
    runArgs = ' '.join('--%s %s' % (i, j) if j is not None else "--%s" % i for i, j in args.iteritems())

    template = ['Executable= ../python/TMVACalib.py',
                'Universe = vanilla',
                'output = {job_name}.out',
                'error = {job_name}.err',
                'log = {job_name}.log',
                'arguments = {args} {inputfiles}',
                'use_x509userproxy = TRUE',
                'getenv = TRUE']
    for i in self.job_arg:
        template.append(i)
    template.append("queue")

    template = '\n'.join(template)
    template = template.format(job_name=job_name, args=runArgs, inputfiles=inputfiles)
    template = template.replace('"', '\\"')
    with open(full_script_name, 'w') as f:
      f.write(template)
    return full_script_name

  def submit(self, job_name, args, inputfiles):
    logging.info("submitting on condor %s", job_name)
    full_script_name = self.prepare_script(job_name, args, inputfiles=inputfiles)
    path, script_name = os.path.split(full_script_name)
    os.chdir(path)

    command = 'condor_submit %s' % full_script_name

    if self.do_submit:
      os.system(command)
    else:
      print command


def run(submitter, inputfiles, etaRange, etRange, particleTypes,
        calibrationTypes, common_args=None, noSubmit=False):
  """
  Send jobs to batch queue, using all the combinations of etaRange, etRange,
  particleTypes and calibrationTypes (which should be iterables).
  <common_args> is a dictionary containing arguments for all jobs"""

  #print etaRange, etRange, particleTypes, calibrationTypes

  # Convert eta and et ranges to pairs if needed
  if isinstance(etRange, (tuple, list)) and len(etRange) > 1:
    etRange = pairwise(etRange)
  # etaRange can also be the actual bin,
  # in which case should not be converted
  if isinstance(etaRange, (tuple, list)) and len(etaRange) > 1 and not all(isinstance(i, int) for i in etaRange):
    etaRange = pairwise(etaRange)

  if common_args:
    args = dict(common_args)  # copy common_args to modify it if needed
  else:
    args = {}

  if not isinstance(inputfiles, str):
    inputfiles = ' '.join(inputfiles)

  # Loop over all combinations of etaRange, etRange, particleTypes, calibrationTypes
  # and submit jobs or print the command
  loop = list(itertools.product(etaRange, etRange, particleTypes, calibrationTypes))

  for i, (eta, et, particle, calibType) in enumerate(loop):
    particleName = particleNames[particle]
    calibName = calibNames[int(calibType)]

    # Change the outputDir if there is more than one calibrationType
    if 'outputDir' in args and \
       isinstance(calibrationTypes, (list, tuple)) and len(calibrationTypes) > 1:
      args['outputDir'] = common_args['outputDir'] + '_%s' % calibName

    # Fix eta and et to TMVACalib.py format (comma separated)
    eta_string = None
    if isinstance(eta, (list, tuple)):
      args['etaRange'] = '%s,%s' % (eta[0], eta[1])
      eta_string = '_'.join(map(str, eta))
    else:  # can also be int for which no conversion is needed
      args['etaRange'] = eta
      eta_string = "%d" % eta

    if et is not None:
      args['etRange'] = '%s,%s' % (et[0], et[1])
      et_string = '_'.join(map(str, et))
      job_name = 'MVACalib_%s_eta%s_Et%s_%s' % (particleName, eta_string, et_string, calibName)
    else:
      job_name = 'MVACalib_%s_eta%s_%s' % (particleName, eta_string, calibName)

    args['particleType'] = particle
    args['calibrationType'] = calibType

    submitter.submit(job_name, args, inputfiles)


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
  group.add_option("-q", "--queue", help="Batch queue (default: %default)", default='1nd')
  group.add_option("-u", "--urgent", help="Urgent priority", default=False, action="store_true")
  group.add_option("--driver", choices=["auto", "LSF", "PBS", "condor"], default="auto")
  group.add_option("--additional-conf", type=str)
  parser.add_option_group(group)
  (options, inputfiles) = parser.parse_args()

  options.outputDir = os.path.abspath(options.outputDir)

  # Eval strings and make sure we have iterables
  iter_options = 'calibrationType', 'particleType', 'etaRange', 'etRange'
  for i in iter_options:
    value = getattr(options, i)
    try:
      value = eval(value)
    except TypeError:  # not a string
      pass
    except NameError:
      pass
    # Make sure it is iterable
    setattr(options, i, make_list(value))

  # Define common arguments for all jobs
  # Construct a dictionary looping over the common variables
  common_variables = parser.option_groups[0].option_list + parser.option_groups[2].option_list + [parser.get_option('--methods')] + [parser.get_option('--target')]
  common_args = {}
  for v in common_variables:
    value = getattr(options, v.dest)
    if value != v.default and (v.default != ('NO', 'DEFAULT') or value is not None):
      if isinstance(value, bool):  # argument does not take a value
        common_args[v.dest] = None
      else:
        common_args[v.dest] = value

  import socket
  hostname = socket.gethostname()
  isCERN = 'cern.ch' in hostname
  isLyon = 'in2p3.fr' in hostname
  isMilan = 'mi.infn.it' in hostname

  job_args = []
  if options.driver == "auto":
    if isCERN:
       options.driver = "LSF"
       if options.urgent:
         job_args.append(' -m g_atlascaturgent')
    elif isLyon:
      options.driver = "pbs"
      job_args = ['-P P_atlas -l ct=03:00:00 -l vmem=3G,fsize=10G,sps=1 -o /sps/atlas/b/blenzi/job_outputs/ -j y']
      if options.urgent:
         job_args.append(' -m g_atlascaturgent')
    elif 'tier3.mi.infn.it' in hostname:
      options.driver = "pbs"
    elif isMilan:
      job_args = ["Requirements = (OpSysMajorVer == 6)"]
      options.driver = "condor"
    else:
      raise ValueError('Invalid host: %s' % os.environ['HOSTNAME'])

  if options.additional_conf:
    job_args.append(options.additional_conf)

  if options.driver == "LSF":
    job_args.append("-q %s" % options.queue)
    submitter = SubmitterLSF(job_args, do_submit=not options.noSubmit)
  elif options.driver == "pbs":
    job_args.append("-q %s" % options.queue)
    submitter = SubmitterPBS(job_args, do_submit=not options.noSubmit)
  elif options.driver == "condor":
    submitter = SubmitterCondor(job_args, do_submit=not options.noSubmit)
  else:
    assert False

  run(submitter, inputfiles,
      options.etaRange, options.etRange, options.particleType, options.calibrationType,
      common_args, options.noSubmit)
