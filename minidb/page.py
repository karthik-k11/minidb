PAGE_SIZE = 4096


class Page:
    def __init__(self, page_id: int, data: bytes = None):
        self.page_id = page_id

        if data:
            if len(data) != PAGE_SIZE:
                raise ValueError("Invalid page size")
            self.data = bytearray(data)
        else:
            self.data = bytearray(PAGE_SIZE)

    def read(self, offset: int, size: int) -> bytes:
        return bytes(self.data[offset: offset + size])

    def write(self, offset: int, payload: bytes):
        self.data[offset: offset + len(payload)] = payload