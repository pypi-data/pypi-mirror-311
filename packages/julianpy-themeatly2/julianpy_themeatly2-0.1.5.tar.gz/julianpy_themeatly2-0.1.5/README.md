# JulianPy
JulianPy is a API made by Themeatly2 and Harsizcool to interface with Julian's Editor games in a very basic, but efficient way.

## Todo:
- Add basic controls (like keyboard inputs, chat, etc.) -  Done
- Add tools (like hasWifi()) - Done
- Add websocket communication
- Add other things (like Community API, Marketplace API, etc.)

## Example
```
import julianpy
import time

# JulianPy requires a Julian's Editor share link.
# You can get one by clicking the Share icon and then "Copy Link".
id = "https://s.julianseditor.com/3An5lL".replace("https://s.julianseditor.com/", "")
julian = Astronaut(id)
# Move right for 1 second
julian.holdKey("d", 1)
time.sleep(1)
# Send a chat message
julian.sendMessage("Hello from Python!")
time.sleep(3)
# julian.die is required to properly quit the bot, or the bot will stay in the game
# which causes confusion with the server (and even conflicts with other bots) if you try to reconnect.
julian.die()

```