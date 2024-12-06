import os

from .. import sys

TEMP_DIR = 'C:\\Temp' if sys.is_this_windows() else \
           '/tmp'

def get_user_env(name  :str,
                 expand:bool=False):
    
    return (os.popen(f'powershell -NoProfile -Command "(Get-Item -Path HKCU:\\Environment).GetValue(\'{name}\')"')                                         if expand else \
            os.popen(f'powershell -NoProfile -Command "(Get-Item -Path HKCU:\\Environment).GetValue(\'{name}\', $null, \'DoNotExpandEnvironmentNames\')"')).read()
