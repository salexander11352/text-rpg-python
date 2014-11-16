'''
Partial binding to the Win32 API. Just implements the functions needed.
'''
import ctypes as ct
from console.bindhelper import bind_function
# This is stuff required to access the Windows API within python
# You should mostly be able to ignore it.
# This will only be ran on windows.

# Names of the dll's that contain the various functions we need.
user32 = "user32"
kernel32 = 'kernel32'

# Windows API type information
INT = ct.c_int
BOOL = INT
ULONG = ct.c_ulong
SHORT = ct.c_short
WORD = ct.c_ushort
DWORD = ct.c_ulong
PVOID = LPVOID = ct.c_void_p
HANDLE = PVOID
COLORREF = DWORD
LPWORD = ct.POINTER(WORD)
LPDWORD = ct.POINTER(DWORD)

LPCOLORREF = ct.POINTER(COLORREF)


# Reimplementation of macros
def RGB(r, g, b):
    return r | g << 8 | b << 16


# Windows API structures
class COORD(ct.Structure):
    _fields_ = [('X', SHORT),
                ('Y', SHORT)]


class SMALL_RECT(ct.Structure):
    _fields_ = [('Left', SHORT),
                ('Top', SHORT),
                ('Right', SHORT),
                ('Bottom', SHORT)]


class CONSOLE_SCREEN_BUFFER_INFO(ct.Structure):
    _fields_ = [('dwSize', COORD),
                ('dwCursorPosition', COORD),
                ('wAttributes', WORD),
                ('srWindow', SMALL_RECT)]
PCONSOLE_SCREEN_BUFFER_INFO = ct.POINTER(CONSOLE_SCREEN_BUFFER_INFO)


class CONSOLE_SCREEN_BUFFER_INFOEX(ct.Structure):
    _fields_ = [('cbSize', ULONG),
                ('dwSize', COORD),
                ('dwCursorPosition', COORD),
                ('wAttributes', WORD),
                ('srWindow', SMALL_RECT),
                ('dwMaximumWindowSize', COORD),
                ('wPopupAttributes', WORD),
                ('bFullscreenSupported', BOOL),
                ('ColorTable', COLORREF * 16)]
PCONSOLE_SCREEN_BUFFER_INFOEX = ct.POINTER(CONSOLE_SCREEN_BUFFER_INFOEX)


class CONSOLE_CURSOR_INFO(ct.Structure):
    _fields_ = [('dwSize', DWORD),
                ('bVisible', BOOL)]
PCONSOLE_CURSOR_INFO = ct.POINTER(CONSOLE_CURSOR_INFO)

# Enum Values
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLUE = 0x0001
FOREGROUND_GREEN = 0x0002
FOREGROUND_RED = 0x0004
FOREGROUND_INTENSITY = 0x0008
BACKGROUND_BLUE = 0x0010
BACKGROUND_GREEN = 0x0020
BACKGROUND_RED = 0x0040
BACKGROUND_INTENSITY = 0x0080
COMMON_LVB_LEADING_BYTE = 0x0100
COMMON_LVB_TRAILING_BYTE = 0x0200
COMMON_LVB_GRID_HORIZONTAL = 0x0400
COMMON_LVB_GRID_LVERTICAL = 0x0800
COMMON_LVB_GRID_RVERTICAL = 0x1000
COMMON_LVB_REVERSE_VIDEO = 0x4000
COMMON_LVB_UNDERSCORE = 0x8000

GetStdHandle = bind_function(kernel32, 'GetStdHandle', HANDLE, (DWORD,))

GetConsoleScreenBufferInfo = bind_function(
    kernel32,
    'GetConsoleScreenBufferInfo',
    BOOL,
    (HANDLE, PCONSOLE_SCREEN_BUFFER_INFO, ))

GetConsoleScreenBufferInfoEx = bind_function(
    kernel32,
    'GetConsoleScreenBufferInfoEx',
    BOOL,
    (HANDLE, PCONSOLE_SCREEN_BUFFER_INFOEX))

SetConsoleScreenBufferInfoEx = bind_function(
    kernel32,
    'SetConsoleScreenBufferInfoEx',
    BOOL,
    (HANDLE, PCONSOLE_SCREEN_BUFFER_INFOEX))

SetConsoleTextAttribute = bind_function(
    kernel32,
    'SetConsoleTextAttribute',
    BOOL,
    (HANDLE, WORD))

GetConsoleCursorInfo = bind_function(
    kernel32,
    'GetConsoleCursorInfo',
    BOOL,
    (HANDLE, PCONSOLE_CURSOR_INFO))

SetConsoleCursorPosition = bind_function(
    kernel32,
    'SetConsoleCursorPosition',
    BOOL,
    (HANDLE, COORD))

ReadConsoleOutputAttribute = bind_function(
    kernel32,
    'ReadConsoleOutputAttribute',
    BOOL,
    (HANDLE, LPWORD, DWORD, COORD, LPDWORD)
)

SetConsoleCursorPosition = bind_function(
    kernel32,
    'SetConsoleCursorPosition',
    BOOL,
    (HANDLE, COORD))
