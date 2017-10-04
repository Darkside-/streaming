# ---------------------------------------
#   Import Libraries
# ---------------------------------------

import datetime
import time 
import os
import json

import ctypes
import codecs

# ---------------------------------------
#   [Required]  Script Information
# ---------------------------------------

ScriptName = "MultiLink"
Description = "Multi Stream Link Manager"
Website = "https://www.twitch.tv/flash0429"
Creator = "Flash0429"
Version = "2.2.1.0"

#---------------------------------------
#   Classes
#---------------------------------------
class Settings:
    # Tries to load settings from file if given else set defaults
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile,encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f,encoding='utf-8-sig')
        else:
            self.saveMulti = False
            self.commandCooldown = 10
            self.modCanChangeMessage = True
            self.customMessage = "Watch everyone together here:"
            self.timerEnabled = False
            self.modCanChangeTimer = True
            self.timerLength = 10
            self.timerChatters = 10
            
    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data,encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f,encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"),encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__,encoding='utf-8-sig')))
        return

class Multi:
    # Tries to load Multi from file if given else set defaults
    def __init__(self, multiFile = None):
        if multiFile is not None and os.path.isfile(multiFile):
            with codecs.open(multiFile,encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f,encoding='utf-8-sig')
        else:
            self.multi = noMulti
            
    

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f,encoding='utf-8-sig')
        with codecs.open(multiFile.replace("json", "js"),encoding='utf-8-sig',mode='w+') as f:
            f.write("var multi = {0};".format(json.dumps(self.__dict__,encoding='utf-8-sig')))
        return

# ---------------------------------------
#   Extra Functions
# ---------------------------------------

def setMulti(data, multi):
    if len(data.GetParam(2)) != 2 or sites.get(data.GetParam(2).lower(), 'invalid') == 'invalid':
        Parent.SendTwitchMessage("Invalid Site Choice!!")

    else:
        i = 3
        duplicates = 0

        m_Site = sites[data.GetParam(2).lower()]
        multi = m_Site + m_channelName

        global dupCheck
                
        while i < data.GetParamCount():
            dupCheck = multi.find(data.GetParam(i).lower())            
            if dupCheck == -1:
                multi = multi + "/" + data.GetParam(i).lower()                    
                i += 1
                
            else:
                duplicates += 1
                i += 1        
            
        Parent.SendTwitchMessage("Multi Set!!")
        if duplicates > 0:
            Parent.SendTwitchMessage(str(duplicates) + " Duplicate Users Not Added")
        return multi

def addMulti(data, multi):
    i = 2
    duplicates = 0

    if multi == noMulti:
        Parent.SendTwitchMessage("Sorry there is no multi to edit right now try using !multi set to make a new multi link")

    else:
        while i < data.GetParamCount():
            if multi.find(data.GetParam(i)) == -1:
                multi = multi + "/" + data.GetParam(i).lower()
                i += 1

            else:
                duplicates += 1
                i += 1
        
        Parent.SendTwitchMessage("Adding Done!!")
        if duplicates > 0:
            Parent.SendTwitchMessage(str(duplicates) + " Duplicate Users Not Added")        
        return multi
    return multi

def removeMulti(data, multi):
    i = 2

    if multi == noMulti:
        Parent.SendTwitchMessage("Sorry there is no multi to edit right now try using !multi set to make a new multi link")

    else:
        while i < data.GetParamCount():
            if data.GetParam(i).lower() == Parent.GetChannelName():
                Parent.SendTwitchMessage("Cannot remove channel name from multi link")
                i += 1
            else:
                oldMulti = multi                                         
                multi = oldMulti.replace("/" + data.GetParam(i).lower(), "")                    
                i += 1

        Parent.SendTwitchMessage("Removing Done!!")
        return multi
    return multi

def changeMulti(data, multi):    
    if len(data.GetParam(2)) != 2 or sites.get(data.GetParam(2).lower(), 'invalid') == 'invalid':
        Parent.SendTwitchMessage("Invalid Site Choice!!")

    else:
        if multi == noMulti:
            Parent.SendTwitchMessage("Sorry there is no multi to edit right now try using !multi set to make a new multi link")

        else:
            multiSplit = multi.split(Parent.GetChannelName())
            m_Site = sites[data.GetParam(2).lower()]
            multi = m_Site + Parent.GetChannelName() + multiSplit[1]

            Parent.SendTwitchMessage("Multi Site Changed!!")
            return multi
        return multi

def clearMulti(multi):    
    multi = noMulti
    Parent.SendTwitchMessage("Multi Cleared!!")
    return multi

def enableMultiTimer(data):
    if multiSettings.modCanChangeTimer:
        if data.GetParam(2).lower() != 'on' and data.GetParam(2).lower() != 'off':
            Parent.SendTwitchMessage("Sorry that is not a valid option. Valid options are 'on' or 'off'.")

        elif data.GetParam(2).lower() == 'on' :
            if multiSettings.timerEnabled:
                Parent.SendTwitchMessage("Multi timer is already on!")                

            else:
                multiSettings.timerEnabled = True
                Parent.SendTwitchMessage("Multi timer on.")

        elif data.GetParam(2).lower() == 'off':
            if multiSettings.timerEnabled:
                multiSettings.timerEnabled = False
                Parent.SendTwitchMessage("Multi Timer Off.")

            else:
                Parent.SendTwitchMessage("Multi timer is already off!")
    else:
        Parent.SendTwitchMessage("Sorry, Mod permission not enabled.")

def changeMultiMessage(data):
    if multiSettings.modCanChangeMessage:
        c_Message = data.Message.split(' ', 2)
        multiSettings.customMessage = c_Message[2]
        Parent.SendTwitchMessage("Custom message changed.")

    else:
        Parent.SendTwitchMessage("Sorry, Mod permission not enabled.")
    return 

