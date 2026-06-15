from src.Agents.planner.planner import Planner
from src.Agents.executor.executor import Executor
from src.Agents.reflector.reflector import Reflector
from src.Agents.replanner.replanner import Replanner

from src.state.research_state import ResearchState
from src.report.report_generator import (
    ReportGenerator
)


class ResearchWorkflow:

    def __init__(self):

        self.planner = Planner()
        self.executor = Executor()
        self.reflector = Reflector()
        self.replanner = Replanner()
        self.report_generator = (ReportGenerator())

    def run(self, goal: str):

        state = ResearchState(
            goal=goal
        )

        # Planning
        state.tasks = self.planner.create_plan(
            goal
        )

        while True:

            # Execute pending tasks
            for task in state.tasks:

                if task.status == "pending":

                    self.executor.execute_task(
                        task,
                        state
                    )

            # Reflect
            reflection = (
                self.reflector.reflect(
                    state
                )
            )

            print(
                reflection.feedback
            )

            if reflection.passed:

                break

            if (
                state.replan_count
                >= state.max_replans
            ):
                break

            new_tasks = self.replanner.replan(state)

            if not new_tasks:
                break
        
        self.report_generator.generate(state)
        
        return state