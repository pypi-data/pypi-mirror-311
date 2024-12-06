from a1_loggermanager import logger_manager 


### functions

def get_logger_manager():
    return _logger_manager


### initialisation

# set various logger formats
  # message formats
default_format = "{asctime} {levelname} {filename}: {message}:"
default_short_format = "{asctime} {levelname}: {message}:"
  # date format
date_and_time_format1 = "%Y-%m-%d %H:%M:%S"
time_format1 = "%H:%M:%S"
  # my_formatters parms
myf = (
  { 'name': 'default_format',
    'format': default_format,
    'parms': {
      'datefmt': date_and_time_format1,
      'style': "{"
    }
  }, 
  { 'name': 'default_short_format',
    'format': default_short_format,
    'parms': {
      'datefmt': time_format1,
      'style': "{"
    }
  },
)
  # my_handlers parms
myh = (
  { 'name': 'default_streamhandler',
    'formatter_name': 'default_format',
    'handler_type': 'StreamHandler'
  },
)
  # my_loggers parms
myl = (
  { 'name': 'default_console_logger',
    'level': 'info',
    'handler_names': ('default_streamhandler',),
  },
)

# get a logger manager and add formatter, handler and logger parms
_logger_manager = logger_manager.LoggerManager()
_logger_manager.add_my_formatters(myf)
_logger_manager.add_my_handlers(myh)
_logger_manager.add_my_loggers(myl)


# KWIKFIX (20241121): this is a better use logger manager..
# make available default logger
# TODO: make available various default logger
default_console_logger = _logger_manager.get_my_logger('default_console_logger').logger


