"""Concurrency Semaphore Guard.
100% Python Standard Library.
"""
import time

class ConcurrencySemaphoreGuard:
    """In-memory concurrency leaky-bucket and fair semaphore guard."""

    def __init__(self, max_concurrency: int = 5, rate_limit_per_min: int = 60):
        self.max_concurrency = max_concurrency
        self.rate_limit_per_min = rate_limit_per_min
        self.active_leases = set()
        self.history = []

    def acquire(self, lease_id: str, current_time: float = None) -> dict:
        now = current_time or time.time()
        self.history = [t for t in self.history if now - t <= 60.0]

        if len(self.active_leases) >= self.max_concurrency:
            return {"acquired": False, "reason": "Concurrency capacity reached"}

        if len(self.history) >= self.rate_limit_per_min:
            return {"acquired": False, "reason": "Rate limit (RPM) exceeded"}

        self.active_leases.add(lease_id)
        self.history.append(now)
        return {
            "acquired": True,
            "lease_id": lease_id,
            "current_concurrency": len(self.active_leases),
            "remaining_rpm": self.rate_limit_per_min - len(self.history)
        }

    def release(self, lease_id: str) -> dict:
        if lease_id in self.active_leases:
            self.active_leases.remove(lease_id)
            return {"released": True, "active_leases_count": len(self.active_leases)}
        return {"released": False, "error": "Lease ID not found"}
