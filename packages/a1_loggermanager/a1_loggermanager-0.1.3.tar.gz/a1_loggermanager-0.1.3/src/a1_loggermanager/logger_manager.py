import logging
from a1_loggermanager import my_logger, my_formatter
from a1_loggermanager.handlers import my_file_handler, my_rotating_file_handler, my_stream_handler, my_timed_rotating_file_handler

class LoggerManager:

  my_formatters: dict[str:]
  my_handlers: dict[str:]
  my_loggers: dict[str:]

  DEFAULT_HANDLER_TYPE = 'StreamHandler'

  logger: my_logger.MyLogger
  
  def __init__(self, parms = {}):
    #
    self.my_formatters = {}
    self.my_handlers = {}
    self.my_loggers = {}

    # add default formatter, handler and logger
    self.my_formatters['default'] = self.set_default_my_formatter()
    self.my_handlers['default'] = self.set_default_my_handler()
    self.my_loggers['default'] = self.set_default_my_logger()

    # set logger
    self.logger = self.my_loggers['default'].logger      

    # add values passed as parms
    formatters = parms.get('formatters')
    if formatters:
      self.add_my_formatters(formatters)
    handlers = parms.get('handlers')
    if handlers:
      self.add_my_handlers(handlers)
    loggers = parms.get('loggers')
    if loggers:
      self.add_my_loggers(loggers)

  def add_my_formatter(self, my_formattr):
    self.my_formatters[my_formattr['name']] = my_formatter.MyFormatter(my_formattr['format'], my_formattr.get('parms', {}))

  def add_my_formatters(self, my_formatters):
    for my_formatter in my_formatters:
      self.add_my_formatter(my_formatter)

  def add_my_handler(self, my_handler):
    try:
      handler_type = my_handler.get('handler_type', self.DEFAULT_HANDLER_TYPE)  
      match handler_type:
        case 'FileHandler':
          self.my_handlers[my_handler['name']] = my_file_handler.MyFileHandler(my_handler['name'], my_handler['parms']['filepath'], my_handler.get('parms', {}))
        case 'RotatingFileHandler':
          self.my_handlers[my_handler['name']] = my_rotating_file_handler.MyRotatingFileHandler(my_handler['name'], my_handler['parms']['filepath'], my_handler.get('parms', {}))
        case 'StreamHandler':
          self.my_handlers[my_handler['name']] = my_stream_handler.MyStreamHandler(my_handler['name'])
        case 'TimedRotatingFileHandler':
          self.my_handlers[my_handler['name']] = my_timed_rotating_file_handler.MyTimedRotatingFileHandler(my_handler['name'], my_handler['parms']['filepath'], my_handler.get('parms', {}))
        case _:
          self.logger.error(f"Unknown handler type '{handler_type}'")
      # add formatter to handler if specified otherwise use default formatter
      self.my_handlers[my_handler['name']].set_formatter(self.my_formatters[my_handler.get('formatter_name', "default")].formatter)
    except:
      mess = f"Could not add handler with {my_handler}"
      self.logger.error(mess)
      raise Exception(mess)

  def add_my_handlers(self, my_handlers):
    for my_handler in my_handlers:
      self.add_my_handler(my_handler)

  def add_my_logger(self, my_loggr):
    name = my_loggr.get('name', 'default')
    self.my_loggers[name] = my_logger.MyLogger(name, my_loggr.get('level', None))
        # add default handler if none specified
    if not my_loggr.get('handler_names'):
      my_loggr['handler_names'] = ('default',)
    # add handlers to loggers
    for my_handler_name in my_loggr['handler_names']:
        self.my_loggers[name].add_handler(self.my_handlers[my_handler_name].handler)
    return self.my_loggers[name]        

  def add_my_loggers(self, my_loggers):
    for my_logger in my_loggers:
      self.add_my_logger(my_logger)

  # get logger
  @staticmethod
  def get_logger(name = 'default'):
    return logging.getLogger(name)
  
  def get_my_logger(self, name = 'default'):
    try:
      self.logger.info(f"Logger '{name}' returned")
      return self.my_loggers[name]
    except:
      raise Exception(f"Can't get my_logger with name '{name}'")

  def set_default_my_formatter(self):
    my_formattr = self.my_formatters.get('default')
    if not my_formattr:
      my_formattr = my_formatter.MyFormatter(
        '{asctime} {levelname} ({filename} {lineno}): {message}',
        { 'datefmt': "%Y-%m-%d %H:%M",
          'style': "{"
        }
      )
    return my_formattr

  def set_default_my_handler(self):
    handler = self.my_handlers.get('default')
    if not handler:
      handler = my_stream_handler.MyStreamHandler('default')
      handler.set_formatter(self.my_formatters['default'].formatter)
    return handler

  def set_default_my_logger(self):
    logger = my_logger.MyLogger('default')
    logger.add_handler(self.my_handlers['default'].handler)
    return logger

  def set_my_logger_level(self, level, my_logger = None):
    if not my_logger:
      my_logger = self.get_my_logger()
    my_logger.set_level(level)      



