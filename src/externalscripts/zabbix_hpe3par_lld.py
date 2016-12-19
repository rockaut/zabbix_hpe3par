#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import httplib, urllib2, pprint, sys, os, getopt, socket
import simplejson as json
import subprocess

# build_apiHeaders function
def build_apiHeaders( sessionKey = "" ):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    if sessionKey == "":
        return headers

    headers["X-HP3PAR-WSAPI-SessionKey"] = sessionKey

    return headers
    # end build_apiHeaders function

# get_cred function
def get_cred( sessionHost, sessionUser, sessionPassword, sessionPort = 8080 ):
    credUrl = '/api/v1/credentials'
    credBody = '{"user":"%s","password":"%s"}' % ( sessionUser, sessionPassword )
    apiHeaders = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    conn = httplib.HTTPSConnection(sessionHost, sessionPort, timeout=10)
    conn.request("POST", credUrl, credBody, apiHeaders )
    response = conn.getresponse()
    credResponseData = response.read()
    credResponseStatus = response.status
    credResponseReason = response.reason
    conn.close()

    parsed_response = json.loads( credResponseData )

    responseSessionKey = ""

    if credResponseStatus != 201 or credResponseReason != "Created":
        raise Exception("got no session key")
        return False

    if "key" in parsed_response:
        #print json.dumps(parsed_response, sort_keys=True, indent=4, separators=(',', ': '))
        responseSessionKey = parsed_response["key"]
    else:
        print "******"
        print "%s: %s" % ( "Status", credResponseStatus )
        print "%s: %s" % ( "Reason", credResponseReason )
        print "-----"
        print "No session key received"
        print "******"
        raise Exception("got no session key")
        return False

    return ( responseSessionKey )
   # end get_cred function


def remove_cred( sessionHost, sessionKey, sessionPort = 8080 ):
    apiUrl = '/api/v1/credentials'
    apiUrl = '%s/%s' % ( apiUrl, sessionKey)
    apiHeaders = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    conn = httplib.HTTPSConnection(sessionHost, sessionPort, timeout=10)
    conn.request("DELETE", apiUrl, "", apiHeaders )
    response = conn.getresponse()
    credResponseStatus = response.status
    credResponseReason = response.reason
    conn.close()

    if credResponseStatus != 200 or credResponseReason != "OK":
        print "******"
        print "%s: %s" % ( "URL", apiUrl )
        print "%s: %s" % ( "Status", credResponseStatus )
        print "%s: %s" % ( "Reason", credResponseReason )
        print "******"

def get_system( sessionKey, sessionHost, sessionPort = 8080 ):
    volUrl = '/api/v1/system'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", volUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    #print "<<<3parwsapi.system>>>"
    #print "******"
    #print "%s: %s" % ( "Status", responseStatus )
    #print "%s: %s" % ( "Reason", responseReason )
    #print "-----"
    #print json.dumps(parsed_response, sort_keys=True, indent=4, separators=(',', ': '))
    #print "******"

    return parsed_response

def get_volumes( sessionKey, sessionHost, sessionPort = 8080 ):
    volUrl = '/api/v1/volumes'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", volUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    #print "<<<3parwsapi.volumes>>>"
    #print "******"
    #print "%s: %s" % ( "Status", responseStatus )
    #print "%s: %s" % ( "Reason", responseReason )
    #print "-----"
    #print json.dumps(parsed_response, sort_keys=True, indent=4, separators=(',', ': '))
    #print "******"

    return parsed_response

def get_hosts( sessionKey, sessionHost, sessionPort = 8080 ):
    volUrl = '/api/v1/hosts'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", volUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response

def get_cpgs( sessionKey, sessionHost, sessionPort = 8080 ):
    volUrl = '/api/v1/cpgs'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", volUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response

def get_ports( sessionKey, sessionHost, sessionPort = 8080 ):
    volUrl = '/api/v1/ports'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", volUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response

def get_flashcache( sessionKey, sessionHost, sessionPort = 8080 ):
    volUrl = '/api/v1/flashcache'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", volUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response

def get_remotecopygroups( sessionKey, sessionHost, sessionPort = 8080 ):
    qUrl = '/api/v1/remotecopygroups'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", qUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response

def get_sysrep_cachememorystatistics( sessionKey, sessionHost, sessionPort = 8080 ):
    qUrl = '/api/v1/systemreporter/attime/cachememorystatistics/hires'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", qUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response

def get_sysrep_cpgstatistics( sessionKey, sessionHost, sessionPort = 8080 ):
    qUrl = '/api/v1/systemreporter/attime/cpgstatistics/hires'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", qUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response

def get_sysrep_physicaldiskcapacity( sessionKey, sessionHost, sessionPort = 8080 ):
    qUrl = '/api/v1/systemreporter/attime/physicaldiskcapacity/hires'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", qUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response

def get_sysrep_physicaldiskspacedata( sessionKey, sessionHost, sessionPort = 8080 ):
    qUrl = '/api/v1/systemreporter/attime/physicaldiskspacedata/hires'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", qUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response
    
def get_sysrep_physicaldiskstatistics( sessionKey, sessionHost, sessionPort = 8080 ):
    qUrl = '/api/v1/systemreporter/attime/physicaldiskstatistics/hires'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", qUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response
        
def get_sysrep_vlunstatistics( sessionKey, sessionHost, sessionPort = 8080 ):
    qUrl = '/api/v1/systemreporter/attime/vlunstatistics/hires'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", qUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response

def get_sysrep_portstatistics( sessionKey, sessionHost, sessionPort = 8080 ):
    qUrl = '/api/v1/systemreporter/attime/portstatistics/hires'
    apiHeaders = build_apiHeaders( sessionKey )

    conn = httplib.HTTPSConnection( sessionHost, sessionPort, timeout=10)
    conn.request("GET", qUrl, "", apiHeaders)
    response = conn.getresponse()
    responseData = response.read()
    responseStatus = response.status
    responseReason = response.reason
    conn.close()

    parsed_response = json.loads( responseData )

    return parsed_response

def output_hosts( sessionKey, sessionHost ):
	hosts = get_hosts( sessionKey, sessionHost )

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
        sessionKey = get_cred( sessionHost, sessionUser, sessionPassword )

        if "hosts" in fetchValue:
        	output_hosts( sessionKey, sessionHost )

    except:
        print("Unexpected error:", sys.exc_info()[0])
        if sessionKey != "":
            remove_cred( sessionHost, sessionKey )
        raise
    else:
        if sessionKey != "":
            remove_cred( sessionHost, sessionKey )

if __name__ == "__main__":
    main(sys.argv[1:])
