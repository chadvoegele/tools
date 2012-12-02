#!/usr/bin/env python
import mpd

def mpdInfo():
  client = mpd.MPDClient()
  try:
    client.connect('localhost', 6600)
    client.command_list_ok_begin()
    client.currentsong()
    client.status()
    results = client.command_list_end()
    client.disconnect()
    status = results[1]['state']
    artist = results[0]['artist']
    title = results[0]['title']
    if status == 'pause':
      return "Paused"
    else:
      if len(artist) > 20:
        artist = artist[0:18] + "..."
      if len(title) > 18:
        title = title[0:16] + "..."
      return title + " by " + artist
  except:
    return "No Tunes"
