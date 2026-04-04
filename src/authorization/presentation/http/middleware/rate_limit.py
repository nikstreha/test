import asyncio
import time
from collections import deque

import structlog
from fastapi import HTTPException, Request, status

from authorization.presentation.http.util.get_ip import get_client_ip

logger = structlog.get_logger(__name__)


class LoginRateLimiter:
    def __init__(self, max_attempts: int = 5, window_seconds: int = 60) -> None:
        self._max_attempts = max_attempts
        self._window_seconds = window_seconds
        self._buckets: dict[str, deque[float]] = {}
        self._lock = asyncio.Lock()

    async def __call__(self, request: Request) -> None:
        client_ip = get_client_ip(request)
        now = time.monotonic()
        window_start = now - self._window_seconds

        async with self._lock:
            bucket = self._buckets.setdefault(client_ip, deque())

            while bucket and bucket[0] < window_start:
                bucket.popleft()

            if len(bucket) >= self._max_attempts:
                retry_after = int(bucket[0] - window_start) + 1
                logger.warning(
                    "rate_limit.exceeded", client_ip=client_ip, retry_after=retry_after
                )
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many login attempts. Try again later.",
                    headers={"Retry-After": str(retry_after)},
                )

            bucket.append(now)
