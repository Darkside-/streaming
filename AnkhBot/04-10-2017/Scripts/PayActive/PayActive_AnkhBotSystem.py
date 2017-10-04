#---------------------------------------
#	Import Libraries
#---------------------------------------
import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import os
import codecs
import json

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "PayActive"
Website = "https://www.twitch.tv/furriffic"
Creator = "FurRiffic"
Version = "1.0.0.0"
Description = "!payactive <amount> <time> (just amount or no paramaters works too)"

#---------------------------------------
#	Set Variables
#---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
m_countdownActive = 0
m_countdownPoints = 0
m_countdownTime = 0
#---------------------------------------
# Save/Load
#---------------------------------------

class Settings(object):
	""" Load in saved settings file if available else set default values. """
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.m_command = "!payactive"
			self.m_settingsCommand = "!paysettings"
			self.m_excludeStreamer = False
			self.m_notLivePoints = 10
			self.m_notLiveMin = 3600
			self.m_notLiveMax = 7200
			self.m_notLivePayout = True
			self.m_defaultPoints = 50
			self.m_defaultCooldown = 300
			self.m_maxPayout = 1000
			self.m_defaultMessage = "Hey there, chatters, in 5 minutes everyone who has been active in the last 15 minutes will receive {0} {1}!" #{0} = m_defaultPoints, {1} = currencyname
			self.m_secondsMessage = "Hey there, chatters, in {2} seconds everyone who has been active in the last 15 minutes will receive {0} {1}!" #{0} = m_defaultPoints, {1} = currencyname, {2} = seconds
			self.m_minutesMessage = "Hey there, chatters, in {2} minutes everyone who has been active in the last 15 minutes will receive {0} {1}!" #{0} = m_defaultPoints, {1} = currencyname, {2} = minutes
			self.m_payMessage = "The following users have gotten {0} {1}: {2}." #{0} = m_defaultPoints, {1} = currencyname, {2} = comma-seperated list of viewers
			self.m_manyEnd = "... and more then twitch can handle!"
			self.m_overPayout = "{0}, I think you made a typo there, the max is {1}" #{0} = user {1} = Max Payout message
			self.m_noPayout = "Seems like there was no-one here to give these {0} {1} to, oh well, more for me!" #{0} = Points that would have been given {1} = Currencyname
			self.m_wrongParamters = "{0}, I dont get what you mean with that" #{0} = user

	def Reload(self, jsondata):
		""" Reload settings from AnkhBot user interface by given json data. """
		self.__dict__ = json.loads(jsondata, encoding="utf-8")
		return

	def Save(self, settingsfile):
		""" Save settings contained within to .json and .js settings files. """
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
				json.dump(self.__dict__, f, encoding="utf-8")
			with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
				f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
		except:
			Parent.Log(ScriptName, "Failed to save settings to file.")
		return

#---------------------------------------
#	[Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
	Parent.AddCooldown(ScriptName, "!PayActiveOfflineCommandThingie", 910) #15 minutes + 10 seconds to prevent mod-payout
	global ScriptSettings
	ScriptSettings = Settings(SettingsFile)
	return
#---------------------------------------
#	Save on unload
#---------------------------------------
def Unload():
	ScriptSettings.Save(SettingsFile)
	return
def ReloadSettings(jsondata):
	global ScriptSettings
	ScriptSettings.Reload(jsondata)
	return
def ScriptToggled(state):
	global ScriptSettings
	if not state:
		ScriptSettings.Save(SettingsFile)
	return
