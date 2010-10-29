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
    , 'chat'       : { 'fg':188, 'bg':234 }
    , 'line'       : { 'fg':188, 'bg':235 }
    , 'time'       : { 'fg':101, 'bg':232 }
    , 'input'      : { 'fg':251, 'bg':234 }
  }
  def __init__(self):
    Theme.__init__(self, self.theme)


class XoriaTheme(Theme):
  theme = {
      'status'     : { 'fg':230, 'bg':237 }
    , 'topic'      : { 'fg':230, 'bg':237 }
    , 'chat'       : { 'fg':188, 'bg':234 }
    , 'line'       : { 'fg':252, 'bg':234 }
    , 'time'       : { 'fg':248, 'bg':232 }
    , 'input'      : { 'fg':251, 'bg':234 }
  }
  def __init__(self):
    Theme.__init__(self, self.theme)
