import logging

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.setup_logger()
        return cls._instance

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)
        
    def error(self, message):
        self.logger.error(message)
        