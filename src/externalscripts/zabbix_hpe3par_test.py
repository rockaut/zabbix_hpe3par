#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import httplib, urllib2, pprint, sys, os, getopt, socket
import simplejson as json
import subprocess
import tempfile

import zabbix_hpe3par_inc

def write_host_values( tempfile, sessionKey, sessionHost ):
    hosts = zabbix_hpe3par_inc.get_hosts( sessionKey, sessionHost )
    senderLine = ""
    for member in hosts["members"]:
        if senderLine != "":
            xtempfile.write( "\n" )
        senderLine = "%s hpe3par.host.ports[%s] %s" % ( itemname, member["name"], len(member["FCPaths"]) )
        xtempfile.write( senderLine )

    xtempfile.flush()

def print_usage():
    print 'usage: -H <Host> -U <User> -P <Password> -S <Set> -I <ZabbixItemname>'

#   .--Main----------------------------------------------------------------.
#   |                        __  __       _                                |
#   |                       |  \/  | __ _(_)_ __                           |
#   |                       | |\/| |/ _` | | '_ \                          |
#   |                       | |  | | (_| | | | | |                         |
#   |                       |_|  |_|\__,_|_|_| |_|                         |
#   |                                                                      |
#   +----------------------------------------------------------------------+

_defaultSet = [ "system" ]

def main( argv ):
    fetchSet = _defaultSet

    sessionHost = ''
    sessionUser = ''
    sessionPassword = ''
    sessionKey = ''
    itemname = ''
    verbose = 0

    try:
        opts, args = getopt.getopt( argv, "hH:U:P:S:I:v:", ["Host=", "User=", "Password=", "Set=", "Itemname=","verbose="] )
        if not opts:
            print_usage()
            sys.exit(2)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-H", "--Host"):
            sessionHost = arg
        elif opt in ("-S", "--Set"):
            fetchSet = arg.split(",")
        elif opt in ("-U", "--User"):
            sessionUser = arg
        elif opt in ("-P", "--Password"):
            sessionPassword = arg
        elif opt in ("-I", "--Itemname"):
            itemname = arg
        elif opt in ("-v", "--Verbose"):
            verbose = arg

    if sessionHost == "" or sessionUser == "" or sessionPassword == "" or itemname == "":
        if sessionHost == "":
            print " - sessionHost missing"
        if sessionUser == "":
            print " - sessionUser missing"
        if sessionPassword == "":
            print " - sessionPassword missing"
        if itemname == "":
            print " - itemname missing"
        print_usage()
        sys.exit(2)

    try:
        sessionKey = zabbix_hpe3par_inc.get_cred( sessionHost, sessionUser, sessionPassword )

        print tempfile.gettempdir()

        xtempfile = tempfile.NamedTemporaryFile(delete=True)

        print 'File: ', xtempfile.name

        if "hosts" in fetchSet:
            write_host_values( xtempfile, sessionKey, sessionHost )   

        xtempfile.seek(0)
        print 'Content: ', xtempfile.read()

        #cmdSend = "zabbix_sender -z %s -i %s" % ( "127.0.0.1", xtempfile.name )
        #if verbose != 0:
        #    cmdSend +=  " -vv"
        #    print subprocess.check_output( cmdSend, shell=True, executable='/bin/bash' )
        #else:
        #    result = subprocess.check_output( cmdSend, shell=True, executable='/bin/bash' )

    except:
        print("Unexpected error:", sys.exc_info()[0])
        if sessionKey != "":
            zabbix_hpe3par_inc.remove_cred( sessionHost, sessionKey )
        raise
    else:
        if sessionKey != "":
            zabbix_hpe3par_inc.remove_cred( sessionHost, sessionKey )
    finally:
        if xtempfile != "":
            xtempfile.close()

if __name__ == "__main__":
    main(sys.argv[1:])
