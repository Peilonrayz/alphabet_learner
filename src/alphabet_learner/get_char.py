from .ansi import ANSI

try:
    import msvcrt
except ImportError:
    import tty, sys, termios, functools

    class GetChar:
        def __enter__(self):
            self.fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setraw(sys.stdin.fileno())
            return functools.partial(sys.stdin.read, 1)

        def __exit__(self, _1, _2, _3):
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


else:
    _KEYCODES = {
        b"\x00H": ANSI.UP,
        b"\x00P": ANSI.DOWN,
    }

    def _get_char():
        char = msvcrt.getch()
        if char == b"\x00":
            char += msvcrt.getch()
        if char == b"\x03":
            raise KeyboardInterrupt()
        return _KEYCODES.get(char, char)

    class GetChar:
        def __enter__(self):
            return _get_char

        def __exit__(self, _1, _2, _3):
            pass
