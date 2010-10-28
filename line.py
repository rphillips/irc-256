import time

class Line:
  def __init__(self, attr, data, timestamp=False):
    self.attr = attr
    self.data = data
    self.timestamp = None
    if timestamp:
      self.timestamp = time.strftime("%H:%m:%S ")

