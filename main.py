from cli import start_cli
from minidb.pager import Pager

pager = Pager()
page_id = pager.allocate_page()

page = pager.read_page(page_id)
page.write(0, b"HelloPage")

pager.write_page(page)

page2 = pager.read_page(page_id)
print(page2.read(0, 9))

if __name__ == "__main__":
    start_cli()