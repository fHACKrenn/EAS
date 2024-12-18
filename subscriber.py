import redis

r = redis.Redis(host="localhost", port=6379)

def listen_to_channel(channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    print(f"Mendengarkan channel: {channel}")

    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Pesan diterima: {message['data'].decode('utf-8')}")

if __name__ == "__main__":
    listen_to_channel("chat_channel")
