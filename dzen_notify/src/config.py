import os

def is_desktop():
  return os.uname()[1] == "chaddesk"

def is_laptop():
  return os.uname()[1] == "chadlaptop"

if os.uname()[1] == "chaddesk":
  infocolor="#dddddd"
  bgcolor="#444444"
  alert_bgcolor="#90001F"
  alert_fgcolor="#FFFFFF"
  interface="eth0"
  width=1920
  font_size=20
  x_pos=0
  date_offset=100
  net_prof_dir = "/run/network/profiles";

elif os.uname()[1] == "chadlaptop":
  infocolor="#444444"
  bgcolor="#e0e0e0"
  alert_bgcolor="#90001F"
  alert_fgcolor="#FFFFFF"
  interface="wlan0"
  width=1280
  font_size=14
  x_pos=0
  date_offset=20
  net_prof_dir = "/run/network/profiles";
