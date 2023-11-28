#!/usr/bin/python
# Author: 0xJuaNc4

# Módulos
import subprocess
import re
from platform import system
from time import sleep
from sys import exit
from colorama import Fore

# Paleta de colores
GREEN = Fore.GREEN
RED = Fore.RED
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
RESET = Fore.RESET

#Banner
def banner():
    print(f"{YELLOW}█▀█ █▄█ █▀▀ █░█ ▄▀█ █▄░█ █▀▀ █▀▀ █▀█")
    print(f"█▀▀ ░█░ █▄▄ █▀█ █▀█ █░▀█ █▄█ ██▄ █▀▄{RESET}   Hecho por {YELLOW}(0xJuaNc4){RESET}")
    sleep(1)

#Verificar root
def verify_root():
    uid = int(subprocess.check_output(["id", "-u"]))
    if uid != 0:
        print(f"\n{RED}[!]{RESET} Necesitas permisos de superusuario {RED}(root){RESET} para ejecutar el script")
        exit(1)

# Verificar machanger
def check_macchanger():
     if subprocess.call("command -v macchanger > /dev/null 2>&1", shell=True) != 0:
        print(f"\n{RED}[!]{RESET} La herramienta {YELLOW}macchanger{RESET} no se encuentra en el sistema.")
        exit(1)

#Seleccionar interfaz
def select_interface():
    global interface
    print(f"\n\n{YELLOW}[*]{RESET} Selecciona una interfaz de red inalámbrica:\n")
    subprocess.call("iw dev | grep Interface | awk '{print $2}'", shell=True)
    interface = input("\n> ").lower()
    if subprocess.call(f"ifconfig {interface} > /dev/null 2>&1", shell=True) !=0:
        print(f"\n{RED}[!]{RESET} La interfaz {YELLOW}{interface}{RESET} no se ha encontrado")
        exit(1)
    else:
        print(f"\n{GREEN}[*]{RESET} Interfaz {YELLOW}{interface}{RESET} seleccionada")
        subprocess.call(f"ifconfig {interface} down", shell=True)
        sleep(1)

#MAC Spoofing
def mac_spoofing():
    global interface
    while True:
        interface_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
        subprocess.call("clear", shell=True)
        banner()
        print(f"\n\n{YELLOW}[*]{RESET} Selecciona una opción para configurar la interfaz:")
        print(f"\n{YELLOW}1.{RESET} Imprimir la dirección MAC actual")
        print(f"{YELLOW}2.{RESET} Establecer una dirección MAC personalizada")
        print(f"{YELLOW}3.{RESET} Establecer una dirección MAC totalmente aleatoria")
        print(f"{YELLOW}4.{RESET} Restaurar a la dirección MAC original")
        option = input("\n> ")

        if option == "1":
            print(f"\n{GREEN}[*]{RESET} Dirección MAC actual de la interfaz {interface}: {YELLOW}{interface_mac}{RESET}")

        elif option == "2":
            mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
            input_mac = input(f"\n{YELLOW}[*]{RESET} Introduce la dirección MAC nueva: ").strip().lower()

            if input_mac != interface_mac and mac_pattern.match(input_mac):
                print(f"\n{YELLOW}[*]{RESET} Estableciendo dirección MAC {YELLOW}{input_mac}{RESET} en la interfaz {YELLOW}{interface}{RESET} ...")
                subprocess.call(f"macchanger --mac={input_mac} {interface} > /dev/null 2>&1", shell=True)
                sleep(1)
                new_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
                print(f"\n{GREEN}[*]{RESET} Dirección MAC modificada exitosamente!")
                print(f"\n{CYAN}[*]{RESET} Dirección MAC antigua: {YELLOW}{interface_mac}{RESET}")
                print(f"\n{CYAN}[*]{RESET} Dirección MAC actual: {YELLOW}{new_mac}{RESET}")
            else:
                if input_mac == interface_mac:
                    print(f"\n{RED}[!]{RESET} La nueva dirección MAC es la misma que la dirección MAC actual.")
                else:
                    print(f"\n{RED}[!]{RESET} Formato de dirección MAC incorrecto")
                exit(1)
        elif option == "3":
             print(f"\n{YELLOW}[*]{RESET} Estableciendo dirección MAC aleatoria en la interfaz {YELLOW}{interface}{RESET} ...")
             subprocess.call(f"macchanger --random {interface} > /dev/null 2>&1", shell=True)
             sleep(1)
             new_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
             print(f"\n{GREEN}[*]{RESET} Dirección MAC modificada exitosamente!")
             print(f"\n{CYAN}[*]{RESET} Dirección MAC antigua: {YELLOW}{interface_mac}{RESET}")
             print(f"\n{CYAN}[*]{RESET} Dirección MAC actual: {YELLOW}{new_mac}{RESET}")
        elif option == "4":
            print(f"\n{YELLOW}[*]{RESET} Restaurando la dirección MAC original en la interfaz {YELLOW}{interface}{RESET} ...")
            subprocess.call(f"macchanger --show {interface} --another > /dev/null 2>&1", shell=True)
            sleep(1)
            restored_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
            print(f"\n{GREEN}[*]{RESET} Dirección MAC actual restaurada exitosamente!")
            print(f"\n{CYAN}[*]{RESET} Dirección MAC original: {YELLOW}{restored_mac}{RESET}")
        else:
            print(f"{RED}[!]{RESET} Opción inválida")
            exit(1)
        subprocess.call(f"ifconfig {interface} up > /dev/null 2>&1", shell=True)
        user_choice = input(f"\n{YELLOW}[*]{RESET} ¿Quieres realizar otra operación? (s/n): ")
        if user_choice.lower() != "s":
            print(f"\n{RED}[!]{RESET} Saliendo...")
            exit(1)

#Funcion principal
def main():
    subprocess.call("clear", shell=True)
    verify_root()
    check_macchanger()
    banner()
    select_interface()
    mac_spoofing()


#Programa principal
if __name__ == "__main__":
    if system() == "Windows":
        print(f"\n{RED}[!]{RESET} El script no soporta el sistema operativo Windows\n")
    else:
        try:
            main()
        except KeyboardInterrupt:
            print(f"\n\n{RED}[!]{RESET} Saliendo...")
