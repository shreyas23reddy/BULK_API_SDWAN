import requests
import json
from auth_header import Authentication as auth
from operations import Operation 


#function to get the url provide api endpoint 
def url(vmanage_host,vmanage_port,api):
    return f"https://{vmanage_host}:{vmanage_port}{api}"


#vmanage details 
vmanage_host = '172.16.104.81'
vmanage_port = '8443'
username = 'admin'
password = 'admin'

# call the auth_header library which provides cookies and token  
header= auth.get_header(vmanage_host, vmanage_port,username, password)


print ( f'''
ID    Data Type Parameter	Description

1	BFDSessions	            BFD sessions
2	BGPNeighbor	            BGP neighbors
3	Bridge	                    Bridge interfaces
4	ControlConnection	    Active control connections
5	ControlLocalProperty        Basic configuration parameters and local device properties related to the control plane
6	ControlWanInterface	    WAN interface control connection information
7	HardwareAlarms	            Active hardware alarms
8	HardwareEnvironment	    Status information about router components, including temperature
9	HardwareInventory	    Inventory of router hardware components, including serial numbers
10	Interface	            Interface information
11	OMPPeer	                    Active OMP peering sessions
12	SystemStatus	            Logging, reboot, and configuration history
13	System	                    Summary of general system-wide parameters

''')

data_type_ID = int(input('Please enter a valid Data_Type ID : '))
count = int(input('count Number of devices to query 1 - 1000 : '))

assert data_type_ID > 0 and data_type_ID < 14, "The ID must be between 1 - 13"

data_type_parameter = ['BFDSessions', 'BGPNeighbor', 'Bridge',
                       'ControlConnection', 'ControlLocalProperty',
                       'ControlWanInterface', 'HardwareAlarms',
                       'HardwareEnvironment','HardwareInventory',
                       'Interface', 'OMPPeer', 'SystemStatus', 'System']


def bulk_State( startId ):
    api_bulk_state = '/dataservice/data/device/state/' + data_type_parameter[data_type_ID-1]+ '?startId='+ str(startId) +'&count=' + str(count) 
    url_bulk_state = url(vmanage_host,vmanage_port,api_bulk_state)


    bulk_state = Operation.get_method(url_bulk_state,header)

    if data_type_ID == 1:
        for state in bulk_state['data']:
            print (f'''system-ip : {state['system-ip']} site-id : {state['site-id']}
                                                    color : {state['local-color']} src-ip : {state['src-ip']} dst-ip : {state['dst-ip']}
                                                    src-port : {state['src-port']} dst-port : {state['dst-port']} state : {state['state']}
                                                ''')

    print(bulk_state['pageInfo'])
    if bulk_state['pageInfo']['moreEntries'] == True:
        bulk_State(bulk_state['pageInfo']['endId'])
                                                

 

bulk_State(0)




'''
output field for BFDSessions
[
  {
    "property": "vdevice-name",
    "dataType": "string"
  },
  {
    "property": "vdevice-host-name",
    "dataType": "string"
  },
  {
    "property": "system-ip",
    "dataType": "ip"
  },
  {
    "property": "site-id",
    "dataType": "number"
  },
  {
    "property": "state",
    "dataType": "string"
  },
  {
    "property": "local-color",
    "dataType": "string"
  },
  {
    "property": "color",
    "dataType": "string"
  },
  {
    "property": "src-ip",
    "dataType": "ip"
  },
  {
    "property": "dst-ip",
    "dataType": "ip"
  },
  {
    "property": "dst-port",
    "dataType": "number"
  },
  {
    "property": "proto",
    "dataType": "string"
  },
  {
    "property": "src-port",
    "dataType": "number"
  },
  {
    "property": "detect-multiplier",
    "dataType": "string"
  },
  {
    "property": "tx-interval",
    "dataType": "number"
  },
  {
    "property": "transitions",
    "dataType": "number"
  },
  {
    "property": "uptime-date",
    "dataType": "date"
  },
  {
    "property": "uptime",
    "dataType": "uptime"
  },
  {
    "property": "lastupdated",
    "dataType": "date"
  }
]

'''

