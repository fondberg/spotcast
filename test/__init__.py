import tracemalloc
from logging import basicConfig, FATAL, getLogger

basicConfig(level=FATAL)
logger = getLogger(__name__)
logger.propagate = False
tracemalloc.start()
