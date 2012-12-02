#!/usr/bin/env python
import os,sys,time,shutil,tarfile,re,subprocess

def check_root():
  if not os.getuid() == 0: 
    print("not root, quitting")
    exit(1)

def show_help():
  print """backup.py Usage
    -c, --config              : backup configs (~/.backup/config)
    -f, --files               : backup files (~/.backup/files)
    -d, --dest-dir [dest dir] : backup to dest dir
    -h, --help                : show this help menu
    neither -c,-f             : backup config, files to /mnt/ext_hd/bak"""
  exit(1)

def print_args(args):
  for i in args:
    print i

def check_path(path):
  r = re.compile(".*\*.*")
  if r.match(path):
    return
  else:
    if not os.path.exists(path):
      raise RuntimeError(path + " does not exist")

def config_backup(args):
  print("config backup code")
  verbose = args[3]
  backupFileList = os.environ.get("HOME") + "/.backup/config"
  check_path(backupFileList)
  backupFile = "config-" + os.uname()[1] + "-" + time.strftime('%Y%m%d')
  folder = os.environ.get("HOME") + "/bak_tmp"
  backupDir = args[2]
  if backupDir == '/mnt/ext_hd/bak':
    backupDir = '/mnt/ext_hd/bak/configs'
  check_path(backupDir)
  
  if os.path.exists(folder + "/" + backupFile):
    print("backup folder in /tmp exists! quitting...")
    sys.exit(1)
  
  os.mkdir(folder)
  os.mkdir(folder + "/" + backupFile)
  backupFileOpen = open(backupFileList, "r")
  backupFileRead = backupFileOpen.readlines()
  
  p = re.compile('\\n')
  for i in range(0, len(backupFileRead)):
    backupFileRead[i] = p.sub('', backupFileRead[i])
    try:
      check_path(backupFileRead[i])
    except Exception, err:
      sys.stderr.write('ERROR: %s\n' %str(err))
      print 'removing bak_tmp, quitting'
      shutil.rmtree(folder + "/" + backupFile)
      shutil.rmtree(folder)
      sys.exit(1)
    if verbose:
      print 'copying' + backupFileRead[i] + " to " + folder + "/" + backupFile
    subprocess.call('cp -p --parents -r ' + backupFileRead[i] + " " + 
      folder + "/" + backupFile, shell=True)
  
  targz = tarfile.open(backupDir + "/" + backupFile + ".tar.gz", "w:gz")
  targz.add(folder + "/" + backupFile, backupFile)
  targz.close()
  
  shutil.rmtree(folder + "/" + backupFile)
  shutil.rmtree(folder)

def file_backup(args):
  print("file backup code")
  verbose = args[3]
  backup_file_list = os.environ.get("HOME") + "/.backup/files"
  try:
    check_path(backup_file_list)
  except Exception, err:
    sys.stderr.write('ERROR: %s\n' %str(err))
    print "quitting"
    exit(1)
  backup_dir_root = args[2]
  check_path(backup_dir_root)
  hostname = os.uname()[1]
  backup_dir = backup_dir_root + "/" + hostname
  if not os.path.exists(backup_dir):
    os.mkdir(backup_dir)
  
  backupFileOpen = open(backup_file_list, "r")
  backupFileRead = backupFileOpen.readlines()
  p = re.compile('\\n')
  files = []
  for i in range(0, len(backupFileRead)):
    backupFileRead[i] = p.sub('', backupFileRead[i])
    check_path(backupFileRead[i])
    files.append(backupFileRead[i])
  files_string = ""
  for i in files:
    files_string = files_string + " " + i
  cmd = "rsync -aRrP --inplace --delete " + files_string + " " + backup_dir
  if verbose:
    print files
    print files_string
    print(cmd)
  subprocess.call(cmd, shell=True)


check_root()
argi = 1
args = [False, False, '/mnt/ext_hd/bak', False]
  #args[0] -- config backup
  #args[1] -- files backup
  #args[2] -- dest-dir
  #args[3] -- verbose
while argi <= len(sys.argv[1:]):
  current_arg = sys.argv[argi]
  if current_arg == "-c" or current_arg == "--config":
    args[0] = True
  if current_arg == "-f" or current_arg == "--files":
    args[1] = True
  if current_arg == "-d" or current_arg == "--dest-dir":
    args[2] = sys.argv[argi+1]
    argi = argi+1
  if current_arg == "-h" or current_arg == "--help":
    show_help()
  if current_arg == "-v" or current_arg == "--verbose":
    args[3] = True
  argi = argi+1
  
if args[0] == False and args[1] == False:
  args[0] = True; args[1] = True

if args[0] == True:
  if args[3] == True:
    print("backing up configs")
  config_backup(args)

if args[1] == True:
  if args[3] == True:
    print("backing up files")
  file_backup(args)

