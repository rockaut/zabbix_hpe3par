#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import httplib, urllib2, pprint, sys, os, getopt, socket
import simplejson as json
import subprocess

import zabbix_hpe3par_inc

def output_hosts( sessionKey, sessionHost ):
	hosts = zabbix_hpe3par_inc.get_hosts( sessionKey, sessionHost )

	result = { "data": [] }

	for member in hosts["members"]:
		result["data"].append(
				{
					"{#HOSTNAME}": member["name"]
				}
			)

	print json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

def output_cpgs( sessionKey, sessionHost, cpgOptions ):
    cpgs = zabbix_hpe3par_inc.get_cpgs( sessionKey, sessionHost )

    result = { "data": [] }

    cpgOptions = int(cpgOptions)

    for member in cpgs["members"]:

        if cpgOptions == 1 and member["UsrUsage"]["totalMiB"] <= 0:
            continue

        result["data"].append(
                {
                    "{#CPGNAME}": member["name"],
                    "{#CPGUUID}": member["uuid"]
                }
            )

    print json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

def output_volumes( sessionKey, sessionHost ):
    volumes = zabbix_hpe3par_inc.get_volumes( sessionKey, sessionHost )

    result = { "data": [] }

    for member in volumes["members"]:
        result["data"].append(
                {
                    "{#VOLUMENAME}": member["name"],
                    "{#VOLUMEUUID}": member["uuid"]
                }
            )

    print json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

def output_ports( sessionKey, sessionHost ):
    ports = zabbix_hpe3par_inc.get_ports( sessionKey, sessionHost )
    result = { "data": [] }

    for member in ports["members"]:
        memberpos = "%s:%s:%s" % ( member["portPos"]["node"], member["portPos"]["slot"], member["portPos"]["cardPort"] )

        if "label" in member:
            label = member["label"]
        else:
            label = memberpos

        if "portWWN" in member:
            puuid = member["portWWN"]
        else:
            puuid = member["HWAddr"]

        result["data"].append(
                {
                    "{#PORTLABEL}": label,
                    "{#PORTPOS}": memberpos,
                    "{#PORTUUID}": puuid
                }
            )

    print json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

def print_usage():
    print 'usage: zabbix_hpe3par_lld -H <Host> -U <User> -P <Password> -S <Value> -c <Value>'

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
    fetchValue = _defaultSet

    sessionHost = ''
    sessionUser = ''
    sessionPassword = ''
    sessionKey = ''

    cpgOptions = 1

    try:
        opts, args = getopt.getopt( argv, "hH:U:P:S:c:", ["Host=", "User=", "Password=", "Set=", "CpgOptions="])
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
            fetchValue = arg.split(",")
        elif opt in ("-U", "--User"):
            sessionUser = arg
        elif opt in ("-P", "--Post"):
            sessionPassword = arg
        elif opt in ("-c", "--CpgOptions"):
            cpgOptions = arg

    if sessionHost == "" or sessionUser == "" or sessionPassword == "":
        print_usage()
        sys.exit(2)

    try:
        sessionKey = zabbix_hpe3par_inc.get_cred( sessionHost, sessionUser, sessionPassword )

        if "hosts" in fetchValue:
        	output_hosts( sessionKey, sessionHost )

        if "cpgs" in fetchValue:
            output_cpgs( sessionKey, sessionHost, cpgOptions )

        if "volumes" in fetchValue:
            output_volumes( sessionKey, sessionHost )

        if "ports" in fetchValue:
            output_ports( sessionKey, sessionHost )

    except:
        print("Unexpected error:", sys.exc_info()[0])
        if sessionKey != "":
            zabbix_hpe3par_inc.remove_cred( sessionHost, sessionKey )
        raise
    else:
        if sessionKey != "":
            zabbix_hpe3par_inc.remove_cred( sessionHost, sessionKey )

if __name__ == "__main__":
    main(sys.argv[1:])
