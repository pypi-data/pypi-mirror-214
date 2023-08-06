import functools
import types
import typing

from .__type import Provider
from .chatgpt3 import ChatGPT3Provider

DEFAULT_PROVIDER = ChatGPT3Provider()


class Magicfunc:
    def __init__(self, _globals): self.__dict__ = _globals

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            def proxy(*args, **kwargs):
                return magic(item, DEFAULT_PROVIDER, *args, **kwargs)(*args, **kwargs)

            return proxy


def magic(func: typing.Union[typing.Callable, str, None] = None, provider: Provider = DEFAULT_PROVIDER, module: types.ModuleType = None, *args, **kwargs):
    if module is not None:
        return functools.wraps(func)(lambda func: getattr(module, func.__name__))
    elif func is None:
        return provider.magic
    elif isinstance(func, str):
        return provider.guess(func, *args, **kwargs)
    else:
        return provider.magic(func)
