#---------------------------------------
#   Import Libraries
#---------------------------------------
import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

print sys.path
#---------------------------------------
#   [Required] Script Information
#---------------------------------------
ScriptName = "Parameter Demo"
Website = "https://www.AnkhBot.com"
Description = "Right Click -> Insert API Key"
Creator = "AnkhHeart"
Version = "1.0.0.0"

#---------------------------------------
#   [Required] Initialize Data / Load Only
#---------------------------------------
def Init():
	return
	
def Parse(parseString,user,target,message):
	if "$myparameter" in parseString:
		return parseString.replace("$myparameter","I am a cat!")
	return parseString