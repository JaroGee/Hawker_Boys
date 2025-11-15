from __future__ import annotations

import json
from typing import Any, Callable

import rq
from redis import Redis

from tms.infra.config import settings
from tms.infra.logging import get_logger

logger = get_logger(__name__)

redis_conn = Redis.from_url(settings.redis_url)
queue = rq.Queue(getattr(settings, "rq_default_queue", "ssg-sync"), connection=redis_conn, default_timeout=600)


class JobQueue:
    def __init__(self) -> None:
        self.queue = queue

    def enqueue(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> rq.job.Job:
        logger.info("queue_enqueue", job=str(func), args=json.dumps(args, default=str))
        return self.queue.enqueue(func, *args, **kwargs)


def get_job_queue() -> JobQueue:
    return JobQueue()


def enqueue_ssg_sync(job_name: str, *args: Any, **kwargs: Any) -> rq.job.Job:
    logger.info("queue_enqueue_named", job=job_name, args=json.dumps(args, default=str))
    return queue.enqueue(job_name, *args, **kwargs)
