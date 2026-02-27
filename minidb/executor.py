from minidb.query import CreateTable, Insert, Select


class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, command):
        if isinstance(command, CreateTable):
            self.db.create_table(command.table_name)
            return "Table created"

        elif isinstance(command, Insert):
            table = self.db.get_table(command.table_name)
            table.insert(command.key, command.value)
            return "Inserted"

        elif isinstance(command, Select):
            table = self.db.get_table(command.table_name)
            result = table.select(command.key)
            return result

        else:
            raise Exception("Unknown command type")