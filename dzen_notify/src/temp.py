#!/usr/bin/env python
import string, re
import config
alert_fgcolor = config.alert_fgcolor
alert_bgcolor = config.alert_bgcolor

def getTemp():
  if config.is_desktop():
    cpuTempFile0 = '/sys/devices/platform/coretemp.0/temp2_input'
    cpuTempRead0 = open(cpuTempFile0, 'r')
    cpuTemp0 = int(int(cpuTempRead0.readline())/1000)
    cpuTempRead0.close()

    cpuTempFile1 = '/sys/devices/platform/coretemp.0/temp3_input'
    cpuTempRead1 = open(cpuTempFile1, 'r')
    cpuTemp1 = int(int(cpuTempRead1.readline())/1000)
    cpuTempRead1.close()

    cpuTempFile2 = '/sys/devices/platform/coretemp.0/temp4_input'
    cpuTempRead2 = open(cpuTempFile2, 'r')
    cpuTemp2 = int(int(cpuTempRead2.readline())/1000)
    cpuTempRead2.close()

    cpuTempFile3 = '/sys/devices/platform/coretemp.0/temp5_input'
    cpuTempRead3 = open(cpuTempFile3, 'r')
    cpuTemp3 = int(int(cpuTempRead3.readline())/1000)
    cpuTempRead3.close()

    itTempFile1 = '/sys/devices/platform/it87.656/temp1_input'
    itTempRead1 = open(itTempFile1, 'r')
    itTemp1 = int(int(itTempRead1.readline())/1000)
    itTempRead1.close()

    itTempFile2 = '/sys/devices/platform/it87.656/temp2_input'
    itTempRead2 = open(itTempFile2, 'r')
    itTemp2 = int(int(itTempRead2.readline())/1000)
    itTempRead2.close()

    itTempFile3 = '/sys/devices/platform/it87.656/temp3_input'
    itTempRead3 = open(itTempFile3, 'r')
    itTemp3 = int(int(itTempRead3.readline())/1000)
    itTempRead3.close()

    outString = str(cpuTemp0) + " " + str(cpuTemp1) + " " + \
      str(cpuTemp2) + " " + str(cpuTemp3) + " " + str(itTemp1) + " " + \
      str(itTemp2) + " " + str(itTemp3)

    return outString
  
  elif config.is_laptop():
    import iwlagn
    cpuTempFile = '/proc/acpi/ibm/thermal'
    cpuTempRead = open(cpuTempFile, 'r')
    cpuTemp = cpuTempRead.readline()[14:]
    sp =  ' '
    outtemps = cpuTemp[:2] + sp + cpuTemp[3:5] + sp + cpuTemp[11:13] + sp \
          + cpuTemp[14:16] + sp + cpuTemp[22:24] + sp + cpuTemp[30:32] \
          + sp + cpuTemp[33:35]
    cpuTempRead.close()

    try:
      temp_val = str(iwlagn.read_val(iwlagn.find_temp()))
    except:
      temp_val = "!"
    if temp_val == "0" or temp_val == "!":
      temp_str = "^fg(" + alert_fgcolor + ")^bg(" + alert_bgcolor + ") " +\
        temp_val + " ^fg()^bg()"
    else:
      temp_str = "^bg()" + temp_val + "^bg()"

    out = str(outtemps) + sp + temp_str
    return out
