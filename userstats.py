#!/usr/bin/python2
#
# run this script in the top level of a repo. I generally save
# the output by redirecting it to a file.
#
# Runs a formatted 'git log' command and then parses its output,
# generates per-user repo usage and commit statistics per user:
#   Per user:
#   # of commits, # of merge pull requests, # of other merges
#   then per file type (extension)
#      # of lines added, removed for text-type files
#      # of binary files modified
# Format used:
# git log '--pretty=format:COMMIT: %h %cn %an %ct %s' --numstat
# except that instead of spaces, @ is used for easier parsing
#

import os
import sys
import re
import subprocess
import datetime

debug = 0

# Overall data structure that holds accumulated stats
# each element index is a username, each element is a
# dictionary itself, with data as below in code (sorry!)
userData = {}

#---------------------------------------------------------
# Run the git log command and parse commit lines
#---------------------------------------------------------
def processGitLogCmd():
   global userData, debug
   user = 'none'
   sout = subprocess.check_output(['git', 'log', '--all',\
          '--pretty=format:COMMIT:@%h@%cn@%an@%ct@%s', '--numstat']).split('\n')
   for line in sout:
      v = re.match("COMMIT:@([^@]+)@([^@]+)@([^@]+)@([^@]+)@(.*)",line)
      if debug > 1: print line
      if debug > 0: print "Commit {0} user={1} time={2} msg=[{3}]"\
                    .format(chash,user,timestamp,message)
      if v is None:
         # line is not a commit, assume it is file stats
         processFileLine(line,user)
         continue
      chash = v.group(1)
      user = v.group(3)
      timestamp = v.group(4)
      message = v.group(5)
      if not user in userData:
         userData[user] = {}
         userData[user]['commits'] = 0
         userData[user]['merges'] = 0
         userData[user]['pullrequests'] = 0
         userData[user]['filedata'] = {}
         userData[user]['binfiledata'] = {}
      userData[user]['commits'] += 1
      if message.find('Merge pull request') >= 0:
         userData[user]['pullrequests'] += 1
      elif message.find('Merge') >= 0:
         userData[user]['merges'] += 1

#---------------------------------------------------------
# Match a file statistics line of input
# - will be after a commit line, so user is valid
#---------------------------------------------------------
def processFileLine(line,user):
   global userData
   #v = re.match(" *(.*[^ ]) *\| *(.*)",line)  // for --stat line
   v = re.match("([0-9-]+)\t([0-9-]+)\t(.*)",line)
   if v is None:
      return
   filetype = os.path.splitext(v.group(3))[1]
   if filetype =='':
      filetype = 'no-ext'
   added = v.group(1)
   deleted = v.group(2)
   if debug > 0: print "  File ({0})  info ({1} {2})".\
                 format(filetype,added,deleted)
   if added.isdigit() and deleted.isdigit():
      if not filetype in userData[user]['filedata']:
         userData[user]['filedata'][filetype] = (int(added),int(deleted))
      else:
         cadd = userData[user]['filedata'][filetype][0]
         cdel = userData[user]['filedata'][filetype][1]
         userData[user]['filedata'][filetype] = \
                                 (int(added)+cadd,int(deleted)+cdel)
   else:
      if not filetype in userData[user]['binfiledata']:
         userData[user]['binfiledata'][filetype] = 1
      else:
         userData[user]['binfiledata'][filetype] += 1

#---------------------------------------------------------
# Walk the data and output the results
#---------------------------------------------------------
def outputUserData():
   print "User statistics, generated on {0}".format(str(datetime.datetime.now()))
   print "------"
   for user in userData:
      print "User: {0:16} commits:{1:<8} pullrequests:{3:<8} othermerges:{2:<8}".\
            format(user,userData[user]['commits'],userData[user]['merges'],\
                   userData[user]['pullrequests'])
      for tfile in userData[user]['filedata']:
         print "   filetype:{0:10} added:{1:<9}  removed:{2}".format(tfile,\
               userData[user]['filedata'][tfile][0],\
               userData[user]['filedata'][tfile][1])
      for bfile in userData[user]['binfiledata']:
         print "   binfile:{0:11} number:{1}".format(bfile,\
               userData[user]['binfiledata'][bfile])
      print "------"
   
#---------------------------------------------------------
# MAIN
#---------------------------------------------------------

# No arguments for now

processGitLogCmd()
outputUserData()
quit()


