import datetime
import json
import os
import zipfile


class Logger:
    """Logging to a file"""
    _LEVELS = {'DEBUG': 1, 'INFO': 2, 'WARNING': 3, 'ERROR': 4, 'CRITICAL': 5}

    def __init__(self, filename: str = 'logs.txt', level: str = 'DEBUG'):
        self._filename = filename
        self._level = self._LEVELS[level]

    def _log(self, level: str, message: str):
        """Records a message if its level is equal to or higher than the set"""
        if self._LEVELS[level] >= self._level:
            timestamp = datetime.datetime.now().strftime('%Y-%d-%m %H:%M:%S.%f')[:-1]
            formatted_message = f'[{timestamp}] - {level} | {message}\n'
            self._write_to_file(formatted_message)

    def _write_to_file(self, message: str):
        """Writes a message to a file"""
        with open(self._filename, 'a', encoding='UTF-8') as file:
            file.write(message)

    def http(self, request_code: int, request_message: str, url: str = None):
        """Sending logs with HTTP requests"""
        timestamp = datetime.datetime.now().strftime('%Y-%d-%m %H:%M:%S.%f')[:-1]
        if url is None:
            formatted_message = f'[{timestamp}] - HTTP {request_code} | {request_message}\n'
        else:
            formatted_message = f'[{timestamp}] - HTTP {request_code} | {request_message} - ({url})\n'
        self._write_to_file(formatted_message)

    def debug(self, message: str):
        """Sending debug level logs"""
        self._log('DEBUG', message)

    def info(self, message: str):
        """Sending info level logs"""
        self._log('INFO', message)

    def warning(self, message: str):
        """Sending warning level logs"""
        self._log('WARNING', message)

    def error(self, message: str):
        """Sending error level logs"""
        self._log('ERROR', message)

    def critical(self, message: str):
        """Sending critical level logs"""
        self._log('CRITICAL', message)

    @staticmethod
    def _log_counts(file_name):
        file_path = os.path.abspath(file_name)
        log_counts = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0}
        try:
            with open(file_path, 'r', encoding='UTF-8') as file:
                for line in file:
                    log_type = line.split('] - ')[1].split(' |')[0]
                    if log_type not in log_counts:
                        log_counts[log_type] = 0
                    log_counts[log_type] += 1
        except FileNotFoundError:
            log_error = Logger('logger_errors.txt')
            log_error.error('The log file is missing')
            print('\033[91mFileNotFoundError: The log file is missing')
        return log_counts

    def log_stats(self):
        stats = Logger._log_counts(self._filename)
        return stats

    def export_json(self, export_file: str = 'log_export.json'):
        """Function for exporting logs to JSON"""
        try:
            with open(self._filename, 'r', encoding='UTF-8') as log_file, open(export_file, 'w',
                                                                               encoding='UTF-8') as json_file:
                logs_list = []
                for line in log_file:
                    logs_list.append(line.strip())
                json.dump(logs_list, json_file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            log_error = Logger('logger_errors.txt')
            log_error.error('The log file is missing')
            print('\033[91mFileNotFoundError: The log file is missing')

    def export_html(self, export_file: str = 'log_export.html'):
        """Exporting logs to an HTML file"""
        try:
            with open(self._filename, 'r', encoding='UTF-8') as log_file, open(export_file, 'w',
                                                                               encoding='UTF-8') as html_file:
                html_file.write('<html><head><title>Logs</title></head><body><pre>\n')
                for line in log_file:
                    html_file.write(line)
                html_file.write('</pre></body></html>')
        except FileNotFoundError:
            log_error = Logger('logger_errors.txt')
            log_error.error('The log file is missing')
            print('\033[91mFileNotFoundError: The log file is missing')

    def rotate_logs(self, max_megabytes_size: float = 8):
        """Log rotation when the maximum size in megabytes is reached"""
        if os.path.getsize(self._filename) > max_megabytes_size * 1024 * 1024:
            base, extension = os.path.splitext(self._filename)
            log_number = 1
            new_log_file = f"{base}_{log_number}{extension}"
            while os.path.exists(new_log_file):
                log_number += 1
                new_log_file = f"rotate_{base}_{log_number}{extension}"
            os.rename(self._filename, new_log_file)

    def deleting_old_logs(self, days: float = 0, hours: float = 0):
        """Clears logs older than the specified number of days"""
        if days == 0 and hours == 0:
            log_error = Logger('logger_errors.txt')
            error_text = 'The number of days and hours must be specified'
            log_error.warning(error_text)
            print(f"\033[91m{error_text}")
            return
        timedelta_value = days if days is not None else hours / 24
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=timedelta_value, hours=hours)

        with open(self._filename, 'r+', encoding='UTF-8') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                timestamp = line.split('] - ')[0].strip('[')
                log_date = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
                if log_date > cutoff_date:
                    file.write(line)
            file.truncate()

    def archive_logs(self, archive_name: str = 'logs_archive.zip'):
        """Archives and delete old logs into a zip file"""
        file_name = self._filename
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_name)
            os.remove(file_name)

    def monitor_log_size(self, max_megabytes_size: float = 8):
        """Checks the size of the logs file and sends a warning"""
        if os.path.getsize(self._filename) > max_megabytes_size * 1024 * 1024:
            self.warning(f"The log file size has exceeded {max_megabytes_size}MB")


