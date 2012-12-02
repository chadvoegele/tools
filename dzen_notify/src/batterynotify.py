#!/usr/bin/env python
import re
import config
alert_fgcolor = config.alert_fgcolor
alert_bgcolor = config.alert_bgcolor

def getBattVal():
  # battLeftFile = '/proc/acpi/battery/BAT0/state'
  # battChargeFile = '/proc/acpi/battery/BAT0/info'
  battLeftFile = '/sys/class/power_supply/BAT0/energy_now'
  battChargeFile = '/sys/class/power_supply/BAT0/energy_full'
  battLeftOpen = open(battLeftFile, 'r')
  battChargeOpen = open(battChargeFile, 'r')
  for line in  battLeftOpen.readlines():
    # if re.search("remaining", line):
    battLeft = line
  for line in battChargeOpen.readlines():
    # if re.search("full", line):
    battCharge = line
  # battLeft = battLeft.split(" ")[7]
  # battCharge = battCharge.split(" ")[8]
  battLeftOpen.close()
  battChargeOpen.close()
  return int(battLeft) * 100 // int(battCharge)

def getBatt():
  battVal = getBattVal()
  if battVal <= 5:
    return "^fg(" + alert_fgcolor + ")^bg(" + alert_bgcolor + \
      ") ^i(/home/chad/.dzen/icons/power-bat.xbm)" + str(battVal) +\
      "% ^fg()^bg()"
  elif battVal <= 2:
    os.system('pm-suspend --quirk-s3-mode')
    return
  else:
    return " ^i(/home/chad/.dzen/icons/power-bat.xbm)" + str(battVal) + "% "
