from .logger import logger
from . import tg_channel_check
from . import tg_web_data
from . import launcher
from . import scripts
from . import default
from . import json_db
from . import proxy


import os

if not os.path.exists(path='sessions'):
    os.mkdir(path='sessions')
