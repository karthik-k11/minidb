from cli import start_cli
from minidb.pager import Pager
from minidb.btree import BTree
from minidb.disk_btree import DiskBTree

pager = Pager()
page_id = pager.allocate_page()

page = pager.read_page(page_id)
page.write(0, b"HelloPage")

pager.write_page(page)

page2 = pager.read_page(page_id)
print(page2.read(0, 9))

tree = BTree()

for i in [10, 20, 5, 6, 12, 30, 7, 17]:
    tree.insert(i, str(i))

print(tree.search(tree.root, 6))
print(tree.search(tree.root, 17))

tree = DiskBTree()

tree.insert_simple(10, 100)
tree.insert_simple(5, 50)
tree.insert_simple(20, 200)

print(tree.search(0, 5))
print(tree.search(0, 20))

for i in [10, 20, 5, 6, 12, 30, 7, 17, 3, 4, 8]:
    tree.insert(i, i * 10)

print(tree.search(tree.root_page, 3))
print(tree.search(tree.root_page, 17))
print(tree.search(tree.root_page, 30))

if __name__ == "__main__":
    start_cli()