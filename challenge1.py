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
raxParse = argparse.ArgumentParser(description='Challenge 1 of the API Challenge')
raxParse.add_argument('-c', '--config', dest='configFile', help="Location of the config file", default=defConfigFile)
raxParse.add_argument('-ls', '--list-servers', action='store_true', help="List Cloud Servers")
raxParse.add_argument('-cs', '--create-server', action='store_true', help="Create Server")
raxParse.add_argument('-ns', '--number-of-servers', dest='numServers', help="Number of servers")
raxParse.add_argument('-sn', '--server-name', dest='svrBaseName', help="Base name of servers")
raxParse.add_argument('-dfw', action='store_true', help='Perform action in DFW')
raxParse.add_argument('-ord', action='store_true', help='Perform action in ORD')
raxParse.add_argument('-lon', action='store_true', help='Perform action in LON')
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

def raxListServers():
    if (raxArgs.dfw or raxArgs.ord or raxArgs.lon):
        ls_pp = pprint.PrettyPrinter(indent=4)
        # Print Server List
        print ""
        print bcolors.HEADER + "Server List"
        print "===========" + bcolors.ENDC
    else:
        print bcolors.FAIL + 'You MUST specify a DC' + bcolors.ENDC
    # Connect to Cloud Servers via dc
    if raxArgs.dfw:
        cs_dfw = pyrax.connect_to_cloudservers(region="DFW")
        dfw_servers = cs_dfw.servers.list()
        print "DFW: "
        ls_pp.pprint(dfw_servers)
    if raxArgs.ord:
        cs_ord = pyrax.connect_to_cloudservers(region="ORD")
        ord_servers = cs_ord.servers.list()
        print "ORD: "
        ls_pp.pprint(ord_servers)
    if raxArgs.lon:
        cs_lon = pyrax.connect_to_cloudservers(region="LON")
        lon_servers = cs_lon.servers.list()
        print "LON: " 
        ls_pp.pprint(lon_servers)

def raxCreateServer(dc):
    raxCldSvr = pyrax.connect_to_cloudservers(region=dc)
    serverImgs = raxCldSvr.images.list()
    numSvrsCreated = 0 # Counter for the number of servers that get created by the script
    svrsCreated = {} # Dictionary to hold info on the servers that get created
    completed = [] # Array to hold the servers that complete creation
    for img in sorted(serverImgs, key=lambda serverImgs: serverImgs.name):
        print img.name, " || ID:", img.id
    imgIDToUse = raw_input('ID of image to use: ')
    imgNameToUse = [img.name for img in serverImgs if img.id == imgIDToUse][0]
    #print str(imgToUse)
    serverFlvrs = raxCldSvr.flavors.list()
    for flvr in serverFlvrs:
        print "Name: " + flvr.name + " || ID:" + flvr.id
    flvrIDToUse = raw_input('ID of flavor to use: ')
    flvrNameToUse = [flvr.name for flvr in serverFlvrs if flvr.id == flvrIDToUse][0]
    print 'Using ' + bcolors.OKBLUE + imgNameToUse + bcolors.ENDC
    try:
        numServers = int(raxArgs.numServers)
    except (ValueError, TypeError) as e:
        numServers = int(raw_input('Number of servers to create: '))
    if (raxArgs.svrBaseName == None):
        svrBaseName = raw_input('What is the server base name to use: ')
    else:
        svrBaseName = raxArgs.svrBaseName
    print 'Creating a new ' + bcolors.OKBLUE + flvrNameToUse + bcolors.ENDC + ' with ' + bcolors.OKBLUE + imgNameToUse + bcolors.ENDC + ' in ' + bcolors.WARNING + dc + bcolors.ENDC + '.'
    print 'Creating ' + str(numServers) + ' servers.'
    print 'Server name will begin with ' + svrBaseName

    for i in xrange(0, numServers):
        svrName = '%s%s' % (svrBaseName, i)
        svrsCreated[svrName] = raxCldSvr.servers.create(svrName, imgIDToUse, flvrIDToUse)
        print "Created server: %s" % svrName
    sys.stdout.write("Waiting for builds to complete")
    sys.stdout.flush()
    while len(completed) < numServers:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(30)
        for name, server in svrsCreated.iteritems():
            if name in completed:
                continue
            server.get()
            if server.status in ['ACTIVE', 'ERROR', 'UNKNOWN']:
                sys.stdout.write("\n")
                print '======================================='
                print 'Name: %s' % server.name
                if (server.status == 'ERROR'):
                    print 'Status: %s %s %s' % bcolors.FAIL, server.status, bcolors.ENDC
                else:
                    print 'Status: %s' % server.status
                print 'ID: %s' % server.id
                print 'Networks: %s' % server.networks
                print 'Password: %s' % server.adminPass
                completed.append(name)


try:
    pyrax.set_credential_file(raxArgs.configFile)
    print bcolors.OKBLUE + "Authentication SUCCEEDED!" + bcolors.ENDC
except exc.AuthenticationFailed:
    print bcolors.FAIL + "Authentication Failed using the credentials in " + str(raxArgs.configFile) + bcolors.ENDC
    raxLoginPrompt()
except exc.FileNotFound:
    print bcolors.WARNING + "No config file found: " + str(raxArgs.configFile) + bcolors.ENDC
    raxLoginPrompt()

if raxArgs.list_servers:
    raxListServers()
if raxArgs.create_server:
    if raxArgs.dfw:
        raxCreateServer('DFW')
    if raxArgs.ord:
        raxCreateServer('ORD')
    if raxArgs.lon:
        raxCreateServer('lon')


