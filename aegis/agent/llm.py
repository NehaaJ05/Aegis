from ollama import chat

class LocalLLM:
    """Interface btw Aegis and local running Ollama model"""

    def __init__(self,model: str="llama3:latest"):
        self.model=model

    def generate(self,prompt:str) -> str:
        """Generate a response from local LLM"""
        response=chat(
            model=self.model,
            messages=[
                {
                    "role":"user",
                    "content":prompt,
                }
            ],
        )
        return response["message"]["content"]