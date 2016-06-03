#!/usr/bin/osascript
if application "iTerm" is running then
  tell application "System Events" to tell process "iTerm2"
    tell menu bar item "Profiles" of menu bar 1
      click
      click menu item "Tmux" of menu 1
    end tell
  end tell
else
  tell application "iTerm" to activate
end if
