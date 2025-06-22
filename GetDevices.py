# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This file includes classes that read in the group of networking devices  
# along with their basic connection information to be iterated against to 
# connect to the devices.

# Author: @nhagan2468

import json
from enum import StrEnum

# Enumeration class for the different Operating Systems Supported
class OSType(StrEnum):
    JUNOS = "JunOS"
    C_ISR = "Cisco ISR"
    C_XR = "Cisco XR"
    NDEF = "Not Defined"

# Device class holding the connection information for that device
class NetDevice:
    devname = ""
    managementIp = ""
    username = ""
    password = ""
    connectMethod = ""
    
    def __init__(self, OSName, name, managementIp, uname, password, connection):
        self.devname = name
        self.managementIp = managementIp
        self.username = uname
        self.password = password
        self.connectMethod = connection
        self.devOS = OSType(OSName)

# Class that handles a list of the device networking information including loading the device
# information from the passed in JSON file
class NetDeviceList:
        
    def __init__(self):
        self.devList = []
        return
        
    def loadDevicesFromJSON(self, fname: str):
        try:
            with open(fname) as fin:
                data = json.load(fin)
                for dev in data['devices']:
                    print(dev['OS'])
                    devObj = NetDevice(dev['OS'], dev['name'], dev['managementIp'], 
                                       dev['username'], dev['password'], dev['connectMethod'])
                    self.devList.append(devObj)
            
        except FileNotFoundError as ferr:
            print(f"JSON file {fname} doesn't exist")
        
        
        