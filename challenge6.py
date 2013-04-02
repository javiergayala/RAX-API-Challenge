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
from helpers import bcolors, raxLogin

# Pre-defined Variables
defConfigFile = os.path.expanduser('~') + '/.pyrax.cfg'
progName = 'RAX Challenge-inator 6000'

# Functions


def printContAttr(cont, state):
    """Print out the attributes of the specified container."""
    print bcolors.HEADER
    print "%s CDN Status" % state
    print "=================="
    print bcolors.OKBLUE
    print "Container: ", cont.name
    print "cdn_enabled: ", cont.cdn_ttl
    print "cdn_log_retention: ", cont.cdn_log_retention
    print "cdn_uri: ", cont.cdn_uri
    print "cdn_ssl_uri: ", cont.cdn_ssl_uri
    print "cdn_streaming_uri: ", cont.cdn_streaming_uri
    print bcolors.ENDC


# Argument Parsing
raxParse = argparse.ArgumentParser(description='Challenge 6 of the API \
    Challenge')
raxParse.add_argument('-c', '--config', dest='configFile', help="Location of \
    the config file", default=defConfigFile)
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

if raxArgs.verbose:
    pyrax.set_http_debug(True)
if raxArgs.dfw:
    dc = 'DFW'
elif raxArgs.ord:
    dc = 'ORD'
else:
    dc = pyrax.safe_region()

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

if (cont.cdn_enabled is False):
    printContAttr(cont, "BEFORE")
    cont.make_public(ttl=1200)
    cont = cf.get_container(raxArgs.contName)
    printContAttr(cont, "AFTER")
else:
    print("%s is already CDN-enabled") % raxArgs.contName
    printContAttr(cont, "CURRENT")
