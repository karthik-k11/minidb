import struct
from pathlib import Path


class LogStorage:
    PUT = 1
    DELETE = 2

    HEADER_FORMAT = ">BII"  

    def __init__(self, file_path="minidb.data"):
        self.file_path = Path(file_path)
        self.file_path.touch(exist_ok=True)

    def append_put(self, key: bytes, value: bytes):
        with self.file_path.open("ab") as f:
            header = struct.pack(
                self.HEADER_FORMAT,
                self.PUT,
                len(key),
                len(value)
            )
            f.write(header)
            f.write(key)
            f.write(value)

    def append_delete(self, key: bytes):
        with self.file_path.open("ab") as f:
            header = struct.pack(
                self.HEADER_FORMAT,
                self.DELETE,
                len(key),
                0
            )
            f.write(header)
            f.write(key)

    def replay(self):
        store = {}

        with self.file_path.open("rb") as f:
            while True:
                header_bytes = f.read(struct.calcsize(self.HEADER_FORMAT))
                if not header_bytes:
                    break

                op, key_size, value_size = struct.unpack(
                    self.HEADER_FORMAT,
                    header_bytes
                )

                key = f.read(key_size)

                if op == self.PUT:
                    value = f.read(value_size)
                    store[key] = value

                elif op == self.DELETE:
                    store.pop(key, None)

        return store