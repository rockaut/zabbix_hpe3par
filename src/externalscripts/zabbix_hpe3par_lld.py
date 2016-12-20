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

	#	result["data"].append( hosts )
	print json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))    
    
def print_usage():
    print 'usage: agent_3parwsapi -H <Host> -U <User> -P <Password> -v <Value>'

#   .--Main----------------------------------------------------------------.
#   |                        __  __       _                                |
#   |                       |  \/  | __ _(_)_ __                           |
#   |                       | |\/| |/ _` | | '_ \                          |
#   |                       | |  | | (_| | | | | |                         |
#   |                       |_|  |_|\__,_|_|_| |_|                         |
#   |                                                                      |
#   +----------------------------------------------------------------------+

_defaultValue = [ "system" ]

def main( argv ):
    fetchValue = _defaultValue

    sessionHost = ''
    sessionUser = ''
    sessionPassword = ''
    sessionKey = ''

    try:
        opts, args = getopt.getopt( argv, "hH:hU:hP:hv:hs:", ["Host=", "User=", "Password=", "Value="])
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
        elif opt in ("-v", "--Values"):
            fetchValue = arg.split(",")
        elif opt in ("-U", "--User"):
            sessionUser = arg
        elif opt in ("-P", "--Post"):
            sessionPassword = arg

    if sessionHost == "" or sessionUser == "" or sessionPassword == "":
        print_usage()
        sys.exit(2)

    try:
        sessionKey = zabbix_hpe3par_inc.get_cred( sessionHost, sessionUser, sessionPassword )

        if "hosts" in fetchValue:
        	output_hosts( sessionKey, sessionHost )

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
