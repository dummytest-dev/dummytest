"""Wrap output colors into classes and functions."""


__all__ = [
    "_ANSIColors",
    "_ColorPrinter",
    "c"
]

class _ANSIColors:
    RESET = "\x1b[0m"

    BLACK = "\x1b[30m"
    BLUE = "\x1b[34m"
    CYAN = "\x1b[36m"
    GREEN = "\x1b[32m"
    GREY = "\x1b[90m"
    MAGENTA = "\x1b[35m"
    RED = "\x1b[31m"
    WHITE = "\x1b[37m"
    YELLOW = "\x1b[33m"

    BOLD = "\x1b[1m"
    BOLD_BLACK = "\x1b[1;30m"
    BOLD_BLUE = "\x1b[1;34m"
    BOLD_CYAN = "\x1b[1;36m"
    BOLD_GREEN = "\x1b[1;32m"
    BOLD_MAGENTA = "\x1b[1;35m"
    BOLD_RED = "\x1b[1;31m"
    BOLD_WHITE = "\x1b[1;37m"
    BOLD_YELLOW = "\x1b[1;33m"

    INTENSE_BLACK = "\x1b[90m"
    INTENSE_BLUE = "\x1b[94m"
    INTENSE_CYAN = "\x1b[96m"
    INTENSE_GREEN = "\x1b[92m"
    INTENSE_MAGENTA = "\x1b[95m"
    INTENSE_RED = "\x1b[91m"
    INTENSE_WHITE = "\x1b[97m"
    INTENSE_YELLOW = "\x1b[93m"

    BACKGROUND_BLACK = "\x1b[40m"
    BACKGROUND_BLUE = "\x1b[44m"
    BACKGROUND_CYAN = "\x1b[46m"
    BACKGROUND_GREEN = "\x1b[42m"
    BACKGROUND_MAGENTA = "\x1b[45m"
    BACKGROUND_RED = "\x1b[41m"
    BACKGROUND_WHITE = "\x1b[47m"
    BACKGROUND_YELLOW = "\x1b[43m"

    INTENSE_BACKGROUND_BLACK = "\x1b[100m"
    INTENSE_BACKGROUND_BLUE = "\x1b[104m"
    INTENSE_BACKGROUND_CYAN = "\x1b[106m"
    INTENSE_BACKGROUND_GREEN = "\x1b[102m"
    INTENSE_BACKGROUND_MAGENTA = "\x1b[105m"
    INTENSE_BACKGROUND_RED = "\x1b[101m"
    INTENSE_BACKGROUND_WHITE = "\x1b[107m"
    INTENSE_BACKGROUND_YELLOW = "\x1b[103m"


class _ColorPrinter(_ANSIColors):

    @staticmethod
    def _wrap(text, color_code):
        return f"{color_code}{text}{_ColorPrinter.RESET}"

    @staticmethod
    def black(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BLACK)

    @staticmethod
    def red(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.RED)

    @staticmethod
    def green(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.GREEN)

    @staticmethod
    def yellow(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.YELLOW)

    @staticmethod
    def blue(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BLUE)

    @staticmethod
    def magenta(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.MAGENTA)

    @staticmethod
    def cyan(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.CYAN)

    @staticmethod
    def white(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.WHITE)

    @staticmethod
    def intense_black(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_BLACK)

    @staticmethod
    def intense_red(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_RED)

    @staticmethod
    def intense_green(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_GREEN)

    @staticmethod
    def intense_yellow(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_YELLOW)

    @staticmethod
    def intense_blue(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_BLUE)

    @staticmethod
    def intense_magenta(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_MAGENTA)

    @staticmethod
    def intense_cyan(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_CYAN)

    @staticmethod
    def intense_white(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_WHITE)

    @staticmethod
    def bold(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BOLD)

    @staticmethod
    def bold_black(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BOLD_BLACK)

    @staticmethod
    def bold_blue(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BOLD_BLUE)

    @staticmethod
    def bold_cyan(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BOLD_CYAN)

    @staticmethod
    def bold_green(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BOLD_GREEN)

    @staticmethod
    def bold_magenta(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BOLD_MAGENTA)

    @staticmethod
    def bold_red(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BOLD_RED)

    @staticmethod
    def bold_white(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BOLD_WHITE)

    @staticmethod
    def bold_yellow(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BOLD_YELLOW)

    @staticmethod
    def bg_black(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BACKGROUND_BLACK)

    @staticmethod
    def bg_blue(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BACKGROUND_BLUE)

    @staticmethod
    def bg_cyan(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BACKGROUND_CYAN)

    @staticmethod
    def bg_green(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BACKGROUND_GREEN)

    @staticmethod
    def bg_magenta(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BACKGROUND_MAGENTA)

    @staticmethod
    def bg_red(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BACKGROUND_RED)

    @staticmethod
    def bg_white(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BACKGROUND_WHITE)

    @staticmethod
    def bg_yellow(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.BACKGROUND_YELLOW)

    @staticmethod
    def bg_intense_black(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_BACKGROUND_BLACK)

    @staticmethod
    def bg_intense_blue(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_BACKGROUND_BLUE)

    @staticmethod
    def bg_intense_cyan(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_BACKGROUND_CYAN)

    @staticmethod
    def bg_intense_green(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_BACKGROUND_GREEN)

    @staticmethod
    def bg_intense_magenta(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_BACKGROUND_MAGENTA)

    @staticmethod
    def bg_intense_red(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_BACKGROUND_RED)

    @staticmethod
    def bg_intense_white(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_BACKGROUND_WHITE)

    @staticmethod
    def bg_intense_yellow(text):
        return _ColorPrinter._wrap(text, _ColorPrinter.INTENSE_BACKGROUND_YELLOW)

# Singleton Mode
c = _ColorPrinter()