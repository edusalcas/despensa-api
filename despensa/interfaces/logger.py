import os
import datetime
import definitions as d

LOG_API_REST = 'api_rest.log'

class Logger:
    def __init__(self, log_file: str):
        # Crea el directorio de logs si no existe
        if not os.path.exists(d.LOGS_DIR):
            os.makedirs(d.LOGS_DIR)
        
        self.log_file_path = os.path.join(d.LOGS_DIR, log_file)

    def _write_log(self, level, message):
        # Obtiene la fecha y hora actual
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Formatea el mensaje del log
        log_message = f"[{current_time}] [{level}] {message}\n"
        
        # Escribe el mensaje en el archivo de logs
        with open(self.log_file_path, 'a') as file:
            file.write(log_message)

    def info(self, message):
        self._write_log('INFO', message)

    def warning(self, message):
        self._write_log('WARNING', message)

    def error(self, message):
        self._write_log('ERROR', message)