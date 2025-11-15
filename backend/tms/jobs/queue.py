from __future__ import annotations

import json
from typing import Any, Callable

from redis import Redis
from rq import Queue

from tms.infra.logging import get_logger
from tms.settings import settings

logger = get_logger(__name__)


class JobQueue:
    def __init__(self) -> None:
        self.redis = Redis.from_url(settings.redis_url)
        self.queue = Queue("ssg-sync", connection=self.redis)

    def enqueue(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        logger.info("queue_enqueue", job=str(func.__name__), args=json.dumps(args, default=str))
        self.queue.enqueue(func, *args, **kwargs)


def get_job_queue() -> JobQueue:
    return JobQueue()
