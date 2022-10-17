import os
import logging
import settings
from logging.handlers import TimedRotatingFileHandler

'''
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
'''

class LogHandler(logging.Logger):

    def __init__(self, name, stream=True, file=True):
        self.name = name
        #self.level = configure.ConfigParser.getInstance().getInt('log', 'level')
        self.level = 20
        logging.Logger.__init__(self, self.name, self.level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        file_name = os.path.join(settings.LOG_PATH, '{name}.log'.format(name=self.name))
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def resetName(self, name):
        self.name = name
        self.removeHandler(self.file_handler)
        self.__setFileHandler__()

logger = LogHandler(name='lc_notify', stream=False, file=True)

if __name__ == '__main__':
    #log = LogHandler(name='messagequeue', stream=False, file=True)
    log = logger 
    log.info('this is a test msg')
    log.debug('this is a loggging debug message')
    log.warning('this is loggging a warning message')
    log.error('this is an loggging error message')
    log.critical('this is a loggging critical message')
