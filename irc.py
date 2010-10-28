import curses
import time

COLORS = [
  (124, 235), # Title
  (172, 235), # Background
  (240, 246), # Status Bar
]

def pad_str(max_x, msg):
  return msg + (((max_x - len(msg)) - 1) * ' ')

def update_topic(stdscr, msg):
  stdscr_y, stdscr_x = stdscr.getmaxyx()
  stdscr.attrset(curses.color_pair(1))
  stdscr.clrtoeol()
  stdscr.addstr(0, 0, pad_str(stdscr_x, msg))
  stdscr.refresh()

def update_status(stdscr, msg):
  stdscr_y, stdscr_x = stdscr.getmaxyx()
  stdscr.attrset(curses.color_pair(3))
  stdscr.clrtoeol()
  stdscr.refresh()

def append_line(stdscr, line):
  t = time.strftime("%H:%m:%S ")
  stdscr_y, stdscr_x = stdscr.getmaxyx()
  stdscr.scroll()
  stdscr.clrtoeol()
  stdscr.attrset(curses.color_pair(2))
  stdscr.addstr(stdscr_y-2, 0, pad_str(stdscr_x, t + line))
  stdscr.move(stdscr_y-1, 0)
  stdscr.refresh()

def setup(stdscr):
  curses.echo()
  stdscr.clear()
  stdscr.scrollok(True)
  stdscr_y, stdscr_x = stdscr.getmaxyx()
  stdscr.setscrreg(1, stdscr_y-2)

  # setup theme
  for i in range(0, len(COLORS)):
    fg, bg = COLORS[i]
    curses.init_pair(i+1, fg, bg)

  stdscr.bkgdset(' ', curses.color_pair(2))
  stdscr.bkgd(curses.color_pair(2))

  # update status bar
  update_status(stdscr, "Testing")

  stdscr.attrset(curses.color_pair(2))
  stdscr.refresh()

def main(stdscr):
  setup(stdscr)
  update_topic(stdscr, "Hello World")

  while 1:
    append_line(stdscr, " rphillips> Hello World")
    curses.napms(100)

if __name__ == "__main__":
  curses.wrapper(main)
