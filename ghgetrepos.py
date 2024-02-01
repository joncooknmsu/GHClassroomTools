#!/usr/bin/python3
#
# Get Repos: use a GitHub Classroom download format CSV input file
# to get student repositories
# - clones if the repo is not yet cloned, otherwise does a pull
# - assumes that things are going to merge well and no interaction
#   is needed
#
# Usage: getrepos.py <ghclassroom-assignment-csv-file>
# 
# input file is a CSV file, data input fields are:
#
#  assignment_name,assignment_url,starter_code_url,
#  github_username,roster_identifier,student_repository_name,
#  student_repository_url,submission_timestamp,points_awarded,
#  points_available
#
# - this is the format that GitHub assignment grading files are in
#
# we use student_repository_name (6th field) to form a URL to clone
#
# TODO: make classroom a command line arg (done??, --room arg)
# TODO: rename the clone directory to be the students name?
#
import os
import sys
import csv
import re
import subprocess
#import json

# name of the GitHub organization that your classrooms fit into
# - is part of the repo URL
#classroom = "NMSU-CS-Cook"
classroom = "NMSU-CS-CS371"

# NOT USED ANYMORE
# name of the assignment (assignments will get confusing at the org
# level if you do not prefix them with course and semester)
#assignment = "cs581-sp2022-individual"
#assignment = "cs371-fa2022-individual"
#git@github.com:NMSU-CS-Cook/cs-581-igloo-djarmas.git

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
   cf = csv.DictReader(f,fieldnames=('assignment_name', 'assignment_url', 'starter_code_url', 'github_username', 'roster_identifier', 'student_repository_name', 'student_repository_url', 'submission_timestamp', 'points_awarded',  'points_available'))
   for student in cf:
      # skip header line
      if student['assignment_name'] == 'assignment_name':
          continue 
      try:
         print("Student: {0},{1},{2}".format(student['github_username'], 
                                      student['roster_identifier'], student['assignment_name']))
         #reponame = "{0}-{1}".format(assignment, student['githubuser'])
         reponame = student['student_repository_name']
         # NOTE: we clone into a directory name that has the student
         # roster id appended on it; I use the student's NMSU id 
         # for this and so it connects me to the student in Canvas
         dirname = reponame + "-" + student['roster_identifier']
         #print("  Repo name: ({0})".format(reponame))
         repourl = "git@github.com:{0}/{1}.git".format(classroom, reponame)
         print("  Repo URL: ({0})".format(repourl))
         if repourl == "":
            print("  No repo, skipping")
            continue
         print("  Has repo: {0}".format(repourl))
         if os.path.isdir(dirname):
            print("  Already cloned, pulling...")
            os.chdir(dirname)
            # --all flag will fetch all branches, not just current (master)
            # (but merging still happens on the current, I think; this 
            # usually works but if current branches are different (we 
            # switched, or a main/master naming difference, it won't)
            subprocess.call(['git','pull','--all'])
            os.chdir('..')
         else:
            print("  Cloning repo...")
            subprocess.call(['git','clone',repourl,dirname])
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
# CSV filename must come first: TODO: better arg parsing
i = 2
while (i < len(sys.argv)):
   v = re.match("--room=(.*)",sys.argv[i])
   if v is not None:
      classroom = v.group(1)
   v = re.match("--assign=(.*)",sys.argv[i])
   if v is not None:
      assignment = v.group(1)
   i += 1
   
#print sys.argv[0], sys.argv[1]
processRepoCSVFile(sys.argv[1])
quit()


