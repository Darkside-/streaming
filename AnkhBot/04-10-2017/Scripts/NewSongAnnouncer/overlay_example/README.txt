# New in 1.2;

  Spotify Mode;
    When using only Spotify to play songs, without the use of AnkhBot.
    For this to work one needs to link Spotfy with AnkhBot, found in connections.

  AnkhBot Mode;
    When playing songs through AnkhBot with playlist and/or song requests.

# New in 1.1;

  Seperate chat message output for when the 'caster' is the requester of the song.
  This will prevent many tags/pings of the chat because of name mentioning.

# Websocket for overlay

  This AnkhBot Python scripts pushes a websocket event on a new detected song.

  Event:
    EVENT_NOW_PLAYING

  Event format:
    {
      "event": "EVENT_NOW_PLAYING",
      "data": {
        "Title": "The title of the new song",
        "Requester": "The requester of the song"
        "IsPlaylist: true if caster is requester or spotify mode, false if requested by viewer
      }
    }

# Example overlay

  An function example overlay is shipped with this script. If you would like
  to change/edit or create your own, make sure to make it in a seperate folder
  so when updating this script it wont be overwriten by the default example.

  This example overlay now also hides the requester of the song if the requester
  is the caster or if it is in Spotify mode. If you would like to still show the
  casters name as the requester, make a copy of the example folder, and rename.
  Then open the script file in an editor and remove the following lines of code;

    if (data.IsPlaylist)
      // Hide requester if caster
      $("#requesterbox").hide();
    else
      // Show requester if viewer
      $("#requesterbox").show();

  found on lines 62 to 67 in script.js