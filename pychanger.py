#!/usr/bin/python
# Author: 0xJuaNc4

# Módules
import subprocess
import re
from platform import system
from time import sleep
from sys import exit

# Color palette
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

#Banner
def banner():
    print(f"{Colors.YELLOW}█▀█ █▄█ █▀▀ █░█ ▄▀█ █▄░█ █▀▀ █▀▀ █▀█")
    print(f"█▀▀ ░█░ █▄▄ █▀█ █▀█ █░▀█ █▄█ ██▄ █▀▄{Colors.RESET}   (Made by {Colors.YELLOW}0xJuaNc4){Colors.RESET}")
    sleep(1)

#Verify root perms
def verify_root():
    uid = int(subprocess.check_output(["id", "-u"]))
    if uid != 0:
        print(f"\n{Colors.RED}[!]{Colors.RESET} You need superuser permissions {Colors.RED}(root){Colors.RESET} to execute the script")
        exit(1)

# Verify machanger tool
def check_macchanger():
     if subprocess.call("command -v macchanger > /dev/null 2>&1", shell=True) != 0:
        print(f"\n{Colors.RED}[!]{Colors.RESET} The {Colors.YELLOW}macchanger{Colors.RESET} tool is not found in the system.")
        exit(1)

#Select interface
def select_interface():
    global interface
    print(f"\n\n{Colors.YELLOW}[*]{Colors.RESET} Select a wireless network interface:\n")
    interfaces = subprocess.check_output("iw dev | grep Interface | awk '{print $2}'", shell=True, text=True).split('\n')
    for counter, interface in enumerate(interfaces, start=1):
        if interface:
            print(f"{Colors.CYAN}{counter}.{Colors.RESET} {interface}")
    interface = input("\n> ").lower()
    if subprocess.call(f"ifconfig {interface} > /dev/null 2>&1", shell=True) !=0:
        print(f"\n{Colors.RED}[!]{Colors.RESET} Interface {Colors.YELLOW}{interface}{Colors.RESET} was not found.")
        exit(1)
    else:
        print(f"\n{Colors.GREEN}[*]{Colors.RESET} Interface {Colors.YELLOW}{interface}{Colors.RESET} selected")
        subprocess.call(f"ifconfig {interface} down", shell=True)
        sleep(1)

#MAC Spoofing
def mac_spoofing():
    global interface
    while True:
        interface_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
        subprocess.call("clear", shell=True)
        banner()
        print(f"\n\n{Colors.YELLOW}[*]{Colors.RESET} Select an option to configure the interface:")
        print(f"\n{Colors.YELLOW}1.{Colors.RESET} Print the current MAC address")
        print(f"{Colors.YELLOW}2.{Colors.RESET} Set a custom MAC address")
        print(f"{Colors.YELLOW}3.{Colors.RESET} Set a completely random MAC address")
        print(f"{Colors.YELLOW}4.{Colors.RESET} Restore to original MAC address")
        option = input("\n> ")

        if option == "1":
            print(f"\n{Colors.GREEN}[*]{Colors.RESET} Current MAC address of the interface {interface}: {Colors.YELLOW}{interface_mac}{Colors.RESET}")

        elif option == "2":
            mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
            input_mac = input(f"\n{Colors.YELLOW}[*]{Colors.RESET} Enter the new MAC address: ").strip().lower()

            if input_mac != interface_mac and mac_pattern.match(input_mac):
                print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Setting MAC address {Colors.YELLOW}{input_mac}{Colors.RESET} on the interface {Colors.YELLOW}{interface}{Colors.RESET} ...")
                subprocess.call(f"macchanger --mac={input_mac} {interface} > /dev/null 2>&1", shell=True)
                sleep(1)
                new_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
                print(f"\n{Colors.GREEN}[*]{Colors.RESET} MAC address successfully modified!")
                print(f"\n{Colors.CYAN}[*]{Colors.RESET} Old MAC address: {Colors.YELLOW}{interface_mac}{Colors.RESET}")
                print(f"\n{Colors.CYAN}[*]{Colors.RESET} Current MAC address: {Colors.YELLOW}{new_mac}{Colors.RESET}")
            else:
                if input_mac == interface_mac:
                    print(f"\n{Colors.RED}[!]{Colors.RESET} The new MAC address is the same as the current MAC address.")
                else:
                    print(f"\n{Colors.RED}[!]{Colors.RESET} Incorrect MAC address format")
                exit(1)
        elif option == "3":
             print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Setting random MAC address on the interface {Colors.YELLOW}{interface}{Colors.RESET} ...")
             subprocess.call(f"macchanger --random {interface} > /dev/null 2>&1", shell=True)
             sleep(1)
             new_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
             print(f"\n{Colors.GREEN}[*]{Colors.RESET} MAC address successfully modified!")
             print(f"\n{Colors.CYAN}[*]{Colors.RESET} Old MAC address: {Colors.YELLOW}{interface_mac}{Colors.RESET}")
             print(f"\n{Colors.CYAN}[*]{Colors.RESET} Current MAC address: {Colors.YELLOW}{new_mac}{Colors.RESET}")
        elif option == "4":
            print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Restoring the original MAC address on the interface {Colors.YELLOW}{interface}{Colors.RESET} ...")
            subprocess.call(f"macchanger --show {interface} --another > /dev/null 2>&1", shell=True)
            sleep(1)
            restored_mac = subprocess.check_output(f"macchanger --show {interface} | awk '{{print $3}}' | head -n 1", shell=True, text=True).strip().lower()
            print(f"\n{Colors.GREEN}[*]{Colors.RESET} Current MAC address successfully restored!")
            print(f"\n{Colors.CYAN}[*]{Colors.RESET} Original MAC address: {Colors.YELLOW}{restored_mac}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!]{Colors.RESET} Invalid option")
            exit(1)
        subprocess.call(f"ifconfig {interface} up > /dev/null 2>&1", shell=True)
        user_choice = input(f"\n{Colors.YELLOW}[*]{Colors.RESET} Do you want to perform another operation (y/n): ")
        if user_choice.lower() != "y":
            print(f"\n{Colors.RED}[!]{Colors.RESET} Exit...")
            exit(1)

# Main function
def main():
    subprocess.call("clear", shell=True)
    verify_root()
    check_macchanger()
    banner()
    select_interface()
    mac_spoofing()


# Main program
if __name__ == "__main__":
    if system() == "Windows":
        print(f"\n{Colors.RED}[!]{Colors.RESET} The script does not support the Windows operating system")
    else:
        try:
            main()
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}[!]{Colors.RESET} Exit...")
