
from aegis.memory.extractor import FactExtractor


def main():
    extractor = FactExtractor()

    # British and American spellings
    assert extractor.extract("My favourite editor is VS Code.") == [
        {
            "key": "favorite_editor",
            "value": "VS Code",
            "category": "preference",
        }
    ]

    assert extractor.extract("My favorite editor is PyCharm!") == [
        {
            "key": "favorite_editor",
            "value": "PyCharm",
            "category": "preference",
        }
    ]

    # Basic facts
    assert extractor.extract("I am studying Computer Science.") == [
        {
            "key": "field_of_study",
            "value": "Computer Science",
            "category": "fact",
        }
    ]

    assert extractor.extract("I study Data Science.") == [
        {
            "key": "field_of_study",
            "value": "Data Science",
            "category": "fact",
        }
    ]

    # Messages that should not produce facts
    assert extractor.extract("Hello Aegis!") == []
    assert extractor.extract("Which editor should I use?") == []
    assert extractor.extract("VS Code is popular.") == []

    print("All fact extractor tests passed.")


if __name__ == "__main__":
    main()
