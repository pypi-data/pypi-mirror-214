class ForText:
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

    def __init__(self):
        # Basic Colors
        self.BLACK = '\033[30m'
        self.RED = '\033[31m'
        self.GREEN = '\033[32m'
        self.YELLOW = '\033[33m'
        self.BLUE = '\033[34m'
        self.MAGENTA = '\033[35m'
        self.CYAN = '\033[36m'
        self.WHITE = '\033[37m'
        # Basic Color Backgrounds
        self.BLACK_BG = '\033[40m'
        self.RED_BG = '\033[41m'
        self.GREEN_BG = '\033[42m'
        self.YELLOW_BG = '\033[43m'
        self.BLUE_BG = '\033[44m'
        self.MAGENTA_BG = '\033[45m'
        self.CYAN_BG = '\033[46m'
        self.WHITE_BG = '\033[47m'
        # Bright Colors
        self.BLACK_BR = '\033[90m'
        self.RED_BR = '\033[91m'
        self.GREEN_BR = '\033[92m'
        self.YELLOW_BR = '\033[93m'
        self.BLUE_BR = '\033[94m'
        self.MAGENTA_BR = '\033[95m'
        self.CYAN_BR = '\033[96m'
        self.WHITE_BR = '\033[97m'
        # Bright Color Backgrounds
        self.BLACK_BRBG = '\033[100m'
        self.RED_BRBG = '\033[101m'
        self.GREEN_BRBG = '\033[102m'
        self.YELLOW_BRBG = '\033[103m'
        self.BLUE_BRBG = '\033[104m'
        self.MAGENTA_BRBG = '\033[105m'
        self.CYAN_BRBG = '\033[106m'
        self.WHITE_BRBG = '\033[107m'
        # Emphasis
        self.BOLD = '\033[1m'
        self.DIM = '\033[2m'
        self.ITALIC = '\033[3m'
        self.UNDERLINE = '\033[4m'
        self.UNDERLINE2 = '\033[21m'
        self.BLINK = '\033[5m'
        self.STRIKE = '\033[9m'
        # Clear
        self.DEFAULT = '\033[39m'
        self.RESET = '\033[0m'
