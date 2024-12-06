# a1_loggermanager

Python logging.Logger manager

## In this README :point_down:

- [Features](#features)
- [Usage](#usage)
  
  
- [FAQ](#faq)
- [Contributing](#contributing)

## Features

- get default logger
- add and store for use formatters, handlers, and loggers
- set logger level
- access logging.logger
- easy to follow example script (see [github](https://github.com/a1publishing/a1_loggermanager) repo)

## Usage

### Get a logger
```
import a1_loggermanager
logger_manager = a1_loggermanager.get_logger_manager()
logger = logger_manager.get_my_logger('default_console_logger')
logger.info('Created `logger_manager` and `logger`')
```
2024-11-15 14:50:18 INFO my_logger.py: Created `logger_manager` and `logger`

### add new logger
```
my_logger_parms = ({
...   'name': 'logger2',
...     'handler_names': ('default_streamhandler',)
...     })
logger_manager.add_my_logger(my_logger_parms)
MyLogger(name='logger2', handlers={}, logger=<Logger logger2 (WARNING)>)
logger2 = logger_manager.get_my_logger('logger2')
logger2.info('Created `logger2`?')
logger2.set_level('info')
logger2.info('Created `logger2`!')
```
2024-11-15 15:10:27 INFO my_logger.py: Created `logger2`!

### add a file handler logger and a combined console and file handler logger
#### set and add a file handler configuration
```
myh = (
  { 'name': 'default_filehandler',
    'formatter_name': 'default_format',
    'handler_type': 'FileHandler',
    'parms': {
      'filepath': filepath,
      'encoding': "utf-8",
      'mode': "a"
    }
  },
)
logger_manager.add_my_handlers(myh)

```
#### set and add a couple of logger configurations with the file handler config
```
myl = (
  { 'name': 'file_logger',
    'level': 'info',
    'handler_names': ('default_filehandler',),
  },
  { 'name': 'console_and_file_logger',
    'level': 'info',
    'handler_names': ('default_streamhandler', 'default_filehandler'),
  }
)
logger_manager.add_my_loggers(myl)
```
#### get the file handler logger and log an entry
```
file_logger = logger_manager.get_my_logger('file_logger')
file_logger.info('Created `file_logger`')
```
#### get the combined console and file handler logger and log an entry
```
console_file_logger = logger_manager.get_my_logger('console_and_file_logger')
console_file_logger.info('Created `console_file_logger`')
```
### accessing logging.logger, eg;
```
logger2.logger.addFilter(filter_debug) 
```

## FAQ

#### Is this package developed primarily for creator use?

Yes, it's a first package published to https://pypi.org/ and as much a learning tool as anything.  That said the logger manager should be useful as a starting point for any similar project or just to avoid getting caught up in logging.Logger docs.  Use it to easily create and manage loggers.

## Contributing

If you find a bug :bug:, have a suggestion :rocket:, etc., please let me know (<mike@a1publishing.com>:)