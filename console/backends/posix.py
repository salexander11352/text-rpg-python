import os
import sys
import struct
import fcntl
import termios
from array import array
import select
import tty
import re

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

ESCAPE = '\x1b'
UP = '\x1b[A'
DOWN = '\x1b[B'
RIGHT = '\x1b[C'
LEFT = '\x1b[D'

charArr = []
def _input_char(num, block=True):
    global charArr

    strAc = ''

    fd = sys.stdin.fileno()
    prevSettings = termios.tcgetattr(fd)
    if block:
        tty.setraw(fd)
        charArr.extend(list(os.read(fd, 1000)))
        termios.tcsetattr(fd, termios.TCSADRAIN, prevSettings)

    else:
        # Copy settings
        newSett = prevSettings[:]
        newSett[3] &= ~termios.ICANON & ~termios.ECHO
        newSett[6][termios.VMIN] = 1
        newSett[6][termios.VTIME] = 0

        termios.tcsetattr(sys.stdin, termios.TCSANOW, newSett)

        buf = array('i', [0])
        fcntl.ioctl(sys.stdin, termios.FIONREAD, buf)
        numIn = buf[0]

        charArr.extend(list(os.read(fd, numIn)))

        termios.tcsetattr(sys.stdin, termios.TCSANOW, prevSettings)
    for i in range(num):
        charlan = len(charArr)
        print charlan
        if charlan > 1 :
            if charArr[0] == '\x1b' and charArr[1] == '[':
                strAc += '%s%s%s' % (charArr.pop(0), charArr.pop(0), charArr.pop(0))

            else:
                strAc += charArr.pop(0)
        elif charlan > 0:
            strAc += charArr.pop(0)
        else:
            break
    return strAc

def _get_cursor_pos():
    os.write(sys.stdin.fileno(), "\x1b[6n")
    value = _input_char(16)

    righ = value.rindex('R')
    left = value.rindex('[')

    valueSplit = value[left+1:righ].split(';')
    return valueSplit[1], valueSplit[0]

def _set_cursor_pos(x, y):
    sys.stdout.write('\x1b[%s;%sH' % (y+1, x+1))

def _clear_screen():
    os.system('clear')

def _clear_color():
    sys.stdout.write('\x1b[0m')