#---------------------------------------
#	Import Libraries
#---------------------------------------
import sys
#Point the file to your Python Install Directory [Required]
sys.path.append("C:\Python27\lib")
import clr
import datetime
import random

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "GambleScript"
Website = "https://www.AnkhBot.com"
Creator = "AnkhHeart"
Version = "1.0.0.0"
Description = "!gamble (amount) to use the command."
#---------------------------------------
#	Set Variables
#---------------------------------------
m_RollMessage = "Rolled {0}. "
m_WonMessage = "{0} won {1} and now has {2}."
m_LostMessage = "{0} lost {1} and now has {2}."
m_NotEnoughCurrency = "{0}, You don't have enough currency."
m_MaxLoseValue = 50
m_MaxWinSingleValue = 90

m_Command = "!gamble"
m_CommandPermission = "everyone"
m_CommandInfo = ""

m_CooldownSeconds = 10
m_LastUsed = datetime.datetime.now()
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
		#---------------------------------------
		# Check if there are enough parameters
		#---------------------------------------
		
		#---------------------------------------
		# Parse the Command & Value
		#---------------------------------------
		if data.GetParam(0).lower() == m_Command and not Parent.IsOnUserCooldown(ScriptName,m_Command,data.User) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo) and data.GetParam(1).isdigit():
			gambleInt = int(data.GetParam(1))
			
			if Parent.RemovePoints(data.User,gambleInt):
				#---------------------------------------
				# Roll a Random Number
				#---------------------------------------
				randomNumber = Parent.GetRandom(0,100)

				#---------------------------------------
				# Determine Outcome
				#---------------------------------------
				if randomNumber < m_MaxLoseValue:
					Parent.SendTwitchMessage(m_RollMessage.format(randomNumber) + m_LostMessage.format(Parent.GetDisplayName(data.User),gambleInt,Parent.GetPoints(data.User)))
				elif randomNumber < m_MaxWinSingleValue:
					Parent.AddPoints(data.User,gambleInt*2)
					Parent.SendTwitchMessage(m_RollMessage.format(randomNumber) + m_WonMessage.format(Parent.GetDisplayName(data.User),gambleInt*2,Parent.GetPoints(data.User)))
				else:
					Parent.AddPoints(data.User,gambleInt*3)
					Parent.SendTwitchMessage(m_RollMessage.format(randomNumber) + m_WonMessage.format(Parent.GetDisplayName(data.User),gambleInt*3,Parent.GetPoints(data.User)))
			
			Parent.AddUserCooldown(ScriptName,m_Command,data.User,m_CooldownSeconds)
		return

#---------------------------------------
#	[Required] Tick Function
#---------------------------------------
def Tick():
	return