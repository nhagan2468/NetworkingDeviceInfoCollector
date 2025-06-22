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

# This class is the base class associated with networking devices that
# the child classes will implement the OS-specific functionality. The
# attributes of this class include the basic information that will be
# gathered from each device. 

# Author: @nhagan2468

class BaseDevice:
    devName = ""			# Name of the device
    manIPAddr = ""			# Ip Address of the Management Interface
    OSVersion = "None"		# OS Version
    cardInfoBySlot = {}		# Dictionary of card names per slot
    commandList = []		# List of commands to send to the device 
    functCalls = []			# List of function callbacks to parse the output
    commandPrompt = ""		# The standard CLI prompt expected on new lines
    
    def __init__(self, name, IpAddr):
        self.devName = name
        self.manIpAddr = IpAddr
        self.cardInfoBySlot = {}
        self.commandList = []
        self.functCalls = []
        self.commandPrompt = ""
        
    # Add new card information associated with a slot
    def addSlotCardInfo(self, slotNum, info):
        self.cardInfoBySlot[slotNum] = info
    
    # Give the list of commands to be sent to the device
    def getCommandList(self):
        return self.commandList
    
    # Print out the information regarding the device
    def printDevInfo(self):
        # to be fixed to work for the Confluence page output. For now
        # will just write a csv string.
        outstr = self.devName + ',' + self.manIpAddr + ',' + self.OSVersion + ','
        
        # add in the information about the cards in each slot
        for key, value in self.cardInfoBySlot.items():
            outstr = outstr + str(key) + ":" + str(value) + ";" 
        if len(self.cardInfoBySlot) == 0:
            outstr = outstr + "No Card Info"
        
        print(outstr)
        