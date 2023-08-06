'''
Modul utama pypipr yang berisi semua yg ada dalam pypipr
'''


from .lib import *
from .console import *
from .engineering import *
from .ifunctions import *
from .uncategorize import *
from .flow import *


if __name__ == "__main__":
    print_colorize("Anda menjalankan module pypipr", color=colorama.Fore.RED)
