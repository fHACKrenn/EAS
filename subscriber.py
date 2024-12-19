def listen_to_channel(r, channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    print(f"Mendengarkan channel: {channel}")

    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Pesan diterima: {message['data']}")

def subscriber_menu(r):
    print("\n=== MODE SUBSCRIBER ===")
    while True:
        print("\n1. Lihat Daftar Channel")
        print("2. Subscribe ke Channel")
        print("3. Kembali ke Menu Utama")
        choice = input("Pilih opsi: ")

        if choice == "1":
            print("Daftar channel yang tersedia:", r.smembers("channels"))
        elif choice == "2":
            print("Daftar channel yang tersedia:", r.smembers("channels"))
            channel = input("Masukkan nama channel untuk subscribe: ")
            if not r.sismember("channels", channel):
                print("Channel tidak ditemukan.")
                continue
            listen_to_channel(r, channel)
        elif choice == "3":
            break
        else:
            print("Pilihan tidak valid.")
