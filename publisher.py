import time

def send_message(r, channel, message):
    r.publish(channel, message)
    print(f"Pesan terkirim ke {channel}: {message}")

def send_important_message(r, channel, message):
    lock = r.set("important_lock", "locked", nx=True, ex=5)  # Distributed Mutual Exclusion
    if lock:
        print("Mengirim pesan penting...")
        r.publish(channel, message)
        time.sleep(5)
        r.delete("important_lock")  # Lepas lock
    else:
        print("Pesan penting sedang dikirim oleh user lain.")

def publisher_menu(r):
    print("\n=== MODE PUBLISHER ===")
    while True:
        print("\n1. Buat Channel Baru")
        print("2. Kirim Pesan ke Channel yang Ada")
        print("3. Kembali ke Menu Utama")
        choice = input("Pilih opsi: ")

        if choice == "1":
            channel = input("Masukkan nama channel baru: ")
            r.sadd("channels", channel)
            print(f"Channel {channel} berhasil dibuat.")
        elif choice == "2":
            print("Daftar channel yang tersedia:", r.smembers("channels"))
            channel = input("Masukkan nama channel: ")
            if not r.sismember("channels", channel):
                print("Channel tidak ditemukan.")
                continue
            message = input("Masukkan pesan: ")
            if message.startswith("!important"):
                send_important_message(r, channel, message)
            else:
                send_message(r, channel, message)
        elif choice == "3":
            break
        else:
            print("Pilihan tidak valid.")
