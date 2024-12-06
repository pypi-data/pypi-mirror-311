from typing import Optional, Literal
from datetime import datetime
import sys
import os

# Define the path for the current directory
pathin = os.path.dirname(__file__)

# Raise an error if the platform is macOS
if sys.platform == 'darwin':
    raise NotImplementedError("MacOS is not supported")

# Framework metadata
__version__ = '0.0.2'
__author__ = 'Matvei Kostenko'
__license__ = open(os.path.join(pathin, 'LICENSE'), 'r').read()
__copyright__ = '© 2024 Matvei Kostenko. All rights reserved.'
__contributors__ = [
    'Matvei K. : Lead Developer',
    'Nikita M. : ... Developer',
    'Denis  G. : ... Developer',
    'Vasya  K. : Not Developer (Geometry Dasher)',
]

# Environment variables for PyInfinity settings
os.environ['PYINFINITY-IS-INITIALIZED'] = "false"
os.environ['PYINFINITY-LOGGER'] = "false"
os.environ['PYINFINITY-LOGGER-FILE'] = "none"
os.environ['PYINFINITY-AUTO-INSTALL-PACKAGE'] = "true"

# Metadata functions
def getContributors() -> str:
    """Return contributors."""
    return '\n'.join(__contributors__)

def getAuthor() -> str:
    """Return author."""
    return __author__

def getLicense() -> str:
    """Return license."""
    return __license__

def getCopyright() -> str:
    """Return copyright."""
    return __copyright__

def getVersion() -> str:
    """Return version."""
    return __version__

# Framework initialization
def Initialize(
        logs: bool = False,
        logfile: Optional[str] = None,
        autoinstallpackage: bool = True,
) -> None:
    """Initialize the framework."""
    os.environ['PYINFINITY-IS-INITIALIZED'] = "true"
    os.environ['PYINFINITY-LOGGER'] = str(logs).lower() if isinstance(logs, bool) else "false"
    os.environ['PYINFINITY-LOGGER-FILE'] = str(logfile) if isinstance(logfile, str) else "none"
    os.environ['PYINFINITY-AUTO-INSTALL-PACKAGE'] = ("true" if autoinstallpackage else "false") if isinstance(autoinstallpackage, bool) else "false"

def isInitialized() -> bool:
    """Check if the framework is initialized."""
    return os.environ["PYINFINITY-IS-INITIALIZED"] == "true"

def Finalize() -> None:
    """Finalize the framework."""
    os.environ['PYINFINITY-IS-INITIALIZED'] = "false"
    os.environ['PYINFINITY-LOGGER'] = "false"
    os.environ['PYINFINITY-LOGGER-FILE'] = "none"

# Utility functions
def getLocalTime() -> str:
    """Get the current local time."""
    return datetime.now().strftime("%H:%M:%S")

# Logging types
LOGTYPEINFO: Literal[1] = 0x00000001
LOGTYPEWARN: Literal[16] = 0x00000010
LOGTYPEERROR: Literal[256] = 0x00000100

def log(msg: str, 
        time: str = 'local', 
        type: int = LOGTYPEINFO,
        fulltype: bool = False,
        file: str = os.environ['PYINFINITY-LOGGER-FILE'],
        ln: str = 'MAIN') -> None:
    """Framework logger."""
    if time == 'local':
        time = getLocalTime()

    type_label = 'INFO' if type == LOGTYPEINFO else 'WARN' if type == LOGTYPEWARN else 'ERROR'

    if fulltype:
        type_label = 'INFORMATION' if type == LOGTYPEINFO else 'WARNING' if type == LOGTYPEWARN else 'ERROR'

    msg = f"[{time}] [{ln}] [{type_label}]: {msg}"

    if file == "none":
        print(msg)
    else:
        with open(file, 'a') as f:
            f.write(msg + '\n')
        print(msg)

# Pycache management
def deleteAllPycashes(directory: str) -> None:
    """Delete all Python cache files in a directory."""
    pth = os.path.join(
        os.path.dirname(__file__), 
        'DELETE-ALL-PYCASHE!.py'
    )

    lcl = {}
    exec(open(pth, 'r').read(), globals(), lcl)
    lcl['deleteAllCache'](directory)

def deleteAllPycashesInPyInfinity() -> None:
    """Delete all Python cache files in the PyInfinity directory."""
    deleteAllPycashes(os.path.dirname(__file__))

def deleteAllPycashesInPython() -> None:
    """Delete all Python cache files in the Python installation directory."""
    deleteAllPycashes(sys.prefix)

# Credits
def credits() -> str:
    """Return credits information."""
    return open(os.path.join(pathin, 'CREDITS'), 'r').read()

prefixlen = len(os.path.abspath(sys.prefix))

for arg in sys.argv:
    arg=os.path.abspath(arg)
    if sys.prefix.upper()==arg[:prefixlen].upper():
        if'site-packages'in arg or'Lib'in arg:
            parts=arg.split(os.sep)
            if'site-packages'in parts:idx=parts.index('site-packages')
            elif'Lib'in parts:idx=parts.index('Lib')
            modulename=parts[idx+1]
            if modulename!='PyInfinity':
                print('\033[35m'+f'Welcome to the module "{modulename}" using PyInfinity'+'\033[0m')

__all__ = [
    'getContributors',
    'getAuthor',
    'getLicense',
    'getCopyright',
    'getVersion',
    'Initialize',
    'isInitialized',
    'Finalize',
    'getLocalTime',
    'log',
    'LOGTYPEINFO',
    'LOGTYPEWARN',
    'LOGTYPEERROR',
    'deleteAllPycashes',
    'deleteAllPycashesInPyInfinity',
    'deleteAllPycashesInPython',
    'credits'
]