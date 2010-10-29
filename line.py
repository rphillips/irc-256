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

import time

class Line:
  def __init__(self, attr, data, timestamp=False):
    self.attr = attr
    self.data = data
    self.timestamp = None
    if timestamp:
      self.timestamp = time.strftime("%H:%m:%S ")

  def add_ch(self, ch):
    self.data += ch

  def backspace(self):
    self.data = self.data[:-1]

  def clear_data(self):
    self.data = ""

  def width(self):
    return len(self.data)
