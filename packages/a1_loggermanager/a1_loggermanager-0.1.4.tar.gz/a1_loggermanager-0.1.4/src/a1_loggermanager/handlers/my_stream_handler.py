import a1_sys.logging.my_handler as my_handler
from dataclasses import dataclass
import logging

@dataclass
class MyStreamHandler(my_handler.MyHandler) :

  def __init__(self, name):
    super().__init__(name)
    super().set_handler(logging.StreamHandler())

  def get_handler_type(self):
    return 'StreamHandler'