#!/usr/bin/env python
import time, os, pexpect, setproctitle
import config

setproctitle.setproctitle('dzen_python')

if config.is_desktop():
  import temp, fan, meminfo, mailnotify, imnotify, weathernotify, dropbox
elif config.is_laptop():
  import temp, fan, meminfo, mailnotify, imnotify, weathernotify, dropbox
  import batterynotify

infocolor = config.infocolor
bgcolor = config.bgcolor
alert_fgcolor = config.alert_fgcolor
alert_bgcolor = config.alert_bgcolor
width = config.width
config_date_offset = config.date_offset
font_size = config.font_size
interface = config.interface

t=0
intWeather = 60
intMail = 60
dateTimeString = None

dzen_config = 'dzen2 -fg ' + infocolor + ' -bg ' + bgcolor + ' -h 19 ' + \
    '-ta c -x ' + str(config.x_pos) + ' -w ' + str(width) + \
    ' -fn \"-*-terminus-medium-*-*-*-' + str(font_size) + '-*-*-*-*-*-*-*\"'
dzen = pexpect.spawn(dzen_config)

rxfile = '/sys/class/net/' + interface + '/statistics/rx_bytes'
txfile = '/sys/class/net/' + interface + '/statistics/tx_bytes'
rxopen = open(rxfile, 'r')
txopen = open(txfile, 'r')
rxbytes = int(rxopen.readline())
txbytes = int(txopen.readline())
rxopen.close()
txopen.close()

while 1:

  if t%5 == 0:
    tempVal = temp.getTemp()
    tempOut = "^i(/home/chad/.dzen/icons/cpu.xbm)" + tempVal + " "

  if t%5 == 0:
    fanString = fan.getFan()
    fanOut = " ^i(/home/chad/.dzen/icons/fan.xbm)" + fanString + " "

  if t % 30 == 0:
    memUsage = meminfo.memUsage()
    memOut = " ^i(/home/chad/.dzen/icons/mem.xbm)" + str(int(memUsage)) + "% "

  try:
    rxopen = open(rxfile, 'r')
    txopen = open(txfile, 'r')
    rxbytesn = int(rxopen.readline())
    txbytesn = int(txopen.readline())
  except:
    pass
  rxr=int((rxbytesn-rxbytes)/1024/(1+.15))
  txr=int((txbytesn-txbytes)/1024/(1+.15))
  if len(os.listdir(config.net_prof_dir)) != 0:
    netOut = " ^bg()^i(/home/chad/.dzen/icons/down.xbm)" + str(rxr) + \
      "^i(/home/chad/.dzen/icons/up.xbm)" + str(txr) + "^bg() "
  else:
    netOut = "^fg(" + alert_fgcolor + ")^bg(" + alert_bgcolor + \
      ") ^i(/home/chad/.dzen/icons/down.xbm)! " + \
      "^i(/home/chad/.dzen/icons/up.xbm)! ^fg()^bg()"
  rxbytes=rxbytesn
  txbytes=txbytesn
  rxopen.close()
  txopen.close()

  if t % intMail == 0:
    newMailTup = mailnotify.newMail()
    newMail = newMailTup[0]
    intMail = newMailTup[1]
    mailOut = " ^i(/home/chad/.dzen/icons/mail.xbm)" + str(newMail) + " "

#  if t % 2 == 0:
#    getIM = imnotify.getIM()
#    imOut = getIM

  if t % intWeather == 0:
    weatherInfoTup = weathernotify.getWeatherNoaa()
    weatherInfo = weatherInfoTup[0]
    intWeather = weatherInfoTup[1]
    weatherOut = " ^i(/home/chad/.dzen/icons/temp.xbm)" + weatherInfo + " "

  dropboxStatus = dropbox.dropbox_status()
  dropboxOut = " ^i(/home/chad/.dzen/icons/dropbox.xbm)" + dropboxStatus + " "

  if config.is_laptop():
    if (t % 300) == 0:
      battOut = batterynotify.getBatt()

#  if t % 60 == 0:
#    mpdInfo = mpdinfo.mpdInfo()
#    mpdOut = "^i(/home/chad/inc/dzen_bak/icons/mpd.xbm)" + mpdInfo

  if t % 5 == 0:
    if dateTimeString is None or dateTimeString == '%B%e,%l:%M':
      dateTimeString = '%B%e,%l.%M'
    else:
      dateTimeString = '%B%e,%l:%M'
    dateTime = time.strftime(dateTimeString)
    dateTimeLen = len(dateTime)
    dateOffset = -1 * (dateTimeLen * 8 + config_date_offset)
    dateOut = "^p(_RIGHT)^p(" + str(dateOffset) + ")" + dateTime

  sep = "|"
  if config.is_desktop():
    outString = tempOut + sep + fanOut + sep + memOut + sep + netOut + sep \
      + mailOut + sep + weatherOut + sep + dropboxOut + sep + dateOut
  elif config.is_laptop():
    outString = tempOut + sep + fanOut + sep + memOut + sep + netOut + sep \
      + mailOut + sep + weatherOut + sep + dropboxOut + sep + battOut \
      + dateOut
  dzen.sendline(outString)

  time.sleep(1)
  if t == 3600:
    t=0
  t+=1

dzen.close()
