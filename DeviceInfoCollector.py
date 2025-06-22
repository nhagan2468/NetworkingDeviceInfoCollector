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

# This is the main file of the project that will load the information
# about all of the devices, connect to the devices individually, collect
# the desired information on the hardware, and write the output to a
# confluence page.

# Author: @nhagan2468

from GetDevices import OSType, NetDevice, NetDeviceList
from TelnetConnection import TelnetConnection
from BaseDevice import BaseDevice
from CiscoIOSDevice import CiscoIOSDevice

DEVICE_INFO_FILE = "devices.json"

# Create a list of devices to connect from the json file with the connection info
testlist = NetDeviceList()
testlist.loadDevicesFromJSON(DEVICE_INFO_FILE)

# Loop through the devices and process them according to the Operating System
for i in testlist.devList:
    print(i.devname)
    devType = BaseDevice(i.devname, i.managementIp)
    
    # Pick the appropriate BaseDevice child class based on the OS
    match i.devOS:
        case OSType.JUNOS:
            devType = BaseDevice(i.devname, i.managementIp)	# To be implemented
        case OSType.C_IOS:
            devType = CiscoIOSDevice(i.devname, i.managementIp)
        case OSType.C_XR:
            devType = BaseDevice(i.devname, i.managementIp)	# To be implemented
        case OSType.NDEF:
            devType = BaseDevice(i.devname, i.managementIp)	# To deal with this error case somehow in the future
    
    # Get the list of callback functions and then connect to grab the data
    # TODO: use the JSON file to identify the connection type instead of just hardcoding Telnet
    commands = devType.getCommandList()
    tc = TelnetConnection(i.username, i.password, commands, devType.commandPrompt)
    tc.send(i.managementIp, devType.functCalls)
    
    # Printout the device information to the screen
    # TODO: Make this update the confluence page instead
    devType.printDevInfo()