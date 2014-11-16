import platform
import ctypes as ct
from ctypes.util import find_library


def bind_function(libName, name, returnType, params):
    '''Helper function that allows usage of C functions in dynamic libraries'''

    osName = platform.system()

    if osName == "Windows":
        function = ct.WINFUNCTYPE(returnType, *params)
        lib = ct.WinDLL(libName)
    elif osName == "Darwin" or osName == "Linux":
        function = ct.CFUNCTYPE(returnType, *params)
        lib = ct.CDLL(find_library(libName))

    address = getattr(lib, name)
    new_func = ct.cast(address, function)

    return new_func
