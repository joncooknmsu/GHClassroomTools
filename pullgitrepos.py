#!/usr/bin/python3

import os
import argparse

doGit = True
doSvn = True
dryRun = True
debug = False
maxDepth = 3

def processDir(cwd,depth):
   if depth >= maxDepth: 
      return False
   indent = ""
   for i in range(depth):
      indent = indent+"   "
   print("{1}dir ({0})".format(cwd,indent),end="")
   if os.path.exists(cwd):
      os.chdir(cwd)
   else:
      return False
   if debug: print("{0}entered".format(indent))
   if os.path.exists(".svn"):
      print("is an SVN repo, let's update")
      if (not dryRun and doSvn):
         os.system("svn update")
      os.chdir("..")
      return True
   if os.path.exists(".git"):
      print("{0}is a Git repo, let's pull".format(indent))
      if (not dryRun and doGit):
         os.system("git pull -a")
      os.chdir("..")
      return True
   print("")
   if debug: print("{0}not a Git repo".format(indent))
   sd = os.scandir()
   for f in sd:
      if f.is_dir():
         processDir(f.name,depth+1)
   os.chdir("..")
   if debug: print("{0}done".format(indent))
   return False

# 
# Main
#
argParser = argparse.ArgumentParser(description='Git repo management')
argParser.add_argument('--dry', help='perform dry run, no operations')
argParser.add_argument('--svn', help='turn on svn update for svn repo')
args = argParser.parse_args()
print(args)

if dryRun:
   print("No action, just dry run")
processDir(os.path.abspath("."),0)
exit()

