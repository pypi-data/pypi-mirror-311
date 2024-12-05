#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/23 22:30
fileName    : LOG.py
'''
import os, sys
from datetime import datetime
from ..config.log_config import file_name
from .. import LOG_DIR_PATH

class Logger(object):
    def __init__(self):
        self.logfile = os.path.join(LOG_DIR_PATH, file_name)

    def logging(self, message, level, stream=sys.stdout):
        if level.lower() in ['debug', 'info', 'warning', 'error']:
            log = [
                f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]',
                ' - ',
                f'[{level.upper()}]',
                ' - ',
                f'{message}',
                f'\n'
            ]
            log_content =  ''.join(log)
            if os.path.isfile(self.logfile):
                with open(self.logfile, 'a') as f:
                    f.write(log_content + '\n')
                    f.close()
            stream.write(log_content)
        else:
            raise ValueError(f"无效的日志level: {level}, 有效level范围是：'debug', 'info', 'warning', 'error'")

    def info(self, message: str = ''):
        self.logging(message, level='INFO')

    def error(self, message: str = ''):
        self.logging(message, level='ERROR', stream=sys.stderr)

    def warning(self, message: str = ''):
        self.logging(message, level='WARNING')

    def debug(self, message: str = ''):
        self.logging(message, level='DEBUG',)
