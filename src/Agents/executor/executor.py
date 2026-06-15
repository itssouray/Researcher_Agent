from src.Agents.executor.prompts import (
    EXECUTOR_PROMPT
)

from src.llm.openai_client import llm

from src.tools.RAG.retriever import Retriever

from src.state.research_state import (
    Task,
    Finding,
    ResearchState,
)


class Executor:

    def __init__(self):

        self.retriever = Retriever()

    def execute_task(
        self,
        task: Task,
        state: ResearchState,
        k: int = 5,
    ):

        if task.status != "pending":
            return

        # ReAct Step 1: Retrieve Evidence
        results = self.retriever.retrieve(
            query=task.description,
            k=k,
        )

        # ReAct Step 2: Observe
        context = "\n\n".join(
            [
                f"""
Source: {item["source"]}
Page: {item["page"]}

{item["text"]}
"""
                for item in results
            ]
        )

        # ReAct Step 3: Reason
        response = llm.invoke(
            [
                ("system", EXECUTOR_PROMPT),
                (
                    "user",
                    f"""
Task:
{task.description}

Evidence:
{context}
""",
                ),
            ]
        )

        # Store task result
        task.result = response.content
        task.status = "completed"

        # Store evidence in state
        for item in results:

            state.findings.append(
                Finding(
                    task_id=task.id,
                    source=item["source"],
                    page=item["page"],
                    content=item["text"],
                    score=item["score"],
                )
            )