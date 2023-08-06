class Color:
    BLACK = '\x1b[30m'
    WHITE = '\x1b[97m'
    DARK_RED = '\x1b[31m'
    DARK_GREEN = '\x1b[32m'
    DARK_YELLOW = '\x1b[33m'
    DARK_BLUE = '\x1b[34m'
    DARK_PURPLE = '\x1b[35m'
    DARK_AQUA = '\x1b[36m'
    GRAY = '\x1b[37m'
    DARK_GRAY = '\x1b[90m'

    RED = '\x1b[91m'
    GREEN = '\x1b[92m'
    YELLOW  = '\x1b[93m'
    BLUE  = '\x1b[94m'
    PURPLE = '\x1b[95m'
    AQUA  = '\x1b[96m'


class Format:
    OBFUSCATED = "\x1b[8m"
    BOLD = '\x1b[1m'
    STRIKETHROUGH = '\x1b[9m'
    UNDERLINE = '\x1b[4m'
    ITALIC = '\x1b[3m'
    RESET = '\x1b[0m'

    BLINK = "\x1b[5m"
    OVERLINE = "\x1b[53m"
    DOUBLE_UNDERLINE = "\x1b[21m"
    INVERT = "\x1b[7m"