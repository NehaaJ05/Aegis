from typing import Callable

from aegis.agent.llm import LocalLLM
from aegis.memory.store import MemoryStore


class AegisAgent:
    """Core Aegis agent responsible for reasoning, memory, and tools."""

    def __init__(
        self,
        model: str = "llama3:latest",
        memory_path: str = "data/aegis.db",
    ):
        self.llm = LocalLLM(model=model)
        self.memory = MemoryStore(memory_path)

        self.tools: dict[str, Callable] = {}
        self.history: list[dict[str, str]] = []

    def register_tool(self, name: str, function: Callable) -> None:
        """Register a callable tool with the agent."""
        self.tools[name] = function

    def run(self, prompt: str) -> str:
        """Process a user request using conversation and persistent memory."""

        self.history.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        memories = self.memory.search(prompt)

        context_messages = []

        if memories:
            memory_context = "\n".join(
                f"- {memory}"
                for memory in memories
            )

            context_messages.append(
                {
                    "role": "system",
                    "content": (
                        "The following are relevant memories about the user. "
                        "Use them when appropriate, but do not invent information "
                        "that is not present in the memories.\n\n"
                        f"{memory_context}"
                    ),
                }
            )

        context_messages.extend(self.history)

        response = self.llm.generate(context_messages)

        self.history.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        self.memory.add(prompt)

        return response