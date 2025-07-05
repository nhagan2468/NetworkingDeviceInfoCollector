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

# This is a test function that serves as a telnet server to test out the 
# telnet connection when a test device is not available. 

# Author: @nhagan2468

import socket
import sys
import os
import threading

# read the file whose name is passed in and return the contents of the file
def readFile(fname):
    try:
        with open(fname) as fin:
            data = fin.read()
            return data
    except FileNotFoundError as ferr:
        print(f"file {fname} doesn't exist")
    

def iosCommands(indata, send_resp_line):
    send_resp = ['Username: ',
                 'Password: ',
                 'Cisco-RTR# '
                ]
        
    if indata == 'show version'.encode('utf-8'):
        datToSend = readFile('ios_showVersionOutput.txt')
        datToSend = datToSend + send_resp[send_resp_line]
        print("sending show version file")
    elif indata == 'show diag'.encode('utf-8'):
        datToSend = readFile('ios_showDiagOutput.txt')
        datToSend = datToSend + send_resp[send_resp_line]
        print("sending show diag file")
    else:
        datToSend = send_resp[send_resp_line]
        print(f"Sending: {send_resp[send_resp_line]}")
    
    return datToSend


def junosCommands(indata, send_resp_line, uname, devname):
    send_resp = ['Username: ',
                 'Password: ',
                 uname + '@' + devname + '% ',
                 uname + '@' + devname + '> '
                ]
    
    if indata == 'cli'.encode('utf-8'):
        datToSend = send_resp[3]
        print("entering cli")
    elif indata == 'show version brief'.encode('utf-8'):
        datToSend = readFile('junos_showVersionOutput.txt')
        datToSend = datToSend + send_resp[3]
        print("sending show version file")
    elif indata == 'show chassis hardware'.encode('utf-8'):
        datToSend = readFile('junos_showChassisHwOutput.txt')
        datToSend = datToSend + send_resp[3]
        print("sending show chassis hardware file")
    elif indata == 'exit'.encode('utf-8'):
        datToSend = send_resp[2]
        print("exiting cli")
    else:
        datToSend = send_resp[send_resp_line]
        print(f"Sending: {send_resp[send_resp_line]}")
    
    return datToSend

# function to handle an incoming network socket connection from a client
# and will automatically send the appropriate data.
def handleIncoming(insock, deviceIdx, deviceList):
    
    send_resp_line = 0
    
    print(f"device number {deviceIdx} being handled")
    
    # First ask for the Username before the client sends anything
    insock.send('Username: '.encode('utf-8'))
    print("Sending: Username: ")
    send_resp_line += 1

    # loop through sending all responses until receive a quit
    while True:
        datToSend = ""
        indata = insock.recv(1024)

        if not indata:
            break
        elif indata == 'quit'.encode('utf-8'):
            # TODO: Update this to be the standard CTRL + ] to exit Telnet 
            print("device quit connection")
            insock.close()
            break
        elif deviceList[deviceIdx].devOS == OSType.C_IOS:
            datToSend = iosCommands(indata, send_resp_line)
        elif deviceList[deviceIdx].devOS == OSType.JUNOS:
            datToSend = junosCommands(indata,
                                      send_resp_line,
                                      deviceList[deviceIdx].username,
                                      deviceList[deviceIdx].devname)
        else:
            print(f"Invalid Device type: {deviceList[deviceIdx].devOS}")
        
        insock.send(datToSend.encode('utf-8'))
        
        # Update to the appropriate prompt array entry
        if send_resp_line < 2:
            send_resp_line += 1
    
    insock.close()
        

# Read the devices.json file to see what devices the software is going to
# try to connect to and select the appropriate files to read for them.

# devices.json is one directory higher than this testing directory
sys.path.append(r"..")

# now can import the method to parse the json
from GetDevices import OSType, NetDevice, NetDeviceList

DEVICE_INFO_FILE = "devices.json"
currDir = os.path.dirname(__file__)
devfilepath = os.path.abspath(os.path.join(currDir, "..", DEVICE_INFO_FILE))

# Create a list of devices to connect from the json file with the connection info
testlist = NetDeviceList()
testlist.loadDevicesFromJSON(devfilepath)

devicesHandled = 0

# Set up the actual socket connection using threading to
# allow the KeyboardInterrupt to not be blocked by the recv

HOSTIP = "127.0.0.1"		# Use the localhost for this test
PORT = 23				# Random port value

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
inhandlers = []

try:
    mysock.bind((HOSTIP, PORT))
except socket.error as msg:
    print("womp womp, bind failed")
    sys.exit()
    
try:
    # listening for connections coming in with a timeout to allow Keyboard Interrupt
    mysock.listen(5)
    mysock.settimeout(0.5)

    while True:
        try:
            insock, addr = mysock.accept()
            threadhandle = threading.Thread(target=handleIncoming, args=(insock, devicesHandled, testlist.devList,))
            threadhandle.start()
            inhandlers.append(threadhandle)
            devicesHandled += 1
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            break
                
except KeyboardInterrupt:
    # End the current handler threads and exit
    for h in inhandlers:
        h.join()
        
    mysock.close()
    sys.exit()
    
except Exception as e:
    # Not sure what happened, will just get out
    print(e)
    sys.exit()

# Cleanup nicely and get out of here
for h in inhandlers:
    h.join()
    
mysock.close()
sys.exit()    
