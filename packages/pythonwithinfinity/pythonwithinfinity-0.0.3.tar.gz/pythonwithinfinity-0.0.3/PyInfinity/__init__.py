"""Framework PyInfinity.
Megagolab, 2024.
pip3 install ..."""

from PyInfinity.init import (
    __version__, __author__,                     # constants
    __license__, __copyright__,                  # constants
    __contributors__,                            # constants

    Initialize, isInitialized, Finalize,         # initialization and finalization framework
    
    getAuthor, getVersion,                       # getters
    getLicense, getCopyright, getContributors,   # getters
    getLocalTime, credits,                       # getters

    log, LOGTYPEERROR, LOGTYPEINFO, LOGTYPEWARN, # logs

    deleteAllPycashes,                           # cache
    deleteAllPycashesInPyInfinity,               # cache
    deleteAllPycashesInPython,                   # cache

    __all__ as __init_all__
)

from PyInfinity.option import Option
from PyInfinity.constants import (
    C, PYINFINITYPATH, NULL,

    __all__ as __constants_all__
)

from PyInfinity.randoms import (
    rand,
    choiseObjectInList,
    choiseObjectInTuple,
    randList,
    random,

    __all__ as __randoms_all__
)

from PyInfinity.getpip import main as installPip

__all__ = []

for obj in __init_all__:
    __all__.append(obj)

for obj in __constants_all__:
    __all__.append(obj)

for obj in __randoms_all__:
    __all__.append(obj)

__all__.append('Option')
__all__.append('printAllDataOfPyInfinity')
__all__.append('installPip')
__all__.append('updatePyInfinity')

del obj

__all__ = sorted(__all__)

def updatePyInfinity() -> None:
    """Update PyInfinity."""
    print('\033[1m'+'\033[31m'+'Update PyInfinity...'+'\033[0m')

    try:
        import pip
    except (ImportError, ModuleNotFoundError):
        installPip()
        import pip

    pip.main(['install', '--upgrade', 'pythonwithinfinity', '--quiet'])

def printAllDataOfPyInfinity() -> None:
    contributors = getContributors()
    
    print('\033[1m', end='')  # Bold text
    print('\033[31m', end='')  # Red color
    print('This message printed at ' + getLocalTime())  # Current time output
    print('All Data Of PyInfinity\n')
    print('\033[37m', end='')  # White color
    print('-' * 100)
    
    # Outputting __all__ in stylized form
    print('\033[33m', end='')  # Yellow color
    print('All: ' + repr(__all__).replace(', ', ',\n' + ' ' * 6) + '\n')
    print('\033[37m', end='')  # White color
    
    # Derivation of the number of functions
    print('\033[35m', end='')  # Magenta color
    print(f'Functions: {len(__all__)}')
    print('\033[37m', end='')  # White color
    print('-' * 100)
    
    # Output of additional metadata
    print('\033[31m', end='')  # Red color
    print(f'Version: {getVersion()}')
    print(f'Author: {getAuthor()}')
    print('\033[35m', end='')  # Magenta color
    print(f'License:\n{getLicense()}')
    print('\033[31m', end='')  # Red color
    print(f'Copyright: {getCopyright()}')
    
    # Output of the list of contributors
    print('Contributors:')
    for index, contributor in enumerate(contributors.split('\n')):
        indent = ' ' * (14 if index > 0 else 0)  # Retreat after the first participant
        print(f"{indent}{contributor}")
    
    print('-' * 100)
    print('Credits\n')
    print(credits())

    print('\033[37m', end='')  # White color
    print('-' * 100)
    print('\033[0m', end='')  # Reset styles

if __name__ == '__main__':
    printAllDataOfPyInfinity()