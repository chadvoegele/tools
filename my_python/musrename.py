#!/usr/bin/env python2
import sys,os,tagpy,re,shutil

for file in sys.argv[1:]:
  file = os.path.abspath(file)
  if os.path.isfile(file):
    #base dir can also be found by os.path.dirname(file)
    baseDirSplit = file.split('/')[:-1]
    baseDir = ""
    for i in range(1,len(baseDirSplit)):
      baseDir = baseDir + "/" + baseDirSplit[i]
    cwd = os.getcwd()

    ext = file[-3:]

    fileRef = tagpy.FileRef(file)
    fileRefTag = fileRef.tag()
    artist = fileRefTag.artist
    title = fileRefTag.title
    track = fileRefTag.track

    ext = ext.lower()
    artist = artist.lower()
    title = title.lower()

    artist = re.sub(" ", "_", artist)
    title = re.sub(" ", "_", title)
    #artist = re.sub("\\", "_", artist)
    #title = re.sub("\\", "_", title)

    if track < 10:
      track = "0" + repr(track)
    else:
      track = repr(track)

    newFileName = track + "-" + artist + "-" + title + "." + ext
    #newFileName = artist + "-" + title + "." + ext


    relFile = file.split('/')[-1:][0]
    if newFileName == relFile:
      print(file + " is already named correctly")
    else:
      if cwd == baseDir:
        shutil.move(file, newFileName)
      else:
        newFileName = baseDir + "/" + newFileName
        shutil.move(file, newFileName)
  else:
    print(file + " is not a file")
