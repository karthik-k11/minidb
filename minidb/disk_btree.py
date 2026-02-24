import struct
from minidb.pager import Pager
from minidb.page import PAGE_SIZE

ORDER = 4
MAX_KEYS = ORDER - 1


class DiskBTreeNode:
    FORMAT = ">B I 3i 3i 4i"
    # B = is_leaf
    # I = key_count
    # 3i = keys
    # 3i = values
    # 4i = children

    SIZE = struct.calcsize(FORMAT)

    def __init__(self, page_id, leaf=True):
        self.page_id = page_id
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []

    def serialize(self):
        key_count = len(self.keys)

        keys = self.keys + [0] * (MAX_KEYS - len(self.keys))
        values = self.values + [0] * (MAX_KEYS - len(self.values))
        children = self.children + [0] * (ORDER - len(self.children))

        return struct.pack(
            self.FORMAT,
            int(self.leaf),
            key_count,
            *keys,
            *values,
            *children
        )

    @classmethod
    def deserialize(cls, page_id, data):
        unpacked = struct.unpack(cls.FORMAT, data[:cls.SIZE])

        leaf = bool(unpacked[0])
        key_count = unpacked[1]

        keys = list(unpacked[2:2 + MAX_KEYS])[:key_count]
        values = list(unpacked[2 + MAX_KEYS:2 + 2 * MAX_KEYS])[:key_count]
        children = list(unpacked[2 + 2 * MAX_KEYS:])

        node = cls(page_id, leaf)
        node.keys = keys
        node.values = values
        node.children = children if not leaf else []

        return node