from minidb.table import Table

class MiniDB:

    def __init__(self):
        self.tables = {}

    def create_table(self, name: str):
        if name in self.tables:
            raise Exception("Table already exists")

        self.tables[name] = Table(name)

    def get_table(self, name: str):
        if name not in self.tables:
            raise Exception("Table not found")

        return self.tables[name]