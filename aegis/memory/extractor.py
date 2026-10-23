
import re


class FactExtractor:
    """Extract explicit facts and preferences from user messages."""

    PATTERNS = [
        (
            re.compile(
                r"\bmy favourite editor is (?P<value>.+?)[.!?]*$",
                re.IGNORECASE,
            ),
            "favorite_editor",
            "preference",
        ),
        (
            re.compile(
                r"\bmy favorite editor is (?P<value>.+?)[.!?]*$",
                re.IGNORECASE,
            ),
            "favorite_editor",
            "preference",
        ),
        (
            re.compile(
                r"\bi(?:'m| am) studying (?P<value>.+?)[.!?]*$",
                re.IGNORECASE,
            ),
            "field_of_study",
            "fact",
        ),
        (
            re.compile(
                r"\bi study (?P<value>.+?)[.!?]*$",
                re.IGNORECASE,
            ),
            "field_of_study",
            "fact",
        ),
    ]

    def extract(self, message: str) -> list[dict[str, str]]:
        """Return structured facts explicitly stated in a message."""
        facts = []

        for pattern, key, category in self.PATTERNS:
            match = pattern.search(message.strip())

            if match:
                value = match.group("value").strip().rstrip(".!? ")

                if value:
                    facts.append(
                        {
                            "key": key,
                            "value": value,
                            "category": category,
                        }
                    )

                break

        return facts
