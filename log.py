from datetime import datetime
import inspect
from pathlib import Path
import os


class Log:

    def __init__(self, *args, **kwargs):
        self.write = False
        self.path = Path(__file__).parent / f'log/{inspect.getmodulename(__file__)}.log'

    def add(self, path=""):
        self.write = True
        if path:
            if "." in str(path):
                self.path = path
            else:
                self.path = f'{path}/{inspect.getmodulename(__file__)}.log'
        if not os.path.exists(path):
            if "." not in str(path):
                path.mkdir(parents=True)

    def log(self, code, args):
        code_dict = {
            30: "HIDE",
            31: "ERROR",
            32: "SUCCESS",
            33: "WARNING",
            34: "DEBUG",
            35: "TIP",
            38: "INFO",
            41: "CRITICAL",
        }
        data = {
            "time": str(datetime.now()),  # 当前时间
            "code": str(code),  # 代码
            "type": code_dict[code],  # 类型
            "file": inspect.getmodulename(__file__),  # 文件名
            "line": str(inspect.stack()[2].lineno),  # 代码行
            "text": " ".join([str(a) for a in args]),  # 内容
        }
        out = f'\x1b[{32}m{data["time"]} \x1b[0m \x1b[{code}m{data["type"]} \x1b[0m \x1b[{36}m{data["file"]} {data["line"]} \x1b[0m \x1b[{code}m{data["text"]}\x1b[0m'
        print(out)
        if self.write:
            print(self.path)
            with open(self.path, 'a') as f:
                f.write(" ".join(data.values()))
        return data

    def hide(self, *args):
        return self.log(30, args)

    def err(self, *args):
        return self.log(31, args)

    def success(self, *args):
        return self.log(32, args)

    def waring(self, *args):
        return self.log(33, args)

    def debug(self, *args):
        return self.log(34, args)

    def tip(self, *args):
        return self.log(35, args)

    def info(self, *args):
        return self.log(38, args)

    def critical(self, *args):
        return self.log(41, args)


if __name__ == '__main__':
    log = Log()
    path = Path(__file__).parent / '.test/test.log'
    log.add(path=path)
    info = log.info("Hello world!")
