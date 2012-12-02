#!/usr/bin/env python2
import sys, os, re, tagpy, shutil

music_dir = "/mnt/z/tunes"

for dir in sys.argv[1:]:
  dir = os.path.abspath(dir)
  listDir = os.listdir(dir)
  mp3Exp = re.compile('mp3*')
  mp3file = filter(mp3Exp.search, listDir)[0]

  fileRef = tagpy.FileRef(dir + "/" + mp3file)
  fileRefTag = fileRef.tag()
  artist = fileRefTag.artist
  album = fileRefTag.album

  miscExp = re.compile('.*m3u$|.*nfo$|.*txt$|.*sfv$|.*mpg$|.*url$|.*avi$|.*mht$|.*log$|.*cue$|.*doc$|.*rar$|.*db$|.*lrc$|.*zip$|.*html$|.*7z$')
  miscFiles = filter(miscExp.search, listDir)

  for i in range(0, len(miscFiles)):
    print "removing " + dir + "/" + miscFiles[i]
    os.remove(dir + "/" + miscFiles[i])

  if os.path.exists(music_dir + "/" + artist + "/" + album):
    print "album folder exists already... quitting"
    sys.exit(1)

  if os.path.exists(music_dir + "/" + artist):
    print "artist folder exists"
  else:
    print "making dir " + music_dir + "/" + artist
    os.mkdir(music_dir + "/" + artist)

  print "moving " + dir + " to " + music_dir + "/" + artist + "/" + album
  shutil.move(dir, music_dir + "/" + artist + "/" + album)
