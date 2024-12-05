

import pyfiglet
from colorama import Fore
 
DEBU = Fore.CYAN
INFO = Fore.GREEN
WARN = Fore.BLUE
ERRO = Fore.YELLOW
CRIT = Fore.RED
NORM = Fore.WHITE

fore_color_map = {
	'cyan': Fore.CYAN,
	'green': Fore.GREEN,
	'blue': Fore.BLUE,
	'yellow': Fore.YELLOW,
	'red': Fore.RED,
	'white': Fore.WHITE,
	None: Fore.WHITE,
	'black': Fore.BLACK,
	'magenta': Fore.MAGENTA,

}

def print_banner(banner, color):
	banner = pyfiglet.figlet_format(banner, font='doom')
	print(fore_color_map[color] + banner)
	print(Fore.WHITE + "")

