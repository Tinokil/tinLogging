# tinLogging

`tinLogging` is a versatile logging library for Python that provides a range of functionalities to enhance your application's logging capabilities.

## Features

- Supports multiple logging levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- Ability to log `HTTP` requests with detailed information.
- Export logs to `JSON` and `HTML` formats for easy analysis.
- Log rotation and archiving to manage log file sizes efficiently.

## Installation

Install `tinLogging` with pip using the following command:

```
pip install tinLogging
```
Quick Start
Here's how you can get started with `tinLogging`:
```
from tinLogging import Logger

# Creating a class object
logger = Logger()

# Writing logs to a file
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning')
logger.error('This is an error message')
logger.critical('This is a critical message')
```
# Documentation
`tinLogging` is a robust logging library for Python applications, offering a wide range of functionalities to enhance logging capabilities. It simplifies event tracking, debugging, and application behavior analysis.
## Getting Started
### Installation
To install `tinLogging`, run the following command:
```
pip install tinLogging
```
## Basic Usage
To begin using `tinLogging`, import the `Logger` class and create an instance:
```
from tinLogging import Logger
logger = Logger()
```
## Logging Messages
`tinLogging` supports various logging levels. Here's how to log messages at different levels:
```
logger.debug('This is a DEBUG level message')
logger.info('This is an INFO level message')
logger.warning('This is a WARNING level message')
logger.error('This is an ERROR level message')
logger.critical('This is a CRITICAL level message')
```
## HTTP Request Logging
`tinLogging` can log HTTP requests with detailed information:
```
logger.http(200, 'OK', 'https://example.com/api')
```
## Exporting Logs
You can export logs to `JSON` or `HTML` formats:
```
logger.export_json('exported_logs.json')
logger.export_html('exported_logs.html')
```
## Advanced Features
### Log Rotation
`tinLogging` can rotate logs when the file size reaches a specified limit:
```
logger.rotate_logs(max_megabytes_size=10)
```
### Deleting Old Logs
You can delete logs older than a specified number of days or hours:
```
logger.deleting_old_logs(days=7)
```
### Archiving Logs
`tinLogging` can archive and delete old logs:
```
Logger.archive_logs('logs.txt', 'logs_archive.zip')
```
### Monitoring Log Size
`tinLogging` can monitor the log file size and send a warning if it exceeds a certain limit:
```
logger.monitor_log_size(max_megabytes_size=8)
```
## Console Logging
`tinLogging` also includes a `ConsoleLogger` for logging messages to the console with color coding:
```
from tinLogging import ConsoleLogger

console_logger = ConsoleLogger(debug_color = 'Blue')
console_logger.debug('This is a debugging message')
```
## Conclusion
`tinLogging` is a powerful tool for managing application logs. With its user-friendly interface and extensive features, it's an excellent choice for developers looking to implement robust logging in their Python applications

# Contributing
Contributing in `tinLogging` is welcome! To contact us, write to the mail `zemedeuk@gmail.com`

# License
`tinLogging` is released under the MIT License. See the LICENSE file for more details
