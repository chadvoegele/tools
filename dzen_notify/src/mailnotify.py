#!/usr/bin/env python
import imaplib, sys, os
import socket
import config

def newMail():
  password=""
  if os.path.exists(config.net_prof_dir) \
      and len(os.listdir(config.net_prof_dir)) > 0 \
      and not password == "":
    try:
      mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
      mail.login("cavoegele@gmail.com", password)
      mail.select()
      counter=0
      typ, messages = mail.search(None, 'UNSEEN')
      for msg in messages[0].split():
        counter=counter+1
      mail.close()
      mail.logout()
      return (str(counter), 240)
    except (socket.gaierror, mail.abort) as err:
      return ("!", 60)
  else:
    return ("!", 60)
