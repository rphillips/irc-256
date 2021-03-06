# Copyright 2010 Ryan Phillips
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import curses
import irclib
from curses.ascii import isprint
from line import Line

class UI:
  def __init__(self, irc, server, room, screen, theme):
    self.theme = theme
    self.screen = screen
    self.irc = irc
    self.server = server
    self.room = room
    self.height, self.width = self._limits();
    self.topic = Line('topic', '', False)
    self.status = Line('status', '', False)
    self.input_line = Line('input', '', False)

    self.lines = []

    curses.echo()
    curses.start_color()
    self.screen.clear()
    self.screen.timeout(0)
    self.screen.scrollok(True)
    self.screen.setscrreg(1, self.height-3)

    self._draw_chat()

    self.irc.add_global_handler("welcome", self.on_connect)
    self.irc.add_global_handler("motd", self.on_motd)
    self.irc.add_global_handler("pubmsg", self.on_pubmsg)
    self.irc.add_global_handler("currenttopic", self.on_currenttopic)

  def _limits(self):
    return self.screen.getmaxyx()

  def _draw_line(self, linenum, line):
    self.screen.move(linenum,0)
    offset = 0
    if line.timestamp:
      self.screen.attrset(self.theme.color_pair('time'))
      self.screen.addnstr(line.timestamp, self.width)
      offset += len(line.timestamp)

    self.screen.attrset(self.theme.color_pair(line.attr))
    if line.data:
      self.screen.addnstr(line.data, self.width)
      offset += len(line.data)

    pad_count = self.width - offset - 1
    while pad_count > 0:
      self.screen.addch(' ')
      pad_count -= 1

  def _draw_chat(self):
    pair = self.theme.color_pair('chat')
    self.screen.bkgdset(' ', pair)

  def _goto_input(self):
    self.screen.move(self.height-1, self.input_line.width())

  def _draw_topic(self):
    self._draw_line(0, self.topic)

  def _draw_status(self):
    self._draw_line(self.height-2, self.status)

  def _draw_lines(self):
    i = 1
    for line in self.lines[-self.height:]:
      self._draw_line(i, line)
      i = i+1

  def _draw_input(self):
    self._draw_line(self.height-1, self.input_line)

  def draw(self):
    self._draw_topic()
    self._draw_status()
    self._draw_lines()
    self._draw_input()
    self._goto_input()
    self.screen.refresh()

  def add_line(self, line):
    self.lines.append(line)
    self.screen.scroll()
    self._draw_line(self.height-3, line)
    self._draw_input()
    self.screen.refresh()

  def on_currenttopic(self, connection, event):
    topic = event.arguments()[1]
    self.topic = Line('topic', topic.strip(), False)
    self._draw_topic()
    self._goto_input()

  def on_connect(self, connection, event):
    if irclib.is_channel(self.room):
      connection.join(self.room)
      who = event.source()[0:event.source().find("!")]
      self.status = Line('status', "[%s] [%s]" % (who, self.room))
      self._draw_status()
      self._goto_input()

    self.add_line(Line('chat', "Connected", timestamp=True))

  def on_pubmsg(self, connection, event):
    who = event.source()[0:event.source().find("!")]
    msg = who + "> " + " ".join(event.arguments())
    self.add_line(Line('chat', msg, timestamp=True))

  def on_motd(self, connection, event):
    self.add_line(Line('chat', " ".join(event.arguments()), timestamp=False))

  def run(self):
    while 1:
      ch = self.screen.getch()
      if ch != -1:
        if ch == ord('\n'):
          msg = self.input_line.data
          self.add_line(Line('chat', msg, timestamp=True))
          self.server.privmsg(self.room, msg)
          self.input_line.clear_data()
          self._draw_input()
        elif ch == 127: #backspace
          self.input_line.backspace()
          self._draw_input()
        elif isprint(ch):
          self.input_line.add_ch(chr(ch))

      self.irc.process_once()