#---------------------------------------
#	[Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
	global m_countdownPoints
	global m_countdownActive
	if data.IsChatMessage():
		if data.GetParam(0).lower() == ScriptSettings.m_command and not Parent.IsOnCooldown(ScriptName, ScriptSettings.m_command) and Parent.HasPermission(data.User, "moderator", ""):
			if data.GetParamCount() == 1:
				Parent.AddCooldown(ScriptName, ScriptSettings.m_command, ScriptSettings.m_defaultCooldown)
				m_countdownPoints = ScriptSettings.m_defaultPoints
				m_countdownActive = 1
				Parent.SendTwitchMessage(ScriptSettings.m_defaultMessage.format(ScriptSettings.m_defaultPoints, Parent.GetCurrencyName()))
			elif data.GetParamCount() == 2:
				try:
					m_countdownPoints = int(data.GetParam(1))
					if m_countdownPoints > ScriptSettings.m_maxPayout:
						Parent.SendTwitchMessage(ScriptSettings.m_overPayout.format(data.User, ScriptSettings.m_maxPayout))
						return
					PayActive()
				except:
					Parent.SendTwitchMessage(ScriptSettings.m_wrongParamters.format(data.User))
			elif data.GetParamCount() == 3:
				if data.GetParam(2).lower().endswith('m'):
					try:
						m_countdownPoints = int(data.GetParam(1))
						if m_countdownPoints > ScriptSettings.m_maxPayout:
							Parent.SendTwitchMessage(ScriptSettings.m_overPayout.format(data.User, ScriptSettings.m_maxPayout))
							return
						minutes = data.GetParam(2)
						minutes = minutes[:-1]
						seconds = int(minutes)*60
						Parent.AddCooldown(ScriptName, ScriptSettings.m_command, seconds)
						m_countdownActive = 1
						Parent.SendTwitchMessage(ScriptSettings.m_minutesMessage.format(m_countdownPoints, Parent.GetCurrencyName(), minutes))
					except:
						Parent.SendTwitchMessage(ScriptSettings.m_wrongParamters.format(data.User))
				else:
					try:
						m_countdownPoints = int(data.GetParam(1))
						if m_countdownPoints > ScriptSettings.m_maxPayout:
							Parent.SendTwitchMessage(ScriptSettings.m_overPayout.format(data.User, ScriptSettings.m_maxPayout))
							return
						m_countdownTime = int(data.GetParam(2))
						Parent.AddCooldown(ScriptName, ScriptSettings.m_command, m_countdownTime)
						m_countdownActive = 1
						Parent.SendTwitchMessage(ScriptSettings.m_secondsMessage.format(m_countdownPoints, Parent.GetCurrencyName(), m_countdownTime))
					except:
						Parent.SendTwitchMessage(ScriptSettings.m_wrongParamters.format(data.User))
		return
#---------------------------------------
#	[Required] Tick Function
#---------------------------------------
def Tick():
	global m_countdownPoints
	global m_countdownActive
	if m_countdownActive == 1:
		if not Parent.IsOnCooldown(ScriptName, ScriptSettings.m_command):
			m_countdownActive = 0
			PayActive()
			m_countdownPoints = 0
	if not Parent.IsLive() and not Parent.IsOnCooldown(ScriptName, "!PayActiveOfflineCommandThingie") and ScriptSettings.m_notLivePayout and not Parent.IsOnCooldown(ScriptName, ScriptSettings.m_command):
		Parent.AddCooldown(ScriptName, ScriptSettings.m_command, 900)
		randomTimer = Parent.GetRandom(ScriptSettings.m_notLiveMin, ScriptSettings.m_notLiveMax)
		Parent.AddCooldown(ScriptName, "!PayActiveOfflineCommandThingie", randomTimer)
		m_countdownActive = 1
		#global m_countdownPoints
		m_countdownPoints = ScriptSettings.m_notLivePoints
		Parent.SendTwitchMessage("Hey there, chatters, in 15 minutes everyone who has been active in the last 15 minutes will receive {} {}!".format(ScriptSettings.m_notLivePoints, Parent.GetCurrencyName()))
	if Parent.IsLive() and not Parent.IsOnCooldown(ScriptName, "!PayActiveOfflineCommandThingie"):
		Parent.AddCooldown(ScriptName, "!PayActiveOfflineCommandThingie", 5400)
	return

def PayActive():
	ActiveUsers = Parent.GetActiveUsers()
	if ScriptSettings.m_excludeStreamer:
		ActiveUsers2 = [username for username in ActiveUsers if username != Parent.GetChannelName()]
		ActiveUsers = ActiveUsers2
	myDict = {}
	for username in ActiveUsers:
		myDict[username] = m_countdownPoints
	if not bool(myDict):
		Parent.SendTwitchMessage(ScriptSettings.m_noPayout.format(m_countdownPoints, Parent.GetCurrencyName()))
		return
	str1 = ', '.join(ActiveUsers)
	Parent.AddPointsAll(myDict)
	sendMessage = ScriptSettings.m_payMessage.format(m_countdownPoints, Parent.GetCurrencyName(), str1)
	if len(sendMessage) > (490 - len(ScriptSettings.m_manyEnd)):
		sendMessage = sendMessage[:-len(ScriptSettings.m_manyEnd)] + ScriptSettings.m_manyEnd
	Parent.SendTwitchMessage(sendMessage)
	Parent.AddCooldown(ScriptName, ScriptSettings.m_command, 4)
	return
