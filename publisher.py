import redis
import sys
import time

# Connect to the Redis Cluster using RedisCluster from redis-py
from rediscluster import RedisCluster

# Set up cluster nodes
startup_nodes = [{"host": "localhost", "port": "7000"}, {"host": "localhost", "port": "7001"}, {"host": "localhost", "port": "7002"}]
r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

def send_message(channel, message):
    r.publish(channel, message)
    print(f"Pesan terkirim: {message}")

def send_important_message(channel, message):
    lock = r.set("important_lock", "locked", nx=True, ex=5)  # Distributed Mutual Exclusion
    if lock:
        print("Mengirim pesan penting...")
        r.publish(channel, message)
        time.sleep(2)  # Simulasi delay
        r.delete("important_lock")  # Lepas lock
    else:
        print("Pesan penting sedang dikirim oleh user lain.")

if __name__ == "__main__":
    channel = "chat_channel"
    print("Masukkan pesan (ketik 'exit' untuk keluar)")
    while True:
        message = input("Pesan: ")
        if message == "exit":
            sys.exit()
        elif message.startswith("!important"):  # Pesan penting
            send_important_message(channel, message)
        else:
            send_message(channel, message)
