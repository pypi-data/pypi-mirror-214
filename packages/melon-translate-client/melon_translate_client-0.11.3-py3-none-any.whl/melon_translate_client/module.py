import redis_lock
from redis_om import Migrator, get_redis_connection


class LockContextManager:
    """Lock context manager."""

    def __init__(self, lock):
        self.lock = lock

    def __enter__(self):
        try:
            self.lock.acquire(timeout=1)
        except redis_lock.NotAcquired:
            return None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()


class TranslateClientModule:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.conn = get_redis_connection()
        self.lock = redis_lock.Lock(self.conn, "melon_translate_process_lock")
        Migrator().run()

    def lock_context(self) -> LockContextManager:
        """Return lock context manager."""
        return LockContextManager(self.lock)


translate_module = None
