import sqlite3
from pathlib import Path


class MemoryStore:
    """Persistent SQLite-backed memory for Aegis."""

    def __init__(self, db_path: str = "data/aegis.db"):
        self.db_path = Path(db_path)

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize(self) -> None:
        """Create the memory table if it does not exist."""

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.commit()

    def add(self, content: str) -> int:
        """Store a memory and return its ID."""

        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO memories (content) VALUES (?)",
                (content,),
            )

            connection.commit()

            return cursor.lastrowid

    def get_all(self) -> list[str]:
        """Return all stored memories."""

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT content
                FROM memories
                ORDER BY created_at ASC
                """
            ).fetchall()

        return [row[0] for row in rows]