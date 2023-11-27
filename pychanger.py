#!/usr/bin/python
# Author: 0xJuaNc4

# Módulos
import subprocess
from sys import exit
from colorama import Fore

# Paleta de colores
GREEN = Fore.GREEN
RED = Fore.RED
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
RESET = Fore.RESET

#Funcion principal
def main():
    print(f"{YELLOW}[*]{RESET} Selecciona una interfaz de red inalámbrica:\n")
    subprocess.call("iw dev | grep Interface | awk '{print $2}'", shell=True)
    interface = input("> ")

#Programa principal
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{RED}[!]{RESET} Saliendo...")
