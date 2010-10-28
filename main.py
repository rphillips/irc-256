import curses
from theme import *
from ui    import *

def main(stdscr):
  theme = WombatTheme()
  ui = UI(stdscr, theme)
  ui.draw()
  ui.run()

if __name__ == "__main__":
  curses.wrapper(main)
