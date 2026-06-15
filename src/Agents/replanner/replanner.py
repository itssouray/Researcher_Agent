import ast

from src.llm.openai_client import llm

from src.Agents.replanner.prompts import (
    REPLANNER_PROMPT
)

from src.state.research_state import (
    Task,
    ResearchState,
)


class Replanner:

    def replan(
        self,
        state: ResearchState,
    ) -> list[Task]:

        latest_reflection = (
            state.reflections[-1]
        )

        existing_tasks = "\n".join(
            [
                task.description
                for task in state.tasks
            ]
        )

        response = llm.invoke(
            [
                ("system", REPLANNER_PROMPT),
                (
                    "user",
                    f"""
Goal:
{state.goal}

Existing Tasks:
{existing_tasks}

Reflection:
{latest_reflection.feedback}
""",
                ),
            ]
        )

        task_descriptions = ast.literal_eval(
            response.content
        )

        new_tasks = []

        next_id = (
            max(
                task.id
                for task in state.tasks
            )
            + 1
        )

        for task_desc in task_descriptions:

            new_tasks.append(
                Task(
                    id=next_id,
                    description=task_desc,
                )
            )

            next_id += 1

        state.tasks.extend(
            new_tasks
        )

        state.replan_count += 1

        return new_tasks