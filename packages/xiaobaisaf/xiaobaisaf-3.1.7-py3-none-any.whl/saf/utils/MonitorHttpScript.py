#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2024/8/18 23:28
@File  : MonitorHTTP.py
'''

from mitmproxy import flow
from collections.abc import Iterable

def modify(data: bytes) -> bytes | Iterable[bytes]:
    # if flow.request.url.startswith("https://etax.chinatax.gov.cn/"):
    return b'{"code": 200, "msg": "ok"}'
    # else:
        # return data

def responseheaders(flow):
    flow.response.stream = modify
