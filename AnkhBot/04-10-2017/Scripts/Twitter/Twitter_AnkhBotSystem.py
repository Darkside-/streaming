#---------------------------------------
# Import Libraries
#---------------------------------------
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

import json
import os
import re
import codec
from twython import Twython


#---------------------------------------
# [Required] Script Information
#---------------------------------------
debuggingMode = True
ScriptName = "Twitter"
Website = "https://www.AnkhBot.com"
Description = "Sends out a Tweet with stream information when the stream begins."
Creator = "Kroot"
Version = "0.1.0.0"


#---------------------------------------
# Set Variables
#---------------------------------------
APP_KEY = 'CcINPk5tD9CPqlRWiuXcgYPot'
APP_SECRET = 'KymVs21tyxlxEuuhSI7O3Hq2VUt7Yu4W4V1yaMgMaek6FC6ZNJ'
OAUTH_TOKEN = '7289822-brKfNH63IlJn9d4l2MjhpUL7FiAftnbm9HD8OhW7gj'
OAUTH_TOKEN_SECRET = 'MgcuyVmr3huG2CB9KrWldaLu9S2pBorGqaasASiaJI6xT'
twitter = Twython(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
twitter_msg = ''

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
	
 return

 
#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
 if data.IsChatMessage():
 if data.GetParam(0).lower() == m_Command and not
Parent.IsOnCooldown(ScriptName,m_Command) and
Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):
 Parent.SendTwitchMessage(m_Response)
 return
 

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
 return

#---------------------------------------
#  Send a tweet
#---------------------------------------
def sendTweet():
	twitter.update_status(twitter_msg)
	return
