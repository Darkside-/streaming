#!/usr/bin/python
# -*- coding: utf-8 -*-

""" LOAD SAVE SETTINGS DEMO SCRIPT

This script demonstrates how to create a settings class that can hold
all of your settings variables made through the user interface.

The class also demonstrates the use of various methods to use to load
in settings from file, reload settings from given json string, save back
potentially changed settings back to file and even demonstrate how to
make use of the default settings if a settings file is not given to
create a 'Default Settings' function to reset settings back to defaults.

If the settings file to load, created either by pressing 'Save Settings'
on the UI or the script calls the Settings.Save() method, is not present
it will load in the given defaults.

It is mandatory that the properties of the class match the name of the
UI element in UI_Config. It is preffered to match the value of said
property with the default value set in UI_Config to avoid confusion.

AnkhBot writes the settings file as UTF-8 with BOM which means it is
allowed to use unicode in the settings file. To use plain unicode in
a Python source, and not having to use unicode escape characters, one
must define the script encoding as utf-8 as can be seen at the first
two lines of this script.

Also you can create a defaults button that reset the settings to the
set defaults by the creator of the script. You can do that by
overwriting the global ScriptSettings with a new Settings class but
not supply the settings file path, it will then set the defaults.

Within the script you can find some additional information about the
available build in functions that is also described in the documents.
If you were to use this file as 'template' you can safely remove them
as they would serve no use to those that know what said functions do.

Version
	1.2.0
		Small update on the Settings class and added comments in default
		functions. Added a 'Default Settings' button to demonstrate how
		to let users reset settings to defaults.

	1.1.0
		Using codec to read and save settings files as UTF-8
		and demonstrating Unload and ScriptToggled to save settings.

		Also showing how to use unicode within the source code of
		Python without the need to escape, by defining encoding.

	1.0.1
		Clean up code

	1.0.0
		Initial public release

"""

#---------------------------------------
# Import Libraries
#---------------------------------------
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

import os
import codecs
import json
import time

#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = "Load Save Settings Demo Script"
Website = "http://www.twitch.tv/ocgineer"
Description = "Demo to show load, reload and save settings methods on a settings class"
Creator = "Ocgineer"
Version = "1.2.0.0"

#---------------------------------------
# Variables
#---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
# Classes
#---------------------------------------
class Settings(object):
	""" Load in saved settings file if available else set default values. """
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.Command = "!settingsdemo"
			self.SomeMessage = "Hello! こんにちわ！"

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
# Initialize Data on Load
#---------------------------------------
def Init():

	"""
		Init is a required function and is called the script is being loaded into memory
		and becomes	active. In here you can initialize any data your script will require,
		for example read the settings file for saved settings.
	"""

	# Globals
	global ScriptSettings

	# Load in saved settings
	ScriptSettings = Settings(SettingsFile)

	# End of Init
	return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsondata):

	"""
		ReloadSettings is an optional function that gets called once the user clicks on
		the Save Settings button of the corresponding script in the scripts tab if an
		user interface has been created for said script. The entire Json object will be
		passed to the function	so you can load that back	into your settings without
		having to read the newly saved settings file.
	"""

	# Globals
	global ScriptSettings

	# Reload newly saved settings
	ScriptSettings.Reload(jsondata)

	# End of ReloadSettings
	return

#---------------------------------------
#	Script is going to be unloaded
#---------------------------------------
def Unload():

	"""
		Unload is an optional function that gets called when a script is getting
		reloaded, unloaded, or AnkhBot gets closed so you can do some final	actions	in
		here for example saving any data. In this example we save the changed	settings
		back to file, so upon reload the proper setting values are loaded	back in.
	"""

	# Save changed settings on unload
	ScriptSettings.Save(SettingsFile)

	# End of Unload
	return

#---------------------------------------
#	Script is enabled or disabled on UI
#---------------------------------------
def ScriptToggled(state):

	"""
		ScriptToggled is an optional function that gets called when your script is
		Enabled or Disabled through the AnkhBot UI. The state object is Boolean which
		either is 'True' if the script has become enabled	or 'False' when the script
		has	become disabled.

		This function is also called after Init as AnkhBot needs to determine the state
		of the script and the state will still contain the actual state of the switch the
		user has set it to.
	"""

	# Globals
	global ScriptSettings

	# Upon disabled (toggled off)
	if not state:

		# Even though script stays in memory
		# but the execute and tick are not called
		# we just save here to demonstrate this
		ScriptSettings.Save(SettingsFile)

	# End of Unload
	return

#---------------------------------------
# Execute data and process messages
#---------------------------------------
def Execute(data):

	"""
		Execute is a required function that gets called when there is new data to be
		processed. Like a Twitch or Discord chat messages or even raw data send from
		Twitch IRC.	This function will _not_ be called when the user disabled the script
		with the switch on the user interface.
	"""

	# Continue if it is a Twich or Discord message
	if data.IsChatMessage():

		# Globals
		global ScriptSettings

		# Continue if command matches
		if data.GetParam(0).lower() == ScriptSettings.Command:

			old = ScriptSettings.SomeMessage
			new = "時間 {}".format(time.time())
			ScriptSettings.SomeMessage = new

			Parent.SendTwitchMessage("The 'Some Message' settings value is now internally changed from {} to {}.".format(old, new))
			Parent.SendTwitchMessage("It will be saved upon Unload (reload scripts / close AnkhBot) OR ScriptToggled (script enable to 'off').")

	# End of execute
	return

#---------------------------------------
# Tick
#---------------------------------------
def Tick():

	"""
		Tick is a required function and will be called every time the program progresses.
		This can be used for example to create simple timer if you want to do let the
		script do something on a timed basis.This function will _not_ be called	when the
		user disabled the script	with the switch on the user interface.
	"""

	return

#---------------------------------------
# SetDefaults Custom User Interface Button
#---------------------------------------
def SetDefaults():

	# Globals
	global ScriptSettings

	# Set defaults by not supplying a settings file
	ScriptSettings = Settings()

	# Save defaults back to file
	ScriptSettings.Save(SettingsFile)

	# End of SetDefaults
	return
