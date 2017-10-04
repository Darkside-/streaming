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
ScriptName = "GET Request Demo"
Website = "http://www.twitch.tv/ocgineer"
Description = "GET Request Demo replacing $weather parameter with response from a weather api"
Creator = "Ocgineer"
Version = "1.1.0.0"

# Version
# > 1.1.0 : Updated response parsing as AnkhBot includes status in the response
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
			self.City = "London"

	# Reload settings on save through UI
	def ReloadSettings(self, data):
		self.__dict__ = json.loads(data)
		return

#---------------------------------------
# Initialize data on load
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
# Parse parameters
#---------------------------------------
def Parse(parseString, user, target, message):

	# $chours parameter
	if "$weather" in parseString:
	
		# Weather API Uri
		WeatherApiUri = "http://api.scorpstuff.com/weather.php?city={0}"

		# Header is mandatory python dictionary, even if it is empty
		WeatherApiHeaders = {}
		
		# GET Request API endpoint
		response = Parent.GetRequest(WeatherApiUri.format(ScriptSettings.City), WeatherApiHeaders)

		# Parse the response (to extract status and response)
		reponseObj = json.loads(response)

		# if status 200 : success
		if reponseObj["status"] == 200:

			# replace parameter with response output
			return parseString.replace("$weather", reponseObj["response"])

		# on error:
		else:
			
			# replace parameter with error
			return parseString.replace("$weather", "API Error: {0}".format(reponseObj["status"]))	
		
	# Return unaltered parseString
	return parseString