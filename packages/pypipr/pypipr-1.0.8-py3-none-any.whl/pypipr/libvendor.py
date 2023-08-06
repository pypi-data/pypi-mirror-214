import colorama
import lxml
import lxml.html
import lxml.etree
import requests
import yaml
import pint


''' colorama '''
colorama.init()


''' pint '''
PintUreg = pint.UnitRegistry()
PintUregQuantity = PintUreg.Quantity


if __name__ == "__main__":
    print_colorize("Anda menjalankan module pypipr", color=colorama.Fore.RED)
