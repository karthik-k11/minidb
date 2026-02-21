from minidb.engine import StorageEngine


def start_cli():
    engine = StorageEngine()

    print("MiniDB v0.1 (in-memory)")
    print("Commands: PUT key value | GET key | DEL key | COUNT | EXIT")

    while True:
        try:
            command = input("minidb> ").strip()

            if not command:
                continue

            parts = command.split()

            if parts[0].upper() == "PUT":
                key = parts[1].encode()
                value = parts[2].encode()
                engine.put(key, value)
                print("OK")

            elif parts[0].upper() == "GET":
                key = parts[1].encode()
                value = engine.get(key)
                print(value.decode())

            elif parts[0].upper() == "DEL":
                key = parts[1].encode()
                engine.delete(key)
                print("Deleted")

            elif parts[0].upper() == "COUNT":
                print(engine.count())

            elif parts[0].upper() == "EXIT":
                break

            else:
                print("Unknown command")

        except Exception as e:
            print("Error:", e)