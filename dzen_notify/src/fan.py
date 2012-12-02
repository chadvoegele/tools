#!/usr/bin/env python
import string, re, os
import config
alert_fgcolor = config.alert_fgcolor
alert_bgcolor = config.alert_bgcolor

def getFan():
  if os.uname()[1] == "chaddesk":
    itFanFile1 = '/sys/devices/platform/it87.656/fan1_input'
    itFanRead1 = open(itFanFile1, 'r')
    itFan1 = int(itFanRead1.readline())
    itFanRead1.close()

    itFanFile2 = '/sys/devices/platform/it87.656/fan2_input'
    itFanRead2 = open(itFanFile2, 'r')
    itFan2 = int(itFanRead2.readline())
    itFanRead2.close()

    out = str(itFan1) + " " + str(itFan2)

    return out

  elif os.uname()[1] == "chadlaptop":
    fan_speed_file = '/proc/acpi/ibm/fan'
    fan_speed_read = open(fan_speed_file, 'r')
    fan_speed = fan_speed_read.readline()
    fan_speed = fan_speed_read.readline()
    outfan = int(fan_speed[8:])
    fan_speed_read.close()

    uh_file = '/sys/block/sda/device/unload_heads'
    uh_read = open(uh_file, 'r')
    uh_val = int(uh_read.readline())
    if uh_val == 0:
      uh_str = str(uh_val)
    else:
      uh_str = "^fg(" + alert_fgcolor + ")^bg(" + alert_bgcolor + ") " +\
        "X" + " ^fg()^bg()" 
    uh_read.close()

    out = str(outfan) + " " + str(uh_str)

    return out

  else:
    out = "None"
