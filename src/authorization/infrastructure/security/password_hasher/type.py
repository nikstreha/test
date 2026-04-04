import asyncio
from concurrent.futures import ThreadPoolExecutor


class PasswordHasherThreadPoolExecutor(ThreadPoolExecutor):
    pass


class PasswordHasherSemaphore(asyncio.Semaphore):
    pass
