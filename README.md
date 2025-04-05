This python script is used to update cpplinter.lua after my edits which has lua functions pointing to the specific luascript.cpp function it calls

To use, place your cpplinter with the required lines before every function you want to point to somewhere in luascript.cpp; example
```lua
---*int LuaScriptInterface::luaGameGetPlayers(lua_State* L) -- Function getPlayers() calls
---@source ../src/luascript.cpp:4567 -- Line that the function is on
---@field getPlayers fun(): table<number, Player> 
```

Once a copy of luascript.cpp and cpplinter.lua file is in the same folder, run update_cpplinter.py.

Enjoy an updated cpplinter.lua
