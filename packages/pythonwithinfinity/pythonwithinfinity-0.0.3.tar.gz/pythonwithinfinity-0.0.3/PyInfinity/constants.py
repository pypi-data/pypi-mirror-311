import os

# Define the absolute path of the current directory
PYINFINITYPATH = os.path.abspath(os.path.dirname(__file__))

class __C:
    """Constants that mimic standard limits for various data types."""
    ULLONGMAX = 0xffffffffffffffff  # 18446744073709551615
    LLONGMAX = 9223372036854775807
    LLONGMIN = -LLONGMAX - 1
    ULONGMAX = 0xffffffff  # 4294967295
    LONGMAX = 2147483647
    LONGMIN = -LONGMAX - 1
    UINTMAX = ULONGMAX
    INTMAX = LONGMAX
    INTMIN = LONGMIN
    USHRTMAX = 0xffff  # 65535
    SHRTMAX = 32767
    SHRTMIN = -SHRTMAX - 1
    MBLENMAX = 5
    CHARMAX = -127
    CHARMAXWITHJ = 255
    CHARMIN = -CHARMAX - 1
    CHARMINWITHJ = -CHARMAXWITHJ - 1
    SCHARMAX = CHARMAX
    SCHARMIN = CHARMIN
    CHARBIT = 8

# Instance of constants
C = __C()

class NULL(object):
    """Represents a NULL object."""
    def __repr__(self) -> str:
        return 'NULL'

__all__ = [
    'C', 'PYINFINITYPATH', 'NULL'
]