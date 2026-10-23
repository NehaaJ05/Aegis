
from pathlib import Path
from tempfile import TemporaryDirectory

from aegis.memory.store import MemoryStore


def main():
    with TemporaryDirectory() as temp_dir:
        db_path = str(Path(temp_dir) / "test.db")
        memory = MemoryStore(db_path)

        memory.remember(
            "favorite_editor", "VS Code", category="preference"
        )
        memory.remember(
            "field_of_study", "Computer Science", category="fact"
        )
        
        assert "favorite_editor: VS Code" in memory.search("editor")

        # Updating an existing key replaces its value.
        memory.remember(
            "favorite_editor", "PyCharm", category="preference"
        )
        assert memory.search("editor") == [
            "favorite_editor: PyCharm"
        ]

        # Forgetting a memory should work only once.
        assert memory.forget("favorite_editor") is True
        assert memory.forget("favorite_editor") is False

        assert memory.get_all() == [
            "field_of_study: Computer Science"
        ]

    print("All structured memory tests passed.")


if __name__ == "__main__":
    main()
