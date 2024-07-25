[![PyPI version](https://badge.fury.io/py/tinLogging.svg)](https://badge.fury.io/py/tinLogging)
[![Python versions](https://img.shields.io/pypi/pyversions/tinLogging.svg)](https://pypi.org/project/tinLogging/)
[![License](https://img.shields.io/pypi/l/tinLogging.svg)](https://pypi.org/project/tinLogging/)
[![GitHub stars](https://img.shields.io/github/stars/Tinokil/tinLogging.svg)](https://github.com/Tinokil/tinLogging/stargazers)
[![GitHub release date](https://img.shields.io/github/release-date/Tinokil/tinLogging.svg)](https://github.com/Tinokil/tinLogging/releases)

# tinLogging
`tinLogging` is a versatile logging library for Python that provides a range of functionalities to enhance your application's logging capabilities
## Installation
`pip install tinLogging`
## Update
`pip install --upgrade tinLogging`
## Quick start
```python
from tinLogging import Logger, ConsoleLogger

logger = Logger(filename='log.txt', level='DEBUG', buffer_size=10, log_format='[%time] - %lvl | %text')
console_logger = ConsoleLogger(level='DEBUG', log_format='%time | %lvl | %text')
# Writing a log to a file 'log.txt'
logger.debug('This is a debug message')
# Log output to the console
console_logger.debug('This is a debug message')
console_logger.info('This is an info message')
console_logger.warning('This is a warning message')
console_logger.error('This is an error message')
```
This is what the color text output looks like in the console:
![Console Output](https://github.com/Tinokil/tinLogging/raw/main/images/quick_start_console.PNG)
## Logging to a file
### Main functions
```python
from tinLogging import Logger

logger = Logger(filename='log.txt', level='DEBUG', buffer_size=10, log_format='[%time] - %lvl | %text')
# Enabling automatic file rotation with zip archiving
logger.rotate_logs(max_megabytes_size=1, zip_compression=True, auto_rotate=True)
# Sending a log
logger.critical('This is a critical message')
# Creating a new log level with priority 3
logger.new_level(level_name='MyNewLevel', level_priority=3)
# Sending a log with a new level
logger.log('MyNewLevel', 'This is a MyNewLevel message')
# Deleting the old log level
logger.del_level('WARNING')
```
### Additional functions
#### Export
``` Python
logger.export_json(export_file='my_export_log.json')
logger.export_html(export_file='my_new_export_log.html')
```
#### Search and filtering
``` Python
# Text search
search = logger.search_logs('message')
# Filtering by level
filter_logs = logger.filter_logs('CRITICAL')
```
#### Statistics
``` Python
logger.log_stats(files_name='log.txt')
```
#### Archiving
``` Python
logger.archive_logs(archive_name='my_zip_log.zip')
```
#### Checking for acceptable file size
``` Python
logger.monitor_log_size(max_megabytes_size=8)
# Returns True if it exceeds the specified size
```
#### Buffer
``` Python
# buffer_size - buffer size for optimizing I/O requests
logger = Logger(filename='log.txt', level='DEBUG', buffer_size=10, log_format='[%time] - %lvl | %text')
# Recording the remaining logs in the buffer
logger.close()
```
## Logging to a Console
Logging into the console will allow you to display colored logs to facilitate the search for the necessary logging levels. But do not forget that after restarting the interpreter, the console is cleared
```python
from tinLogging import ConsoleLogger
# You can customize the colors to suit your taste, but by default there are always the most suitable colors
logger = ConsoleLogger(level='DEBUG', log_format='%time | %lvl | %text', debug_color='standard', info_color='green')
# Creating a new log level
logger.new_level('HTTP', 4)
# Logging with the HTTP level highlighted in green
logger.log(level='HTTP', message='Code 200 - the site is working', color='green')
```
## Contributing
We welcome contributions to the `tinLogging` project! If you have any bug reports, feature requests, or pull requests, please feel free to submit them on our [GitHub repository](https://github.com/Tinokil/tinLogging)
## License
`tinLogging` is licensed under the MIT License. See the [LICENSE](https://github.com/Tinokil/tinLogging/blob/main/LICENSE) file for more information
