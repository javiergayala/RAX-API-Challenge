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
from helpers import bcolors, raxLogin

# Pre-defined Variables
defConfigFile = os.path.expanduser('~') + '/.pyrax.cfg'
progName = 'RAX Challenge-inator 8000'
metaWeb = 'X-Container-Meta-Web-Index'
indexFile = 'index.html'
indexHtml = """\
<html>
    <head>
        <title>
            Cloud Files Page
        </title>
        <style type="text/css" media="screen">
body{padding:20px;text-align:center;background:#fff}
.msgbox{position:absolute;width:400px;height:400px;left:50%;top:50%;margin-left:-200px;margin-top:-200px;border-radius:0 79px 0 79px;-moz-border-radius:0 79px;-webkit-border-radius:0 79px 0 79px;border:8px solid #000;background-color:#cf2d36}
.innerbox{position:relative;margin-top:-75px;margin-left:-400px;top:50%;left:50%;overflow:hidden}
        </style>
    </head>
    <body>
        <div class='msgbox'>
            <div class='innerbox'>
                <h1>
                    This is a CF hosted site
                </h1>
                <p>
                    By Javier Ayala
                </p>
            </div>
        </div>
    </body>
</html>
"""

# Argument Parsing
raxParse = argparse.ArgumentParser(description='Challenge 8 of the API \
    Challenge')
raxParse.add_argument('-c', '--config', dest='configFile', help="Location of \
    the config file", default=defConfigFile)
raxParse.add_argument('-co', '--container', dest='contName', help="Name \
    of the new CF Container to hold the uploaded files", required=True)
raxParse.add_argument('-dns', dest='dnsDomain', help="DNS Domain to use")
raxParse.add_argument('-cn', dest='cname', help="CNAME to use")
raxParse.add_argument('-dfw', action='store_true', help='Perform action in \
    DFW')
raxParse.add_argument('-ord', action='store_true', help='Perform action in \
    ORD')
raxParse.add_argument('-v', dest='verbose', action='store_true', help="Show \
    debug info, such as HTTP responses")
raxParse.add_argument('-V', '--version', action='version', version='%(prog)s \
    0.1 by Javier Ayala')
raxArgs = raxParse.parse_args()


def printContAttr(cont):
    """Print out the attributes of the specified container."""
    print bcolors.HEADER
    print "CDN Status"
    print "=========="
    print bcolors.OKBLUE
    print "Container: ", cont.name
    print "cdn_enabled: ", cont.cdn_ttl
    print "cdn_log_retention: ", cont.cdn_log_retention
    print "cdn_uri: ", cont.cdn_uri
    print "cdn_ssl_uri: ", cont.cdn_ssl_uri
    print "cdn_streaming_uri: ", cont.cdn_streaming_uri
    print bcolors.ENDC


if raxArgs.verbose:
    pyrax.set_http_debug(True)
if raxArgs.dfw:
    dc = 'DFW'
elif raxArgs.ord:
    dc = 'ORD'
else:
    dc = pyrax.safe_region()
if raxArgs.contName:
    contName = raxArgs.contName
else:
    contName = raw_input("Enter the name of the new container: ")
if raxArgs.dnsDomain:
    dnsDomain = raxArgs.dnsDomain
else:
    dnsDomain = raw_input("Enter the domain name (not CNAME): ")
if raxArgs.cname:
    cname = raxArgs.cname
else:
    cname = raw_input("Enter the FQDN name of the new CNAME: ")

print "\n%(header)sWelcome to the %(progname)s! %(endc)s" % {
    "header": bcolors.HEADER, "progname": progName, "endc": bcolors.ENDC}

try:
    myLogin = raxLogin(raxArgs.configFile)
    myLogin.authenticate()
except:
    print bcolors.FAIL + "Couldn't login" + bcolors.ENDC
    sys.exit(2)

cf = pyrax.connect_to_cloudfiles(region=dc)

print "\n%(header)sCreating Cloud Files Container... %(endc)s" % {
    "header": bcolors.HEADER, "endc": bcolors.ENDC}
try:
    cont = cf.create_container(contName)
    print("%(hdr)sSuccessfully created %(contname)s"
          "%(endc)s") % {"hdr": bcolors.HEADER, "contname": cont.name,
                         "endc": bcolors.ENDC}
except Exception as e:
    print("%(fail)sCan't create container: "
          "%(e)s%(endc)s") % {"fail": bcolors.FAIL,
                              "e": e, "endc": bcolors.ENDC}
    sys.exit(2)

print "\n%(header)sCreating index.html file... %(endc)s" % {
    "header": bcolors.HEADER, "endc": bcolors.ENDC}
try:
    indexObj = cf.store_object(cont, 'index.html', indexHtml)
except:
    print "\n%(fail)sERROR Creating index.html file... %(endc)s" % {
        "fail": bcolors.FAIL, "endc": bcolors.ENDC}
    sys.exit(3)

print "\n%(header)sEnabling %(mw)s for Cloud Files Container... %(endc)s" % {
    "header": bcolors.HEADER, "mw": metaWeb, "endc": bcolors.ENDC}
metaEntry = {metaWeb: indexFile}
try:
    cf.set_container_metadata(cont, metaEntry)
except:
    print "\n%(fail)sERROR Setting Meta Info... %(endc)s" % {
        "fail": bcolors.FAIL, "endc": bcolors.ENDC}
    sys.exit(3)

print "\n%(header)sEnabling CDN for Cloud Files Container... %(endc)s" % {
    "header": bcolors.HEADER, "endc": bcolors.ENDC}
cont.make_public(ttl=1200)
cont = cf.get_container(contName)
printContAttr(cont)

print "\n%(header)sCreating CNAME for %(cname)s --> %(cdn)s. %(endc)s" % {
    "header": bcolors.HEADER, "cname": cname,
    "cdn": cont.cdn_uri, "endc": bcolors.ENDC}
dns = pyrax.cloud_dns
try:
    dom = dns.find(name=dnsDomain)
except:
    print "\n%(fail)sERROR Can't find domain %(dns)s... %(endc)s" % {
        "fail": bcolors.FAIL, "dns": dnsDomain, "endc": bcolors.ENDC}
cname_rec = {"type": "CNAME",
             "name": cname,
             "data": cont.cdn_uri}
print dom.add_records(cname_rec)

print "\n%(okb)sComplete!%(endc)s" % {
    "okb": bcolors.OKBLUE, "endc": bcolors.ENDC}
