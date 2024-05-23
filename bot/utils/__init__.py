from .logger import logger
from . import launcher


import os

if not os.path.exists(path='sessions'):
    os.mkdir(path='sessions')
