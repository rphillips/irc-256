import curses
from line import *

class UI:
  def __init__(self, irc, screen, theme):
    self.theme = theme
    self.screen = screen
    self.irc = irc
    self.height, self.width = self._limits();
    self.topic = Line('topic', 'this just in: bloglines is hard', False)
    self.status = Line('status', '[20:49] [rphillips(+Zi)] [6:#bloglines(+ns)]', False)
    self.input_line = Line('input', '', False)

    self.lines = []

    curses.echo()
    curses.start_color()
    self.screen.clear()
    self.screen.timeout(0)
    self.screen.scrollok(True)
    self.screen.setscrreg(1, self.height-3)

    self._draw_chat()

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
    self.screen.move(self.height-1, self.input_line.width())

  def draw(self):
    self._draw_topic()
    self._draw_status()
    self._draw_lines()
    self._draw_input()
    self.screen.refresh()

  def add_line(self, line):
    self.lines.append(line)
    self.screen.scroll()
    self._draw_line(self.height-3, line)
    self._draw_input()
    self.screen.refresh()

  def _in_cb(self, msg):
    if msg != "":
      self.add_line(Line('chat', msg, timestamp=True))

  def run(self):
    while 1:
      ch = self.screen.getch()
      if ch != -1:
        if ch == ord('\n'):
          msg = self.input_line.data
          self.add_line(Line('chat', msg, timestamp=True))
          self.irc.write(msg)
          self.input_line.clear_data()
          self._draw_input()
        elif ch == 127: #backspace
          self.input_line.backspace()
          self._draw_input()
        else:
          self.input_line.add_ch(chr(ch))

      #self.irc.run_once(self._in_cb)
