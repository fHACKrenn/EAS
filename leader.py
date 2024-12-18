import redis
import time

r = redis.Redis(host="localhost", port=6379)

def elect_leader():
    leader = r.set("leader_lock", "leader_node", nx=True, ex=10)
    if leader:
        print("Node ini menjadi LEADER. Menjalankan tugas logging...")
        log_messages()
    else:
        print("Node ini bukan leader. Menunggu...")

def log_messages():
    pubsub = r.pubsub()
    pubsub.subscribe("chat_channel")
    with open("chat_log.txt", "a") as log_file:
        for message in pubsub.listen():
            if message['type'] == 'message':
                log_file.write(message['data'].decode('utf-8') + "\n")
                print("Pesan dicatat ke log.")

if __name__ == "__main__":
    while True:
        elect_leader()
        time.sleep(5)
