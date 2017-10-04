#################
Info
#################

Description: A Two player score keeper with customizable overlay scoreboard.
Created by: Ocgineer - www.twitch.tv/ocgineer
Version: 1.1.1.0

#################
Commands
#################

!score          - Print both players current score in chat
!score clear    - Clears data to default values and hide overlay
!score show     - Show scoreboard on the overlay
!score hide     - Hide scoreboard on the overlay
!score setname [p1 | p2] [name]		      - Set the name of player 1 or 2
!score [p1 | <name>] [<value> | + | -]	- Set the score of player 1, or shows the score of player 1 if no [value | + | -] is given
!score [p2 | <name>] [<value> | + | -]	- Set the score of player 2, or shows the score of player 2 if no [value | + | -] is given

*note <name> can contain spaces

################
Usage
################

In AnkhBot right-click on the script and select "Insert API Key",
this will automatically create a file API_Key.js that is required
by the javascript to connect to AnkhBot and receive info.

The HTML file is supposed to be used as overlay to show the scoreboard,
and is purely made out of CSS. You can write your own style using the
current HTML/JS/CSS file as example or base and use the WebSocket events
to control the overlay. 

If you are less tech-savy you can change colors at least through the
AnkhBot script UI where you can also cusomize/localize chat messages
that are being printed in chat when using commands.

Current overlay 'browser source' resolution recommendation is use the
same resolution as your base canvas. The scoreboard will be centered
to the top automatically and width is calulated and set by the longest name.

Every time the scoreboard is updated, be it with points or name, the
most recent values will be stored, and recalled upon restart/reload.

###############
Version History
###############

1.1.1: 
  * Code cleanup

1.1.0:
  * [script][html] Added override width option to disable auto width
        and to fix the width of the scoreboard regardless of longest name.

1.0.0:
  * Release version
  * [html] Auto-calculates and set width of the scoreboard by longest name
  * [script] Accepts names with whitespaces now through commands

0.3.0:
  * [script][html] Combined Scoreboard data (names/points) with settings file
  * [script] Added functionality to set and update names/scores from UI

0.2.0:
  * [script][html] Incorporated new script custom UI for settings;
    - [script][html] Overlay colors can be set now
    - [script] Chat reply messages can be customized/localized
    - [script] Show and Hide button to control visibility on the overlay
  * [script] Removed `!score toggle` chat command

0.1.1:
  * [script] Changed Scriptname due to change in AnkhBot scripting

0.1.0:
  * Initial version


