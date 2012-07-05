#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import socket
import string
import threading
import time


#HOST=sys.argv[1]
PORT=6667
#NICK=sys.argv[2]
HOST='irc.recycled-irc.net'
NICK='moztn'
IDENT="Mozilla Tunisia Bot"
REALNAME="moztnBot"
#readbuffer=""
CHANNEL = '#esprit-libre'

cmd_list=['quit','names','join']

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("JOIN %s\r\n" % CHANNEL)

def GetMsg(msg):
  msg = msg[msg.find('PRIVMSG'):]
  msg = msg[msg.find(':')+1:]
  msg = msg[:msg.find('\r')]
  return msg

def GetUname(msg):
  return msg[msg.find(':')+1:msg.find('!')]
  
def printMsg(msg):
  print '@'+GetUname(msg)+': '+GetMsg(msg)

class PingThread(threading.Thread):
  def __init__(self,conn):
    threading.Thread.__init__(self)
    self.connexion = conn
    
  def run(self):
   readbuffer = ""
   while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )
    #print temp
    #print GetMsg(temp[0])
    printMsg(temp[0])
    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)
        if(line[0]=="PING"):
            self.connexion.send("PONG %s\r\n" % line[1])
            
class InputThread(threading.Thread):
  def __init__(self,conn):
    threading.Thread.__init__(self)
    self.connexion = conn
    
  def run(self):
    while 1:
      msg = raw_input()
      #print msg
      smsg = msg.split(' ')
      if(smsg[0] in cmd_list):
	if (smsg[0] == 'quit'):
	  self.connexion.send('quit :*se fait absorber par un trou noir généré par une division par zéro!*\r\n')
	  PingThread().stop()
	  quit()
	elif(smsg[0] == 'join'):
	  s.send("JOIN %s\r\n" % smsg[1])
	else:
	  self.connexion.send('%s\r\n' % msg)
	  
      else:
	req = self.connexion.send("PRIVMSG %s :%s\r\n" % (CHANNEL,msg))

PingThread(s).start()
InputThread(s).start()
