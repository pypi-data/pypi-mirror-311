import a1_misc.regex.regex_equal as regex_equal
from dataclasses import dataclass
import logging


@dataclass
class MyLogger:
#class MyLogger(logging.Logger):


  name: str
  handlers: dict[str:]
  logger: logging.Logger
  
  def __init__(self, name, level = None):
    self.name = name
    level = "WARNING" if level is None else level 

    # 
    self.logger = logging.getLogger(name)
    self.logger.level = self.get_logging_level(level)
    #
    self.handlers = {}
  
  def add_handler(self, handler):
    self.logger.addHandler(handler)

  def critical(self, message):
    self.logger.critical(message)

  def debug(self, message):
    self.logger.debug(message)

  def error(self, message):
    self.logger.error(message)

  def get_logger(self):
    return self.logger

  @staticmethod
  #def get_logging_level(self, level):
  def get_logging_level(level):
    match regex_equal.RegexEqual(level):
      case 'DEBUG|debug':
        return logging.DEBUG
      case 'INFO|info':
        return logging.INFO
      case 'WARNING|warning':
        return logging.WARNING
      case 'ERROR|error':
        return logging.ERROR
      case 'CRITICAL|critical':
        return logging.CRITICAL
      case _:
        raise Exception(f"Can't match level '{level}'")

  def info(self, message):
    self.logger.info(message)
  
  def set_level(self, level):
    self.logger.setLevel(self.get_logging_level(level))

  def warning(self, message):
    self.logger.warning(message)

