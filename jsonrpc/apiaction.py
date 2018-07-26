#! /usr/bin/env python
#  encoding: utf-8


from jsonrpc import AutoLoad
import json
import requests

def api_action(method="", params={}):
    try:
        module, func = method.split('.')
    except ValueError,e:
        print "method传值有误：{}".format(method)
        print e.message
        return False

    at=AutoLoad()
    if not at.isVaildModule(module):
        print "{} 模块不可用".format(module)
        return False
    if not at.isVaildMethod(func):
        print "{} 函数不可用".format(func)
        return False
    try:
        called = at.getCallMethod()
        if callable(called):
            return called(**params)
        else:
            print "函数不能被调用{}.{}".format(module, func)
            return False
    except Exception,e
        print "调用模块执行中出错：{}".format(e.message)

def url_api_action(method="", params={}):
    url = "http://127.0.0.1:8000/api"
    c = {
        "jsonrpc": "2.0",
        "id": "1",
        "method":method,
        "auth": "",
        "params": params
    }
    r = requests.post(url, headers=header, data=json.dumps(params))


