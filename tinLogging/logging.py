import datetime
import json
import os
import zipfile
import re
import atexit


class Levels:

    def __init__(self):
        self._LEVELS = {'DEBUG': 1, 'INFO': 2, 'WARNING': 3, 'ERROR': 4, 'CRITICAL': 5}

    def new_level(self, level_name: str, level_priority: int):
        """Adding a new log level and changing the priority of some level"""
        self._LEVELS[level_name.upper()] = level_priority

    def del_level(self, level_name: str):
        """Deleting the log level"""
        del self._LEVELS[level_name.upper()]


class Logger(Levels):
    """Logging to a file"""

    def __init__(self, filename: str, level: str = 'DEBUG', buffer_size: int = 1,
                 log_format: str = '[%time] - %lvl | %text'):
        self._filename: str = filename
        super().__init__()
        self._level: int = self._LEVELS[level]
        self._format: str = log_format
        self._buffer_size: int = buffer_size
        self._log_buffer: list = []
        self._rotate_data: dict = {"max_size": None, "zip": False}

        try:
            with open(self._filename, 'a'):
                pass
        except IOError as e:
            self._log_error(f'IOError: {e}', 'ERROR')

        # Сохранение буфера в файл после завершения работы интерпритатора
        atexit.register(self.close)

    def _format_message(self, level: str, message: str):
        """Custom format processing"""
        current_time = datetime.datetime.now()
        return self._format.replace('%time', str(current_time)).replace('%lvl', level).replace('%text', message)

    def _log(self, level: str, message: str):
        """Saving logs to the buffer and then saving logs in file"""
        self._log_buffer.append(self._format_message(level, message))
        try:
            if len(self._log_buffer) >= self._buffer_size:
                self.close()
        except KeyError as e:
            self._log_error(f'KeyError: {e}', 'ERROR')

    def close(self):
        """Saving a buffer to a file"""
        if self._log_buffer:
            self.rotate_logs(self._rotate_data['max_size'], self._rotate_data['zip'])
            try:
                with open(self._filename, 'a', encoding='UTF-8') as file:
                    file.write('\n'.join(self._log_buffer) + '\n')
                self._log_buffer.clear()
            except FileNotFoundError as e:
                self._log_error(f'FileNotFoundError: {e}', 'ERROR')

    @staticmethod
    def _log_error(message: str, level: str = 'WARNING'):
        """Logs errors to a separate error file"""
        message = f'{datetime.datetime.now()} | {level.upper()} | {message}'
        with open('logger_errors.txt', 'a', encoding='UTF-8') as error_file:
            error_file.write(f'{message}\n')
        print(f'\033[91m{message}\033[0m')

    def debug(self, message: str):
        """Sending debug level logs"""
        if self._level <= self._LEVELS['DEBUG']:
            self._log('DEBUG', message)

    def info(self, message: str):
        """Sending info level logs"""
        if self._level <= self._LEVELS['INFO']:
            self._log('INFO', message)

    def warning(self, message: str):
        """Sending warning level logs"""
        if self._level <= self._LEVELS['WARNING']:
            self._log('WARNING', message)

    def error(self, message: str):
        """Sending error level logs with optional exception info"""
        if self._level <= self._LEVELS['ERROR']:
            self._log('ERROR', message)

    def critical(self, message: str):
        """Sending critical level logs with optional exception info"""
        self._log_buffer.append(self._format_message('CRITICAL', message))
        self.close()

    def log(self, level: str, message: str):
        """Sending custom level logs"""
        if self._level <= self._LEVELS[level.upper()]:
            self._log(level.upper(), message)

    def log_stats(self, files_name: str | list | tuple):
        """Getting statistics on logs"""
        if type(files_name) is str:
            files_name = (files_name,)
        log_counts = {level: 0 for level in set(self._LEVELS)}
        for file_name in files_name:
            try:
                file_path = os.path.abspath(file_name)
            except FileNotFoundError as e:
                self._log_error(f'FileNotFoundError: {e}', 'ERROR')
                return
            try:
                with open(file_path, 'r', encoding='UTF-8') as file:
                    for line in file:
                        for level in log_counts.keys():
                            if level in line.upper():
                                log_counts[level] += 1
            except FileNotFoundError as e:
                self._log_error(f'FileNotFoundError: {e}', 'ERROR')
                return
        return log_counts

    def export_json(self, export_file: str = 'log_export.json'):
        """Exporting logs to an JSON file"""
        try:
            with open(self._filename, 'r', encoding='UTF-8') as log_file, open(export_file, 'w',
                                                                               encoding='UTF-8') as json_file:
                logs_list = []
                for line in log_file:
                    logs_list.append(line.strip())
                json.dump(logs_list, json_file, ensure_ascii=False, indent=4)
        except FileNotFoundError as e:
            self._log_error(f'FileNotFoundError: {e}', 'ERROR')

    def export_html(self, export_file: str = 'log_export.html'):
        """Exporting logs to an HTML file"""
        try:
            with open(self._filename, 'r', encoding='UTF-8') as log_file, open(export_file, 'w',
                                                                               encoding='UTF-8') as html_file:
                html_file.write('<html><head><title>Logs</title></head><body><pre>\n')
                for line in log_file:
                    html_file.write(line)
                html_file.write('</pre></body></html>')
        except FileNotFoundError as e:
            self._log_error(f'FileNotFoundError: {e}', 'ERROR')

    def rotate_logs(self, max_megabytes_size: float, zip_compression: bool):
        """Log rotation when the maximum size in megabytes is reached"""
        self._rotate_data = {"max_size": max_megabytes_size, "zip": zip_compression}
        try:
            if not os.path.exists(self._filename):
                open(self._filename, 'w').close()
            if os.path.getsize(self._filename) > max_megabytes_size * 1024 * 1024:
                base, extension = os.path.splitext(self._filename)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                new_log_file = f"{base}_{timestamp}{extension}"
                counter = 1
                while os.path.exists(new_log_file):
                    new_log_file = f"{base}_{timestamp}_{counter}{extension}"
                    counter += 1
                os.rename(self._filename, new_log_file)
                if zip_compression:
                    with zipfile.ZipFile(f"{new_log_file}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
                        zipf.write(new_log_file, os.path.basename(new_log_file))
                    os.remove(new_log_file)
        except FileNotFoundError as e:
            self._log_error(f'FileNotFoundError: {e}', 'ERROR')
        except OSError as e:
            self._log_error(f"Unknown OSError: {e}", 'CRITICAL')

    def archive_logs(self, archive_name: str = 'logs_archive.zip'):
        """Archives and delete old logs into a zip file"""
        file_name = self._filename
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_name)
            os.remove(file_name)

    def monitor_log_size(self, max_megabytes_size: float = 8):
        """Checks the size of the logs file and sends a warning"""
        try:
            if os.path.getsize(self._filename) > max_megabytes_size * 1024 * 1024:
                return True
            else:
                return False
        except FileNotFoundError as e:
            self._log_error(f'FileNotFoundError: {e}', 'ERROR')

    def filter_logs(self, level: str):
        """Filter logs by level from log file"""
        filtered_logs = []
        try:
            with open(self._filename, 'r', encoding='UTF-8') as log_file:
                for line in log_file:
                    match = re.search(rf'{level.upper()}', line)
                    if match:
                        filtered_logs.append(line.strip())
        except FileNotFoundError as e:
            self._log_error(f'FileNotFoundError: {e}', 'ERROR')
        return filtered_logs

    def search_logs(self, text: str):
        """Search logs by text from log file"""
        searched_logs = []
        try:
            with open(self._filename, 'r', encoding='UTF-8') as log_file:
                for line in log_file:
                    if text.lower() in line.lower():
                        searched_logs.append(line.strip())
        except FileNotFoundError as e:
            self._log_error(f'FileNotFoundError: {e}', 'ERROR')
        return searched_logs


