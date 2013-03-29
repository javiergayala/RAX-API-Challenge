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
raxParse.add_argument('-ci', '--create-image', action='store_true', help="Create an Image from a server")
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

def raxCloneSvr(dc):
    """List existing servers, then prompt the user to choose a server from which to create an image."""
    servers = cs.servers.list()
    if (len(servers) < 1):
        print "%(fail)sNo servers to clone from in %(dc)s! %(endc)s" % {"fail": bcolors.FAIL, "dc": dc, "endc": bcolors.ENDC}
        sys.exit(1)
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
    return imgId

def raxCreateServer(dc, imgIDToUse):
    """Provided an Image ID, create cloned server(s) from the image."""
    numSvrsCreated = 0 # Counter for the number of servers that get created by the script
    svrsCreated = {} # Dictionary to hold info on the servers that get created
    completed = [] # Array to hold the servers that complete creation
    serverFlvrs = cs.flavors.list()
    print "%(header)s Select a flavor to use: %(endc)s" % {"header": bcolors.HEADER, "endc": bcolors.ENDC}
    for flvr in serverFlvrs:
        print "Name: " + flvr.name + " || ID:" + flvr.id
    flvrIDToUse = raw_input('ID of flavor to use: ')
    flvrNameToUse = [flvr.name for flvr in serverFlvrs if flvr.id == flvrIDToUse][0]
    try:
        numServers = int(raxArgs.numServers)
    except (ValueError, TypeError) as e:
        numServers = int(raw_input('Number of servers to create: '))
    if (raxArgs.svrBaseName == None):
        svrBaseName = raw_input('What is the server base name to use: ')
    else:
        svrBaseName = raxArgs.svrBaseName
    print 'Creating a new ' + bcolors.OKBLUE + flvrNameToUse + bcolors.ENDC + ' from Image ID ' + bcolors.OKBLUE + imgIDToUse + bcolors.ENDC + ' in ' + bcolors.WARNING + dc + bcolors.ENDC + '.'
    print 'Creating ' + str(numServers) + ' servers.'
    print 'Server name will begin with ' + svrBaseName
    imgReady = False
    while (imgReady == False):
        image = [img for img in cs.images.list() if imgIDToUse in img.id][0]
        print "Waiting for image '%(name)s' to become active: %(progress)s%%" % {"name": image.name, "progress": image.progress}
        if image.status == 'ACTIVE':
            print "Image is ready"
            imgReady = True
        else:
            time.sleep(10)
            image.get()
    for i in xrange(0, numServers):
        svrName = '%s%s' % (svrBaseName, i)
        svrsCreated[svrName] = cs.servers.create(svrName, imgIDToUse, flvrIDToUse)
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


if raxArgs.dfw:
    dc = 'DFW'
elif raxArgs.ord:
    dc = 'ORD'
elif raxArgs.lon:
    dc = 'LON'
else:
    print "%(fail)sMust define the DC!%(endc)s" % {"fail": bcolors.FAIL, "endc": bcolors.ENDC}
    sys.exit(1)

try:
    myLogin = raxLogin(raxArgs.configFile)
    myLogin.authenticate()
except:
    print bcolors.FAIL + "Couldn't login" + bcolors.ENDC
    sys.exit(2)

cs = pyrax.connect_to_cloudservers(region=dc)

if raxArgs.debug:
    pyrax.set_http_debug(True)
if raxArgs.create_image:
    raxCloneSvr(dc)
if raxArgs.create_server:
    try:
        cloneImage = raxCloneSvr(dc)
    except:
        print "%(fail)sCouldn't clone server!%(endc)s" % {"fail": bcolors.FAIL, "endc": bcolors.ENDC}
        sys.exit(1)
    raxCreateServer(dc, cloneImage)


