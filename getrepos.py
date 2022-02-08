#!/usr/bin/python3
#
# Get Repos: use a CSV input file to get student repositories
# - clones if the repo is not yet cloned, otherwise does a pull
# - assumes that things are going to merge well and no interaction
#   is needed
#
# Usage: getrepos.py <input-file> [--room=<classroom>] [--asign=<assignment>]
# 
# input file is a CSV file, data input fields are:
#
#  LastName,FirstName,NMSUUserID,GitHubUserID
#
# Actually, only the github user id is used
# - TODO: rename the clone directory to be the students name?
#
import os
import sys
import csv
import re
import subprocess
#import json

# name of the GitHub organization that your classrooms fit into
# - is part of the repo URL
classroom = "NMSU-CS-Cook"
# name of the assignment (assignments will get confusing at the org
# level if you do not prefix them with course and semester)
assignment = "cs581-sp2022-individual"

#-------------------------------------------------
# If repo processing gets more complicated, move 
# it into its own function. For now, not.
#-------------------------------------------------
#def getSingleRepo(repoURL):

#-------------------------------------------------
#-------------------------------------------------
def processRepoCSVFile(filename):
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
         else:
            print("  Cloning repo...")
            subprocess.call(['git','clone',repourl])
      except:
         print("Exception: failed on {0}".format(student))
   f.close()
   return

#-------------------------------------------------
# Main
#-------------------------------------------------
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
processRepoCSVFile(sys.argv[1])
quit()


