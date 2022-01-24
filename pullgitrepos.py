#!/usr/bin/python3

import os;

def processDir(cwd,indent):
   print("{1}processing dir ({0})".format(cwd,indent))
   if os.path.exists(cwd):
      os.chdir(cwd)
   else:
      return False
   print("{0}entered".format(indent))
   if os.path.exists(".git"):
      print("is root of a Git repo!")
      os.chdir("..")
      return True
   print("{0}not a Git repo".format(indent))
   sd = os.scandir()
   for f in sd:
      if f.is_dir():
         processDir(f.name,indent+"  ")
   os.chdir("..")
   print("{0}done".format(indent))
   return False


processDir(os.path.abspath("."),"")
exit()

