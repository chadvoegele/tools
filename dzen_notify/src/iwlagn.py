#!/usr/bin/env python
import os,fnmatch

def find_power():
  pattern = 'power_level'
  root = '/sys/devices'
  for path, dirs, files in os.walk(os.path.abspath(root)):
    for filename in fnmatch.filter(files, pattern):
      return os.path.join(path, filename)

def read_val(file):
  file_read = open(file, "r").readline()
#  return int(file_read[:-1][-1:])
  return file_read[:-1]

def find_temp():
  pattern = 'temperature'
  root = '/sys/devices/pci0000:00'
  for path, dirs, files in os.walk(os.path.abspath(root)):
    for filename in fnmatch.filter(files, pattern):
      return os.path.join(path, filename)
