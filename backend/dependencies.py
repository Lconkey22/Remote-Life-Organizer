"""FastAPI dependencies for shared application components."""

from __future__ import annotations

from backend.store.memory_store import InMemoryStore

_STORE = InMemoryStore()


def get_store() -> InMemoryStore:
    """Return the shared in-memory store instance."""

    return _STORE
