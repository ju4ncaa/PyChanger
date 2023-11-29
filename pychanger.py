#!/usr/bin/python
# Author: 0xJuaNc4

# Módulos
import subprocess
import re
from platform import system
from time import sleep
from sys import exit

# Paleta de colores
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

#Banner
def banner():
    print(f"{Colors.YELLOW}█▀█ █▄█ █▀▀ █░█ ▄▀█ █▄░█ █▀▀ █▀▀ █▀█")
    print(f"█▀▀ ░█░ █▄▄ █▀█ █▀█ █░▀█ █▄█ ██▄ █▀▄{Colors.RESET}   Hecho por {Colors.YELLOW}(0xJuaNc4){Colors.RESET}")
    sleep(1)

#Verificar root
def verify_root():
    uid = int(subprocess.check_output(["id", "-u"]))
    if uid != 0:
        print(f"\n{Colors.RED}[!]{Colors.RESET} Necesitas permisos de superusuario {Colors.RED}(root){Colors.RESET} para ejecutar el script")
        exit(1)

# Verificar machanger
def check_macchanger():
     if subprocess.call("command -v macchanger > /dev/null 2>&1", shell=True) != 0:
        print(f"\n{Colors.RED}[!]{Colors.RESET} La herramienta {Colors.YELLOW}macchanger{Colors.RESET} no se encuentra en el sistema.")
        exit(1)

#Seleccionar interfaz
def select_interface():
    global interface
    print(f"\n\n{Colors.YELLOW}[*]{Colors.RESET} Selecciona una interfaz de red inalámbrica:\n")
    subprocess.call("iw dev | grep Interface | awk '{print $2}'", shell=True)
    interface = input("\n> ").lower()
    if subprocess.call(f"ifconfig {interface} > /dev/null 2>&1", shell=True) !=0:
        print(f"\n{Colors.RED}[!]{Colors.RESET} La interfaz {Colors.YELLOW}{interface}{Colors.RESET} no se ha encontrado")
        exit(1)
    else:
        print(f"\n{Colors.GREEN}[*]{Colors.RESET} Interfaz {Colors.YELLOW}{interface}{Colors.RESET} seleccionada")
        subprocess.call(f"ifconfig {interface} down", shell=True)
        sleep(1)

#MAC Spoofing
def mac_spoofing():
    global interface
    while True:
        interface_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
        subprocess.call("clear", shell=True)
        banner()
        print(f"\n\n{Colors.YELLOW}[*]{Colors.RESET} Selecciona una opción para configurar la interfaz:")
        print(f"\n{Colors.YELLOW}1.{Colors.RESET} Imprimir la dirección MAC actual")
        print(f"{Colors.YELLOW}2.{Colors.RESET} Establecer una dirección MAC personalizada")
        print(f"{Colors.YELLOW}3.{Colors.RESET} Establecer una dirección MAC totalmente aleatoria")
        print(f"{Colors.YELLOW}4.{Colors.RESET} Restaurar a la dirección MAC original")
        option = input("\n> ")

        if option == "1":
            print(f"\n{Colors.GREEN}[*]{Colors.RESET} Dirección MAC actual de la interfaz {interface}: {Colors.YELLOW}{interface_mac}{Colors.RESET}")

        elif option == "2":
            mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
            input_mac = input(f"\n{Colors.YELLOW}[*]{Colors.RESET} Introduce la dirección MAC nueva: ").strip().lower()

            if input_mac != interface_mac and mac_pattern.match(input_mac):
                print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Estableciendo dirección MAC {Colors.YELLOW}{input_mac}{Colors.RESET} en la interfaz {Colors.YELLOW}{interface}{Colors.RESET} ...")
                subprocess.call(f"macchanger --mac={input_mac} {interface} > /dev/null 2>&1", shell=True)
                sleep(1)
                new_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
                print(f"\n{Colors.GREEN}[*]{Colors.RESET} Dirección MAC modificada exitosamente!")
                print(f"\n{Colors.CYAN}[*]{Colors.RESET} Dirección MAC antigua: {Colors.YELLOW}{interface_mac}{Colors.RESET}")
                print(f"\n{Colors.CYAN}[*]{Colors.RESET} Dirección MAC actual: {Colors.YELLOW}{new_mac}{Colors.RESET}")
            else:
                if input_mac == interface_mac:
                    print(f"\n{Colors.RED}[!]{Colors.RESET} La nueva dirección MAC es la misma que la dirección MAC actual.")
                else:
                    print(f"\n{Colors.RED}[!]{Colors.RESET} Formato de dirección MAC incorrecto")
                exit(1)
        elif option == "3":
             print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Estableciendo dirección MAC aleatoria en la interfaz {Colors.YELLOW}{interface}{Colors.RESET} ...")
             subprocess.call(f"macchanger --random {interface} > /dev/null 2>&1", shell=True)
             sleep(1)
             new_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
             print(f"\n{Colors.GREEN}[*]{Colors.RESET} Dirección MAC modificada exitosamente!")
             print(f"\n{Colors.CYAN}[*]{Colors.RESET} Dirección MAC antigua: {Colors.YELLOW}{interface_mac}{Colors.RESET}")
             print(f"\n{Colors.CYAN}[*]{Colors.RESET} Dirección MAC actual: {Colors.YELLOW}{new_mac}{Colors.RESET}")
        elif option == "4":
            print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Restaurando la dirección MAC original en la interfaz {Colors.YELLOW}{interface}{Colors.RESET} ...")
            subprocess.call(f"macchanger --show {interface} --another > /dev/null 2>&1", shell=True)
            sleep(1)
            restored_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
            print(f"\n{Colors.GREEN}[*]{Colors.RESET} Dirección MAC actual restaurada exitosamente!")
            print(f"\n{Colors.CYAN}[*]{Colors.RESET} Dirección MAC original: {Colors.YELLOW}{restored_mac}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!]{Colors.RESET} Opción inválida")
            exit(1)
        subprocess.call(f"ifconfig {interface} up > /dev/null 2>&1", shell=True)
        user_choice = input(f"\n{Colors.YELLOW}[*]{Colors.RESET} ¿Quieres realizar otra operación? (s/n): ")
        if user_choice.lower() != "s":
            print(f"\n{Colors.RED}[!]{Colors.RESET} Saliendo...")
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
        print(f"\n{Colors.RED}[!]{Colors.RESET} El script no soporta el sistema operativo Windows")
    else:
        try:
            main()
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}[!]{Colors.RESET} Saliendo...")
