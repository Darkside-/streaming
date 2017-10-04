#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr, sys, json, os, codecs
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "MakeItRain"
Website = "https://www.AnkhBot.com"
Creator = "Castorr91"
Version = "1.1.0.3"
Description = "Make it rain! Points for everyone!"

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
#   Version Information
#---------------------------------------

# Version:
# > 1.1.0.3 <
    # bugfix, with cost setting to 0 you can now use the command if you have 0 points

# > 1.1.0.2 <
    # fixed default responses
    # added restore default settings

# > 1.1.0.1 <
    # fixed cost setting
    # removed enable/disable button in config

# > 1.1.0.0 <
    # Cleaned up code
    # fixed missing permission check
    # added "only live mode"

# > 1.0.1.0 < 
    # Cleaned up code 
    # fixed missing info in textboxes 

# > 1.0.0.0 < 
    # Official Release

class Settings:
    # Tries to load settings from file if given 
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig') 
        else: #set variables if no settings file
            self.OnlyLive = False
            self.Command = "!makeitrain"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Cost = 300
            self.UseCD = True
            self.Cooldown = 0
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.BaseResponse = "{0} just spent {1} {3} to make it rain! Everyone in chat got awarded {2} {3}!"
            self.NotEnoughResponse = "{0} you don't have enough points to make it rain"
            self.Payout = 30
            
    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    # Globals
    global MySettings

    # Load in saved settings
    MySettings = Settings(settingsFile)

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return

def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == MySettings.Command:
       
        #check if command is in "live only mode"
        if MySettings.OnlyLive:

            #set run permission
            startCheck = data.IsLive() and Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo)

        else: #set run permission
            startCheck = True

        #check if user has permission
        if startCheck and  Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo):

            #check if command is on cooldown
            if Parent.IsOnCooldown(ScriptName,MySettings.Command) or Parent.IsOnUserCooldown(ScriptName,MySettings.Command,data.User):
               
                #check if cooldown message is enabled
                if MySettings.UseCD: 

                    #set variables for cooldown
                    cooldownDuration = Parent.GetCooldownDuration(ScriptName,MySettings.Command)
                    usercooldownDuration = Parent.GetUserCooldownDuration(ScriptName,MySettings.Command,data.User)
                    
                    #check for the longest CD!
                    if cooldownDuration > usercooldownDuration:

                        #set cd remaining
                        m_CooldownRemaining = cooldownDuration

                        #send cooldown message
                        Parent.SendTwitchMessage(MySettings.OnCooldown.format(data.User,m_CooldownRemaining))


                    else: #set cd remaining
                        m_CooldownRemaining = Parent.GetUserCooldownDuration(ScriptName,MySettings.Command,data.User)
                        
                        #send usercooldown message
                        Parent.SendTwitchMessage(MySettings.OnUserCooldown.format(data.User,m_CooldownRemaining))
            
            else: #check if user got enough points
                if Parent.GetPoints(data.User) >= MySettings.Cost:

                    #remove points from the user triggering the command
                    Parent.RemovePoints(data.User, MySettings.Cost)

                    #create a dict and fill with viewers
                    dict = {};
                    for viewer in Parent.GetViewerList():
                        dict[viewer] = MySettings.Payout
    
                    #add points to all viewers in dict
                    Parent.AddPointsAll(dict)
    
                    #send successful message
                    Parent.SendTwitchMessage(MySettings.BaseResponse.format(data.User, MySettings.Cost, MySettings.Payout, Parent.GetCurrencyName()))
    
                    # add cooldowns
                    Parent.AddUserCooldown(ScriptName, MySettings.Command,data.User, MySettings.UserCooldown)
                    Parent.AddCooldown(ScriptName, MySettings.Command, MySettings.Cooldown)
                
                else:
                    #send not enough currency response
                    Parent.SendTwitchMessage(MySettings.NotEnoughResponse.format(data.User, Parent.GetCurrencyName(), MySettings.Command, MySettings.Cost))
    return

def Tick():
    return

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return
def SetDefaults():
    """Set default settings function"""
    # Globals
    global MySettings

    # Set defaults by not supplying a settings file
    MySettings = Settings()

    # Save defaults back to file
    MySettings.Save(settingsFile)

    # End of SetDefaults
    return
