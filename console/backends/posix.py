import os
import sys
import struct
import fcntl
import termios
import tty

_BLACK = '0'
_RED = '1'
_GREEN = '2'
_YELLOW = '3'
_BLUE = '4'
_MAGENTA = '5'
_CYAN = '6'
_GRAY = '7'

_DARK_FG = '3'
_DARK_BG = '4'
_LIGHT_FG = '9'
_LIGHT_BG = '10'

none = None
darkred = _DARK_FG + _RED
darkgreen = _DARK_FG + _GREEN
darkyellow = _DARK_FG + _YELLOW
darkblue = _DARK_FG + _BLUE
darkmagenta = _DARK_FG + _MAGENTA
darkcyan = _DARK_FG + _CYAN
grey = _DARK_FG + _GRAY

black = _DARK_FG + _BLACK
darkgrey = _LIGHT_FG + _BLACK

red = _LIGHT_FG + _RED
green = _LIGHT_FG + _GREEN
yellow = _LIGHT_FG + _YELLOW
blue = _LIGHT_FG + _BLUE
magenta = _LIGHT_FG + _MAGENTA
cyan = _LIGHT_FG + _CYAN
white = _LIGHT_FG + _GRAY


ESCAPE = '\x1b'
UP = '\x1b[A'
DOWN = '\x1b[B'
RIGHT = '\x1b[C'
LEFT = '\x1b[D'


def _get_console_size():
    '''Get the console size on *nix platforms.'''
    winsize = struct.pack('HHHH', 0, 0, 0, 0)
    result = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, winsize)
    height, width, pw, ph = struct.unpack('HHHH', result)

    return (width, height)


def _set_console_size(x, y):
    '''Set the console size on *nix platforms.'''
    sys.stdout.write('\x1b[8;%s;%st' % (y, x))


def _set_text_color(text, background):
    colors = ''
    if not text is None:
        colors += text
    if not background is None:
        if not colors == '':
            colors += ';'
        colors += str(int(background) + 10)
    sys.stdout.write('\x1b[0;%sm' % colors)


def _clear_backscroll():
    sys.stdout.write('\033c')

charArr = []


def _input_char(block=True, lower=False):
    global charArr

    fd = sys.stdin.fileno()
    prevSettings = termios.tcgetattr(fd)

    if True:
        tty.setraw(fd)
        attr = termios.TCSADRAIN

    else:
        # Copy settings
        newSett = prevSettings[:]
        newSett[3] &= ~termios.ICANON & ~termios.ECHO
        newSett[6][termios.VMIN] = 0
        newSett[6][termios.VTIME] = 0

        attr = termios.TCSANOW
        termios.tcsetattr(sys.stdin, attr, newSett)

    charArr.extend(list(os.read(fd, 1000)))

    termios.tcsetattr(sys.stdin, attr, prevSettings)

    charlan = len(charArr)
    # print charlan
    if charlan > 1:
        if charArr[0] == '\x1b' and charArr[1] == '[':
            char = '%s%s%s' % (charArr.pop(0), charArr.pop(0), charArr.pop(0))

        else:
            char = charArr.pop(0)
    elif charlan > 0:
        char = charArr.pop(0)

    else:
        char = ''

    if lower:
        char = char.lower()

        # print '%r' % strAc
    return char


def _get_cursor_pos():
    os.write(sys.stdin.fileno(), "\x1b[6n")
    value = _input_char(16)

    righ = value.rindex('R')
    left = value.rindex('[')

    valueSplit = value[left + 1:righ].split(';')
    return valueSplit[1], valueSplit[0]


def _set_cursor_pos(x, y):
    sys.stdout.write('\x1b[%s;%sH' % (y + 1, x + 1))


def _clear_screen():
    os.system('clear')


def _clear_color():
    sys.stdout.write('\x1b[0m')


def _clear_size():
    _set_console_size(*_size)


# get default size
_size = _get_console_size()
