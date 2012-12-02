#!/usr/bin/env python
import os, sys, re

home = os.environ.get('HOME')
site_file = home + '/.config/fflinks/sites'
site_file_open = open(site_file, 'r')

keylist=[]
linklist=[]
p = re.compile('\\n')
for line in site_file_open:
  if len(line.split(' ')) == 2:
    key=line.split(' ')[0]
    address=line.split(' ')[1]
    address = p.sub('',address)
    keylist.append(key)
    linklist.append(address)

site_file_open.close()

search_file = home + '/.config/fflinks/searches'
search_file_open = open(search_file, 'r')

s_keylist=[]
s_linklist=[]
for line in search_file_open:
  if len(line.split(' ')) == 2:
    s_key=line.split(' ')[0]
    s_address=line.split(' ')[1]
    s_address = p.sub('', s_address)
    s_keylist.append(s_key)
    s_linklist.append(s_address)

search_file_open.close()

s = re.compile('%s')

if os.path.basename(sys.argv[0]) == 'f':
  browser = "firefox"
elif os.path.basename(sys.argv[0]) == 'g':
  browser = "chromium"

if len(sys.argv) == 1:
  sys_cmd = browser
elif len(sys.argv[1:]) == 1:
  open_site = sys.argv[1]
  open_address = ''
  for i in range(0, len(keylist)):
    if keylist[i] == open_site:
      open_address = linklist[i]
  if len(open_address) != 0:
    sys_cmd = browser + " " + open_address
  else:
    # sys_cmd = "firefox"
    exit(1)
elif len(sys.argv[1:]) >= 2:
  open_search = sys.argv[1]
  search_string = ' '.join(sys.argv[2:])
  search_link = ''
  for i in range(0, len(s_keylist)):
    if s_keylist[i] == open_search:
      search_link = s_linklist[i]
  if len(search_link) != 0:
    search_link = s.sub(search_string, search_link)
    sys_cmd = browser + " \"" + search_link + "\""
  else:
    exit(1)

print(sys_cmd)
os.system(sys_cmd)
