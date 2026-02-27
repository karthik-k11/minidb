from minidb.query import CreateTable, Insert, Select
import time

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

            start_time = time.perf_counter()

            if command.key == "ALL":
                result = table.scan_all()
                plan = "Full Table Scan"
            else:
                key = int(command.key)
                result = table.select(key)
                plan = "Index Lookup"

            end_time = time.perf_counter()
            elapsed = end_time - start_time

            return {
                "plan": plan,
                "result": result,
                "time": elapsed
            }

        else:
            raise Exception("Unknown command type")