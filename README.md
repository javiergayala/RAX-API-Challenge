RAX-API-Challenge
=================

Script submissions for the Rackspace Support Cloud API Challenge using pyrax


## Challenge 1 _(challenge1.py)_ ##
#### Cloud Servers ####

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
	  -d                    Show debug info, such as HTTP responses
	  -V, --version         show program's version number and exit
	  
## Challenge 2 _(challenge2.py)_ ##
#### Cloud Servers ####

__Goal:__ Write a script that clones a server (takes an image and deploys the image as a new server).

	usage: challenge2.py [-h] [-c CONFIGFILE] [-ci] [-cs] [-ns NUMSERVERS]
                     [-sn SVRBASENAME] [-dfw] [-ord] [-lon] [-d] [-V]

	Challenge 2 of the API Challenge
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONFIGFILE, --config CONFIGFILE
	                        Location of the config file
	  -ci, --create-image   Create an Image from a server
	  -cs, --create-server  Create Server
	  -ns NUMSERVERS, --number-of-servers NUMSERVERS
	                        Number of servers
	  -sn SVRBASENAME, --server-name SVRBASENAME
	                        Base name of servers
	  -dfw                  Perform action in DFW
	  -ord                  Perform action in ORD
	  -lon                  Perform action in LON
	  -d                    Show debug info, such as HTTP responses
	  -V, --version         show program's version number and exit
	  
## Challenge 3 _(challenge3.py)_ ##
#### Cloud Files ####

__Goal:__ Write a script that accepts a directory as an argument as well as a container name. The script should upload the contents of the specified directory to the container (or create it if it doesn't exist). The script should handle errors appropriately. (Check for invalid paths, etc.)

	usage: challenge3.py [-h] [-c CONFIGFILE] -d ORIGINDIR -cn CONTNAME [-dfw]
                     [-ord] [-v] [-V]

	Challenge 3 of the API Challenge

	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONFIGFILE, --config CONFIGFILE
	                        Location of the config file
	  -d ORIGINDIR, --dir ORIGINDIR
	                        Directory containing source files to upload to CF
	                        Container
	  -cn CONTNAME, --container CONTNAME
	                        Name of the new CF Container to hold the uploaded
	                        files
	  -dfw                  Perform action in DFW
	  -ord                  Perform action in ORD
	  -v                    Show debug info, such as HTTP responses
	  -V, --version         show program's version number and exit
## Challenge 4 _(challenge4.py)_ ##
#### Cloud DNS ####

__Goal:__ Write a script that uses Cloud DNS to create a new A record when passed a FQDN and IP address as arguments.  

	usage: challenge4.py [-h] [-c CONFIGFILE] [-dls] [-da AFQDN] [-dip AIP] [-V]

	Challenge 4 of the API Challenge
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONFIGFILE, --config CONFIGFILE
	                        Location of the config file
	  -ld, --list-domains   List Domain Names in DNS
	  -a AFQDN, --a-record AFQDN
	                        FQDN for new A record
	  -ip AIP, --add-a-ip AIP
	                        IP for new A record
	  -dn DOMAIN_NAME, --domain-name DOMAIN_NAME
	                        Domain
	  -d                    Debug
	  -V, --version         show program's version number and exit
	  
## Challenge 5 _(challenge5.py)_ ##
#### Cloud Databases ####

__Goal:__ Write a script that creates a Cloud Database instance. This instance should contain at least one database, and the database should have at least one user that can connect to it.

	usage: challenge5.py [-h] [-c CONFIGFILE] [-cd] [-di INSTANCENAME]
                     [-dn DBNAME] [-du DBUSER] [-dp DBPASS] [-dfw] [-ord] [-d]
                     [-V]

	Challenge 5 of the API Challenge
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONFIGFILE, --config CONFIGFILE
	                        Location of the config file
	  -cd, --create-db      Create a Cloud Database
	  -di INSTANCENAME, --db-instance INSTANCENAME
	                        Name of the Database Instance
	  -dn DBNAME, --db-name DBNAME
	                        Name of the Database
	  -du DBUSER, --db-user DBUSER
	                        Name of the Database User
	  -dp DBPASS, --db-pass DBPASS
	                        Password for the Database User
	  -dfw                  Perform action in DFW
	  -ord                  Perform action in ORD
	  -d                    Show debug info, such as HTTP responses
	  -V, --version         show program's version number and exit
	  
## Challenge 6 _(challenge6.py)_ ##
#### Cloud Files (CDN) ####

__Goal:__ Write a script that creates a CDN-enabled container in Cloud Files.

	usage: challenge6.py [-h] [-c CONFIGFILE] -cn CONTNAME [-dfw] [-ord] [-v] [-V]

	Challenge 6 of the API Challenge

	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONFIGFILE, --config CONFIGFILE
	                        Location of the config file
	  -cn CONTNAME, --container CONTNAME
	                        Name of the new CF Container to hold the uploaded
	                        files
	  -dfw                  Perform action in DFW
	  -ord                  Perform action in ORD
	  -v                    Show debug info, such as HTTP responses
	  -V, --version         show program's version number and exit
## Challenge 7 _(challenge7.py)_ ##
#### Cloud Loadbalancers ####

__Goal:__ Write a script that will create 2 Cloud Servers and add them as nodes to a new Cloud Load Balancer.

	usage: challenge7.py [-h] [-c CONFIGFILE] [-sn SVRBASENAME] [-si IMGIDTOUSE]
                     [-sf FLVRIDTOUSE] [-ln LBNAME] [-n NUMSERVERS] [-dfw]
                     [-ord] [-v] [-V]

	Challenge 7 of the API Challenge

	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONFIGFILE, --config CONFIGFILE
	                        Location of the config file
	  -sn SVRBASENAME, --server-name SVRBASENAME
	                        Base name of the newly created servers
	  -si IMGIDTOUSE, --server-image IMGIDTOUSE
	                        ID of the server image to use
	  -sf FLVRIDTOUSE, --server-flavor FLVRIDTOUSE
	                        ID of the server flavor to use
	  -ln LBNAME, --lb-name LBNAME
	                        Name of the load-balacer to create
	  -n NUMSERVERS, --num-servers NUMSERVERS
	                        Number of servers to create
	  -dfw                  Perform action in DFW
	  -ord                  Perform action in ORD
	  -v                    Show debug info, such as HTTP responses
	  -V, --version         show program's version number and exit
## Challenge 8 _(challenge8.py)_ ##
#### Cloud Files (CDN) & Cloud DNS ####

__Goal:__ Write a script that will create a static webpage served out of Cloud Files. The script must create a new container, cdn enable it, enable it to serve an index file, create an index file object, upload the object to the container, and create a CNAME record pointing to the CDN URL of the container.

	usage: challenge8.py [-h] [-c CONFIGFILE] -co CONTNAME [-dns DNSDOMAIN]
                     [-cn CNAME] [-dfw] [-ord] [-v] [-V]

	Challenge 8 of the API Challenge

	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONFIGFILE, --config CONFIGFILE
	                        Location of the config file
	  -co CONTNAME, --container CONTNAME
	                        Name of the new CF Container to hold the uploaded
	                        files
	  -dns DNSDOMAIN        DNS Domain to use
	  -cn CNAME             CNAME to use
	  -dfw                  Perform action in DFW
	  -ord                  Perform action in ORD
	  -v                    Show debug info, such as HTTP responses
	  -V, --version         show program's version number and exit
## Requirements ##

- Rackspace Cloud Account
- Python 2.7 or higher
- pyrax Python Module

## Status ##

Currently a work in progress