def helpMessageBox():
    
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(0, "Welcome to MultiLink \r\n \r\n You can use this To easily make and edit a multi command \r\n \r\n UI Explained: \r\n \r\n       General: \r\n            Save Timer: If enabled will Save the timer upon bot close or reset, if disabled multi will revert back to Default \r\n \r\n       Response Messgage: \r\n              Mod Access: Allows Mods to Edit Custom Message From chat Using !multi msg new message here \r\n              Custom Messge: This is the message that will appear before the multi link \r\n \r\n       Timer: \r\n              Enable Timer: This Will Enable and Diasble the timer \r\n              Mod Access: this will allow Mods to start multi timer from chat \r\n              Timer Length: this is how between each posting of the multi when the timer is on (In Minutes)  \r\n \r\n General Usage: \r\n \r\n              mt = multitwitch.tv \r\n              ms = multistre.am \r\n              kl = kadgar.net/live/ \r\n \r\n       !multi set mt|ms|kl user1 user2 i.e. !multi set ms user1 user2 would make multistre.am/CASTOR/user1/user2 \r\n \r\n       !multi add user1 user2 i.e. !multi add user3 user4 would make the previous multi multistre.am/CASTOR/user1/user2/user3/user4 \r\n \r\n       !multi remove user1 user2 will remove said users from multi i.e. !multi remove user1 user4 to the previous multi would make multistre.am/CASTOR/user2/user3 \r\n \r\n       !multi clear will revert the multi back to Default \r\n \r\n       !multi timer on|off will turn the timer on or off \r\n \r\n       !multi change ms|mt|kl will change the Multi site of choice i.e !multi change kl to the previous multi would make kadgar.net/live/CASTOR/user1/user2 \r\n \r\n       !multi msg (new message here) will change the custom message that appears before the multi link", "Everything You Need To Know", 0)
    

# ---------------------------------------
#   Set Variables
# ---------------------------------------

m_Command = "!multi"
m_Site = ""
duplicates = 0

chatters = 0

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
multiFile = os.path.join(os.path.dirname(__file__), "multi.json")

sites = { 'mt': 'http://multitwitch.tv/',
          'ms': 'http://multistre.am/',
          'kl': 'http://kadgar.net/live/' }

options = { 'set': setMulti,
            'add': addMulti,
            'remove': removeMulti,
            'change': changeMulti }

optionsMisc = { 'timer': enableMultiTimer,
            'msg': changeMultiMessage }

# ---------------------------------------
#   [Required] Intialize Data (Only called on Load)
# ---------------------------------------


def Init():

    # Globals
    global multiSettings
    global multi
    global TimeStamp
    
    global noMulti
    noMulti = "Sorry, No Multi Right Now"

    global chatters
    chatters = 0

    #Set Initial Time Stamp
    TimeStamp = time.time()

    # Load in saved settings
    multiSettings = Settings(settingsFile)
    multi = Multi(multiFile)

    
    # End of Init
    return
#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global multiSettings
    global TimeStamp

    # Set timestamp
    TimeStamp = time.time()

    # Reload saved settings
    multiSettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return
# ---------------------------------------
#   [Required] Execute Data / Process Messages
# ---------------------------------------

def Execute(data):
    if data.IsChatMessage():        
        
        global i
        global oldMulti
        global m_Site
        global m_Option
        global dublicates
        global chatters
        
        global m_channelName
        m_channelName = Parent.GetChannelName()

        chatters = chatters + 1

        if data.GetParam(0).lower() == m_Command:
            if data.GetParamCount() > 1:
                if Parent.HasPermission(data.User,"moderator",""):
                    if options.get(data.GetParam(1).lower(), 'invalid') != 'invalid':
                        m_Option = options[data.GetParam(1).lower()]
                        multi.multi = m_Option(data, multi.multi) 

                    elif optionsMisc.get(data.GetParam(1).lower(), 'invalid') != 'invalid':
                        m_Option = optionsMisc[data.GetParam(1).lower()]
                        m_Option(data)

                    elif data.GetParam(1).lower() == 'clear':
                        multi.multi = clearMulti(multi.multi)                       

                    else:
                        Parent.SendTwitchMessage("Available options are !multi set|add|remove|clear|change|timer|msg ")
                else:
                    Parent.SendTwitchMessage("Sorry " + data.User + ", you don't have permission to do that!")
                    
            elif not Parent.IsOnCooldown(ScriptName, m_Command):
                if multi.multi == noMulti:
                    Parent.SendTwitchMessage(multi.multi)
                    Parent.AddCooldown(ScriptName, m_Command, multiSettings.commandCooldown) 
                else:
                    fullMessage = multiSettings.customMessage + " {0}"
                    Parent.SendTwitchMessage(fullMessage.format(multi.multi))            
                    Parent.AddCooldown(ScriptName, m_Command, multiSettings.commandCooldown)          
                   
# ---------------------------------------
#   [Required] Tick Function
# ---------------------------------------

def Tick():

    if multiSettings.timerEnabled and (time.time() - TimeStamp) >= (multiSettings.timerLength * 60) and chatters >= multiSettings.timerChatters and multi.multi != noMulti:
            
        # Globals
        global TimeStamp
        global chatters
        
        # Set new timestamp
        TimeStamp = time.time()

        # Reset chatters
        chatters = 0

        #Post Multi        
        fullMessage = multiSettings.customMessage + " {0}"
        Parent.SendTwitchMessage(fullMessage.format(multi.multi))

    return

def Unload():    

    multiSettings.SaveSettings(settingsFile)

    if multiSettings.saveMulti:
        multi.SaveSettings(multiFile)

    else:
        multi.multi = noMulti
        multi.SaveSettings(multiFile)



    return
