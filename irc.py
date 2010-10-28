import curses
import time
import pdb

class Line:
  def __init__(self, attr, data, timestamp=False):
    self.attr = attr
    self.data = data
    self.timestamp = None
    if timestamp:
      self.timestamp = time.strftime("%H:%m:%S ")

class Theme:
  def __init__(self, theme=None):
    self.theme = theme or {}
    self.theme['default'] = {'bg':-1, 'fg':-1}
    self._init_pairs()

  def _init_pairs(self):
    i=1
    for color in self.theme.keys():
      if self.theme[color].has_key('bg'):
        bg = self.theme[color]['bg']
      else:
        bg = -1
      if self.theme[color].has_key('fg'):
        fg = self.theme[color]['fg']
      else:
        fg = -1
      curses.init_pair(i, fg % curses.COLORS, bg % curses.COLORS)
      self.theme[color]['pair'] = i
      i = i+1

  def color_pair(self, key):
    return curses.color_pair(self.theme[key]['pair'])

class WombatTheme(Theme):
  theme = {
      'status'     : { 'fg':230, 'bg':237 }
    , 'topic'      : { 'fg':230, 'bg':237 }
    , 'background' : { 'fg':188, 'bg':234 }
    , 'line'       : { 'fg':188, 'bg':235 }
    , 'time'       : { 'fg':101, 'bg':232 }
    , 'input'      : { 'fg':251, 'bg':234 }
  }
  def __init__(self):
    Theme.__init__(self, self.theme)

class UI:
  def __init__(self, screen, theme):
    self.theme = theme
    self.screen = screen
    self.topic = Line('topic', 'this just in: bloglines is hard', False)
    self.status = Line('status', '[20:49] [rphillips(+Zi)] [6:#bloglines(+ns)]', False)
    self.input_line = Line('input', ' ', False)
    self.height, self.width = self._limits();
    self.lines = []
    for i in range(0, self.height - 3):
      self.lines.insert(i, Line('background', "Blah %i" % i, timestamp=True))

    curses.echo()
    curses.start_color()

    self.screen.clear()
    self.screen.scrollok(True)
    self.screen.setscrreg(1, self.height-3)

    self._draw_background()

  def _limits(self):
    return self.screen.getmaxyx()

  def _draw_line(self, linenum, line):
    self.screen.move(linenum,0)
    offset = 0
    if line.timestamp:
      self.screen.attrset(self.theme.color_pair('time'))
      self.screen.addnstr(line.timestamp, self.width)
      offset += len(line.timestamp)
    if line.data:
      self.screen.attrset(self.theme.color_pair(line.attr))
      self.screen.addnstr(line.data, self.width)
      offset += len(line.data)

    pad_count = self.width - offset - 1
    while pad_count > 0:
      self.screen.addch(' ')
      pad_count -= 1

  def _draw_background(self):
    pair = self.theme.color_pair('background')
    self.screen.bkgdset(' ', pair)

  def _draw_topic(self):
    self._draw_line(0, self.topic)

  def _draw_status(self):
    self._draw_line(self.height-2, self.status)

  def _draw_lines(self):
    i = 1
    for line in self.lines:
      self._draw_line(i, line)
      i = i+1

  def _draw_input(self):
    self._draw_line(self.height-1, self.input_line)
    self.screen.move(self.height-1,0)

  def draw(self):
    self._draw_topic()
    self._draw_status()
    self._draw_lines()
    self._draw_input()
    self.screen.refresh()

  def run(self):
    while 1:
      self.screen.getch()

def main(stdscr):
  theme = WombatTheme()
  ui = UI(stdscr, theme)
  ui.draw()
  ui.run()

if __name__ == "__main__":
  curses.wrapper(main)
