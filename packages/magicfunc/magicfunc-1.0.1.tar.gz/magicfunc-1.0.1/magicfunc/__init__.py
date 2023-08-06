import sys

from .__core import Magicfunc, magic
from .chatgpt3 import ChatGPT3Provider

sys.modules[__name__] = Magicfunc(globals())
