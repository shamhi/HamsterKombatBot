from os.path import exists
from shutil import copy2
import asyncio
from contextlib import suppress

from bot.utils.launcher import process


async def main():
    await process()


if __name__ == '__main__':
    if not exists('sessions/profiles.json'):
        copy2('profiles.json', 'sessions/')
    
    with suppress(KeyboardInterrupt, RuntimeError, RuntimeWarning):
        asyncio.run(main())
