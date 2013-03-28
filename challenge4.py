#!/usr/bin/python
import os
import sys
import time
import re
import argparse
import getpass
import socket
import pprint
import pyrax
import pyrax.exceptions as exc
from bcolors import bcolors

# Pre-defined Variables
defConfigFile = os.path.expanduser('~') + '/.pyrax.cfg'

# Argument Parsing
raxParse = argparse.ArgumentParser(description='Challenge 4 of the API Challenge')
raxParse.add_argument('-c', '--config', dest='configFile', help="Location of the config file", default=defConfigFile)
raxParse.add_argument('-ld', '--list-domains', action='store_true', help="List Domain Names in DNS")
raxParse.add_argument('-a', '--a-record', dest='aFQDN', help="FQDN for new A record")
raxParse.add_argument('-ip', '--add-a-ip', dest='aIP', help="IP for new A record")
raxParse.add_argument('-dn', '--domain-name', dest='domain_name', help='Domain')
raxParse.add_argument('-d', dest='debug', action='store_true', help="Show debug info, such as HTTP responses")
raxParse.add_argument('-V', '--version', action='version', version='%(prog)s 0.1 by Javier Ayala')
raxArgs = raxParse.parse_args()





# See if there is a pyrax.cfg file
configFileTest = os.path.isfile(raxArgs.configFile)



def raxLoginPrompt():
    raxUser = raw_input('Username: ')
    raxAPIKey = getpass.getpass('API Key: ')
    try:
        pyrax.set_credentials(raxUser, raxAPIKey)
        print bcolors.OKBLUE + "Authentication SUCCEEDED!" + bcolors.ENDC
    except exc.AuthenticationFailed:
        print bcolors.FAIL + "Authentication Failed using the Username and API Key provided!" + bcolors.ENDC
        sys.exit(1)


def isFQDN(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1:] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
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
        #print '%(id)s: %(name)s' % {"id" : str(domain.id), "name" : domain.name}
        print '%(name)s' % {"name" : domain.name}
    dom = raw_input('Choose a domain to view records, or \'q\' to quit: ')
    if (dom == 'q'):
        sys.exit()
    domId = raxDns.find(name=dom)
    recs = raxDns.list_records(domId)
    for rec in recs:
        print rec

def raxAddDNSA():
    if (raxArgs.aFQDN == None):
        aRecName = raw_input('Input FQDN: ')
    else:
        aRecName = raxArgs.aFQDN
    if (raxArgs.aIP == None):
        aIPAddr = raw_input('Input IP: ')
    else:
        aIPAddr = raxArgs.aIP

    try:
        domid = raxDns.find(name=raxArgs.domain_name)
    except NotFound:
        print bcolors.FAIL + raxArgs.domain_name + 'NOT FOUND!!!' + bcolors.ENDC
        sys.exit()

    if (isIP(aIPAddr) == True) and (isFQDN(aRecName) == True):
        print "Creating DNS Record"
        aRec = [{
            "type": "A",
            "name": aRecName,
            "data": aIPAddr,
        }]
        print domid.add_records(aRec)
    else:
        print bcolors.FAIL + "There was a problem with your IP or FQDN! Check them!" + bcolors.ENDC
        print "IP: %s" % aIPAddr
        print "FQDN: %s" % aRecName

if (len(sys.argv) == 1):
    raxParse.print_usage()
    sys.exit()

try:
    pyrax.set_credential_file(raxArgs.configFile)
    print bcolors.OKBLUE + "Authentication SUCCEEDED!" + bcolors.ENDC
except exc.AuthenticationFailed:
    print bcolors.FAIL + "Authentication Failed using the credentials in " + str(raxArgs.configFile) + bcolors.ENDC
    raxLoginPrompt()
except exc.FileNotFound:
    print bcolors.WARNING + "No config file found: " + str(raxArgs.configFile) + bcolors.ENDC
    raxLoginPrompt()
finally:
    raxDns = pyrax.cloud_dns


if raxArgs.debug:
    pyrax.set_http_debug(True)
if raxArgs.list_domains:
    raxListDomains()
if (raxArgs.aFQDN or raxArgs.aIP):
    raxAddDNSA()

