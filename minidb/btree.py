ORDER = 4

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []

class BTree:
    def __init__(self):
        self.root = BTreeNode()

    def search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]

        if node.leaf:
            return None

        return self.search(node.children[i], key)

def split_child(self, parent, index):
    full_child = parent.children[index]
    new_child = BTreeNode(leaf=full_child.leaf)
    mid = ORDER // 2

    parent.keys.insert(index, full_child.keys[mid])
    parent.values.insert(index, full_child.values[mid])
    parent.children.insert(index + 1, new_child)

    new_child.keys = full_child.keys[mid + 1:]
    new_child.values = full_child.values[mid + 1:]

    full_child.keys = full_child.keys[:mid]
    full_child.values = full_child.values[:mid]

    if not full_child.leaf:
        new_child.children = full_child.children[mid + 1:]
        full_child.children = full_child.children[:mid + 1]

def insert_non_full(self, node, key, value):
    i = len(node.keys) - 1

    if node.leaf:
        node.keys.append(None)
        node.values.append(None)

        while i >= 0 and key < node.keys[i]:
            node.keys[i + 1] = node.keys[i]
            node.values[i + 1] = node.values[i]
            i -= 1

        node.keys[i + 1] = key
        node.values[i + 1] = value
    else:
        while i >= 0 and key < node.keys[i]:
            i -= 1
        i += 1

        if len(node.children[i].keys) == ORDER - 1:
            self.split_child(node, i)

            if key > node.keys[i]:
                i += 1

        self.insert_non_full(node.children[i], key, value)