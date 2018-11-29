from rq import Queue
from redis import Redis

from lib import Config

cfg = Config()
cfg.load_from_yaml("config.yml")

redis_conn = Redis(host=cfg.get("db.host"),
                   port=cfg.get("db.port"))
queue = Queue(connection=redis_conn)
