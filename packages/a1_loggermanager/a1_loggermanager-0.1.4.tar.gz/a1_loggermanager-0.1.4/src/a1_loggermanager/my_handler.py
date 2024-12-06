from dataclasses import dataclass

@dataclass
class MyHandler:

  #name: str
  #handler_type: str

  #def __init__(self, name, handler_type):
  def __init__(self, name):    
    self.name = name
    #self.handler_type = handler_type
    self.handler_type = self.get_handler_type()

  def set_formatter(self, formatter):
    self.handler.setFormatter(formatter)
    #pass
  
  def set_handler(self, handler):
    self.handler = handler

