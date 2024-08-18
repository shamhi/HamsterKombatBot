import sys
if sys.version_info.major != 3 or sys.version_info.minor < 10 or sys.version_info > 11:
    print('Python version not supported:', sys.version)
    print('\n\nInstall Python 3.11: https://www.python.org/downloads/')
    sys.exit(1)
