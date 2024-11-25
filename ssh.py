import paramiko
import threading
import os
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Menampilkan judul alat
def print_title():
    title = """
    =============================================
    |         SSH Mass Login Tool v1.0          |
    =============================================
    """
    print(Fore.CYAN + title)

# Membaca file input
def read_hosts(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    hosts = []
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) == 3:
            hosts.append(parts)
        else:
            print(Fore.RED + f"Invalid line format (skipping): {line.strip()}")
    return hosts

# Fungsi untuk mencoba login SSH
def ssh_login(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password)
        print(Fore.GREEN + f"Success: {hostname}")
        return True
    except Exception as e:
        print(Fore.RED + f"Failed: {hostname} - {e}")
        return False
    finally:
        client.close()

# Fungsi untuk memproses login dan menyimpan hasil
def process_host(host):
    hostname, username, password = host
    if ssh_login(hostname, username, password):
        with open("results/success_logins.txt", "a") as f:
            f.write(f"{hostname}|{username}|{password}\n")

# Fungsi utama untuk mengelola threading
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
    print_title()
    file_path = input("Masukkan nama file (contoh: file.txt): ")
    num_threads = int(input("Masukkan jumlah thread: "))
    main(file_path, num_threads)
