import subprocess
import requests
import platform
import os
import sys
from colorama import Fore, init

init(autoreset=True)  # Automatically reset colorama color styles after they're printed

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def install_package(package):
    try:
        subprocess.check_call(["pip", "install", package])
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(["pip3", "install", package])
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}[!] Failed to install {package} using pip or pip3.{Fore.RESET}")

def import_or_install(packages):
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{Fore.RED}[!] {package} not found! Installing...{Fore.RESET}")
            install_package(package)
            print(f"{Fore.GREEN}[+] {package} has been successfully installed!{Fore.RESET}")

class KeyAuth:
    def __init__(self, app_id, base_url="https://api.keyauth.tech/api/v1", max_tries=3, success=None, fail=None):
        self.app_id = app_id
        self.auth_url = f"{base_url}/auth/{app_id}"
        self.license_url = f"{base_url}/license"
        self.max_tries = max_tries
        self.success = success
        self.fail = fail

    def exit(self):
        sys.exit()

    def install(self, packages):
        import_or_install(packages)
        
    def get_hwid(self):
        system = platform.system()
        if system == 'Darwin':
            cmd = ['system_profiler', 'SPHardwareDataType']
            output = subprocess.check_output(cmd).decode()
            for line in output.split('\n'):
                if 'Hardware UUID' in line:
                    uuid = line.split(':')[-1].strip()
                    break
        elif system == 'Windows':
            cmd = ['wmic', 'csproduct', 'get', 'uuid']
            output = subprocess.check_output(cmd).decode()
            for line in output.split('\n'):
                if line.strip() != 'UUID':
                    uuid = line.strip()
                    break
        else:
            uuid = None
        return str(uuid)

    def authenticate(self):
        tries = 0
        while tries < self.max_tries:
            data = {"hwid": self.get_hwid()}
            response = requests.post(self.auth_url, json=data, timeout=100)
            json_response = response.json()
            if json_response.get('message') == 'Login Success' and json_response.get('status') == 'success':
                clear()
                print(f"{Fore.GREEN}[+] Successfully authenticated!{Fore.RESET}")
                if self.success:
                    self.success()
                return True
            else:
                print(f"{Fore.RED}[!] HWID: {self.get_hwid()} is not authenticated!{Fore.RESET}")
                key = input(f"{Fore.RED}License Key: {Fore.RESET}")
                clear()
                key_payload = {'license_key': key, 'hwid': self.get_hwid()}
                headers = {'x-app-id': self.app_id}

                key_response = requests.post(self.license_url, json=key_payload, headers=headers, timeout=100)
                license_response = key_response.json()
                if license_response.get('message') == 'License key is valid. HWID added.' and license_response.get('status') == 'success':
                    clear()
                    print(f"{Fore.GREEN}[+] Successfully authenticated!{Fore.RESET}")
                    if self.success:
                        self.success()
                    return True
                else:
                    clear()
                    print(f"{Fore.RED}[!] Invalid License Key!{Fore.RESET}")
                    tries += 1
        print(f"{Fore.RED}[!] Maximum authentication attempts exceeded!{Fore.RESET}")
        if self.fail:
            self.fail()
        return False