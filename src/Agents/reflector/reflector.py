from src.llm.openai_client import llm

from src.Agents.reflector.prompts import (
    REFLECTOR_PROMPT
)

from src.state.research_state import (
    Reflection,
    ResearchState,
)


class Reflector:

    def reflect(
        self,
        state: ResearchState,
    ) -> Reflection:

        completed_results = "\n\n".join(
            [
                f"""
Task:
{task.description}

Result:
{task.result}
"""
                for task in state.tasks
                if task.status == "completed"
            ]
        )

        response = llm.invoke(
            [
                ("system", REFLECTOR_PROMPT),
                (
                    "user",
                    f"""
Goal:
{state.goal}

Research Results:
{completed_results}
""",
                ),
            ]
        )

        content = response.content.strip()

        passed = content.startswith("PASS")

        reflection = Reflection(
            passed=passed,
            feedback=content,
        )

        state.reflections.append(
            reflection
        )

        return reflection