import a1_sys.logging.handlers.my_file_handler as my_file_handler
from dataclasses import dataclass
import datetime
import logging.handlers

@dataclass
class MyTimedRotatingFileHandler(my_file_handler.MyFileHandler) :

  atTime: datetime.time
  backupCount: int
  interval: int
  when: str


  def __init__(self, name, filepath, parms = {}):
    #
    super().__init__(name, filepath, parms)
    # back up 4
    self.atTime = parms.get('atTime', None )  
    self.backupCount = parms.get('backupCount', 4)
    self.interval = parms.get('interval', 4)
    self.when = parms.get('when', 'W0') # (Weekday (0=Monday))
    #
    super().set_handler(
      logging.handlers.TimedRotatingFileHandler(
        self.filepath, 
        when = self.when, 
        interval = self.interval, 
        backupCount = self.backupCount, 
        encoding = self.encoding, 
        atTime = self.atTime
      )
    )

  def get_handler_type(self):
    return 'TimedRotatingFileHandler'
