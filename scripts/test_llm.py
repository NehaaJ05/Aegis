from aegis.agent.llm import LocalLLM


def main():
    llm = LocalLLM()

    response = llm.generate(
        "Explain what a database is in one sentence."
    )

    print("\nAegis response:")
    print(response)


if __name__ == "__main__":
    main()