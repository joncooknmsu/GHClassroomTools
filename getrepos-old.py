#!/usr/bin/python2
#
# Original getrepos, simple, no options, hardcoded for me
#

import os
import sys
import csv
import re
import subprocess
#import json

# Fields are:
#LastName,FirstName,UserID,GitHubRepo

def processFile(filename):
   f = open(filename,"r")
   cf = csv.DictReader(f,fieldnames=('lastname', 'firstname', 'userid', 'githubrepo'))
   for student in cf:
      try:
         print "Student: ", student['firstname'], student['lastname'], student['userid']
         repo = student['githubrepo']
         if repo == "":
            print "  No repo, skipping"
            continue
         print "  Has repo: ",repo
         v = re.match('git@github.com:NMSU-CS-Cook/(.*).git',repo)
         reponame = v.group(1)
         print "  Repo name: ({0})".format(reponame)
         if os.path.isdir(reponame):
            print "  Already cloned, pulling"
            os.chdir(reponame)
            # --all flag will fetch all branches, not just current (master)
            subprocess.call(['git','pull','--all'])
            os.chdir('..')
            continue
         subprocess.call(['git','clone',repo])
      except:
         print "Skipping",student
   f.close()
   return

if (len(sys.argv) < 2):
    print "CSV filename must be given."
    quit()
print sys.argv[0], sys.argv[1]
processFile(sys.argv[1])
quit()


