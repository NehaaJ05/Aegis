
from pathlib import Path
from tempfile import TemporaryDirectory

from aegis.agent.core import AegisAgent


class FakeLLM:
    """Avoid requiring Ollama during integration tests."""

    def generate(self, messages):
        return "Test response."


def main():
    with TemporaryDirectory() as temp_dir:
        db_path = str(Path(temp_dir) / "aegis_test.db")
        agent = AegisAgent(memory_path=db_path)

        # Replace the real model with a predictable test double.
        agent.llm = FakeLLM()

        response = agent.run("My favourite editor is VS Code.")
        assert response == "Test response."

        # The agent should extract and persist the fact automatically.
        results = agent.memory.search("editor")
        assert "favorite_editor: VS Code" in results

        # A new statement should update the same structured fact.
        agent.run("My favourite editor is PyCharm.")

        results = agent.memory.search("editor")
        assert "favorite_editor: PyCharm" in results
        assert "favorite_editor: VS Code" not in results

        # Confirm persistence by opening the same database again.
        reopened_memory = AegisAgent(memory_path=db_path).memory
        results = reopened_memory.search("editor")
        assert "favorite_editor: PyCharm" in results
        assert "favorite_editor: VS Code" not in results

    print("All agent memory integration tests passed.")


if __name__ == "__main__":
    main()