class ConsoleLogger:
    """Logging into the console"""
    _LEVELS = {'DEBUG': 1, 'INFO': 2, 'WARNING': 3, 'ERROR': 4, 'CRITICAL': 5}
    _COLORS = {
        'Standard': '\033[0m',
        'Red': '\033[91m',
        'Green': '\033[92m',
        'Yellow': '\033[93m',
        'Blue': '\033[94m',
        'Magenta': '\033[95m',
        'Cyan': '\033[96m',
        'White': '\033[97m'
    }

    def __init__(self, level: str = 'DEBUG', debug_color: str = 'Cyan', info_color: str = 'Standard',
                 warning_color: str = 'Yellow', error_color: str = 'Red', critical_color: str = 'Magenta',
                 http_color: str = 'Green'):
        self._level: int = self._LEVELS.get(level, 2)
        self._debug_color: str = self._COLORS[debug_color]
        self._info_color: str = self._COLORS[info_color]
        self._warning_color: str = self._COLORS[warning_color]
        self._error_color: str = self._COLORS[error_color]
        self._critical_color: str = self._COLORS[critical_color]
        self._http_color: str = self._COLORS[http_color]

    def _log(self, level: str, message: str):
        """Records a message if its level is equal to or higher than the set"""
        if self._LEVELS.get(level, 0) >= self._level:
            timestamp = datetime.datetime.now().strftime('%Y-%d-%m %H:%M:%S.%f')[:-1]
            color = getattr(self, f'_{level.lower()}_color')
            formatted_message = f'[{timestamp}] - {color}{level} {self._COLORS['Standard']}| {message}'
            print(formatted_message)

    def http(self, request_code: int, request_message: str, url: str = None):
        """Sending logs with HTTP requests"""
        timestamp = datetime.datetime.now().strftime('%Y-%d-%m %H:%M:%S.%f')[:-1]
        color = self._http_color
        if url is None:
            formatted_message = (f'[{timestamp}] - {color}HTTP {request_code} {self._COLORS['Standard']}| '
                                 f'{request_message}\n')
        else:
            formatted_message = (f'[{timestamp}] - {color}HTTP {request_code} {self._COLORS['Standard']}| '
                                 f'{request_message} - ({url})\n')
        print(formatted_message)

    def debug(self, message: str):
        """Sending debug level logs"""
        self._log('DEBUG', message)

    def info(self, message: str):
        """Sending info level logs"""
        self._log('INFO', message)

    def warning(self, message: str):
        """Sending warning level logs"""
        self._log('WARNING', message)

    def error(self, message: str):
        """Sending error level logs"""
        self._log('ERROR', message)

    def critical(self, message: str):
        """Sending critical level logs"""
        self._log('CRITICAL', message)


if __name__ == '__main__':
    # Example of using the ConsoleLogger class
    logger = ConsoleLogger(http_color='Blue')
    logger.debug('This is a debugging message')
    logger.info('This is an informational message')
    logger.warning('This is a warning')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    logger.http(404, 'Unknown page', 'https://random_unknown_url/b')
  
