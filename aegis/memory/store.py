import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

class MemoryStore:
    """Persistent SQLite-backed structured memory for Aegis."""

    def __init__(self, db_path: str = "data/aegis.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    
    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.db_path)
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()


    def _initialize(self) -> None:
        """Create the structured memory table without deleting legacy data."""

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS structured_memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL UNIQUE,
                    value TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT 'fact',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add(self, content: str) -> int:
        """Preserve the legacy API for storing free-form memories."""

        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO memories (content) VALUES (?)",
                (content,),
            )
            return cursor.lastrowid

    def get_all(self) -> list[str]:
        """Return legacy and structured memories when their tables exist."""

        with self._connect() as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }

            results = []

            if "memories" in tables:
                rows = connection.execute(
                    "SELECT content FROM memories ORDER BY id ASC"
                ).fetchall()
                results.extend(row[0] for row in rows)

            if "structured_memories" in tables:
                rows = connection.execute(
                    """
                    SELECT key, value
                    FROM structured_memories
                    ORDER BY key ASC
                    """
                ).fetchall()
                results.extend(
                    f"{row[0]}: {row[1]}" for row in rows
                )

        return results

    def search(self, query: str, limit: int = 5) -> list[str]:
        """Search legacy and structured memories using keyword matching."""

        if limit <= 0:
            return []

        terms = list(dict.fromkeys(
            term.casefold().strip(".,!?;:'\"()[]{}")
            for term in query.split()
            if len(term.strip(".,!?;:'\"()[]{}")) >= 3
        ))

        if not terms:
            return []

        matches = []

        with self._connect() as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }

            for term in terms:
                if "memories" in tables:
                    rows = connection.execute(
                        """
                        SELECT content
                        FROM memories
                        WHERE instr(lower(content), lower(?)) > 0
                        ORDER BY id DESC
                        LIMIT ?
                        """,
                        (term, limit),
                    ).fetchall()

                    matches.extend(row[0] for row in rows)

                if "structured_memories" in tables:
                    rows = connection.execute(
                        """
                        SELECT key, value
                        FROM structured_memories
                        WHERE instr(lower(key), lower(?)) > 0
                           OR instr(lower(value), lower(?)) > 0
                        ORDER BY updated_at DESC
                        LIMIT ?
                        """,
                        (term, term, limit),
                    ).fetchall()

                    matches.extend(
                        f"{row[0]}: {row[1]}" for row in rows
                    )

        return list(dict.fromkeys(matches))[:limit]

    def remember(
        self,
        key: str,
        value: str,
        category: str = "fact",
    ) -> None:
        """Create or update a structured memory by key."""

        key = key.strip().casefold()
        value = value.strip()
        category = category.strip().casefold()

        if not key or not value or not category:
            raise ValueError("Key, value, and category must not be empty.")

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO structured_memories (key, value, category)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    category = excluded.category,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (key, value, category),
            )

    def forget(self, key: str) -> bool:
        """Delete a structured memory. Return whether one existed."""

        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM structured_memories WHERE key = ?",
                (key.strip().casefold(),),
            )
            return cursor.rowcount > 0
