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

# This class is a base class for connections to send commands to the
# cli of networking devices. 

# Author: @nhagan2468

class DeviceConnection:
    callbacks = []		# array of function callbacks that will be used to process returned data
    
    # Initialization of the object, saving off the commands to be executed
    def __init__(self):
        return
        
    # Send the commands and return the output
    # Assuming that the child class will select the appropriate port for the connection
    def send(self, ipaddr, callbacks):
        return
        
            