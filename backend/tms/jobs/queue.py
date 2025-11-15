from __future__ import annotations

import rq
from redis import Redis

from tms.infra.config import settings

redis_conn = Redis.from_url(settings.redis_url)
queue = rq.Queue(settings.rq_default_queue, connection=redis_conn, default_timeout=600)


def enqueue_ssg_sync(job_name: str, *args, **kwargs) -> rq.job.Job:
    return queue.enqueue(job_name, *args, **kwargs)
