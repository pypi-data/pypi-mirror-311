import a1_sys.logging.handlers.my_file_handler as my_file_handler
from dataclasses import dataclass
import logging.handlers

@dataclass
class MyRotatingFileHandler(my_file_handler.MyFileHandler) :

  backupCount: int
  maxBytes: int

  def __init__(self, name, filepath, parms = {}):
    # 
    super().__init__(name, filepath, parms)
    #
    self.maxBytes = parms.get('maxBytes', 10000)
    self.backupCount = parms.get('backupCount', 4)
    #
    super().set_handler(
        logging.handlers.RotatingFileHandler(
      self.filepath, mode = self.mode , maxBytes = self.maxBytes, backupCount = self.backupCount, encoding = self.encoding
        )
    )

  def get_handler_type(self):
    return 'RotatingFileHandler'
