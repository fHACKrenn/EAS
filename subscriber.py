import redis
from rediscluster import RedisCluster

# Connect to the Redis Cluster using RedisCluster from redis-py
startup_nodes = [{"host": "localhost", "port": "7000"}, {"host": "localhost", "port": "7001"}, {"host": "localhost", "port": "7002"}]
r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

def listen_to_channel(channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    print(f"Mendengarkan channel: {channel}")

    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Pesan diterima: {message['data']}")

if __name__ == "__main__":
    listen_to_channel("chat_channel")
