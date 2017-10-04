#---------------------------------------
#   Import Libraries
#---------------------------------------
import sys, os, json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime
import json
import codecs
import operator
from settingsmodule import Settings

#---------------------------------------
#   [Required] Script Information
#---------------------------------------
ScriptName = "Currency Ws"
Website = "https://www.AnkhBot.com"
Description = "!points will display the user's currency on screen."
Creator = "AnkhHeart"
Version = "1.0.0.0"

m_ConfigFile = os.path.join(os.path.dirname(__file__), "Settings/settings.json")
m_ConfigFileJs = os.path.join(os.path.dirname(__file__), "Settings/settings.js")
#---------------------------------------
#   [Required] Declare Variables
#---------------------------------------
MySettings = Settings()

#---------------------------------------
#   [Required] Initialize Data / Load Only
#---------------------------------------
def Init():
    global MySettings
    MySettings = Settings()

    if not os.path.isfile(m_ConfigFile):
        text_file = codecs.open(m_ConfigFile, encoding='utf-8-sig',mode='w')
        out = json.dumps(MySettings.__dict__, encoding="utf-8-sig")
        text_file.write(out)
        text_file.close()
    else:
        with codecs.open(m_ConfigFile,encoding='utf-8-sig',mode='r') as ConfigFile:
            MySettings.__dict__ = json.load(ConfigFile)

    if not os.path.isfile(m_ConfigFileJs):
        text_file = codecs.open(m_ConfigFileJs, encoding='utf-8-sig',mode='w')
        jsFile = "var settings =" + json.dumps(MySettings.__dict__, encoding="utf-8-sig") + ";"
        text_file.write(jsFile)
        text_file.close()

    return

def Execute(data):
    if data.IsChatMessage() and MySettings.Enabled and data.GetParam(0).lower() == MySettings.Command.lower():
        if data.GetParam(1).lower() == "":
            userCurrency = Parent.GetPoints(data.User)
            if userCurrency != 0:
                dict = {Parent.GetDisplayName(data.User): int(userCurrency)}
                Parent.BroadcastWsEvent("EVENT_CURRENCY_SHOW",json.dumps(dict))
        else:
            userCurrency = Parent.GetPoints(data.GetParam(1))
            if userCurrency != 0:
                dict = {Parent.GetDisplayName(data.GetParam(1)): int(userCurrency)}
                Parent.BroadcastWsEvent("EVENT_CURRENCY_SHOW",json.dumps(dict))
    return

def Tick():
    return

def ReloadSettings(jsonData):
    MySettings.__dict__ = json.loads(jsonData)
    Parent.BroadcastWsEvent("EVENT_CURRENCY_RELOAD",jsonData)
    return
