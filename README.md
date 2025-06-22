# DeviceInfoCollector
DeviceInfoCollector is a Python program that is designed to connect to a list of networking devices of various vendors over their managment interface, run information regarding their hardware configuration, and publish the information to a Confluence Page. The output includes:
- Device hostname name
- Management IP address
- Firmware version
- Description of the hardware in each slot

## Overview/Requirements
This was developed with Python 3.12.2 and the follow additional libraries are needed: telnetlib3. Your mileage may vary if you are using other versions of Python.

## Usage  
`python DeviceInfoCollector.py`
The script has no required parameters. The script required the user to update the information for how to connect to the networking devices in the devices.json file. It will currently connect to Cisco IOS-based systems and will output the information to the screen. Adding the publishing of the information to a Confluence page will be coming soon.

## Structure of Classes
### Necessary Classes/Files
- `device.json` is a JSON file that contains the information about each networking device including the hostname, management ip address, signin information, and connection method.
- `DeviceInfoCollector.py` is the primary file of the project that will use the associated classed to load the information about all of the devices, connect to the devices individually, collect the desired information on the hardware, and write the output to the screen.
- `DeviceConnection.py` is a base class for connections to send commands to the cli of networking devices and have a list of callback functions to process the returned data.
- `TelnetConnection.py` is a child class of DeviceConnection for telnet connections to send commands to the cli of networking devices. For received data, it will use the array of callback functions to enable processing the data appropriately.
- `BaseDevice.py` is the base class associated with networking devices that the child classes will implement the OS-specific functionality. The attributes of this class include the basic information that will be gathered from each device.
- `CiscoIOSDevice.py ` is the child class of BaseDevice associated with Cisco IOS networking devices that will implement the OS-specific functionality. The attributes of this class include the basic information that will be gathered from each Cisco IOS device. 
-`GetDevices.py` includes classes that read in the group of networking devices along with their basic connection information to be iterated against to connect to the devices.

### Testing Classes and Files
-`Testing/TelnetTestServer.py` - script that will serve as a telnet server to test out the telnet connection when a test device is not available.
-`Testing/showVersionOutput.txt` - text file with sample Cisco IOS output for the cli command `show version`
-`Testing/showDiagOutput.txt` - text file with sample Cisco IOS output for the cli command `show diag`

## Future Directions
* Add in the creation of a Confluence page and saving the output in a table onto a confluence page
* Expanding child classes of BaseDevice to include other similar networking Operating Systems such as Juniper JunOS, and Palo Alto Firewall configurations. 
* Add other connection types beyond Telnet like ssh
* Expand the test server to identify the device type from `devices.json` and send the appropriate output for each device family
* Allow the TelnetConnection class to perform a real disconnect instead of the current method to enter "quit"

## References
* <ins>Cisco IOS in a Nutshell, Second Edition</ins> by James Boney, O'Reilly Media, Inc
* [Cisco IOS Configuration Fundamentals Configuration Guide, Release 12.2SR](https://www.cisco.com/c/en/us/td/docs/ios/fundamentals/configuration/guide/12_2sr/cf_12_2sr_book.html) by Cisco
* <ins>Cisco Cookbook</ins> by Kevin Dooley, Ian Brown, O'Reilly Media, Inc.
* <ins>Cisco LAN Switching Configuration Handbook
* [Cisco E-learning Using Cisco IOS Software](https://www.cisco.com/E-Learning/bulk/public/tac/cim/cib/using_cisco_ios_software/cmdrefs/show_version.htm) by Cisco
* [Maintenance with the 'show diag' command in Cisco IOS](https://www.cellstream.com/2014/09/29/show-diag-ciscoios/) by CellStream, Inc.
* [Cisco IOS/XR and Junos Command Reference](https://ipwithease.com/cisco-ios-xr-and-junos-command-reference/) by IpWithEase