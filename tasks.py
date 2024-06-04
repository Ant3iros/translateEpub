from crewai import Task
from textwrap import dedent

# This is an example of how to define custom tasks.
# You can define as many tasks as you want.
# You can also define custom agents in agents.py
class CustomTasks:
    def __tip_section(self):
        return "rester sur de la donnée vérifiée, n'inventez pas, basez vous sur le référentiel"

    def translate(self, agent, var1):
        return Task(
            description=dedent(
                f"""

                traduit cet extrait de roman en français, essaye de respecter un format roman

                fait des retours à la ligne là où il te semble correct comme lorsqu'un personnage parle par exemple.

                Le texte : { var1 }

                """
            ),
            agent=agent,
            expected_output="un rapport",
            tools=[]
        )
