#!/usr/bin/env python
import re
from subprocess import check_output

def dropbox_status():
    cli_output = check_output(["dropbox", "status"]).decode()
    return dropbox_status_parser(cli_output)

def dropbox_status_parser(cli_output):
    if cli_output == "Up to date\n":
        return "-"
    else:
        lines = cli_output.split("\n")
        for line in lines:
            result = re.match("Syncing \"(.*)\"", line)
            if not result == None:
                upfile = result.groups(0)[0]
                takelen = min(len(upfile), 7)
                upfile = result.groups(0)[0][0:takelen]
                return "Uploading " + upfile

            result = re.match("Syncing \((\d+) files remaining\)", line)
            if not result == None:
                num = result.groups(0)[0]
                return "Uploading " + num + " files"
        trimoutput = min(len(cli_output), 10)
        return "Error: " + cli_output[0:trimoutput]

def dropbox_test1():
    output = "Up to date\n"
    print(dropbox_status(output))

def dropbox_test2():
    output = "Syncing \"test.txt\"\nIndexing \"test.txt\"..."
    print(dropbox_status(output))

def dropbox_test3():
    output = "Syncing (2 files remaining)\nIndexing \"test.txt\"" + \
        "...\nUploading \"test.txt\"..."
    print(dropbox_status(output))

