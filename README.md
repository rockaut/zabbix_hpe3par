# zabbix_hpe3par
A external script for monitoring HPE 3Par in Zabbix

# Prerequisites

## Software on Zabbix
- Zabbix 3.2.2 ( tested on Ubuntu-Docker )
- python-simplejson

## Software on HPE 3Par
- A read-only user
- WSAPI enabled

## Host-Macros
- {$USERNAME} : read-only role
- {$PASSWORD} : password for user