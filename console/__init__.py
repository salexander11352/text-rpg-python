import platform

osName = platform.system()

# Import the implementations based on the operating system used.
if osName == 'Windows':  # Windows works in both powershell and Command Prompt
    import console.backends.windows as impl
    from console.backends.windows import darkblue, darkgreen, darkcyan, darkred
    from console.backends.windows import darkmagenta, darkyellow, darkgrey
    from console.backends.windows import black, grey, blue, green, cyan, red
    from console.backends.windows import magenta, yellow, white

elif osName in ('Linux', 'Darwin'):  # Posix supporting operating systems
    import console.backends.posix as impl
    from console.backends.posix import darkblue, darkgreen, darkcyan, darkred
    from console.backends.posix import darkmagenta, darkyellow, darkgrey
    from console.backends.posix import black, grey, blue, green, cyan, red
    from console.backends.posix import magenta, yellow, white, none

# Generic implementation
else:
    raise EnvironmentError("OS Not supported.")


# Wrappers over platform implementations
def get_console_size():
    '''Get current console size'''
    # TODO - Check for python 3 and use native STL function for getting size
    return impl._get_console_size()


def set_console_size(x, y):
    '''Set console size'''
    impl._set_console_size(x, y)


def set_text_color(text, background):
    impl._set_text_color(text, background)


def clear_screen():
    print ('')
    impl._clear_screen()


def clear_color():
    impl._clear_color()


def clear_size():
    impl._clear_size()


def get_cursor_pos():
    return impl._get_cursor_pos()


def set_cursor_pos(x, y):
    impl._set_cursor_pos(x, y)


def input_char(block=True, lower=False):
    return impl._input_char(block, lower)


# Helper functions
def center_text(text, padding=' '):
    maxWidth, maxHeight = get_console_size()
    lines = text.split('\n')
    centeredLines = []
    for line in lines:
        totalPadding = maxWidth - len(line)
        if totalPadding % 2 == 0:
            leftPadding = rightPadding = int(totalPadding / 2) - 1
        else:
            leftPadding = int(totalPadding / 2) - 1
            rightPadding = leftPadding + 1
        lp = padding * leftPadding
        rp = padding * rightPadding
        centeredLines.append(lp + ' ' + line + ' ' + rp)

    return '\n'.join(centeredLines)


def fill_line(char=" "):
    '''Fill a full line with char. Defaults to spaces.'''
    maxWidth, maxHeight = get_console_size()
    return char * maxWidth


def make_heading(text):
    '''Print a heading to the screen.'''
    print (fill_line(char='#'))
    print (center_text(text))
    print (fill_line(char='#'))
