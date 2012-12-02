#!/usr/bin/env python

import os, argparse, sys, re, math

def my_parse_args():
  parser = argparse.ArgumentParser(description='Split csv.')
  parser.add_argument('-v', dest="verbose", action="store_true", default=False,
      help='verbose')
  parser.add_argument('-s', dest="split_size", action="store", type=int,
      required=True, help='split file into sizes')
  parser.add_argument('orig_files', nargs='+', 
      help='original csv file')
  args = parser.parse_args()
  return args

def locate_split(first_id, last_id, args):
  split_size = args.split_size
  num_ids = last_id - first_id + 1
  num_files = math.ceil(num_ids/split_size)
  num_each=[]
  for i in range(0,num_files):
    num_each.append(num_ids//num_files)
  remainder = num_ids % num_files
  for i in range(0,remainder):
    num_each[i]=num_each[i]+1
  cur_id = first_id
  ids = [];
  for num in num_each:
    ids.append(cur_id)
    cur_id = cur_id + num - 1
    # if not num == 1:
    ids.append(cur_id)
    cur_id = cur_id + 1
  return ids

args = my_parse_args()
if args.verbose:
  print(args)

for cur_orig_file in args.orig_files:
  if not os.path.exists(cur_orig_file):
    sys.exit(cur_orig_file + " does not exist")

  # make output dir
  orig_file_dir = os.path.dirname(os.path.realpath(cur_orig_file))
  split_file_dir = orig_file_dir + '/out'
  if not os.path.exists(split_file_dir):
    os.mkdir(split_file_dir)

  cur_file = open(cur_orig_file,'r')
  cur_read = cur_file.readlines()
  cur_first_line = cur_read[0]
  last_line_num = len(cur_read)-1;
  while re.match("\s", cur_read[last_line_num]) and last_line_num > 0:
    last_line_num = last_line_num - 1
  cur_last_line = cur_read[last_line_num]

  first_id = int(cur_first_line.split(',')[0])
  last_id = int(cur_last_line.split(',')[0])

  id_split_locs = locate_split(first_id, last_id, args) 
  line_split_locs = [1];
  last_id = first_id
  i = 1; k = 1
  while i < len(cur_read):
    cur_line = cur_read[i]
    if not cur_line.isspace():
      cur_id = int(cur_line.split(',')[0])
      if not last_id == cur_id and k+1 < len(id_split_locs):
        if cur_id == id_split_locs[k+1] and last_id == id_split_locs[k]:
          line_split_locs.append(i-1+1)
          line_split_locs.append(i+1)
          k=k+2
    last_id = cur_id
    i=i+1
  line_split_locs.append(len(cur_read)-1)

  id_sep = '-idsep-'
  for i in range(0,len(line_split_locs)//2):
    i = 2*i;
    beg_line = line_split_locs[i]
    end_line = line_split_locs[i+1]
    file_name = str(id_split_locs[i]) + id_sep + str(id_split_locs[i+1]) +\
      '.csv'
    if os.path.exists(file_name):
      sys.exit(file_name + " already exists")
    file_open = open(file_name,'w')
    file_open.writelines(cur_read[beg_line-1:end_line])
    file_open.close()
