import logging
import os
from datetime import datetime

class PoplarLogger:
    def __init__(self):
        self.log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(self.log_directory, exist_ok=True)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)

        log_file = os.path.join(self.log_directory, f'{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.log')

        self.file_handler = logging.FileHandler(filename=log_file)  # Store file handler as instance variable
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)

    def save(self):
        self.file_handler.flush()
        self.file_handler.close()  # Close the file handler after flushing
