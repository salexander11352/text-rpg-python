''' Helps ease compatibility issues between python 2 and 3 '''
import sys

PYTHON_3 = sys.version_info.major == 3

if PYTHON_3:
    range = range
    unicode = str
    input = input
else:
    range = xrange
    unicode = unicode
    input = raw_input

__all__ = ['PYTHON_3', 'range', 'unicode', 'input']
