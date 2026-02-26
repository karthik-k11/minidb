from minidb.disk_btree import DiskBTree


class Table:

    def __init__(self, name: str):
        self.name = name
        self.index = DiskBTree(f"{name}.tree")

    def insert(self, key: int, value: int):
        self.index.insert(key, value)

    def select(self, key: int):
        return self.index.search(self.index.root_page, key)