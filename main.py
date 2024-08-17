import check_python
def in_venv():
    return sys.prefix != sys.base_prefix
if not in_venv():
    print('Not in venv')
    print('\n\nrun INSTALL.bat, then START.bat')
    sys.exit()
import importlib.util
if importlib.util.find_spec('loguru') is None:
    print('missing module loguru')
    print('\n\nrun INSTALL.bat first')
    sys.exit()
import asyncio
from contextlib import suppress

from bot.utils.launcher import process


async def main():
    await process()


if __name__ == '__main__':
    with suppress(KeyboardInterrupt, RuntimeError, RuntimeWarning):
        asyncio.run(main())
