#!/usr/bin/env python
# Copyright 2013 Javier Ayala
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os
import sys
import argparse
import pyrax
import pyrax.exceptions as exc
import time
from helpers import bcolors, raxLogin

# Pre-defined Variables
defConfigFile = os.path.expanduser('~') + '/.pyrax.cfg'
progName = 'RAX Challenge-inator 3000'

# Argument Parsing
raxParse = argparse.ArgumentParser(description='Challenge 3 of the API \
    Challenge')
raxParse.add_argument('-c', '--config', dest='configFile', help="Location of \
    the config file", default=defConfigFile)
raxParse.add_argument('-d', '--dir', dest='originDir', help="Directory \
    containing source files to upload to CF Container", required=True)
raxParse.add_argument('-cn', '--container', dest='contName', help="Name \
    of the new CF Container to hold the uploaded files", required=True)
raxParse.add_argument('-dfw', action='store_true', help='Perform action in \
    DFW')
raxParse.add_argument('-ord', action='store_true', help='Perform action in \
    ORD')
raxParse.add_argument('-v', dest='verbose', action='store_true', help="Show \
    debug info, such as HTTP responses")
raxParse.add_argument('-V', '--version', action='version', version='%(prog)s \
    0.1 by Javier Ayala')
raxArgs = raxParse.parse_args()

# See if there is a pyrax.cfg file
configFileTest = os.path.isfile(raxArgs.configFile)

if raxArgs.verbose:
    pyrax.set_http_debug(True)
if raxArgs.dfw:
    dc = 'DFW'
elif raxArgs.ord:
    dc = 'ORD'
else:
    print "%(fail)sMust define the DC!%(endc)s" % {"fail": bcolors.FAIL,
                                                   "endc": bcolors.ENDC}
    sys.exit(1)

print "\n%(header)sWelcome to the %(progname)s! %(endc)s" % {
    "header": bcolors.HEADER, "progname": progName, "endc": bcolors.ENDC}

try:
    myLogin = raxLogin(raxArgs.configFile)
    myLogin.authenticate()
except:
    print bcolors.FAIL + "Couldn't login" + bcolors.ENDC
    sys.exit(2)

cf = pyrax.connect_to_cloudfiles(region=dc)

try:
    originDir = os.access(raxArgs.originDir, os.R_OK)
except Exception as e:
    print e
    print("%(fail)sException: "
          "%(e)s%(endc)s") % {"fail": bcolors.FAIL,
                              "e": e,
                              "endc": bcolors.ENDC}
    sys.exit(1)

if (originDir is False):
    print("%(fail)sUnable to read directory: "
          "%(origindir)s %(endc)s") % {"fail": bcolors.FAIL,
                                       "origindir": raxArgs.originDir,
                                       "endc": bcolors.ENDC}
    sys.exit(1)

try:
    cont = cf.get_container(raxArgs.contName)
    print("%(hdr)sSuccessfully found existing container %(contname)s"
          "%(endc)s") % {"hdr": bcolors.HEADER, "contname": cont.name,
                         "endc": bcolors.ENDC}
except exc.NoSuchContainer:
    print("No existing container found. Creating a new one")
    try:
        cont = cf.create_container(raxArgs.contName)
        print("%(hdr)sSuccessfully created %(contname)s"
              "%(endc)s") % {"hdr": bcolors.HEADER, "contname": cont.name,
                             "endc": bcolors.ENDC}
    except Exception as e:
        print("%(fail)sCan't create container: "
              "%(e)s%(endc)s") % {"fail": bcolors.FAIL,
                                  "e": e, "endc": bcolors.ENDC}
        sys.exit(2)


upload_key, total_bytes = cf.upload_folder(raxArgs.originDir, cont)

print("%(ok)sTotal bytes to upload: %(tb)s"
      "%(endc)s") % {"ok": bcolors.OKBLUE, "tb": total_bytes,
                     "endc": bcolors.ENDC}
uploaded = 0
while uploaded < total_bytes:
    uploaded = cf.get_uploaded(upload_key)
    print("Progress: %4.2f%%") % ((uploaded * 100.0) / total_bytes)
    time.sleep(1)

upFiles = cf.get_container_object_names(cont)
originFiles = 0
for originInfo in os.walk(raxArgs.originDir):
    originFiles += len(originInfo[2])

print("Number of files in origin directory: %s") % str(originFiles)
print("Number of files in Cloud Files container: %s") % len(upFiles)
