import psutil
import os
from .utils import mebibyte
process = psutil.Process(os.getpid())

DEFAULTTHRESHOLD = 100 * 1024 ** 2

MINTHRESHOLD = int(process.memory_info().rss) + mebibyte(1)