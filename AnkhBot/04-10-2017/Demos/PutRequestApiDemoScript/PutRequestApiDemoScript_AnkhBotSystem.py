#---------------------------------------
# Import Libraries
#---------------------------------------
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

import os
import json

#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = "PUT Request Demo"
Website = "http://www.twitch.tv/ocgineer"
Description = "GET Request Demo using Twitch API to update title and game"
Creator = "Ocgineer"
Version = "1.0.1.0"

# Version
# > 1.0.1 : Removed unneeded `import requests`
# > 1.0.0 : Initial public release

#---------------------------------------
# Variables
#---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
# Classes
#---------------------------------------
class Settings:
	# Tries to load settings from file if given else set defaults
	def __init__(self, settingsFile = None):
		if settingsFile is not None and os.path.isfile(settingsFile):
			with open(settingsFile) as f:
				self.__dict__ = json.load(f)
		else:
			self.Command = "!putrequest"
			self.Status = "New title set by API with AnkhBot Scripting"
			self.Game = "IRL"
			self.ClientId = ""
			self.AccessToken = ""

	# Reload settings on save through UI
	def ReloadSettings(self, data):
		self.__dict__ = json.loads(data)
		return

#---------------------------------------
# Initialize Data on Load
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
# Execute data and process messages
#---------------------------------------
def Execute(data):

	# Continue if it is a chat message
	if data.IsChatMessage():

		# Globals
		global MySettings

		# Continue if command matches and script is enabled
		if data.GetParam(0).lower() == ScriptSettings.Command:

			# Set Headers to use Twitch API
			# 'Content-Type: application/json' is set by AnkhBot
			headers = {
				"Accept": "application/vnd.twitchtv.v5+json",
				"Client-ID": ScriptSettings.ClientId,
				"Authorization": "OAuth {}".format(ScriptSettings.AccessToken)
			}

			# GET Request to obtain user object assosiated with accesstoken to get the `id`
			r = Parent.GetRequest("https://api.twitch.tv/kraken/user", headers)

			# Parse response to object
			pr = json.loads(r)

			# If status 200 : success
			# We then have a positive response
			if pr["status"] == 200:

				# parse the response message object
				prm = json.loads(pr["response"])

				# Payload to send
				payload = {
					"channel": {
						"status": ScriptSettings.Status,
						"game": ScriptSettings.Game
					}
				}
				
				# PUT Request to update channel data
				r = Parent.PutRequest("https://api.twitch.tv/kraken/channels/{}".format(prm["_id"]), headers, payload, True)
				
				# Parse response to object
				pr = json.loads(r)
				
				# If status 200 : success
				# We have then a positive response
				if pr["status"] == 200:
					Parent.SendTwitchMessage("Successfully updated channel status and game.")
				
				# PUT Request Error
				else:
					Parent.SendTwitchMessage("Failed to update channel data: {0} - {1}".format(pr["status"], pr["error"]))

			# GET Request Error
			else:
				Parent.SendTwitchMessage("Failed to get authenticated user object: {0} - {1}".format(pr["status"], pr["error"]))

	# End of execute
	return

#---------------------------------------
# Tick
#---------------------------------------
def Tick():
    return