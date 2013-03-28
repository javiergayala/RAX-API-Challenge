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
from helpers import bcolors, raxLogin

# Pre-defined Variables
defConfigFile = os.path.expanduser('~') + '/.pyrax.cfg'

# Argument Parsing
raxParse = argparse.ArgumentParser(description='Challenge 2 of the API Challenge')
raxParse.add_argument('-c', '--config', dest='configFile', help="Location of the config file", default=defConfigFile)
raxParse.add_argument('-ls', '--list-servers', action='store_true', help="List Cloud Servers")
raxParse.add_argument('-cs', '--create-server', action='store_true', help="Create Server")
raxParse.add_argument('-ns', '--number-of-servers', dest='numServers', help="Number of servers")
raxParse.add_argument('-sn', '--server-name', dest='svrBaseName', help="Base name of servers")
raxParse.add_argument('-dfw', action='store_true', help='Perform action in DFW')
raxParse.add_argument('-ord', action='store_true', help='Perform action in ORD')
raxParse.add_argument('-lon', action='store_true', help='Perform action in LON')
raxParse.add_argument('-d', dest='debug', action='store_true', help="Show debug info, such as HTTP responses")
raxParse.add_argument('-V', '--version', action='version', version='%(prog)s 0.1 by Javier Ayala')
raxArgs = raxParse.parse_args()

# See if there is a pyrax.cfg file
configFileTest = os.path.isfile(raxArgs.configFile)

def raxListServers(dc):
    # Connect to Cloud Servers via dc
    cs = pyrax.connect_to_cloudservers(region=dc)
    servers = cs.servers.list()
    server_dict = {}
    print "%(header)s Select a server to clone from: %(endc)s" % {"header": bcolors.HEADER, "endc": bcolors.ENDC}
    for pos, srv in enumerate(servers):
        print "%s: %s" % (pos, srv.name)
        server_dict[str(pos)] = srv.id
    srv2img = None
    while srv2img not in server_dict:
        if srv2img is not None:
            print "  -- Invalid choice"
        srv2img = raw_input("Enter the number for your choice: ")

    srv2imgId = server_dict[srv2img]
    print
    imgName = raw_input("Enter a name for the image: ")

    imgId = cs.servers.create_image(srv2imgId, imgName)
    print "Image '%s' is being created with ID '%s'" % (imgName, imgId)

def raxGetImgStatus(dc, imgId):
    cs = pyrax.connect_to_cloudservers(region=dc)
    imgStatus = cs.images.get(imgId)
    print str(imgStatus)

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
if (len(sys.argv) == 1):
    raxParse.print_usage()
    sys.exit()

try:
    myLogin = raxLogin(raxArgs.configFile)
    myLogin.authenticate()
except:
    print bcolors.FAIL + "Couldn't login" + bcolors.ENDC
    sys.exit()

if raxArgs.debug:
    pyrax.set_http_debug(True)
if raxArgs.list_servers:
    raxGetImgStatus('ORD', raxArgs.numServers)
if raxArgs.create_server:
    if raxArgs.dfw:
        raxListServers('DFW')
    if raxArgs.ord:
        raxListServers('ORD')
    if raxArgs.lon:
        raxListServers('lon')


