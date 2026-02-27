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
            if isinstance(result, dict):
                print(f"Execution Plan: {result['plan']}")

                if result["plan"] == "Bulk Insert":
                    print(f"Rows Inserted: {result['rows']}")

                elif result["plan"] == "Full Table Scan":
                    print(f"Rows Returned: {len(result['result'])}")
                    print(result["result"])

                else: 
                    print(f"Result: {result['result']}")
                    print(f"Time: {result['time']:.6f} sec")

            else:
                print(result)

        except Exception as e:
            print("Error:", e)