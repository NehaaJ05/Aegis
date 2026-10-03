from aegis.memory.store import MemoryStore


def main():
    memory = MemoryStore()

    memory.add("My name is Nehaa.")
    memory.add("I am studying computer science.")
    memory.add("I prefer VS Code.")

    print("Stored memories:")

    for item in memory.get_all():
        print(f"- {item}")


if __name__ == "__main__":
    main()