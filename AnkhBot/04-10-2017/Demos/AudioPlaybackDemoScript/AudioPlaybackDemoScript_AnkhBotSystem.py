#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Audio Playback Demo

This example AnkhBot demo script demonstrates how to playback audio with the build
in Parent.PlaySound() function. This function immediately returns a boolean on the
status of playback. True if it could be played (not that is has finished) or False
if another sound file is already playing and you have 'to try again' later.

The function does not queue up sounds it needs to play so we need to check it within
the script ourself if the file started played or not. But using while loops, for
example, will lock everything including the user interface of AnkhBot.

Therefore this demo uses a playback queue where anywhere in the script you can
'enqueue' a sound file. The created function EnqueueAudioFile(file) accepts a
filename and extention, and within it combines the given file with the set audio
directory path to create a full and valid path to the audio file.

The Tick() function will regually be called so we can use this function perfectly
as the audio playback dequeuer. If the queue contains items it will try to play the
first added audio file. If Parent.PlaySound() returns true it started to play and
we can remove the file from the queue. If its false, it tries again next Tick().

Of course you can preset all audio files, as full path in different variables, your
script needs and remove the fullpath creation in the EnqueueAudioFile(file) function
to hardcode / fix the audio files. However in this demo we go for a more dynamic
approach so for example an end-user can place their own audio file within the audio
directory and only have to give the name of the audio file in the user interface.

	1.0.0
		Initial public release

"""

#---------------------------------------
# Import Libraries
#---------------------------------------
import clr
clr.AddReference("IronPython.Modules.dll")

import os
from collections import deque

#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = "Audio Playback Demo"
Website = "http://www.twitch.tv/ocgineer"
Description = "Demo to show audio playback using AnkhBot PlaySound function."
Creator = "Ocgineer"
Version = "1.0.0.0"

#---------------------------------------
# Variables
#---------------------------------------
# Set location of the audio directory containing audio files
AudioFilesPath = os.path.join(os.path.dirname(__file__), "audio")
AudioPlaybackQueue = deque()

#---------------------------------------
# Functions
#---------------------------------------
def EnqueueAudioFile(audiofile):
	""" Adds an audio file from the audio folder to the play queue. """
	fullpath = os.path.join(AudioFilesPath, audiofile)
	AudioPlaybackQueue.append(fullpath)
	return

#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
	return

#---------------------------------------
# Execute data and process messages
#---------------------------------------
def Execute(data):
	return

#---------------------------------------
# Tick
#---------------------------------------
def Tick():

	# Audio file in the queue?
	if AudioPlaybackQueue:
		# Try to playback left most item in queue
		if Parent.PlaySound(AudioPlaybackQueue[0], 0.5):
			# Pop from queue if has been played
			AudioPlaybackQueue.popleft()

	return

#---------------------------------------
# Custom Button: Play Sound
#---------------------------------------
def PlayAudio1():
	EnqueueAudioFile("mgs_alert.wav")
	return

def PlayAudio2():
	EnqueueAudioFile("dva_countdown.mp3")
	return
