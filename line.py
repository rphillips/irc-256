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
