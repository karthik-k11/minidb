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
        keys = self.keys[:MAX_KEYS]
        keys += [0] * (MAX_KEYS - len(keys))

        values = self.values[:MAX_KEYS]
        values += [0] * (MAX_KEYS - len(values))

        children = self.children[:ORDER]
        children += [0] * (ORDER - len(children))

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

    def insert(self, key, value):
        root = self.read_node(self.root_page)

        if len(root.keys) == MAX_KEYS:
            new_root_page = self.pager.allocate_page()
            new_root = DiskBTreeNode(new_root_page, leaf=False)

            new_root.children.append(self.root_page)

            self.root_page = new_root_page

            self.split_child(new_root, 0)
            self.write_node(new_root)

            root = new_root

        self.insert_non_full(root, key, value)
        
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
    
    def insert_non_full(self, node, key, value):
        i = len(node.keys) - 1

        if node.leaf:
            node.keys.append(0)
            node.values.append(0)

            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
            self.write_node(node)

        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            child = self.read_node(node.children[i])

            if len(child.keys) == MAX_KEYS:
                self.split_child(node, i)
                node = self.read_node(node.page_id)

                if key > node.keys[i]:
                    i += 1

            child = self.read_node(node.children[i])
            self.insert_non_full(child, key, value)
        
    def scan_all(self):
        results = []
        self._inorder_traverse(self.root_page, results)
        return results

    def _inorder_traverse(self, page_id, results):
        node = self.read_node(page_id)

        for i in range(len(node.keys)):
            if not node.leaf:
                self._inorder_traverse(node.children[i], results)

            results.append((node.keys[i], node.values[i]))

        if not node.leaf:
            self._inorder_traverse(node.children[len(node.keys)], results)