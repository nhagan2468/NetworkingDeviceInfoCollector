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

class JuniperJunosDevice(BaseDevice):
    
    def __init__(self, netDev:NetDevice):
        self.devName = netDev.devname
        commandPromptCli = netDev.username + '@' + netDev.devname + '>'
        self.commandPrompt = netDev.username + '@' + netDev.devname + '%'
        self.conIPAddr = netDev.consoleIp
        self.intIPAddr = netDev.interfaceIp
        self.location = netDev.location
        self.devFamily = netDev.devfamily
        self.OSVersion = netDev.devOS
        self.commandList = [
                            (self.commandPrompt, 'cli'),
                            (commandPromptCli, 'show version brief'),
                            (commandPromptCli, 'show chassis hardware'),
                            (commandPromptCli, 'exit')
                           ]
        self.functCalls = [self.doNothing, self.parseShowVersion, self.parseShowChassisHardware, self.doNothing ]
        self.cardInfoBySlot = {}

    # Empty method for when we exit the cli
    def doNothing(self, data):
        return


    # Method to pull the Juniper Junos OS Version string from the show version command
    def parseShowVersion(self, data):
        ver_regex = r"Junos:\s+(.*)\n"
        match = re.search(ver_regex, data)
        if match:
            self.OSVersion = match[1]
        else:
            self.OSVersion = "unknown"
            
            
    # Method to pull the Juniper Junos slot card information from the show chassis hardware command
    def parseShowChassisHardware(self, data):
        # Constants
        reDescriptOffset = 42
        cardDescriptOffset = 53
        
        # First pull out the Routing Engine card information
        re_regex = r"\s*Routing Engine\s*"
        routingEngines = re.split(re_regex, data)
        for reidx in range(1, len(routingEngines)):
            routingEng = routingEngines[reidx]

            # pull out the routing engine number (should only be 0 or 1)
            reNumStr = re.match(r'^([0-1])', routingEng)
            if reNumStr:
                reNum = "RE" + reNumStr.group(0)
            else:
                reNum = "RE_NAN"
                
            # Now parse out the name of the Card in the Routing Engine
            # the offset in the print is at a fixed location in the line, so just grab starting at that loc
            
            # first case is where this is the last of the routing engine lines and we get the rest of the
            # printout
            reDesc = re.search(r'(.*)\n',routingEng[reDescriptOffset:])
            if reDesc:
                reInfo = reDesc.group(0).removesuffix('\n')
                self.addSlotCardInfo(reNum, reInfo)
            else:
                # This case is for when we are getting one of the earlier routing engine lines and we
                # get only a single line with no CR/LF at the end of the line
                reDesc = re.search(r'(.*)$',routingEng[reDescriptOffset:])
                if reDesc:
                    self.addSlotCardInfo(reNum, reDesc.group(0).removesuffix('\n'))
            
        slot_regex = r"\s*FPC\s*"
        slots = re.split(slot_regex, data)
        for slotidx in range(1, len(slots)):
            slot = slots[slotidx]
            # First parse out the slot number as an integer
            slotNumStr = re.match(r'([0-9]|[1-9][0-9])', slot)
            #print(slotNumStr.group(0))
            if slotNumStr:
                slotNum = int(slotNumStr.group(0))
            else:
                slotNum = -1
                
            
            # next parse out the name of the card in the slot
            
            # first case is where this is the last of the card slot lines and we get the rest of the
            # printout with it
            cardNameStr = re.search(r'(.*)\n', slot[cardDescriptOffset:])
            if cardNameStr:
                cardName = cardNameStr.group(0).removeprefix(':\n')
                cardName = cardName.removesuffix('\n')      
                self.addSlotCardInfo(slotNum, cardName)
            else:
                # This case is for when we are getting one of the earlier card slot lines and we
                # get only a single line with no CR/LF at the end of the line
                cardNameStr = re.search(r'(.*)$', slot[cardDescriptOffset:])
                if cardNameStr:
                    self.addSlotCardInfo(slotNum, cardName)