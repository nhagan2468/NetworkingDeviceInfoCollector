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

# This file includes classes and methods to write output to a confluence page  
# whose access information is given in the initialization of the
# ConfluenceWriter object.

# Author: @nhagan2468

from atlassian import Confluence
from BaseDevice import BaseDevice
import os, stat

class ConfluenceWriter:
    url = 'https://confluence.myorg.com'
    pageTitle = "Devices"
    pageSpace = "confluence_space_id"
    passwordFile = '~\\confluence\\login.txt'
    username = ""
    password = ""
    
    # initialization method that uses an atlassian personal access token to
    # connect to the Confluence server
    def __init__(self):
        # Before doing anything, ensure that the tokenFile is not world/group readable
        pswdPerms = os.stat(self.passwordFile).st_mode
        
        if pswdPerms & stat.S_IRGRP or pswdPerms & stat.S_IROTH:
            print("password file is group or world readable, please lock it down")
            return

        # grab the username and password from the file
        try:
            with open(passwordFile) as fin:
                self.username = fin.readline()
                self.password = fin.readline()
        except FileNotFoundError as ferr:
            print(f"file {fname} doesn't exist")
            return
        
        self.confluenceObj = Confluence(url=self.url, username=self.username, password=self.password)
        
        
    def createOrUpdatePage(self, pageTitle, deviceList):
        
        # Fist get what is currently in the page
        self.pageId = self.confluenceObj.get_page_id(space=pageSpace, title=pageTitle)
        pageInfo = self.confluenceObj.get_page_by_id(page_id, expand='body.storage')
        currBody = pageInfo['body']['storage']['value']
        
        currBody = ""
        pageBody = self.buildPageBody(deviceList, currBody)
        self.confluenceObj.update_or_create(self.pageId, title=pageTitle, body=pageBody)
        #print(pageBody)
    
    def buildPageBody(self, deviceList, currBody):
        body = ""
        # Currently not just updating the old body, but that is a future direction

        # create a dictionary of device families and the devices belonging to the family
        devfamilies = {}
        for device in deviceList:
            if device.devFamily in devfamilies.keys():
                devfamilies[device.devFamily].append(device)
            else:
                devfamilies[device.devFamily] = [device]
        
        # For each device family, create a heading and a table with the device information
        for family in devfamilies.keys():
            body += f"h1. {family}\n\n"
            body += "||Name||Console IP||Interface IP||Notes||Location||\n"
            
            for dev in devfamilies[family]:
                body += f"|{dev.devName}|{dev.conIPAddr}|{dev.intIPAddr}|* {dev.OSVersion}\n"
                for key, value in dev.cardInfoBySlot.items():
                    slotNum = str(key)
                    cardName = str(value)
                    body += f"* {slotNum}: {cardName}\n"
                
                body += f"|{dev.location}|\n"
                
            body += "\n"
            
        return body
        
        