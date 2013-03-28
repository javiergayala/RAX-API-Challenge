RAX-API-Challenge
=================

Script submissions for the Rackspace Support Cloud API Challenge using pyrax


## Challenge 1 _(challenge1.py)_ ##

__Goal:__ Write a script that builds three 512MB Cloud Servers that follow a similar naming convention. (i.e. web1, web2, web3) and returns the IP and login credentials for each server.  Use any image.  

	usage: challenge1.py [-h] [-c CONFIGFILE] [-ls] [-cs] [-ns NUMSERVERS]
                     [-sn SVRBASENAME] [-dfw] [-ord] [-lon] [-V]

	Challenge 1 of the API Challenge
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONFIGFILE, --config CONFIGFILE
	                        Location of the config file
	  -ls, --list-servers   List Cloud Servers
	  -cs, --create-server  Create Server
	  -ns NUMSERVERS, --number-of-servers NUMSERVERS
	                        Number of servers
	  -sn SVRBASENAME, --server-name SVRBASENAME
	                        Base name of servers
	  -dfw                  Perform action in DFW
	  -ord                  Perform action in ORD
	  -lon                  Perform action in LON
	  -V, --version         show program's version number and exit
	  
## Challenge 4 _(challenge4.py)_ ##

__Goal:__ Write a script that uses Cloud DNS to create a new A record when passed a FQDN and IP address as arguments.  

	usage: challenge4.py [-h] [-c CONFIGFILE] [-dls] [-da AFQDN] [-dip AIP] [-V]

	Challenge 4 of the API Challenge
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONFIGFILE, --config CONFIGFILE
	                        Location of the config file
	  -dls, --list-domains  List Domain Names in DNS
	  -da AFQDN, --add-a-record AFQDN
	                        FQDN for new A record
	  -dip AIP, --add-a-ip AIP
	                        IP for new A record
	  -V, --version         show program's version number and exit
	  
## Requirements ##

- Rackspace Cloud Account

## Status ##

Currently a work in progress