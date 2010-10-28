import curses
import irclib
import sys
from theme import *
from ui    import *

SERVER='irc.freenode.net'
PORT=6667
NICKNAME='rphillips-2'
ROOM='#rphillips-testing'

def main(stdscr):
  irc = irclib.IRC()
  try:
    server = irc.server().connect(SERVER, PORT, NICKNAME)
  except irclib.ServerConnectionError, x:
    print(x)
    sys.exit(1)

  theme = WombatTheme()
  ui = UI(irc, server, ROOM, stdscr, theme)
  ui.draw()
  ui.run()

if __name__ == "__main__":
  curses.wrapper(main)
