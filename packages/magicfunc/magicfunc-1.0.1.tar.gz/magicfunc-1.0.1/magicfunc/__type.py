import functools
import hashlib
import inspect
import pathlib
import re
import types
import typing


class Provider:
    def magic(self, func: typing.Callable) -> typing.Callable: raise NotImplementedError()

    def guess(self, name: str, *args, **kwargs): raise NotImplementedError()


class GenerateProvider(Provider):
    def magic(self, func: typing.Callable) -> typing.Callable:
        define = inspect.getsource(func)
        return self.make(func.__name__, func, define)

    def guess(self, name: str, *args, **kwargs):
        define = name + str(args)[:-1] + ",".join([k + "_" + f"'{v}'" if isinstance(v, str) else v for k, v in kwargs.items()]) + ')'
        return self.make(name, None, define)

    def make(self, name: str, func: typing.Callable, define: str):
        hid = f'{name}_{hashlib.md5(define.encode()).hexdigest()}.py'
        if pathlib.Path(hid).exists():
            with open(hid, 'r') as file: source = file.read()
        else:
            source = self.generate(func, re.sub(r'@magicfunc.magic.*\n', r'\n', define))
            with open(hid, 'w') as file: file.write(source)
        module = types.ModuleType(hid)
        exec(source, module.__dict__)

        @functools.wraps(func)
        def decorated(*args, **kwargs):
            return getattr(module, name)(*args, **kwargs)

        return decorated

    def generate(self, func: typing.Callable, define: str) -> str: raise NotImplementedError()
