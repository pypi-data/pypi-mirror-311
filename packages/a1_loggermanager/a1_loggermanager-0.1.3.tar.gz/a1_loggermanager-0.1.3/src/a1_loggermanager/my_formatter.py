import logging
from dataclasses import dataclass

@dataclass
class MyFormatter:

  format: str
  style: str
  datefmt: str

  def __init__(self, format, parms = {}):
    self.format = format
    self.style = parms.get('style', '{')
    self.datefmt = parms.get('datefmt', '%Y-%m-%d %H:%M')
    self.formatter = logging.Formatter(self.format, style = self.style, datefmt = self.datefmt)

    