import time

LEADER_LOCK_KEY = "leader_lock"
HEARTBEAT_KEY = "leader_heartbeat"
HEARTBEAT_INTERVAL = 5
HEARTBEAT_EXPIRY = 10

def elect_leader(r):
    leader = r.set(LEADER_LOCK_KEY, "leader_node", nx=True, ex=30)
    if leader:
        print("Node ini menjadi LEADER. Menjalankan tugas...")
        log_messages(r)
        refresh_leader_lock(r)
    else:
        print("Node lain sedang menjadi leader")
        return

def log_messages(r):
    print("Logging messages dari semua channel...")
    pubsub = r.pubsub()
    pubsub.psubscribe('*')
    with open("chat_log.txt", "a") as log_file:
        for message in pubsub.listen():
            log_file.write(f"{message['channel']}: {message['data']}\n")
            print(f"Log: {message['channel']} - {message['data']}")
        
def refresh_leader_lock(r):
    """Leader periodically refreshes the leader lock to prevent it from expiring."""
    while True:
        time.sleep(HEARTBEAT_INTERVAL * 2)  # Refresh before the lock expires
        r.set(LEADER_LOCK_KEY, "leader_node", ex=30)  # Reset the leader lock expiration
        print("Leader lock diperbarui...")
