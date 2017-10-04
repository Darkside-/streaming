#---------------------------------------
#	Import Libraries
#---------------------------------------
import sys
import clr
import datetime

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "DemoScript"
Website = "https://www.AnkhBot.com"
Creator = "AnkhHeart"
Version = "1.0.0.0"
Description = "!test posts a message."

#---------------------------------------
#	Set Variables
#---------------------------------------
m_Response = "This is a test message"
m_Command = "!test"
m_LastUsed = datetime.datetime.now()
m_CooldownSeconds = 10

#---------------------------------------
#	[Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
	return

#---------------------------------------
#	[Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
	if data.IsChatMessage():
		if data.GetParam(0).lower() == m_Command and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,"moderator",""):
			Parent.SendTwitchMessage(m_Response)
			Parent.AddCooldown(ScriptName,m_Command,m_CooldownSeconds)
	return

#---------------------------------------
#	[Required] Tick Function
#---------------------------------------
def Tick():
	return