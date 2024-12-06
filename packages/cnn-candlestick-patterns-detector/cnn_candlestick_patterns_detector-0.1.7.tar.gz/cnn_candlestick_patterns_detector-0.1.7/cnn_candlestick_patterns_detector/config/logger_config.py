import logging
import os
from logging.handlers import TimedRotatingFileHandler

class LoggerConfig:
    @staticmethod
    def set_up_folder(folder):
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

    @staticmethod
    def get_logger(model_id):
        log_dir = 'out/logs'
        LoggerConfig.set_up_folder(log_dir)
        log_file_path = os.path.join(log_dir, f'cnn_{model_id}.log')

        logger = logging.getLogger(model_id)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
            handler.suffix = "%Y-%m-%d"
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger
