import ast

from src.llm.openai_client import llm

from src.Agents.planner.prompts import (
    PLANNER_PROMPT
)

from src.state.research_state import (
    Task
)


class Planner:

    def create_plan(
        self,
        goal: str
    ) -> list[Task]:

        response = llm.invoke(
            [
                ("system", PLANNER_PROMPT),
                ("user", goal),
            ]
        )

        task_descriptions = ast.literal_eval(
            response.content
        )

        tasks = []

        for idx, task in enumerate(
            task_descriptions,
            start=1
        ):
            tasks.append(
                Task(
                    id=idx,
                    description=task
                )
            )

        return tasks