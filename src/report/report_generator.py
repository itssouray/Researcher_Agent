from src.llm.openai_client import llm

from src.report.prompts import (
    REPORT_PROMPT
)

from src.state.research_state import (
    ResearchState
)


class ReportGenerator:

    def generate(
        self,
        state: ResearchState,
    ) -> str:

        task_results = "\n\n".join(
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
                ("system", REPORT_PROMPT),
                (
                    "user",
                    f"""
Goal:
{state.goal}

Research Results:
{task_results}
""",
                ),
            ]
        )

        state.final_report = (
            response.content
        )

        return state.final_report