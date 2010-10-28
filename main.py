import curses
from theme import *
from ui    import *
from irc   import *

SERVER='irc.freenode.net'
PORT=6667
NICK='rphillips-256'
ROOM='#rphillips-test'

def main(stdscr):
  theme = WombatTheme()
  client = IRC(SERVER, PORT, NICK, ROOM)
  ui = UI(client, stdscr, theme)
  ui.draw()
  ui.run()

if __name__ == "__main__":
  curses.wrapper(main)
