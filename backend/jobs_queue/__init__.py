from rq import (
    Queue,
    get_current_job,
)
from redis import Redis

from utils import Config

cfg = Config()
cfg.load_from_yaml("config.yml")

redis_conn = Redis(host=cfg.get("db.host"),
                   port=cfg.get("db.port"))
queue = Queue(connection=redis_conn)
