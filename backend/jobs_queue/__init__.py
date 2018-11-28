from rq import Queue
from redis import Redis

# TODO: Move consts to config
redis_conn = Redis(host="redis")
q = Queue(connection=redis_conn)
