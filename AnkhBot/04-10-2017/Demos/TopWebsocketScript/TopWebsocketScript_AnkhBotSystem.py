#---------------------------------------
#   Import Libraries
#---------------------------------------
import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime
import json
import operator

#---------------------------------------
#   [Required] Script Information
#---------------------------------------
ScriptName = "TopWebsocketScript"
Website = "https://www.AnkhBot.com"
Description = "!top will display the top 10 users in the Html Page"
Creator = "AnkhHeart"
Version = "1.0.0.0"

#---------------------------------------
#   [Required] Declare Variables
#---------------------------------------
g_Command = "!top"
g_Command2 = "!toph"
g_Top = 10
#---------------------------------------
#   [Required] Initialize Data / Load Only
#---------------------------------------
def Init():
    return

def Execute(data):
    if data.IsChatMessage():
        if data.GetParam(0).lower() == g_Command:
            top10 = Parent.GetTopCurrency(g_Top)
            top10 = sorted(top10.iteritems(), key=lambda i: int(i[1]),reverse=True)
            Parent.BroadcastWsEvent("EVENT_TOP_10_POINTS",json.dumps(top10))
        elif data.GetParam(0).lower() == g_Command2:
            top10 = Parent.GetTopHours(g_Top)
            top10 = sorted(top10.iteritems(), key=lambda i: int(i[1]),reverse=True)
            Parent.BroadcastWsEvent("EVENT_TOP_10_HOURS",json.dumps(top10))
    return

def Tick():
    return