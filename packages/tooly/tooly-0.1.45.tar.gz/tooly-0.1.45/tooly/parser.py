import argparse, argcomplete

# argcomplete的安装方法：
# 1. pip install argcomplete
# 2. 配置全局的自动帮助信息：activate-global-python-argcomplete
# 3. 确认脚本的前1024字节中有PYTHON_ARGCOMPLETE_OK
# 4. .bashrc中增加如下行：
# . /etc/bash_completion.d/python-argcomplete
__tasks__ = {}

from tooly.sh import CustomHelpFormatter


class ArgumentParser(argparse.ArgumentParser):
    def parse_args(self, defineTask=False, defaultTask=None, formatter_class=CustomHelpFormatter):
        if defineTask or defaultTask:
            self.add_argument("task", choices=__tasks__.keys(), default=defaultTask)
        argcomplete.autocomplete(self)
        return super().parse_args()


def register_action(*otherNames):
    """
    默认以函数名为key，写入__tasks__的map中（key为函数名，value为函数对应的函数列表）
    @param otherNames: 其他的函数名
    """
    if otherNames and callable(otherNames[0]):  # 判断是否有额外参数传递进来
        # 当作无参数装饰器处理
        func = otherNames[0]
        __tasks__[func.__name__] = [func]

        def decorator(*args, **kwargs):
            return func(*args, **kwargs)

        return decorator
    else:
        # 当作带参数装饰器处理，维持原来的逻辑
        class _Action:
            def __init__(self, func):
                self.fun = func
                for k in [func.__name__, *otherNames]:
                    if k not in __tasks__:
                        __tasks__[k] = []
                    __tasks__[k].append(self.fun)

            def __call__(self, *args, **kwds):
                return self.fun(*args, **kwds)

        return _Action


def runTasks(taskName: str):
    for i in __tasks__[taskName]:
        i()
