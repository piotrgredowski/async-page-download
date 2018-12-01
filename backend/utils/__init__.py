import logging

from .config import Config

logging.basicConfig(format="%(levelname)s:%(name)s: %(message)s", level=logging.INFO)
log = logging.getLogger()
