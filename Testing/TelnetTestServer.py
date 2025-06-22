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
import threading

# read the file whose name is passed in and return the contents of the file
def readFile(fname):
    try:
        with open(fname) as fin:
            data = fin.read()
            return data
    except FileNotFoundError as ferr:
        print(f"Configuration file {fname} doesn't exist")

# function to handle an incoming network socket connection from a client
# and will automatically send the appropriate data.
# TODO: This currently is hardcoded for Cisco IOS, but should be updated
# to be different OS versions based on the JSON file being used
def handleIncoming(insock):
    
    send_resp = ['Username: ',
                 'Password: ',
                 'Cisco-RTR# '
                ]
    
    send_resp_line = 0
    
    # First ask for the Username before the client sends anything
    insock.send(send_resp[send_resp_line].encode('utf-8'))
    print(f"Sending: {send_resp[send_resp_line]}")
    send_resp_line += 1

    # loop through sending all responses until receive a quit
    while True:
        datToSend = ""
        indata = insock.recv(1024)

        if not indata:
            break
        elif indata == 'show version'.encode('utf-8'):
            datToSend = readFile('showVersionOutput.txt')
            datToSend = datToSend + send_resp[send_resp_line]
            print("sending show version file")
        elif indata == 'show diag'.encode('utf-8'):
            datToSend = readFile('showDiagOutput.txt')
            datToSend = datToSend + send_resp[send_resp_line]
            print("sending show diag file")
        elif indata == 'quit'.encode('utf-8'):
            # TODO: Update this to be the standard CTRL + ] to exit Telnet 
            print("device quit connection")
            insock.close()
            break
        else:
            datToSend = send_resp[send_resp_line]
            print(f"Sending: {send_resp[send_resp_line]}")
        
        insock.send(datToSend.encode('utf-8'))
        
        # Update to the appropriate prompt array entry
        if send_resp_line < 2:
            send_resp_line += 1
    
    insock.close()
        

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
            threadhandle = threading.Thread(target=handleIncoming, args=(insock,))
            threadhandle.start()
            inhandlers.append(threadhandle)
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
