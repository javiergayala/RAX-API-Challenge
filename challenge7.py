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
import time
import pyrax
from helpers import bcolors, raxLogin

# Pre-defined Variables
defConfigFile = os.path.expanduser('~') + '/.pyrax.cfg'
progName = 'RAX Challenge-inator 7000'


def raxListImages(raxCldSvr):
    serverImgs = raxCldSvr.images.list()
    for img in sorted(serverImgs, key=lambda serverImgs: serverImgs.name):
        print img.name, " || ID:", img.id
    imgIDToUse = raw_input('ID of image to use: ')
    serverFlvrs = raxCldSvr.flavors.list()
    for flvr in serverFlvrs:
        print "Name: " + flvr.name + " || ID:" + flvr.id
    flvrIDToUse = raw_input('ID of flavor to use: ')
    return imgIDToUse, flvrIDToUse


def raxCreateServer(raxCldSvr, numServers, svrBaseName, imgIDToUse,
                    flvrIDToUse):
    svrsCreated = {}  # Dictionary to hold info on the servers that get created
    nodeInfo = {}  # Dictionary to hold Private IPs of the nodes
    completed = []  # Array to hold the servers that complete creation
    print 'Creating ' + str(numServers) + ' servers.'
    print 'Server name will begin with ' + svrBaseName
    for i in xrange(0, numServers):
        svrName = '%s%s' % (svrBaseName, i)
        svrsCreated[svrName] = raxCldSvr.servers.create(svrName, imgIDToUse,
                                                        flvrIDToUse)
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
                    print 'Status: %s %s %s' % bcolors.FAIL, server.status, \
                        bcolors.ENDC
                else:
                    print 'Status: %s' % server.status
                print 'ID: %s' % server.id
                print 'Networks: %s' % server.networks
                nodeInfo[name] = {}
                nodeInfo[name]['privateIp'] = \
                    str(server.networks['private'][0])
                print 'Password: %s' % server.adminPass
                completed.append(name)
    return nodeInfo

# Argument Parsing
raxParse = argparse.ArgumentParser(description='Challenge 7 of the API \
    Challenge')
raxParse.add_argument('-c', '--config', dest='configFile', help="Location of \
    the config file", default=defConfigFile)
raxParse.add_argument('-sn', '--server-name', dest='svrBaseName', help="Base \
    name of the newly created servers")
raxParse.add_argument('-ln', '--lb-name', dest='lbName', help="Name \
    of the load-balacer to create")
raxParse.add_argument('-n', '--num-servers', dest='numServers', help="Number \
    of servers to create")
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


raxCldSvr = pyrax.connect_to_cloudservers(region=dc)
raxCldLB = pyrax.connect_to_cloud_loadbalancers(region=dc)

if (raxArgs.svrBaseName is None):
    svrBaseName = raw_input('What is the server base name to use: ')
else:
    svrBaseName = raxArgs.svrBaseName
try:
    numServers = int(raxArgs.numServers)
except (ValueError, TypeError):
    numServers = int(raw_input('Number of servers to create: '))
if (raxArgs.lbName is None):
    lbName = raw_input('What is the name of the new load-balancer: ')
else:
    lbName = raxArgs.lbName

imgIDToUse, flvrIDToUse = raxListImages(raxCldSvr)

lbNodes = raxCreateServer(raxCldSvr, numServers, svrBaseName, imgIDToUse,
                          flvrIDToUse)

nodes = {}
print "\n%(header)sCreating LB Nodes! %(endc)s" % {
    "header": bcolors.HEADER, "endc": bcolors.ENDC}
for name in lbNodes:
    nodes[name] = raxCldLB.Node(address=name['privateIp'], port=80,
                                condition='ENABLED')
    print "%(name)s node created..." % name
print "\n%(header)sCreating LB VIP! %(endc)s" % {
    "header": bcolors.HEADER, "endc": bcolors.ENDC}
vip = raxCldLB.VirtualIP(type='PUBLIC')
print "\n%(header)sPiecing it all together! %(endc)s" % {
    "header": bcolors.HEADER, "endc": bcolors.ENDC}
newLb = raxCldLB.create(lbName, port=80, protocol="HTTP", nodes=nodes,
                        virtual_ips=[vip])

print str(newLb)
print str(lbNodes)