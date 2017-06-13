#!C:\Projects\PyMud\PyMudInterpreter\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'nose2==0.5.0','console_scripts','nose2'
__requires__ = 'nose2==0.5.0'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('nose2==0.5.0', 'console_scripts', 'nose2')()
    )
