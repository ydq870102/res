#! /usr/bin/env python
#  encoding: utf-8
import os
import imp



class AutoLoad(object):
    """
        动态加载模块,返回函数对象
    """

    def __init__(self):
        """
            初始化模块路径、模块名称、函数名称、模块对象
        """
        self.module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules"))
        self.module_name = ""
        self.method_name = ""
        self.module = None

    def isVaildModule(self, module_name):
        """
        判断是否为有效模块
        :param module_name: 模块名称
        :return: True/False
        """
        self.module_name = module_name
        return self._load_module()

    def isVaildMethod(self, method_name):
        """
        判断是否为有效函数
        :param method_name: 函数名称
        :return: True/False
        """
        self.method_name = method_name
        if self.module is None:
            return False
        return hasattr(self.module, self.method_name)

    def getCallMethod(self):
        """
        获取函数对象
        :return: 函数对象
        """
        if hasattr(self.module, self.method_name):
            return getattr(self.module, self.method_name)
        return None

    def _load_module(self):
        """
        动态加载模块
        :return: True/False
        """
        ret = False
        for module_file in os.listdir(self.module_dir):
            if module_file.endswith(".py"):
                module_name = module_file.rstrip(".py")
                if module_name != self.module_name:
                    continue
                fp, path, desc = imp.find_module(module_name, [self.module_dir])
                if not fp:
                    continue
                try:
                    self.module = imp.load_module(module_name, fp, path, desc)
                    ret = True
                except Exception:
                    pass
                finally:
                    fp.close()
                break
        return ret


class JsonRPC(object):

    def __init__(self):
        self.jsonData = None
        self.VERSION = "2.0"
        self._response = {}

    def execute(self):
        if self.jsonData.get("id",None) is None:
            self.jsonError("-1", "102", "id 没有传")
            return self._response
        if self.vaildate():
            params = self.jsonData["params"]
            auth = self.jsonData["auth"]
            module, method = self.jsonData["method"].split(".")
            ret = self.callMethod(module, method, auth, params)
            self.processResult(ret)
        return self._response

    def vaildate(self):
        if self.jsonData is None:
            self.jsonError(self.jsonData["id"], "101", "json 数据为空")
            return False
        for opt in ["jsonrpc",  "method", "params", "auth",]:
            if not self.jsonData.has_key(opt):
                self.jsonError(self.jsonData["id"], "102", "{} 没有传".format(opt))
        if str(self.jsonData["jsonrpc"]) != "2.0":
            self.jsonError(self.jsonData["id"], "103", "jsonrpc版本不正确")
        action = self.jsonData["method"].split('.')
        if len(action) != 2:
            self.jsonError(self.jsonData["id"], "104", "method 错误")
        if not str(self.jsonData["id"]).isdigit():
            self.jsonError(self.jsonData["id"], "105", "ID 必须为数字")
        if not isinstance(self.jsonData["params"],dict):
            self.jsonError(self.jsonData["id"], "106", "params 必须为字典")
        return True

    def jsonError(self, id, errno, errmsg):
        self._response = {
            "jsonrpc": self.VERSION,
            "id": id,
            "error_code": errno,
            "errmsg": errmsg
        }

    def requireAuth(self, module_name, method_name):
        white_list = ["user.login", "host.get"]
        if "{}.{}".format(module_name, method_name) in white_list:
            return False
        return True

    def callMethod(self, module, method, auth, params):

        module_name = module.lower()
        method_name = method.lower()

        response = Response()
        at = AutoLoad()

        if not at.isVaildModule(module_name):
            response.errorCode = 107
            response.errorMessage = "模块不存在"
            return response
        if not at.isVaildMethod(method_name):
            response.errorCode = 108
            response.errorMessage = "{}下函数{}不存在".format(method_name,method_name)
            return response
        if self.requireAuth(module_name, method_name):
            if auth is None:
                response.errorCode = 109
                response.errorMessage = "该操作需要提供auth"
                return response
        try:
            called = at.getCallMethod()
            if callable(called):
                response.data = called()
            else:
                response.errorCode = 109
                response.errorMessage = "模块{}下函数{}执行错误".format(method_name, method_name)
        except Exception,e:
                response.errorCode = -1
                response.errorMessage = e.message
        return response


    def processResult(self,response):

        if response.errorCode != 0:
            self.jsonError(self.jsonData["id"],
                           response.errorCode,
                           response.errorMessage)
        else:
            self._response = {
                "jsonrpc": self.VERSION,
                "id": self.jsonData["id"],
                "result": response.data
            }


class Response(object):

    def __init__(self):
        self.data = None
        self.errorCode = 0
        self.errorMessage = None


if __name__ == "__main__":
    js = JsonRPC()
    js.jsonData ={"jsonrpc": "2.0", "id": "1", "method": "host.get", "auth": "", "params": {}}
    print js.execute()
