import os
import sys
import struct
import fcntl
import termios
import StringIO
import tty
import subprocess as sub
# _BLUE = 0x0001
# _GREEN = 0x0002
# _RED = 0x0004
# _INTENSITY = 0x0008

# darkblue    = _BLUE
# darkgreen   = _GREEN
# darkcyan    = _GREEN | _BLUE
# darkred     = _RED
# darkmagenta = _RED | _BLUE
# darkyellow  = _RED | _GREEN
# grey        = _RED | _GREEN | _BLUE

# black       = 0
# darkgrey    = _INTENSITY

# blue        = _INTENSITY | _BLUE
# green       = _INTENSITY | _GREEN
# cyan        = _INTENSITY | _GREEN | _BLUE
# red         = _INTENSITY | _RED
# magenta     = _INTENSITY | _RED | _BLUE
# yellow      = _INTENSITY | _RED | _GREEN
# white       = _INTENSITY | _RED | _GREEN | _BLUE

_BLACK   = '0'
_RED     = '1'
_GREEN   = '2'
_YELLOW  = '3'
_BLUE    = '4'
_MAGENTA = '5'
_CYAN    = '6'
_GRAY    = '7'

_DARK_FG  = '3'
_DARK_BG  = '4'
_LIGHT_FG = '9'
_LIGHT_BG = '10'

none        = None
darkred     = _DARK_FG + _RED
darkgreen   = _DARK_FG + _GREEN
darkyellow  = _DARK_FG + _YELLOW
darkblue    = _DARK_FG + _BLUE
darkmagenta = _DARK_FG + _MAGENTA
darkcyan    = _DARK_FG + _CYAN
grey        = _DARK_FG + _GRAY

black       = _DARK_FG + _BLACK
darkgrey    = _LIGHT_FG + _BLACK

red     = _LIGHT_FG + _RED
green   = _LIGHT_FG + _GREEN
yellow  = _LIGHT_FG + _YELLOW
blue    = _LIGHT_FG + _BLUE
magenta = _LIGHT_FG + _MAGENTA
cyan    = _LIGHT_FG + _CYAN
white   = _LIGHT_FG + _GRAY

def _get_console_size():
    '''Get the console size on platforms that support the posix standard'''
    winsize = struct.pack('HHHH', 0, 0, 0, 0)
    result = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, winsize)
    height, width, pw, ph = struct.unpack('HHHH', result)

    return (width, height)

def _set_text_color(text, background):
    colors = ''
    if not text is None:
        colors += text
    if not background is None:
        if not colors == '':
            colors += ';'
        colors += str(int(background) + 10)
    sys.stdout.write('\x1b[0;%sm' % colors)

def _input_char(num):
    fd = sys.stdin.fileno()
    prevSettings = termios.tcgetattr(fd)
    tty.setraw(fd)

    strAc = os.read(fd, num)
    termios.tcsetattr(fd, termios.TCSADRAIN, prevSettings)
    return strAc

def _get_cursor_pos():
    os.write(sys.stdin.fileno(), "\x1b[6n")
    value = _input_char(16)

    righ = value.rindex('R')
    left = value.rindex('[')

    valueSplit = value[left+1:righ].split(';')
    return valueSplit[1], valueSplit[0]

def _clear_screen():
    os.system('clear')

def _clear_color():
    sys.stdout.write('\x1b[0m')