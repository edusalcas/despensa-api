import os
import datetime
import definitions as d
from environment import Environment, TEST


LOG_API_REST = 'api_rest.log'

class Logger:
    def __init__(self, log_file: str):
        if Environment().get_current_env() != TEST:
            # Crea el directorio de logs si no existe
            if not os.path.exists(d.LOGS_DIR):
                os.makedirs(d.LOGS_DIR)
            
            self.log_file_path = os.path.join(d.LOGS_DIR, log_file)

    def _write_log(self, level, message):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{current_time}] [{level}] {message}\n"
        
        if Environment().get_current_env() != TEST:
            self._write_log_file(log_message)
        else:
            self._write_log_console(log_message)
       
    def _write_log_file(self, message):
        with open(self.log_file_path, 'a') as file:
            file.write(message)

    def _write_log_console(self, message):
        print(message)

    def info(self, message):
        self._write_log('INFO', message)

    def warning(self, message):
        self._write_log('WARNING', message)

    def error(self, message):
        self._write_log('ERROR', message)