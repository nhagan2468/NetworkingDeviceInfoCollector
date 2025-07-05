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

# This class is the child class of BaseDevice associated with Cisco IOS 
# networking devices that will implement the OS-specific functionality. The
# attributes of this class include the basic information that will be
# gathered from each Cisco IOS device. 

# Author: @nhagan2468

import re
from BaseDevice import BaseDevice
from GetDevices import OSType, NetDevice, NetDeviceList

class CiscoIOSDevice(BaseDevice):
    
    def __init__(self, netDev:NetDevice):
        self.devName = netDev.devname
        self.conIPAddr = netDev.consoleIp
        self.intIPAddr = netDev.interfaceIp
        self.location = netDev.location
        self.devFamily = netDev.devfamily
        self.OSVersion = netDev.devOS
        self.commandPrompt = 'Cisco-RTR#'
        self.commandList = [
                            (self.commandPrompt, 'show version'),
                            (self.commandPrompt, 'show diag')
                           ]
        self.functCalls = [self.parseShowVersion, self.parseShowDiag ]
        self.cardInfoBySlot = {}

    
    # Method to pull the Cisco IOS OS Version string from the show version command
    def parseShowVersion(self, data):
        #print(f"Vdata: {data}")
        ver_regex = r"Version\s+(.*)\n"
        match = re.search(ver_regex, data)
        if match:
            self.OSVersion = match[1]
        else:
            self.OSVersion = "unknown"
            
    # Method to pull the Cisco IOS slot card information from the show diag command
    def parseShowDiag(self, data):
        #print(f"Ddata: {data}")
        slot_regex = r"^\s*Slot\s*"
        slots = re.split(slot_regex, data)
        for slot in slots:
            # First parse out the slot number as an integer
            slotNumStr = re.match(r'([0-9]|[1-9][0-9])', slot)
            #print(slotNumStr.group(0))
            if slotNumStr:
                slotNum = int(slotNumStr.group(0))
            else:
                slotNum = -1
            
            # next parse out the name of the card in the slot
            cardNameStr = re.search(r':\s*\n(.*)\n', slot)
            if cardNameStr:
                cardName = cardNameStr.group(0).removeprefix(':\n')
                cardName = cardName.removesuffix('\n')
            
                self.addSlotCardInfo(slotNum, cardName)
        
