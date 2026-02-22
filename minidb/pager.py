from pathlib import Path
from minidb.page import Page, PAGE_SIZE


class Pager:
    def __init__(self, file_path="minidb.pages"):
        self.file_path = Path(file_path)
        self.file_path.touch(exist_ok=True)

    def read_page(self, page_id: int) -> Page:
        with self.file_path.open("rb") as f:
            f.seek(page_id * PAGE_SIZE)
            data = f.read(PAGE_SIZE)

            if len(data) < PAGE_SIZE:
                data += b"\x00" * (PAGE_SIZE - len(data))

            return Page(page_id, data)

    def write_page(self, page: Page):
        with self.file_path.open("r+b") as f:
            f.seek(page.page_id * PAGE_SIZE)
            f.write(page.data)

    def allocate_page(self) -> int:
        size = self.file_path.stat().st_size
        page_id = size // PAGE_SIZE

        with self.file_path.open("ab") as f:
            f.write(b"\x00" * PAGE_SIZE)

        return page_id