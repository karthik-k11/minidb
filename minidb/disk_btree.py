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
class DiskBTree:
    def __init__(self, file_path="minidb.tree"):
        self.pager = Pager(file_path)

        if self.pager.file_path.stat().st_size == 0:
            root_page = self.pager.allocate_page()
            root = DiskBTreeNode(root_page, leaf=True)
            self.write_node(root)

        self.root_page = 0

    def read_node(self, page_id):
        page = self.pager.read_page(page_id)
        return DiskBTreeNode.deserialize(page_id, page.data)

    def write_node(self, node):
        page = self.pager.read_page(node.page_id)
        page.write(0, node.serialize())
        self.pager.write_page(page)

    def search(self, page_id, key):
        node = self.read_node(page_id)

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]

        if node.leaf:
            return None

        return self.search(node.children[i], key)

    def insert_simple(self, key, value):
        node = self.read_node(self.root_page)

        if len(node.keys) >= MAX_KEYS:
            raise Exception("Root full (splitting tomorrow)")

        i = len(node.keys) - 1
        node.keys.append(0)
        node.values.append(0)

        while i >= 0 and key < node.keys[i]:
            node.keys[i + 1] = node.keys[i]
            node.values[i + 1] = node.values[i]
            i -= 1

        node.keys[i + 1] = key
        node.values[i + 1] = value

        self.write_node(node)
        
    def split_child(self, parent, index):
        full_child = self.read_node(parent.children[index])
        new_page_id = self.pager.allocate_page()
        new_child = DiskBTreeNode(new_page_id, leaf=full_child.leaf)
        mid = MAX_KEYS // 2
        promoted_key = full_child.keys[mid]
        promoted_value = full_child.values[mid]
        new_child.keys = full_child.keys[mid + 1:]
        new_child.values = full_child.values[mid + 1:]
        full_child.keys = full_child.keys[:mid]
        full_child.values = full_child.values[:mid]
        
        if not full_child.leaf:
            new_child.children = full_child.children[mid + 1:]
            full_child.children = full_child.children[:mid + 1]
        parent.keys.insert(index, promoted_key)
        parent.values.insert(index, promoted_value)
        parent.children.insert(index + 1, new_page_id)
        self.write_node(full_child)
        self.write_node(new_child)
        self.write_node(parent)