#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/20 0:59
fileName    : ENV.py
'''

import os
from typing import Any

from dotenv import load_dotenv
from .. import ENV_PATH

class ENV(object):
    ''' 持久性环境变量 '''
    def __init__(self):
        pass

    @classmethod
    def load(cls, path: str = ENV_PATH):
        try:
            load_dotenv(dotenv_path=path)
        except Exception as e:
            # 创建文件
            with open(path, 'w', encoding='utf-8') as f:
                f.write('')
                f.close()

    @classmethod
    def set_env(cls, key: str, value: Any):
        ''' 设置环境变量 '''
        os.environ[key] = value

    @classmethod
    def get_env(cls, key: str):
        ''' 获取环境变量 '''
        return os.environ.get(key)