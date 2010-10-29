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
