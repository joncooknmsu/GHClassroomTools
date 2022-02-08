#!/usr/bin/python3
#
# Generic script that walks a directory tree and pulls any
# Git repos it finds, and potentially any SVN repos, too
# - options and help text available on command line (--help)
#
# WARNING: this script can be dangerous if it is going to 
# encounter many repos in a directory tree, especially if 
# they need manual intervention to access or merge
# 

import os
import argparse

doGit = True
doSvn = False
dryRun = False
debug = False
maxDepth = 4

#---------------------------------------------------------
# Process a directory given by cwd (assumes we are currently
# in the parent directory). This function will recurse on
# subdirectories until depth is reached (as long as it is not
# in a repo already)
#---------------------------------------------------------
def processDir(cwd,depth):
   global debug, doGit, doSvn, dryRun, maxDepth
   # first create an indent prefix for pretty-printing
   indent = ""
   for i in range(depth):
      indent = indent+"   "
   if depth >= maxDepth: 
      if debug: print("{0}reached max depth of {1}".format(indent,depth))
      return False
   print("{0}dir ({1}) ".format(indent,cwd),end="")
   if os.path.exists(cwd):
      os.chdir(cwd)
   else:
      return False
   # after here we have entered the subdir, so any function
   # return must do a cd .. before
   if debug: print("{0}entered ".format(indent),end="")
   # a dir that is an SVN repo has a ".svn" subdir in it
   if os.path.exists(".svn"):
      if doSvn: print("is an SVN repo, let's update")
      else: print("")
      if (not dryRun and doSvn):
         os.system("svn update")
      os.chdir("..")
      return True
   # a dir that is an Git repo has a ".git" subdir in it
   if os.path.exists(".git"):
      if doGit: print("{0}is a Git repo, let's pull".format(indent))
      else: print("")
      if (not dryRun and doGit):
         os.system("git pull -a")
      os.chdir("..")
      return True
   print("")
   if debug: print("{0}not a Git repo".format(indent))
   # now process subdirs of this directory (if it was not
   # a repo itself)
   sd = os.scandir()
   for f in sd:
      if f.is_dir():
         processDir(f.name,depth+1)
   os.chdir("..")
   if debug: print("{0}done".format(indent))
   return False

#---------------------------------------------------------
# Main
#---------------------------------------------------------
argParser = argparse.ArgumentParser(description='Git repo management')
argParser.add_argument('--dry', action='store_true', help='perform dry run, no operations (default real-actions)')
argParser.add_argument('--svn', action='store_true', help='turn on svn update for any svn repos (default off)')
argParser.add_argument('--nogit', action='store_false', help='turn OFF git pull for any git repos (default on)')
argParser.add_argument('--debug', action='store_true', help='turn on debugging info (default off)')
argParser.add_argument('--depth', action='store', type=int, default=4, help='maximum directory traversal depth (default 4)')
args = argParser.parse_args()
dryRun = args.dry
doSvn = args.svn
doGit = args.nogit
debug = args.debug
maxDepth = args.depth
if debug:
   print(args)
if dryRun:
   print("No action, just dry run")
   
processDir(os.path.abspath("."),0)
exit()


