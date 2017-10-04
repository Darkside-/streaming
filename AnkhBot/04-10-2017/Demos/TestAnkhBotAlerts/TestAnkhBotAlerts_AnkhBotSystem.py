#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

import json
import os

#---------------------------------------
#	Script Information
#---------------------------------------
ScriptName = "Test AnkhBot Alerts"
Website = "http://www.twitch.tv/ocgineer"
Creator = "Ocgineer"
Version = "1.0.1.0"
Description = "Trigger AnkhBot websocket alerts for testing custom alerts overlay. After editing values, make sure to save first before triggering an alert!"

# Version
# > 1.0.1 : Cleaned up code
# > 1.0.0 : Initial public release

#---------------------------------------
#	Variables
#---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "TestAlertsSettings.json")

#---------------------------------------
#	Classes
#---------------------------------------
class Settings:
	# Tries to load settings from file if given else set defaults
	def __init__(self, settingsFile = None):
		if settingsFile is not None and os.path.isfile(settingsFile):
			with open(settingsFile) as f:
				self.__dict__ = json.load(f)
		else:
			self.display_name = "SomeTwitchName"
			self.host_amount_viewers = 15
			self.cheer_amount_bits = 150
			self.cheer_total_bits = 1200
			self.cheer_message = "cheer50 You are such a pleb! cheer100"
			self.tsub_tier = "1000"
			self.tsub_months = 1
			self.tsub_message = "I subbed like a boss!"
			self.gsub_tier = 1
			self.gsub_months = 1
			self.donation_amount = "10"
			self.donation_currency = "EUR"
			self.donation_message = "Take muh money!"

	# Reload settings on save through UI
	def ReloadSettings(self, data):
		self.__dict__ = json.loads(data)
		return

class FollowAlert:
	def __init__(self, dName):
		self.name = dName.lower()
		self.display_name = dName

class HostAlert:
	def __init__(self, dName, viewers):
		self.name = dName.lower()
		self.display_name = dName
		self.viewers = viewers

class CheerAlert:
		def __init__(self, dName, bits, tBits, message):
			self.name = dName.lower()
			self.display_name = dName
			self.bits = bits
			self.total_bits = tBits
			self.message = message
		
class TwitchSubAlert:
	def __init__(self, dName, tier, months, message):
		self.name = dName.lower()
		self.display_name = dName
		self.tier = tier
		self.is_resub = True if months > 1 else False
		self.months = months if months > 0 else 1
		self.message = message

class GamewispSubAlert:
	def __init__(self, dName, tier, months):
		self.name = dName.lower()
		self.display_name = dName
		self.tier = tier if tier > 0 else 1
		self.is_resub = True if months > 1 else False
		self.months = months if months > 0 else 1

class DonationAlert:
	def __init__(self, dName, amount, currency, message):
		self.name = dName.lower()
		self.display_name = dName
		self.amount = amount
		self.currency = currency
		self.message = message

#---------------------------------------
#	Intialize Data on Load
#---------------------------------------
def Init():
	# Globals
	global ScriptSettings

	# Load in saved settings
	ScriptSettings = Settings(SettingsFile)	

	# End of Init
	return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):	
	# Globals
	global ScriptSettings

	# Reload saved settings
	ScriptSettings.ReloadSettings(jsonData)

	# End of ReloadSettings
	return

#---------------------------------------
#	Execute data and process messages
#---------------------------------------
def Execute(data):
	return

#---------------------------------------
#	Tick
#---------------------------------------
def Tick():
	return

#---------------------------------------
#	Button Functions
#---------------------------------------	
def TriggerFollowAlert():
	followAlertData = FollowAlert(ScriptSettings.display_name)
	Parent.BroadcastWsEvent("EVENT_FOLLOW", json.dumps(followAlertData.__dict__))
	return
	
def TriggerHostAlert():
	hostAlertData = HostAlert(ScriptSettings.display_name, ScriptSettings.host_amount_viewers)
	Parent.BroadcastWsEvent("EVENT_HOST", json.dumps(hostAlertData.__dict__))
	return
	
def TriggerCheerAlert():
	cheerAlertData = CheerAlert(ScriptSettings.display_name, ScriptSettings.cheer_amount_bits, ScriptSettings.cheer_total_bits, ScriptSettings.cheer_message)
	Parent.BroadcastWsEvent("EVENT_CHEER", json.dumps(cheerAlertData.__dict__))
	return

def TriggerTwitchSubAlert():
	twitchSubAlertData = TwitchSubAlert(ScriptSettings.display_name, ScriptSettings.tsub_tier, ScriptSettings.tsub_months, ScriptSettings.tsub_message)
	Parent.BroadcastWsEvent("EVENT_SUB", json.dumps(twitchSubAlertData.__dict__))
	return

def TriggerGameWispSubAlert():
	gamewispSubAlertData = GamewispSubAlert(ScriptSettings.display_name, ScriptSettings.gsub_tier, ScriptSettings.gsub_months)
	Parent.BroadcastWsEvent("EVENT_GW_SUB", json.dumps(gamewispSubAlertData.__dict__))
	return

def TriggerDonationAlert():
	donationAlertData = DonationAlert(ScriptSettings.display_name, ScriptSettings.donation_amount, ScriptSettings.donation_currency, ScriptSettings.donation_message)
	Parent.BroadcastWsEvent("EVENT_DONATION", json.dumps(donationAlertData.__dict__))