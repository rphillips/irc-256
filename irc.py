import select
import socket
import sys
import fcntl
import os

EPOLLIN = select.EPOLLIN
EPOLLOUT = select.EPOLLOUT

epoll = select.epoll(60000)
connections = {}

class IRC(object):
  output = []

  def __init__(self, host, port, nick, room):
    sock=socket.socket()
    sock.connect((host, port))
    sock.setblocking(0)
    fileno = sock.fileno()
    epoll.register(fileno, EPOLLIN|EPOLLOUT)
    connections[fileno] = self

    self.host = host
    self.socket = sock
    self.nick = nick
    self.room = room
    self.output.append("NICK %s\r\n" % self.nick)
    self.output.append("USER %s %s bla :%s\r\n" % (self.nick, self.host, self.nick))
    self.sent = 0

  def event(self, line, in_cb):
    if line.find("001") != -1:
      self.output.append("JOIN %s\r\n" % self.room)
    in_cb(line.replace('\r\n', ''))

  def write(self, cmd):
    self.output.append("PRIVMSG %s :%s\r\n" % (self.room,cmd))

  def onInput(self, in_cb):
    newdata = self.socket.recv(1024)
    if len(newdata) is 0:
      self.close()
    for line in newdata.split("\r\n"):
      self.event(line, in_cb)

  def onOutput(self):
    try:
      o = self.output[0]
      self.sent = self.socket.send(o[self.sent:])
      if o[self.sent:] == '':
        self.sent = 0
        self.output.pop(0)
    except:
      pass

  def close(self):
    fileno = self.socket.fileno()
    del connections[fileno]
    epoll.unregister(fileno)
    self.socket.close()

  def run_once(self, in_cb):
    for fd, event in epoll.poll():
      if event & EPOLLIN:
        connections[fd].onInput(in_cb)

      if event & EPOLLOUT:
        connections[fd].onOutput()
