import os
import ctypes as ct
import msvcrt
import console.win32 as w32

# POTENTIAL FEATURES LIST:
# Use WriteConsoleOutput to render larger portions of the screen. - side by side rendering
# WriteConsoleOutputAttribute - Change color of previous characters.
# Look into adding rgb colors into the library using SetConsoleScreenBufferInfoEx
#   This would not get us more colors at once, but would let us redefine the 16 colors available.
# Look into using FillConsoleOutputCharacter to print the lines of single chars used for headers.
#   Should be faster.


_BLUE = 0x0001
_GREEN = 0x0002
_RED = 0x0004
_INTENSITY = 0x0008

darkblue = _BLUE
darkgreen = _GREEN
darkcyan = _GREEN | _BLUE
darkred = _RED
darkmagenta = _RED | _BLUE
darkyellow = _RED | _GREEN
grey = _RED | _GREEN | _BLUE

black = 0
darkgrey = _INTENSITY

blue = _INTENSITY | _BLUE
green = _INTENSITY | _GREEN
cyan = _INTENSITY | _GREEN | _BLUE
red = _INTENSITY | _RED
magenta = _INTENSITY | _RED | _BLUE
yellow = _INTENSITY | _RED | _GREEN
white = _INTENSITY | _RED | _GREEN | _BLUE


def _get_console_size():
    '''Get the console size on windows using the Windows API'''
    stdHandle = w32.GetStdHandle(w32.STD_OUTPUT_HANDLE)
    csbi = w32.CONSOLE_SCREEN_BUFFER_INFO()
    result = w32.GetConsoleScreenBufferInfo(stdHandle, ct.byref(csbi))

    if result:
        rect = csbi.srWindow
        left = rect.Left
        right = rect.Right
        top = rect.Top
        bottom = rect.Bottom

        width = right - left
        height = bottom - top
    else:
        # Assume size is 80x24
        width, height = 80, 24

    return (width, height)


def _get_default_size():
    '''
    Get the size of the window before we tinker with it.
    Mainly to restore it later.
    '''
    stdHandle = w32.GetStdHandle(w32.STD_OUTPUT_HANDLE)
    csbiex = w32.CONSOLE_SCREEN_BUFFER_INFOEX()
    w32.GetConsoleScreenBufferInfoEx(stdHandle, ct.byref(csbiex))
    return csbiex


def _set_console_size(x, y):
    stdHandle = w32.GetStdHandle(w32.STD_OUTPUT_HANDLE)
    conInfo = w32.CONSOLE_SCREEN_BUFFER_INFOEX()
    conInfo.cbSize = ct.sizeof(conInfo)

    w32.GetConsoleScreenBufferInfoEx(stdHandle, ct.byref(conInfo))

    # Change the console size
    conInfo.dwSize.X = x
    conInfo.dwSize.Y = y
    conInfo.dwMaximumWindowSize.X = x
    conInfo.dwMaximumWindowSize.Y = y

    # This is needed for some odd reason or on repeated calls to this function 
    # the window shrinks in size.
    conInfo.srWindow.Bottom = y
    conInfo.srWindow.Right = x
    w32.SetConsoleScreenBufferInfoEx(stdHandle, ct.byref(conInfo))

def _clear_size():
    stdHandle = w32.GetStdHandle(w32.STD_OUTPUT_HANDLE)
    w32.SetConsoleScreenBufferInfoEx(stdHandle, ct.byref(_defaultSize))

def _input_char(num, block=True):
    val = ''
    for i in range(num):
        if block or msvcrt.kbhit():
            val += msvcrt.getch()
    return val


def _get_cursor_pos():
    stdHandle = w32.GetStdHandle(w32.STD_OUTPUT_HANDLE)
    csbi = w32.CONSOLE_SCREEN_BUFFER_INFO()
    w32.GetConsoleScreenBufferInfo(stdHandle, ct.byref(csbi))

    cursorPos = (csbi.dwCursorPosition.X, csbi.dwCursorPosition.Y)

    return cursorPos


def _set_cursor_pos(x, y):
    stdHandle = w32.GetStdHandle(w32.STD_OUTPUT_HANDLE)
    csbi = w32.CONSOLE_SCREEN_BUFFER_INFOEX()
    result = w32.GetConsoleScreenBufferInfoEx(stdHandle, ct.byref(csbi))

    scrRect = result.srWindow
    adjPos = (x + scrRect.Left, y + scrRect.Top)
    cursorCoord = w32.COORD(adjPos)

    w32.SetConsoleCursorPosition(stdHandle, cursorCoord)


def _get_clear_color():
    cursorPos = _get_cursor_pos()

    rCoord = w32.COORD()
    rCoord.X = 0
    rCoord.Y = cursorPos[1]

    chars = cursorPos[0] + 1

    attr = (w32.WORD * chars)(0)
    attrPtr = ct.cast(attr, ct.POINTER(w32.WORD))

    a = w32.DWORD(0)

    stdHand = w32.GetStdHandle(w32.STD_OUTPUT_HANDLE)
    w32.ReadConsoleOutputAttribute(
        stdHand, attrPtr, chars, rCoord, ct.byref(a))

    return attr[0]


def _set_text_color(text, background):
    bgColor = background << 4
    color = text | bgColor
    m_hcon = w32.GetStdHandle(w32.STD_OUTPUT_HANDLE)
    w32.SetConsoleTextAttribute(m_hcon, color)


def _clear_screen():
    os.system('cls')


def _clear_color():
    m_hcon = w32.GetStdHandle(w32.STD_OUTPUT_HANDLE)
    w32.SetConsoleTextAttribute(m_hcon, _clearColor)


# Get defaults for various values that we need to restore later
_clearColor = _get_clear_color()
_defaultSize = _get_default_size()
