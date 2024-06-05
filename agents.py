from crewai import Agent
from textwrap import dedent
from decouple import config
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq


# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
class CustomAgents:
    def __init__(self):
        self.GroqLlm = ChatGroq(temperature=0, groq_api_key = config("GROQ_API_KEY"), model_name='llama3-70b-8192')


    def translator(self):
        return Agent(
            role="translator",
            backstory=dedent(r"""You are a professionnal translator"""),
            goal=dedent(f"""
                Tu es un traducteur professionnel, tu traduis des romans en français. 
                """),
            allow_delegation=True,
            verbose=True,
            llm=self.GroqLlm,
            tools=[]
        )
 
