#!/usr/bin/python
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
import re
import argparse
import socket
import pyrax
import pyrax.exceptions as exc
from helpers import bcolors, raxLogin

# Pre-defined Variables
defConfigFile = os.path.expanduser('~') + '/.pyrax.cfg'

# Argument Parsing
raxParse = argparse.ArgumentParser(description='Challenge 4 of the \
     API Challenge')
raxParse.add_argument('-c', '--config', dest='configFile',
                      help="Location of the config file",
                      default=defConfigFile)
raxParse.add_argument('-ld', '--list-domains', action='store_true',
                      help="List Domain Names in DNS")
raxParse.add_argument('-a', '--a-record', dest='aFQDN',
                      help="FQDN for new A record")
raxParse.add_argument('-ip', '--add-a-ip', dest='aIP',
                      help="IP for new A record")
raxParse.add_argument('-dn', '--domain-name', dest='domain_name',
                      help='Domain')
raxParse.add_argument('-d', dest='debug', action='store_true',
                      help="Show debug info, such as HTTP responses")
raxParse.add_argument('-V', '--version', action='version',
                      version='%(prog)s 0.1 by Javier Ayala')
raxArgs = raxParse.parse_args()

# See if there is a pyrax.cfg file
configFileTest = os.path.isfile(raxArgs.configFile)


def isFQDN(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1:] == ".":
        hostname = hostname[:-1]  # strip 1 dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def isIP(ipAddr):
    try:
        socket.inet_aton(ipAddr)
        validIP = True
    except socket.error:
        validIP = False

    return validIP


def raxListDomains():
    for domain in raxDns.get_domain_iterator():
        print '%(name)s' % {"name": domain.name}
    dom = raw_input('Choose a domain to view records, or \'q\' to quit: ')
    if (dom == 'q'):
        sys.exit()
    try:
        domId = raxDns.find(name=dom)
    except exc.NotFound:
        print "%(fail)s%(dom)s not found %(endc)s" % {
            "fail": bcolors.FAIL, "dom": dom, "endc": bcolors.ENDC}
        sys.exit(1)
    recs = raxDns.list_records(domId)
    for rec in recs:
        print rec


def raxAddDNSA():
    if (raxArgs.aFQDN is None):
        aRecName = raw_input('Input FQDN: ')
    else:
        aRecName = raxArgs.aFQDN
    if (raxArgs.aIP is None):
        aIPAddr = raw_input('Input IP: ')
    else:
        aIPAddr = raxArgs.aIP

    try:
        domid = raxDns.find(name=raxArgs.domain_name)
    except exc.NotFound:
        print bcolors.FAIL + raxArgs.domain_name + 'NOT FOUND!!!' + \
            bcolors.ENDC
        sys.exit()

    if (isIP(aIPAddr) is True) and (isFQDN(aRecName) is True):
        print "Creating DNS Record"
        aRec = [{
            "type": "A",
            "name": aRecName,
            "data": aIPAddr,
        }]
        print domid.add_records(aRec)
    else:
        print bcolors.FAIL + \
            "There was a problem with your IP or FQDN! Check them!" + \
            bcolors.ENDC
        print "IP: %s" % aIPAddr
        print "FQDN: %s" % aRecName

if (len(sys.argv) == 1):
    raxParse.print_usage()
    sys.exit()

try:
    myLogin = raxLogin(raxArgs.configFile)
    myLogin.authenticate()
    raxDns = pyrax.cloud_dns
except:
    print bcolors.FAIL + "Couldn't login" + bcolors.ENDC
    sys.exit()

if raxArgs.debug:
    pyrax.set_http_debug(True)
if raxArgs.list_domains:
    raxListDomains()
if (raxArgs.aFQDN or raxArgs.aIP):
    raxAddDNSA()
