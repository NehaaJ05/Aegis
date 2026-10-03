from typing import Callable
from aegis.agent.llm import LocalLLM

class AegisAgent:
    """Core Aegis agent responsible for reasoning and tool execution"""
    def __init__(self, model : str="llama3:latest"):
        self.llm=LocalLLM(model=model)
        self.tools:dict[str,Callable]={}
        self.history:list[dict[str,str]]=[]

    def register_tool(self,name:str,function:Callable)-> None:
        """Register a callable tool with the agent"""
        self.tools[name]=function

    def run(self,prompt:str) -> str:
        """Process a user request and return a response"""
        self.history.append(
            {
                "role":"user",
                "content":prompt,
            }
        )

        response=self.llm.generate(self.history)

        self.history.append(
            {
                "role":"assistant",
                "content":response,
            }
        )

        return response