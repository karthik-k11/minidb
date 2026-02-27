class CreateTable:
    def __init__(self, table_name):
        self.table_name = table_name


class Insert:
    def __init__(self, table_name, key, value):
        self.table_name = table_name
        self.key = int(key)
        self.value = int(value)


class Select:
    def __init__(self, table_name, key):
        self.table_name = table_name
        self.key = key

class BulkInsert:
    def __init__(self, table_name, count):
        self.table_name = table_name
        self.count = int(count)

def parse(command: str):
    parts = command.strip().split()

    if not parts:
        return None

    cmd = parts[0].upper()

    if cmd == "CREATE" and parts[1].upper() == "TABLE":
        return CreateTable(parts[2])

    elif cmd == "INSERT":
        return Insert(parts[1], parts[2], parts[3])

    elif cmd == "SELECT":
        if parts[2].upper() == "ALL":
            return Select(parts[1], "ALL")
        else:
            return Select(parts[1], parts[2])
    else:
        raise Exception("Invalid command")