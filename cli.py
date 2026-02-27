from minidb.db_engine import MiniDB
from minidb.query import parse
from minidb.executor import Executor


def start_cli():
    db = MiniDB()
    executor = Executor(db)

    print("MiniDB v0.2")
    print("Commands:")
    print("CREATE TABLE name")
    print("INSERT table key value")
    print("SELECT table key")
    print("EXIT")

    while True:
        try:
            command_str = input("minidb> ")

            if command_str.upper() == "EXIT":
                break

            command = parse(command_str)
            if command is None:
                continue

            result = executor.execute(command)
            print(result)

        except Exception as e:
            print("Error:", e)