#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

import json
import os
import re
import codecs
#---------------------------------------
#	Script Information
#---------------------------------------
ScriptName = "Two Player Scoreboard"
Website = "http://www.twitch.tv/ocgineer"
Creator = "Ocgineer"
Version = "1.1.1.0"
Description = "A Two player score keeper with customizable overlay scoreboard."

# Version
# > 1.1.1 : Code cleanup
# > 1.1.0 : Added override width to fix overlay width
# > 1.0.0 : Initial public release

#---------------------------------------
#	Variables
#---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "ScoreboardSettings.json")
SetNameRE = re.compile(r"(?:setname\s+p[12]\s+)(?P<name>\S.*)", re.I)

#---------------------------------------
#	Classes
#---------------------------------------
class Settings:
	# Tries to load settings from file if given else set defaults
	def __init__(self, settingsFile = None):
		if settingsFile is not None and os.path.isfile(settingsFile):
			with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
				self.__dict__ = json.load(f, encoding='utf-8-sig')
		else:
			self.PlayerOneName = "Player1"
			self.PlayerOneScore = 0
			self.PlayerTwoName = "Player2"
			self.PlayerTwoScore = 0	
			self.control_command = "!score"
			self.control_permission = "Moderator"
			self.control_permission_info = ""
			self.response_score_total = "Current score: {0} [{1}] - {2} [{3}]."
			self.response_score_player = "{0}'s score is {1}."
			self.response_score_update = "{0}'s score is updated to {1}."
			self.response_name_update = "{0}'s name is updated to {1}."
			self.response_scoreboard_show = "Scoreboard is now shown."
			self.response_scoreboard_hide = "Scoreboard is now hidden."
			self.response_score_clear = "Score data is cleared."
			self.override_width = 0
			self.color_seperator = "rgba(230,126,34,1)"
			self.color_seperator_bg = "rgba(30,30,30,1)"
			self.color_p1_name = "rgba(255,255,255,1)"
			self.color_p1_name_bg = "rgba(0,0,0,0.59)"
			self.color_p1_score = "rgba(255,255,255,1)"
			self.color_p1_score_bg = "rgba(255,128,128,0.75)"
			self.color_p2_name = "rgba(255,255,255,1)"
			self.color_p2_name_bg = "rgba(0,0,0,0.59)"
			self.color_p2_score = "rgba(255,255,255,1)"
			self.color_p2_score_bg = "rgba(0,128,255,0.75)"
			self.color_scoreboard_border = "rgba(230,126,34,255)"
			self.color_scoreboard_showborder = True

	# Reload settings on save through UI
	def ReloadSettings(self, data):
		self.__dict__ = json.loads(data, encoding='utf-8-sig')
		return

	# Save settings to files (json and js)
	def SaveSettings(self, settingsFile):
		with codecs.open(settingsFile, encoding='utf-8-sig',mode='w+') as f:
			json.dump(self.__dict__, f)
		with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
			f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
		return

	# Verify values within Settings
	def VerifyValues(self):
		if self.control_command == "":
			self.control_command = "!score"

#---------------------------------------
#	Functions
#---------------------------------------
def UpdateScoreboard():
	Parent.BroadcastWsEvent("EVENT_SCOREBOARD_UPDATE", json.dumps(ScoreboardSettings.__dict__, encoding='utf-8-sig'))
	return

def ShowScoreboard():
	Parent.BroadcastWsEvent("EVENT_SCOREBOARD_SHOW", json.dumps(ScoreboardSettings.__dict__, encoding='utf-8-sig'))
	return
	
def HideScoreboard():
	Parent.BroadcastWsEvent("EVENT_SCOREBOARD_HIDE", None)
	return

#---------------------------------------
#	Intialize Data on Load
#---------------------------------------
def Init():
	# Globals
	global ScoreboardSettings

	# Load in saved settings
	ScoreboardSettings = Settings(SettingsFile)
	ScoreboardSettings.VerifyValues()
			
	# Send scoring data to websocket
	UpdateScoreboard()

	# End of Init
	return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
	# Globals
	global ScoreboardSettings

	# Reload saved settings
	ScoreboardSettings.ReloadSettings(jsonData)

	# Send updated scoring data to websocket
	UpdateScoreboard()

	# End of ReloadSettings
	return
	
