#! /usr/bin/env python
# encoding: utf-8
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


if __name__ == "__main__":

    at = AutoLoad()
    print at.isVaildModule("host")
    print at.isVaildMethod("get")
    func = at.getCallMethod()
    print func()