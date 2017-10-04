#!/usr/bin/python
# -*- coding: utf-8 -*-

""" NEW SONG ANNOUNCER

New Song Announcer will announce in Twitch Chat when a new song is being
played through AnkhBot. It does this by checking the CurrentSong.txt and
compare it with previous checked veresion. When it detects a new song it
will put out a user defined message in the Twitch chat and will trigger
an websocket event to be used as overlay.

There is a seperate chat output for when the song requester is the caster
himself, so one could prevent himself being pinged when a song is being
played from the casters own playlist.

Spotify Mode is for use without song request and song are played through
the Spotify client itself and NOT with AnkhBot. AnkhBot only writes down
a different textfile with the song info to read, hench this mode. To use
this mode, and to detect the songs, one must still link Spotify with
AnkhBot.

Version
	1.3.0
		Added $prevsong and $prevrequestedby parameter to be used in regular commands
		to be replaced with the previous song title and requester.
	1.2.1
		Updated reading settings file as utf-8-sig due to change also making use
		of the new ScriptToggled to prevent a message on enable
	1.2.0
		Added Spotify mode when using only Spotify Client to play music
	1.1.1
		Using os.getcwd() in init to fix textfile path locations
	1.1.0
		Added seperate response for if caster is the requester
	1.0.3
		Clean up code and added overlay example
	1.0.2
		Reading textfiles as unicode as song titles can contain unicode
	1.0.1
		Trimming whitespaces around song title and requester name
	1.0.0
		Initial public release

"""

#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

import json
import os
import time
import codecs

#---------------------------------------
#	Script Information
#---------------------------------------
ScriptName = "New Song Announcer"
Website = "http://www.twitch.tv/ocgineer"
Creator = "Ocgineer"
Version = "1.3.0.0"
Description = "Announces when a new song is playing in chat and optionally on overlay"

#---------------------------------------
#	Variables
#---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "NSASettings.json")
ScriptSettings = None
TextFiles = None
SongInfo = None
TimeStamp = None
PreviousSong = None
CheckUnlocked = False

#---------------------------------------
#	Classes
#---------------------------------------
class Settings:
	# Tries to load settings from file if given else set defaults
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.MessageViewerRequester = "Now playing: {0} - Requested by {1}"
			self.MessageCasterRequester = "Now playing: {0}"
			self.FileCheck = 5
			self.FileMode = "AnkhBot"

	# Reload settings on save through UI
	def Reload(self, jsonData):
		self.__dict__ = json.loads(jsonData, encoding="utf-8")

	# Validate set values
	def ValidateValues(self):
		if self.FileCheck < 1:
			self.FileCheck = 1

class Info:
	def __init__(self):
		self.Title = ""
		self.Requester = ""
		self.IsPlaylist = False

	@classmethod
	def CopyInfo(cls, songInfo):
		""" Create a copy of songInfo, not a refference. """
		cls = Info()
		cls.Title = songInfo.Title
		cls.Requester = songInfo.Requester
		cls.IsPlaylist = songInfo.IsPlaylist
		return cls

class FilePaths:
	def __init__(self, title, requester, spotify):
		self.SongTitle = title
		self.SongRequester = requester
		self.SongSpotify = spotify

#---------------------------------------
#	Functions
#---------------------------------------
def GetTextFileContent(textfile):
	try:
		with codecs.open(textfile, encoding="utf-8-sig", mode="r") as f:
			return f.readline().strip()
	except:
		return ""

#---------------------------------------
#	Intialize Data on Load
#---------------------------------------
def Init():
	# Globals
	global ScriptSettings
	global TextFiles
	global SongInfo
	global PreviousSong
	global TimeStamp
	global CheckUnlocked

	CheckUnlocked = False

	# Get AnkhBotR2.exe dir path by using os.getcwd() but only in
	# Init() it will return the correct path. Upon exiting this
	# function, os.getcwd() is changed thus we make a full path here.
	TextFiles = FilePaths(
		os.path.join(os.getcwd(), "Twitch\\Files\\CurrentSong.txt"),
		os.path.join(os.getcwd(), "Twitch\\Files\\RequestedBy.txt"),
		os.path.join(os.getcwd(), "Twitch\\Files\\SpotifySong.txt")
	)

	# Load saved settings and validate values
	ScriptSettings = Settings(SettingsFile)
	ScriptSettings.ValidateValues()

	# Get 'current' song info
	PreviousSong = None
	SongInfo = Info()
	if ScriptSettings.FileMode == "AnkhBot":
		SongInfo.Title = GetTextFileContent(TextFiles.SongTitle)
		SongInfo.Requester = GetTextFileContent(TextFiles.SongRequester)
	else:
		SongInfo.Title = GetTextFileContent(TextFiles.SongSpotify)
		SongInfo.Requester = Parent.GetChannelName()

	# Set timestamp and unlock checking files
	TimeStamp = time.time()
	CheckUnlocked = True

	# End of Init
	return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsondata):
	# Globals
	global TimeStamp
	global CheckUnlocked
	global PreviousSong

	# Lock checking files
	CheckUnlocked = False

	# Reload saved settings and validate values
	ScriptSettings.Reload(jsondata)
	ScriptSettings.ValidateValues()

	# Get 'current' song info
	PreviousSong = None
	if ScriptSettings.FileMode == "AnkhBot":
		SongInfo.Title = GetTextFileContent(TextFiles.SongTitle)
		SongInfo.Requester = GetTextFileContent(TextFiles.SongRequester)
	else:
		SongInfo.Title = GetTextFileContent(TextFiles.SongSpotify)
		SongInfo.Requester = Parent.GetChannelName()

	# Set timestamp and unlock checking files
	TimeStamp = time.time()
	CheckUnlocked = True

	# End of ReloadSettings
	return

