#!/usr/bin/env python
import config
alert_fgcolor = config.alert_fgcolor
alert_bgcolor = config.alert_bgcolor

def getIM():
  imfile='/home/chad/tmp/unreadim'
  file = open(imfile, 'r')
  msgs = int(file.readline())
  if msgs == 1:
    return "^fg(" + alert_fgcolor + ")^bg(" + alert_bgcolor + ") " + \
        "^i(/home/chad/.dzen/icons/chat.xbm)X ^fg()^bg()"
  else:
    return "^bg() ^i(/home/chad/.dzen/icons/chat.xbm)0 ^bg()"
  file.close()
