from aegis.agent.core import AegisAgent

def main():
    agent=AegisAgent()
    print("Aegis is online! Type 'exit' to quit.\n")

    while True:
        prompt = input("You: ").strip()

        if prompt.lower()=="exit":
            break

        if not prompt:
            continue

        response = agent.run(prompt)
        print(f"\nAegis: {response}\n")

if __name__=="__main__":
    main()