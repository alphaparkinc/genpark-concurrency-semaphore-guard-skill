"""Example usage for Concurrency Semaphore Guard."""
from client import ConcurrencySemaphoreGuard
import json

guard = ConcurrencySemaphoreGuard(max_concurrency=3, rate_limit_per_min=10)

# Acquire lease for worker 1
res = guard.acquire("worker_101")
print("Acquire 101:", json.dumps(res))

# Release lease
rel = guard.release("worker_101")
print("Release 101:", json.dumps(rel))
