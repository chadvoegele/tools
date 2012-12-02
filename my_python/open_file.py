#!/usr/bin/env python
import argparse, subprocess, re, os, magic

def my_arg_parse():
  parser = argparse.ArgumentParser(description='Open files based on mimetype')
  parser.add_argument('file', nargs='+', help='files to open')
  return parser.parse_args()

mime_app = {}
mime_app['application/msword'] = 'abiword'
mime_app['application/pdf'] = 'evince'
mime_app['application/rtf'] = 'abiword'
mime_app['application/vnd.ms-excel'] = 'gnumeric'
mime_app['application/x-perl'] = 'vim -p'
mime_app['application/x-shellscript'] = 'vim -p'
mime_app['application/x-tar'] = 'tar -xf'
mime_app['application/x-xoj'] = 'xournal'
mime_app['application/xml'] = 'vim -p'
mime_app['image/jpeg'] = 'gqview'
mime_app['inode/directory'] = 'cd'
mime_app['text/plain'] = 'vim -p'
mime_app['text/x-c'] = 'vim -p'
mime_app['text/x-c++src'] = 'vim -p'
mime_app['text/x-csrc'] = 'vim -p'
mime_app['text/x-fortran'] = 'vim -p'
mime_app['text/x-java'] = 'vim -p'
mime_app['text/x-log'] = 'vim -p'
mime_app['text/x-matlab'] = 'vim -p'
mime_app['text/x-pascal'] = 'vim -p'
mime_app['text/x-python'] = 'vim -p'
mime_app['text/x-tex'] = 'vim -p'
mime_app['video/x-ms-wmv'] = 'mplayer'
mime_app['video/x-msvideo'] = 'mplayer'

args = my_arg_parse()
mime_files = {}
for afile in args.file:
  try:
    if os.path.islink(afile):
      mime_type = magic.from_file(os.path.realpath(afile), mime=True).decode()
    else:
      mime_type = magic.from_file(afile, mime=True).decode()
  except IOError:
    # print(afile + " does not exist. Skipping")
    # continue
    print(afile + " does not exist. Creating text file.")
    mime_type = 'text/plain'
  if mime_type == None:
    print('no mime type for file: ' + afile)
    exit(1)

  # try to make faster
  # if not mime_type in mime_files:
    # mime_files[mime_type] = []
  try:
    mime_files[mime_type] = []
  except KeyError:
    mime_files[mime_type] = []

  # fix for filenames with spaces
  afile = re.sub(" ", "\ ", afile)
  afile = re.sub("\(", "\\(", afile)
  afile = re.sub("\)", "\\)", afile)
  mime_files[mime_type].append(afile)

for mime in mime_files.keys():
  # print(mime_app[mime] + ' ' + ' '.join(mime_files[mime]))
  if not mime in mime_app:
    print('no app defined for ' + mime)
    exit(1)
  cmd = mime_app[mime] + ' ' + " ".join(mime_files[mime])
  # print(cmd)
  subprocess.call(cmd, shell=True)