#---------------------------------------
#	Script is enabled or disabled on UI
#---------------------------------------
def ScriptToggled(state):
	# Globals
	global TimeStamp
	global CheckUnlocked
	global PreviousSong

	# Script Enabled
	if state:

		# Get 'current' song info
		PreviousSong = None
		if ScriptSettings.FileMode == "AnkhBot":
			SongInfo.Title = GetTextFileContent(TextFiles.SongTitle)
			SongInfo.Requester = GetTextFileContent(TextFiles.SongRequester)
		else:
			SongInfo.Title = GetTextFileContent(TextFiles.SongSpotify)
			SongInfo.Requester = Parent.GetChannelName()

		# Set timestamp and unlock checking files
		TimeStamp = time.time()
		CheckUnlocked = True

	# Script Disabled
	else:

		# Lock checking files
		CheckUnlocked = False

	# End of ScriptToggled
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

	# Globals
	global TimeStamp
	global PreviousSong

	# Only check if script is enable and the
	# FileCheck seconds has elapsed to ease reading
	if CheckUnlocked and time.time() - TimeStamp >= ScriptSettings.FileCheck:

		# Set new timestamp
		TimeStamp = time.time()

		# Get current song title
		if ScriptSettings.FileMode == "AnkhBot":
			currentSong = GetTextFileContent(TextFiles.SongTitle)
		else:
			currentSong = GetTextFileContent(TextFiles.SongSpotify)

		# Continue if it is a new song
		if currentSong != SongInfo.Title:

			# Set (copy) previous song
			PreviousSong = Info.CopyInfo(SongInfo)

			# Set the new song and get requester
			# If Spotify mode, set requester equal to channel
			SongInfo.Title = currentSong
			if ScriptSettings.FileMode == "AnkhBot":
				SongInfo.Requester = GetTextFileContent(TextFiles.SongRequester)
			else:
				SongInfo.Requester = Parent.GetChannelName()

			# Requester is equal to the channel name the bot is connected to
			if Parent.GetChannelName() == SongInfo.Requester:

				# Post message in Twitch Chat and set boolean is playlist (true)
				Parent.SendTwitchMessage(ScriptSettings.MessageCasterRequester.format(SongInfo.Title, SongInfo.Requester))
				SongInfo.IsPlaylist = True

			# Requester is a viewer
			else:

				# Post message in Twitch Chat and set boolean is request (false)
				Parent.SendTwitchMessage(ScriptSettings.MessageViewerRequester.format(SongInfo.Title, SongInfo.Requester))
				SongInfo.IsPlaylist = False

			# Post new song data on websocket
			Parent.BroadcastWsEvent("EVENT_NOW_PLAYING", json.dumps(SongInfo.__dict__, encoding='utf-8'))

	# End of Tick
	return

#---------------------------------------
# Parse parameters
#---------------------------------------
def Parse(parseString, user, target, message):

	# $previoussong - previous played song
	if "$prevsong" in parseString:

		# Replace parameter with resplacement string
		if PreviousSong:
			return parseString.replace("$prevsong", PreviousSong.Title)
		else:
			return parseString.replace("$prevsong", "none")

	# $previousrequestedby - requester of previous song
	if "$prevrequestedby" in parseString:

		# Replace parameter with resplacement string
		if PreviousSong:
			return parseString.replace("$prevrequestedby", PreviousSong.Requester)
		else:
			return parseString.replace("$prevrequestedby", "nobody")

	# Return unaltered parseString
	return parseString