#---------------------------------------
#	Execute data and process messages
#---------------------------------------
def Execute(data):
	# Continue if it is a chat message
	if data.IsChatMessage():

		# Globals
		global ScoreboardSettings
	
		# Check for command and permission
		if (data.GetParam(0).lower() == ScoreboardSettings.control_command and
				Parent.HasPermission(data.User, ScoreboardSettings.control_permission,
				ScoreboardSettings.control_permission_info)):

			# Command has parameters
			if data.GetParamCount() > 1:
				
				# Command: !score clear
				# Clears data to default values
				if data.GetParam(1).lower() == "clear":
					HideScoreboard()
					ScoreboardSettings.PlayerOneName = "Player1"
					ScoreboardSettings.PlayerTwoName = "Player2"
					ScoreboardSettings.PlayerOneScore = 0
					ScoreboardSettings.PlayerTwoScore = 0
					ScoreboardSettings.SaveSettings(SettingsFile)				
					Parent.SendTwitchMessage(ScoreboardSettings.response_score_clear)
					
				# Command !score show
				# Display the scoreboard on the overlay
				elif data.GetParam(1).lower() == "show":
						ShowScoreboard()
						Parent.SendTwitchMessage(ScoreboardSettings.response_scoreboard_show)

				# Command !score hide
				# Hides the scoreboard on the overlay
				elif data.GetParam(1).lower() == "hide":
						HideScoreboard()
						Parent.SendTwitchMessage(ScoreboardSettings.response_scoreboard_hide)
										
				# Command: !score setname [p1 | p2] [name]
				# Sets the name of player 1 or 2
				elif data.GetParam(1).lower() == "setname":	
				
					# Check if player-select and name parameter is present
					if data.GetParamCount() > 3:
					
						# Set name of player 1
						if data.GetParam(2).lower() == "p1":
							# Regex to get name with potential whitespace
							result = SetNameRE.search(data.Message)							
							# Continue of name is given (starting with a non-whitespace char)
							if result is not None:
								ScoreboardSettings.PlayerOneName = result.group('name')
								UpdateScoreboard()
								Parent.SendTwitchMessage(ScoreboardSettings.response_name_update.format("Player 1", ScoreboardSettings.PlayerOneName))

								# Save settings
								ScoreboardSettings.SaveSettings(SettingsFile)
							else:
								Parent.SendTwitchMessage("No valid name was given for p1.")
							
						# Set name of player 2
						elif data.GetParam(2).lower() == "p2":
							# Regex to get name with potential whitespace
							result = SetNameRE.search(data.Message)							
							# Continue of name is given (starting with a non-whitespace char)
							if result is not None:
								ScoreboardSettings.PlayerTwoName = result.group('name')
								UpdateScoreboard()
								Parent.SendTwitchMessage(ScoreboardSettings.response_name_update.format("Player 2", ScoreboardSettings.PlayerTwoName))

								# Save settings
								ScoreboardSettings.SaveSettings(SettingsFile)
							else:
								Parent.SendTwitchMessage("No valid name was given for p2.")
							
						# Invalid player selection
						else:
							Parent.SendTwitchMessage("Setname usage: {0} setname [p1 | p2] <name>".format(ScoreboardSettings.control_command))	
							
					# Invalid parameter count
					else:
						Parent.SendTwitchMessage("Setname usage: {0} setname [p1 | p2] <name>".format(ScoreboardSettings.control_command))
					
				# Command !score [p1 | <name>] [<value> | + | -]
				# Manipulate score of player 1, if no score parameter is given print player current score
				elif data.GetParam(1).lower() == "p1" or data.GetParam(1).lower() == ScoreboardSettings.PlayerOneName.lower():
					
					# Score parameter given
					if data.GetParamCount() > 2:
					
						# Add 1 score parameter given
						if data.GetParam(2) == "+":
							ScoreboardSettings.PlayerOneScore += 1
							
						# Substract 1 score parameter given
						elif data.GetParam(2) == "-":
							ScoreboardSettings.PlayerOneScore -= 1
							
						# Score value parameter given
						else:
							try:
								ScoreboardSettings.PlayerOneScore = int(data.GetParam(2))
							except ValueError:
								Parent.SendTwitchMessage("Invalid number given as score, use a whole number.")
								return
						
						# Send changed data to websocket and show message in Twitch chat
						UpdateScoreboard()
						Parent.SendTwitchMessage(ScoreboardSettings.response_score_update.format(ScoreboardSettings.PlayerOneName, ScoreboardSettings.PlayerOneScore))

						# Save settings
						ScoreboardSettings.SaveSettings(SettingsFile)
						
					# No score parameter given, show player current score in Twitch chat
					else:
						Parent.SendTwitchMessage(ScoreboardSettings.response_score_player.format(ScoreboardSettings.PlayerOneName, ScoreboardSettings.PlayerOneScore))
									
				# Command !score [p2 | <name>] [<value> | + | -]
				# Manipulate score of player 2, if no score parameter is given print player current score
				elif data.GetParam(1).lower() == "p2" or data.GetParam(1).lower() == ScoreboardSettings.PlayerTwoName.lower():
					
					# Score parameter given
					if data.GetParamCount() > 2:
						
						# Add 1 score parameter given
						if data.GetParam(2) == "+":
							ScoreboardSettings.PlayerTwoScore += 1
							
						# Substract 1 score parameter given
						elif data.GetParam(2) == "-":
							ScoreboardSettings.PlayerTwoScore -= 1
							
						# Score value parameter given
						else:
							try:
								ScoreboardSettings.PlayerTwoScore = int(data.GetParam(2))
							except ValueError:
								Parent.SendTwitchMessage("Invalid number given as score, use a whole number.")
								return
								
						# Send changed data to websocket and show message in Twitch chat
						UpdateScoreboard()
						Parent.SendTwitchMessage(ScoreboardSettings.response_score_update.format(ScoreboardSettings.PlayerTwoName, ScoreboardSettings.PlayerTwoScore))
						
						# Save settings
						ScoreboardSettings.SaveSettings(SettingsFile)
						
					# No score parameter given, show player current score in Twitch chat
					else:
						Parent.SendTwitchMessage(ScoreboardSettings.response_score_player.format(ScoreboardSettings.PlayerTwoName, ScoreboardSettings.PlayerTwoScore))
			
				# Incorrect parameter is given, show help message
				else:
					Parent.SendTwitchMessage("Scoreboard Commands: {0} [clear | show | hide | setname | p1 | p2]".format(ScoreboardSettings.control_command))
							
			# Command has no parameters, display current score in Twitch chat
			else:
				Parent.SendTwitchMessage(ScoreboardSettings.response_score_total.format(ScoreboardSettings.PlayerOneName, ScoreboardSettings.PlayerOneScore, ScoreboardSettings.PlayerTwoName, ScoreboardSettings.PlayerTwoScore))

	# End of Execute		
	return

#---------------------------------------
#	Tick
#---------------------------------------
def Tick():
	return