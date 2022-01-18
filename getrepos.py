#!/usr/bin/python3

import os
import sys
import csv
import re
import subprocess
#import json

# input is a CSV file
# Data input fields are:
#LastName,FirstName,NMSUUserID,GitHubUserID

classroom = "NMSU-CS-Cook"
assignment = "cs581-sp2022-individual"

def processFile(filename):
   global classroom, assignment
   f = open(filename,"r")
   cf = csv.DictReader(f,fieldnames=('lastname', 'firstname', 'userid', 'githubuser'))
   for student in cf:
      try:
         print("Student: {0},{1},{2}".format(student['firstname'], 
                                      student['lastname'], student['githubuser']))
         reponame = "{0}-{1}".format(assignment, student['githubuser'])
         print("  Repo name: ({0})".format(reponame))
         repourl = "git@github.com:{0}/{1}.git".format(classroom, reponame)
         print("  Repo URL: ({0})".format(repourl))
         if repourl == "":
            print("  No repo, skipping")
            continue
         print("  Has repo: {0}".format(repourl))
         if os.path.isdir(reponame):
            print("  Already cloned, pulling...")
            os.chdir(reponame)
            # --all flag will fetch all branches, not just current (master)
            subprocess.call(['git','pull','--all'])
            os.chdir('..')
            continue
         print("  Cloning repo...")
         subprocess.call(['git','clone',repourl])
      except:
         print("Exception: failed on {0}".format(student))
   f.close()
   return

if (len(sys.argv) < 2):
    print("CSV filename must be given.")
    quit()
i = 2
while (i < len(sys.argv)):
   v = re.match("--room=(.*)",sys.argv[i])
   if v is not None:
      classroom = v.group(1)
   v = re.match("--assign=(.*)",sys.argv[i])
   if v is not None:
      assignment = v.group(1)
   
#print sys.argv[0], sys.argv[1]
processFile(sys.argv[1])
quit()


