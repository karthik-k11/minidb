from typing import Dict

class StorageEngine:

    def __init__(self):
        self._store: Dict[bytes, bytes] = {}

    def put(self, key: bytes, value: bytes) -> None:
        if not isinstance(key, bytes) or not isinstance(value, bytes):
            raise TypeError("Keys and values must be bytes")

        self._store[key] = value

    def get(self, key: bytes) -> bytes:
        if key not in self._store:
            raise KeyError("Key not found")

        return self._store[key]

    def delete(self, key: bytes) -> None:
        if key not in self._store:
            raise KeyError("Key not found")

        del self._store[key]

    def count(self) -> int:
        return len(self._store)

    def stats(self) -> dict:
        return {
            "keys": len(self._store),
            "memory_bytes": sum(len(k) + len(v) for k, v in self._store.items())
        }