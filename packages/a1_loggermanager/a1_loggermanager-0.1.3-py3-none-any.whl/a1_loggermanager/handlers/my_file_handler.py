import a1_sys.logging.my_handler as my_handler
from dataclasses import dataclass
import logging

@dataclass
class MyFileHandler(my_handler.MyHandler) :

  filepath: str
  mode: str
  encoding: str

  def __init__(self, name, filepath, parms = {}):

    self.filepath = filepath
    self.mode = parms.get('mode', 'a')
    self.encoding = parms.get('encoding', 'UTF-8')

    #self.handler_type = self.get_handler_type()

    #super().__init__(name, self.handler_type)
    super().__init__(name)
    super().set_handler(logging.FileHandler(self.filepath, mode = self.mode , encoding = self.encoding))



  def get_handler_type(self):
    return 'FileHandler'
