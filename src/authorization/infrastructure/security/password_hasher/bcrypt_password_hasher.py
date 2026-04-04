import asyncio
import base64
import functools
import hashlib
from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager

import bcrypt
import structlog

from authorization.domain.port.security.password_hasher import IPasswordHasher
from authorization.domain.value_object.user.password_hash import PasswordHash
from authorization.domain.value_object.user.raw_password import RawPassword
from authorization.infrastructure.security.password_hasher.exception import (
    PasswordHasherError,
    PasswordHasherIsBusyError,
)
from authorization.infrastructure.security.password_hasher.type import (
    PasswordHasherSemaphore,
    PasswordHasherThreadPoolExecutor,
)

logger = structlog.get_logger(__name__)


class BcryptPasswordHasher(IPasswordHasher):
    def __init__(
        self,
        pepper: str,
        executor: PasswordHasherThreadPoolExecutor,
        semaphore: PasswordHasherSemaphore,
        wait_timeout_s: float,
        rounds: int = 12,
    ) -> None:
        self._pepper = pepper.encode("utf-8")
        self._executor = executor
        self._semaphore = semaphore
        self._wait_timeout_s = wait_timeout_s
        self._rounds = rounds

    async def hash(self, *, raw_password: RawPassword) -> PasswordHash:
        async with self._permit():
            loop = asyncio.get_running_loop()
            value = self._apply_pepper(raw_password)

            try:
                salt = bcrypt.gensalt(rounds=self._rounds)
                hash_bytes = await loop.run_in_executor(
                    self._executor,
                    functools.partial(bcrypt.hashpw, value, salt),
                )
                return PasswordHash(hash_bytes.decode("utf-8"))

            except Exception as e:
                logger.critical(
                    "password_hasher.hash_failed", error=str(e), exc_info=True
                )
                raise PasswordHasherError(
                    "PasswordHasher failed to process password"
                ) from e

    async def verify(
        self, *, raw_password: RawPassword, hashed_password: PasswordHash
    ) -> bool:
        async with self._permit():
            loop = asyncio.get_running_loop()
            value = self._apply_pepper(raw_password)

            try:
                return await loop.run_in_executor(
                    self._executor,
                    functools.partial(
                        bcrypt.checkpw,
                        value,
                        hashed_password.value.encode("utf-8"),
                    ),
                )

            except Exception:
                logger.exception("password_hasher.verify_failed")
                return False

    def _apply_pepper(self, password: RawPassword) -> bytes:
        raw = password.value.encode("utf-8") + self._pepper
        return base64.b64encode(hashlib.sha256(raw).digest())

    def _permit(self) -> AbstractAsyncContextManager[None]:
        return self._acquire_lock(
            semaphore=self._semaphore, timeout=self._wait_timeout_s
        )

    @staticmethod
    @asynccontextmanager
    async def _acquire_lock(
        semaphore: asyncio.Semaphore, timeout: float
    ) -> AsyncIterator[None]:
        try:
            await asyncio.wait_for(
                semaphore.acquire(),
                timeout=timeout,
            )
        except TimeoutError as err:
            raise PasswordHasherIsBusyError("Password hasher is too busy") from err

        try:
            yield
        finally:
            semaphore.release()
