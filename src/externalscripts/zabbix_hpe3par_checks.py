#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import httplib, urllib2, pprint, sys, os, getopt, socket, time
import simplejson as json
import subprocess
import tempfile

import zabbix_hpe3par_inc

def write_host_values( sessionKey, sessionHost, ZabbixItemname ):
    hosts = zabbix_hpe3par_inc.get_hosts( sessionKey, sessionHost )
    entries = []
    senderLine = ""
    for member in hosts["members"]:
        senderLine = "%s hpe3par.host.ports[%s] %s" % ( ZabbixItemname, member["name"], len(member["FCPaths"]) )
        entries.append( senderLine )
    
    return entries

def write_cpg_values( sessionKey, sessionHost, ZabbixItemname, cpgOptions ):
    cpgs = zabbix_hpe3par_inc.get_cpgs( sessionKey, sessionHost )
    entries = []
    senderLine = ""
    cpgOptions = int(cpgOptions)

    for member in cpgs["members"]:
        if cpgOptions == 1 and member["UsrUsage"]["totalMiB"] <= 0:
            continue

        senderLine = "%s hpe3par.cpg.state[%s] %s" % ( ZabbixItemname, member["name"], member["state"] )
        entries.append( senderLine )
        senderLine = "%s hpe3par.cpg.UsrUsage.totalMib[%s] %s" % ( ZabbixItemname, member["name"], member["UsrUsage"]["totalMiB"] )
        entries.append( senderLine )
        senderLine = "%s hpe3par.cpg.UsrUsage.usedMiB[%s] %s" % ( ZabbixItemname, member["name"], member["UsrUsage"]["usedMiB"] )
        entries.append( senderLine )

    return entries

def write_system_values( sessionKey, sessionHost, ZabbixItemname ):
    system = zabbix_hpe3par_inc.get_system( sessionKey, sessionHost )

    entries = []
    senderLine = ""

    props = [ "totalNodes", "failedCapacityMiB", "totalCapacityMiB", "masterNode" ]

    for prop in props:
        senderLine = "%s hpe3par.system.%s %s" % ( ZabbixItemname, prop, system[prop] )
        entries.append( senderLine )

    return entries

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
_start = time.time()
_end = time.time()

def main( argv ):
    fetchSet = _defaultSet

    sessionHost = ''
    sessionUser = ''
    sessionPassword = ''
    sessionKey = ''
    itemname = ''
    verbose = 0
    transfer = 1
    entries = []
    cpgOptions = 1

    try:
        opts, args = getopt.getopt( argv, "hH:U:P:S:I:vx", ["Host=", "User=", "Password=", "Set=", "Itemname=", "CpgOptions="] )
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
            verbose = 1
        elif opt in ("-x"):
            transfer = 0
        elif opt in ("-c", "--CpgOptions"):
            cpgOptions = arg

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

        xtempfile = tempfile.NamedTemporaryFile(delete=True)

        if "hosts" in fetchSet:
            entries += ( write_host_values( sessionKey, sessionHost, itemname ) )

        if "system" in fetchSet:
            entries += ( write_system_values( sessionKey, sessionHost, itemname ) )

        if "cpgs" in fetchSet:
            entries += ( write_cpg_values( sessionKey, sessionHost, itemname, cpgOptions ) )

        if verbose != 0:
            print entries
        
        strin = '\n'.join( entries )
        xtempfile.write( strin )
        xtempfile.flush
        xtempfile.seek(0)

        if verbose != 0:
            print '---------- Content ----------\n', xtempfile.read()

        try:
            if transfer != 0:
                cmdSend = "zabbix_sender -z %s -i %s" % ( "127.0.0.1", xtempfile.name )
                if verbose != 0:
                    cmdSend +=  " -vv"
                    print subprocess.check_output( cmdSend, shell=True, executable='/bin/bash' )
                else:
                    result = subprocess.call( cmdSend, executable='/bin/bash', shell=True )
        except subprocess.CalledProcessError:
            print "ERROR", sys.exc_info()
        finally:
            if xtempfile != "":
                xtempfile.close()

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

        _end = time.time()
        print( _end - _start )

if __name__ == "__main__":
    main(sys.argv[1:])
