"""Use PyCon_Text's attributes to change color, emphasis, and background of text printed to the console.
At the end of each print statement you should use either .DEFAULT or .RESET to end text formatting.\n
**Example:**\n
________\n
print(f"{PyCon_Text.GREEN}{PyCon_Text.BOLD}{PyCon_Text.UNDERLINE2}{PyCon_Text.WHITE_BRIGHT_BACKGROUND}
Some Good News!!!{PyCon_Text.RESET}")\n
________\n
**Basic Colors:**\n
BLACK,
RED,
GREEN,
YELLOW,
BLUE,
MAGENTA,
CYAN,
WHITE\n
**Bright Colors:**\n
BLACK_BR,
RED_BR,
GREEN_BR,
YELLOW_BR,
BLUE_BR,
MAGENTA_BR,
CYAN_BR,
WHITE_BR\n
**Basic Color Backgrounds:**\n
BLACK_BG,
RED_BG,
GREEN_BG,
YELLOW_BG,
BLUE_BG,
MAGENTA_BG,
CYAN_BG,
WHITE_BG\n
**Bright Color Backgrounds:**\n
BLACK_BRBG,
RED_BRBG,
GREEN_BRBG,
YELLOW_BRBG,
BLUE_BRBG,
MAGENTA_BRBG,
CYAN_BRBG,
WHITE_BRBG\n
**Emphasis:**\n
BOLD,
DIM,
ITALIC,
UNDERLINE,
UNDERLINE2,
BLINK,
STRIKE\n
**Clear:**\n
DEFAULT,
RESET
"""

# Basic Colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
# Basic Color Backgrounds
BLACK_BG = '\033[40m'
RED_BG = '\033[41m'
GREEN_BG = '\033[42m'
YELLOW_BG = '\033[43m'
BLUE_BG = '\033[44m'
MAGENTA_BG = '\033[45m'
CYAN_BG = '\033[46m'
WHITE_BG = '\033[47m'
# Bright Colors
BLACK_BR = '\033[90m'
RED_BR = '\033[91m'
GREEN_BR = '\033[92m'
YELLOW_BR = '\033[93m'
BLUE_BR = '\033[94m'
MAGENTA_BR = '\033[95m'
CYAN_BR = '\033[96m'
WHITE_BR = '\033[97m'
# Bright Color Backgrounds
BLACK_BRBG = '\033[100m'
RED_BRBG = '\033[101m'
GREEN_BRBG = '\033[102m'
YELLOW_BRBG = '\033[103m'
BLUE_BRBG = '\033[104m'
MAGENTA_BRBG = '\033[105m'
CYAN_BRBG = '\033[106m'
WHITE_BRBG = '\033[107m'
# Emphasis
BOLD = '\033[1m'
DIM = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
UNDERLINE2 = '\033[21m'
BLINK = '\033[5m'
STRIKE = '\033[9m'
# Clear
DEFAULT = '\033[39m'
RESET = '\033[0m'

