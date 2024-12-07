import logging
import os
from logging.handlers import TimedRotatingFileHandler


class Logger:
    _instances = {}
    LOG_LEVELS = {
        'w': logging.WARNING,
        'i': logging.INFO,
        'd': logging.DEBUG
    }

    def __new__(cls, logger_name, *args, **kwargs):
        if logger_name not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[logger_name] = instance
        return cls._instances[logger_name]

    def __init__(self, logger_name, type_log, when='D', interval=45, backup_count=0, log_directory="logs"):
        if hasattr(self, 'initialized') and self.initialized:
            return
        self.logger_name = logger_name
        self.type_log = type_log
        self.when = when
        self.interval = interval
        self.backup_count = backup_count
        self.log_directory = log_directory

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.LOG_LEVELS[self.type_log])

        # Проверка существования обработчика, чтобы избежать дублирования
        if not self.logger.handlers:
            log_path = os.path.join(self.log_directory, f'{self.logger_name}.log')
            handler = TimedRotatingFileHandler(log_path,
                                               when=self.when,
                                               interval=self.interval,
                                               backupCount=self.backup_count)
            handler.setLevel(self.LOG_LEVELS[self.type_log])
            formatter = logging.Formatter('%(levelname)s %(name)s %(asctime)s %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.initialized = True

    def __setattr__(self, name, value):
        if name == "type_log" and value not in self.LOG_LEVELS:
            raise ValueError(f"Invalid type_log provided: {value}. Valid options: {', '.join(self.LOG_LEVELS.keys())}")
        super().__setattr__(name, value)