#!/usr/bin/env python
import string
import re

def memUsage():
  memFile = '/proc/meminfo'
  memRead = open(memFile, 'r')
  for line in memRead.readlines():
    if re.search("MemTotal:", line):
      memTotal = int(line[15:22])
    if re.search("Active:", line):
      memUsed = int(line[14:22])
  memRead.close()
  return memUsed*100/memTotal
