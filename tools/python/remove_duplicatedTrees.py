#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = "Remove all binary trees that are equal to the last one"
__author__ = "Bruno Lenzi <Bruno.Lenzi@cern.ch>"

# WARNING: there are cases in which many trees are equal to the last or the second to last
# trees (e.g. 252, 254, ... 400 are equal and 253, 255 ... 399 are equal)

def removeDuplicatedTrees(xmlfilename, outputfile=None):
  """removeDuplicatedTrees(xmlfilename, outputfile=None) -> 
  Remove all binary trees that are equal to the last one
  overwrite if outputfile not given"""
  
  outputfile = outputfile or xmlfilename
  print 'Removing duplicated trees from', outputfile
  
  from xml.dom.minidom import parse
  
  dom = parse(xmlfilename)
  top_element = dom.documentElement
  wdom = top_element.getElementsByTagName("Weights")[0]
  
  # Set all tree numbers to -1 to compare them
  trees = wdom.getElementsByTagName("BinaryTree")
  for t in trees:
    t.setAttribute("itree", "-1")
  
  # Remove all binary trees that are equal to the last one
  txml = t.toxml()
  for tree in trees[:-1]:
    if tree.toxml() == txml:
      _ = wdom.removeChild(tree.previousSibling) # to avoid an empty line
      _ = wdom.removeChild(tree)
  
  # Fix the number of trees (Ntrees) and the index of each
  # TODO: fix in Options as well...
  trees = wdom.getElementsByTagName("BinaryTree")
  wdom.setAttribute("NTrees", str(len(trees)) )
  for itree, tree in enumerate(trees):
    tree.setAttribute("itree", str(itree) )
  
  # Write modified xmlfile
  with open(outputfile, 'w') as xmlfile: dom.writexml(xmlfile)

if __name__ == '__main__':
  import os
  from optparse import OptionParser
  parser = OptionParser(usage="usage: %prog [options] xmlfile1 .. xmlfileN")
  parser.description = __doc__
  parser.epilog = "\n"
  parser.add_option("-o", "--output", help="Output file or path", default='')
  (options, inputfiles) = parser.parse_args()
  
  for xmlfile in inputfiles:
    outputfile = os.path.join(options.output, os.path.basename(xmlfile)) \
      if os.path.isdir(options.output) else None
    removeDuplicatedTrees(xmlfile, outputfile)
