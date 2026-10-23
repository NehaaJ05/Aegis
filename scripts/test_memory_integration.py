
from pathlib import Path
from tempfile import TemporaryDirectory

from aegis.agent.core import AegisAgent


def main():
    with TemporaryDirectory() as temp_dir:
        db_path = str(Path(temp_dir) / "aegis_test.db")
        agent = AegisAgent(memory_path=db_path)

        # A new preference should be stored automatically.
        agent.memory.add("My favourite editor is VS Code.")
        for fact in agent.extractor.extract("My favourite editor is VS Code."):
            agent.memory.remember(**fact)

        results = agent.memory.search("editor")
        assert results[0] == "favorite_editor: VS Code"

        # A changed preference should update the same key.
        for fact in agent.extractor.extract("My favourite editor is PyCharm."):
            agent.memory.remember(**fact)

        results = agent.memory.search("editor")
        assert results[0] == "favorite_editor: PyCharm"
        assert "favorite_editor: VS Code" not in results

        # The database should contain only one structured editor preference.
        all_memories = agent.memory.get_all()
        editor_facts = [
            item for item in all_memories
            if item.startswith("favorite_editor:")
        ]
        assert editor_facts == ["favorite_editor: PyCharm"]

    print("All memory integration tests passed.")


if __name__ == "__main__":
    main()
