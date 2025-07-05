# DeviceInfoCollector
DeviceInfoCollector is a Python program that is designed to connect to a list of networking devices of various vendors over their managment interface, get information regarding their hardware configuration, and publish the information to a Confluence Page. 
The output includes:
- Device hostname name
- Console IP address
- OS version
- Description of the hardware in each slot
- Location of the equipment by rack and row

## Overview/Requirements
This was developed with Python 3.12.2 and the follow additional libraries are needed: telnetlib3, atlassian-python-api. Your mileage may vary if you are using other versions of Python.

## Usage  
`python DeviceInfoCollector.py`

The script has no required parameters. The script requires the user to update the information necessary to connect to the networking devices in the `devices.json` file. It will currently connects to Cisco IOS-based systems and Juniper Junos-based systems. The script will output the information about the devices to the screen and publish the information to a Confluence page.

## Structure of Classes
### Necessary Classes/Files
- `device.json` is a JSON file that contains the information about each networking device including the hostname, console ip address, sign-in information, and connection method.
- `DeviceInfoCollector.py` is the primary file of the project that will use the associated classed to load the information about all of the devices, connect to the devices individually, collect the desired information on the hardware, write the output to the screen, and call the confluence writer.
- `DeviceConnection.py` is a base class for connections to send commands to the cli of networking devices and have a list of callback functions to process the returned data.
- `TelnetConnection.py` is a child class of DeviceConnection for telnet connections to send commands to the cli of networking devices. For received data, it will use the array of callback functions to enable processing the data appropriately.
- `BaseDevice.py` is the base class associated with networking devices that the child classes will implement the OS-specific functionality. The attributes of this class include the basic information that will be gathered from each device.
- `CiscoIOSDevice.py ` is the child class of BaseDevice associated with Cisco IOS networking devices that will implement the OS-specific functionality. The attributes of this class include the basic information that will be gathered from each Cisco IOS device. 
- `JuniperJunOSDevice.py ` is the child class of BaseDevice associated with Juniper Junos networking devices that will implement the OS-specific functionality. The attributes of this class include the basic information that will be gathered from each Juniper device. 
- `GetDevices.py` includes classes that read in the group of networking devices along with their basic connection information to be iterated against to connect to the devices.
- `ConfluenceWriter.py` is the class that is using the Atlassian Confluence interface to read in a password from a file, log into Confluence, and create or update a defined page with the information obtained from the rest of the program. 
- `ConfluenceWriter_neutered.py` is the class that if testing on a network without access to the Atlassian Confluence server, it will just print to the screen the new body that will be sent to confluence if it was available.

### Testing Classes and Files
- `Testing/TelnetTestServer.py` - script that will serve as a telnet server to test out the telnet connection when a test device is not available.
- `Testing/ios_showVersionOutput.txt` - text file with sample Cisco IOS output for the cli command `show version`
- `Testing/ios_showDiagOutput.txt` - text file with sample Cisco IOS output for the cli command `show diag`
- `Testing/junos_showVersionOutput.txt` - text file with sample Juniper Junos output for the cli command `show version`
- `Testing/junos_showChassisHwOutput.txt` - text file with sample Juniper Junos output for the cli command `show chassis hardware brief`

## Recent Updates
* Added in class to update a confluence page with the information gained about the devices
* Added support for Juniper Junos commands
* Made the Testing Telnet server smarter by allowing it to read the devices.json and change the information served based on which device in the list is being queried

## Future Directions
* Expanding child classes of BaseDevice to include other similar networking Operating Systems such as Palo Alto Firewall configurations. 
* Add other connection types beyond Telnet like ssh and use the JSON file to grab it
* Allow the TelnetConnection class to perform a real disconnect instead of the current method to enter "quit"
* Add in more improved error handling in the TelnetConnection class
* Divide up the output not just by Device family, but by OS and perhaps class of devices (routers vs switches vs firewalls)
* Read in static information on the Confluence page and only change more dynamic information on the page instead of rewriting the entire thing
* Provide more variety in the test server and make it smarter in the printouts and resetting when all of the connections have been completed to run it again instead of restarting it


## References
* <ins>Cisco IOS in a Nutshell, Second Edition</ins> by James Boney, O'Reilly Media, Inc
* [Cisco IOS Configuration Fundamentals Configuration Guide, Release 12.2SR](https://www.cisco.com/c/en/us/td/docs/ios/fundamentals/configuration/guide/12_2sr/cf_12_2sr_book.html) by Cisco
* <ins>Cisco Cookbook</ins> by Kevin Dooley, Ian Brown, O'Reilly Media, Inc.
* <ins>Cisco LAN Switching Configuration Handbook
* [Cisco E-learning Using Cisco IOS Software](https://www.cisco.com/E-Learning/bulk/public/tac/cim/cib/using_cisco_ios_software/cmdrefs/show_version.htm) by Cisco
* [Maintenance with the 'show diag' command in Cisco IOS](https://www.cellstream.com/2014/09/29/show-diag-ciscoios/) by CellStream, Inc.
* [Cisco IOS/XR and Junos Command Reference](https://ipwithease.com/cisco-ios-xr-and-junos-command-reference/) by IpWithEase
* [Atlassian Python API Documentation](https://atlassian-python-api.readthedocs.io/)
* [CLI User Guide for Junos OS](https://www.juniper.net/documentation/us/en/software/junos/cli/)
* [Junos CLI Reference Show Chassis Hardware](https://www.juniper.net/documentation/us/en/software/junos/cli-reference/topics/ref/command/show-chassis-hardware.html)
* [Junos CLI Reference Show Version](https://www.juniper.net/documentation/us/en/software/junos/cli-reference/topics/ref/command/show-version.html)
* [CLI User Guide for Junos OS](https://www.juniper.net/documentation/us/en/software/junos/cli/topics/topic-map/getting-started.html)