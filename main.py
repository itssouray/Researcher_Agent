from src.orchestration.research_workflow import ResearchWorkflow
from src.tools.RAG.ingest import Ingestor


def main():
    """
    Entry point for the Software Architecture Research Agent.

    Uncomment the ingestion step when adding new documents
    to the knowledge base.
    """

    # Build / rebuild the vector database
    # ingestor = Ingestor()
    # ingestor.ingest()

    research_goal = (
        "Explain everything involved when a user logs into a web application."
    )

    workflow = ResearchWorkflow()

    state = workflow.run(research_goal)

    print("\n" + "=" * 80)
    print("FINAL RESEARCH REPORT")
    print("=" * 80 + "\n")

    print(state.final_report)


if __name__ == "__main__":
    main()