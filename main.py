import redis
from rediscluster import RedisCluster
import getpass
import sys
import publisher
import subscriber
import leader

# Set up cluster nodes
startup_nodes = [{"host": "localhost", "port": "7000"},
                 {"host": "localhost", "port": "7001"},
                 {"host": "localhost", "port": "7002"},
                 {"host": "localhost", "port": "7003"},
                 {"host": "localhost", "port": "7004"},
                 {"host": "localhost", "port": "7005"}]
r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

def register_user():
    username = input("Masukkan username baru: ")
    if r.hexists("users", username):
        print("Username sudah terdaftar. Silakan gunakan username lain.")
        return False
    password = getpass.getpass("Masukkan password: ")
    r.hset("users", username, password)
    print("Registrasi berhasil!")
    return True

def login_user():
    username = input("Masukkan username: ")
    if not r.hexists("users", username):
        print("Username tidak ditemukan.")
        return None
    password = getpass.getpass("Masukkan password: ")
    if r.hget("users", username) != password:
        print("Password salah.")
        return None
    print(f"Login berhasil. Selamat datang, {username}!")
    return username

def main_menu(username):
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Menjadi Publisher")
        print("2. Menjadi Subscriber")
        print("3. Standby untuk Log (Leader Mode)")
        print("4. Keluar")
        choice = input("Pilih opsi: ")

        if choice == "1":
            publisher.publisher_menu(r)
        elif choice == "2":
            subscriber.subscriber_menu(r)
        elif choice == "3":
            leader.elect_leader(r)
        elif choice == "4":
            print(f"Keluar. Sampai jumpa, {username}!")
            sys.exit()
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    print("=== SELAMAT DATANG DI SISTEM CHAT ===")
    while True:
        print("\n1. Login")
        print("2. Registrasi")
        print("3. Keluar")
        choice = input("Pilih opsi: ")

        if choice == "1":
            user = login_user()
            if user:
                main_menu(user)
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("Sampai jumpa!")
            sys.exit()
        else:
            print("Pilihan tidak valid.")
