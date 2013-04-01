#!/usr/bin/python
import os
import sys
import argparse
import getpass
import time
import pyrax
from helpers import bcolors, raxLogin

# Pre-defined Variables
defConfigFile = os.path.expanduser('~') + '/.pyrax.cfg'
dbName = None

# Argument Parsing
raxParse = argparse.ArgumentParser(description='Challenge 5 of the API \
    Challenge')
raxParse.add_argument('-c', '--config', dest='configFile', help="Location of \
    the config file", default=defConfigFile)
raxParse.add_argument('-cd', '--create-db', action='store_true', help="Create \
    a Cloud Database")
raxParse.add_argument('-di', '--db-instance', dest='instanceName', help="Name \
    of the Database Instance")
raxParse.add_argument('-dn', '--db-name', dest='dbName', help="Name of the \
    Database")
raxParse.add_argument('-du', '--db-user', dest='dbUser', help="Name of the \
    Database User")
raxParse.add_argument('-dp', '--db-pass', dest='dbPass', help="Password for \
    the Database User")
raxParse.add_argument('-dfw', action='store_true', help='Perform action in \
    DFW')
raxParse.add_argument('-ord', action='store_true', help='Perform action in \
    ORD')
raxParse.add_argument('-d', dest='debug', action='store_true', help="Show \
    debug info, such as HTTP responses")
raxParse.add_argument('-V', '--version', action='version', version='%(prog)s \
    0.1 by Javier Ayala')
raxArgs = raxParse.parse_args()

# See if there is a pyrax.cfg file
configFileTest = os.path.isfile(raxArgs.configFile)


def raxCreateInstance():
    """Create a new Cloud Database Instance"""
    flavors = cdb.list_flavors()
    print "%(header)s Available Cloud DB Flavors: %(endc)s" % {
        "header": bcolors.HEADER, "endc": bcolors.ENDC}
    for pos, flavor in enumerate(flavors):
        print "%s: %s [%s]" % (pos, flavor.name, flavor.ram)
    flavor2use = int(raw_input(
        "Select a Flavor for the new Cloud DB Instance: "))
    if (raxArgs.instanceName is None):
        instanceName = raw_input("Enter a name for your  Cloud DB Instance: ")
    else:
        instanceName = raxArgs.instanceName
    try:
        selected = flavors[flavor2use]
    except IndexError:
        print "%(fail)sInvalid Flavor Selection!%(endc)s" % {
            "fail": bcolors.FAIL, "endc": bcolors.ENDC}
        sys.exit(1)

    instanceSize = int(raw_input("Enter the Instance Size in GB(1-50): "))
    if ((instanceSize < 1) or (instanceSize > 50)):
        print "%(fail)sInstance Size MUST be between 1-50!%(endc)s" % {
            "fail": bcolors.FAIL, "endc": bcolors.ENDC}
        sys.exit(1)

    newInstance = cdb.create(instanceName, flavor=selected,
                             volume=instanceSize)
    dbInstReady = False
    while (dbInstReady is False):
        print "Waiting for instance '%(name)s' to become active..." \
            % {"name": newInstance.name}
        if newInstance.status == 'ACTIVE':
            print "Instance is ready"
            dbInstReady = True
        else:
            time.sleep(30)
            newInstance.get()

    return newInstance


def raxCreateDb(dbInst):
    """Provided an Instance ID, create a cloud database on the instance."""
    if (raxArgs.dbName is None):
        dbName = raw_input("Enter the name of the new database: ")
    else:
        dbName = raxArgs.dbName

    newDbObj = dbInst.create_database(dbName)
    return newDbObj


def raxCreateUser(dbInst, dbName):
    """Provided a Cloud DB Instance and DB Name, create a cloud database user
        on the instance for that database."""
    if (raxArgs.dbUser is None):
        dbUser = raw_input("Enter the name of the new database user: ")
    else:
        dbUser = raxArgs.dbUser
    if (raxArgs.dbPass is None):
        dbPass = getpass.getpass("Enter the password for the new user: ")
    else:
        dbPass = raxArgs.dbPass

    newUserObj = dbInst.create_user(dbUser, dbPass, database_names=dbName)
    return newUserObj


if (len(sys.argv) == 1):
    raxParse.print_usage()
    sys.exit()


if raxArgs.dfw:
    dc = 'DFW'
elif raxArgs.ord:
    dc = 'ORD'
else:
    print "%(fail)sMust define the DC!%(endc)s" % {"fail": bcolors.FAIL,
                                                   "endc": bcolors.ENDC}
    sys.exit(1)

try:
    myLogin = raxLogin(raxArgs.configFile)
    myLogin.authenticate()
except:
    print bcolors.FAIL + "Couldn't login" + bcolors.ENDC
    sys.exit(2)

cdb = pyrax.connect_to_cloud_databases(region=dc)

if raxArgs.debug:
    pyrax.set_http_debug(True)
if raxArgs.create_db:
    try:
        newDbInst = raxCreateInstance()
    except:
        print "%(fail)sUnable to create a new Cloud DB Instance!%(endc)s" % {
            "fail": bcolors.FAIL, "endc": bcolors.ENDC}
        print sys.exc_info()[0]
        sys.exit(2)

    try:
        newDbObj = raxCreateDb(newDbInst)
    except:
        print "%(fail)sUnable to create a new Cloud Database!%(endc)s" % {
            "fail": bcolors.FAIL, "endc": bcolors.ENDC}
        sys.exit(3)

    try:
        newDbUserObj = raxCreateUser(newDbInst, newDbObj.name)
    except:
        print "%(fail)sUnable to create a new Cloud DB User!%(endc)s" % {
            "fail": bcolors.FAIL, "endc": bcolors.ENDC}
        sys.exit(4)

    print
    print "%(hdr)sOperation Complete!%(endc)s" % {
        "hdr": bcolors.HEADER, "endc": bcolors.ENDC}
    print "Instance Created: %s" % newDbInst.name
    print "Instance Hostname: %s" % newDbInst.hostname
    print "Database Created: %s" % newDbObj.name
    print "%(ok)sUser '%(dbuser)s' given rights to '%(dbname)s'%(endc)s" % {
        "ok": bcolors.OKBLUE, "dbuser": newDbUserObj.name,
        "dbname": newDbObj.name, "endc": bcolors.ENDC}