class ConsoleLogger(Levels):
    """Logging into the console"""
    _COLORS = {
        'standard': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[36m',
        'white': '\033[97m'
    }

    def __init__(self, level: str = 'DEBUG', log_format: str = '[%time] - %lvl | %text', debug_color: str = 'cyan',
                 info_color: str = 'white', warning_color: str = 'yellow', error_color: str = 'red',
                 critical_color: str = 'magenta'):
        super().__init__()
        self._level: int = self._LEVELS[level]
        self._debug_color: str = self._COLORS[debug_color]
        self._info_color: str = self._COLORS[info_color]
        self._warning_color: str = self._COLORS[warning_color]
        self._error_color: str = self._COLORS[error_color]
        self._critical_color: str = self._COLORS[critical_color]
        self._format: str = log_format

    def _format_message(self, level: str, message: str, color: str):
        """Custom format processing"""
        format_map = {
            '%time': f'\033[32m{datetime.datetime.now()}\033[0m',
            '%lvl': f'{color}{level}{self._COLORS['standard']}',
            '%text': message
        }
        formatted_message = self._format
        for key, value in format_map.items():
            formatted_message = formatted_message.replace(key, str(value))
        return formatted_message

    def _log(self, level: str, message: str):
        """Records a message if its level is equal to or higher than the set"""
        if self._LEVELS[level] >= self._level:
            color = getattr(self, f'_{level.lower()}_color')
            formatted_message = self._format_message(level, message, color)
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
        """Sending error level logs with optional exception info"""
        self._log('ERROR', message)

    def critical(self, message: str):
        """Sending critical level logs with optional exception info"""
        self._log('CRITICAL', message)

    def log(self, level: str, message: str, color: str = 'standard'):
        """Sending custom level logs"""
        formatted_message = self._format_message(level, message, self._COLORS[color.lower()])
        print(formatted_message)
        
