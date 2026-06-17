# Software Researcher Agent

A research-oriented AI agent system built from scratch to explore how modern agent architectures evolve over time.

This project is not intended to be a production-ready AI application. Instead, it serves as a learning platform for understanding the core building blocks behind modern agent systems such as planning, execution, reflection, replanning, and retrieval-augmented generation (RAG).

The implementation intentionally avoids agent frameworks like LangGraph, CrewAI, and AutoGen in order to expose the underlying architecture and design decisions.

---

# Motivation

Modern AI agent frameworks abstract away many important concepts:

* State management
* Agent communication
* Planning
* Reflection
* Replanning
* Retrieval systems

While these abstractions increase developer productivity, they can make it difficult to understand how agent systems actually work.

This project focuses on implementing these concepts manually to gain a deeper understanding of agent architecture evolution.

---

# Learning Journey

This project is part of a larger Agent Evolution journey.

Architectures explored so far:

1. ReAct
2. Planning
3. Execution
4. Reflection
5. Replanning
6. RAG (Retrieval-Augmented Generation)

Memory has intentionally been excluded from Version 1 and will only be introduced when a real limitation appears.

---

# Project Goal

Given a software engineering research question, the system should:

1. Create a research plan
2. Break the problem into research tasks
3. Gather evidence from a knowledge base
4. Evaluate research coverage
5. Identify missing information
6. Generate follow-up tasks when needed
7. Produce a final research report

Example research questions:

* PostgreSQL vs MongoDB
* REST vs GraphQL
* Redis vs RabbitMQ
* SQL vs NoSQL
* Docker vs Kubernetes
* Monolith vs Microservices
* How applications interact with the kernel
* How a web request travels from browser to database
* Difference between Disk and RAM

---

# Architecture Overview

```text
User Goal
    │
    ▼
Planner
    │
    ▼
Research Tasks
    │
    ▼
Executor
    │
    ▼
RAG Retrieval
    │
    ▼
Findings
    │
    ▼
Reflector

PASS?
├── YES
│     │
│     ▼
│ Report Generator
│
└── NO
      │
      ▼
 Replanner
      │
      ▼
 New Tasks
      │
      ▼
 Executor

(loop until success or limits reached)
```

---

# Core Design Principle

State is the source of truth.

Agents never communicate directly.

Instead, all communication happens through a shared state object.

```text
Planner
   │
   ▼
 State
   ▲
   │

Executor
Reflector
Replanner
Report Generator
```

This mirrors the architecture used by many graph-based and state-machine-based agent systems.

---

# Folder Structure

```text
software-architecture-research-agent/

src/

├── agents/
│
│ ├── planner/
│ │ ├── planner.py
│ │ └── prompts.py
│ │
│ ├── executor/
│ │ ├── executor.py
│ │ └── prompts.py
│ │
│ ├── reflector/
│ │ ├── reflector.py
│ │ └── prompts.py
│ │
│ └── replanner/
│ ├── replanner.py
│ └── prompts.py
│
├── orchestration/
│ └── research_workflow.py
│
├── state/
│ └── research_state.py
│
├── tools/
│ └── rag/
│ ├── embeddings.py
│ ├── chunking.py
│ ├── vector_store.py
│ ├── ingest.py
│ └── retriever.py
│
├── llm/
│ └── openai_client.py
│
├── config/
│ └── settings.py
│
├── report/
│ ├── report_generator.py
│ └── prompts.py
│
└── main.py

data/

├── documents/
└── vectordb/

.env
README.md
```

---

# State Design

The entire workflow revolves around a shared state object.

```python
@dataclass
class Task:
    id: int
    description: str
    status: str = "pending"
    result: str | None = None


@dataclass
class Finding:
    task_id: int
    source: str
    page: int
    content: str
    score: float


@dataclass
class Reflection:
    passed: bool
    feedback: str


@dataclass
class ResearchState:
    goal: str
    tasks: list[Task]
    findings: list[Finding]
    reflections: list[Reflection]

    replan_count: int = 0
    max_replans: int = 3

    final_report: str | None = None
```

### Design Decision

Tasks are stored once and tracked through status updates:

* pending
* completed
* failed

This avoids maintaining multiple task collections and prevents synchronization issues.

---

# Components

## Planner

Responsible for transforming a research goal into actionable research tasks.

Input:

```text
Goal
```

Output:

```text
Research Tasks
```

The planner does not perform retrieval, execution, or reasoning.

---

## Executor

The executor acts as a lightweight ReAct-style agent.

Workflow:

```text
Task
 ↓
Retrieve Evidence
 ↓
Observe Results
 ↓
Reason
 ↓
Generate Findings
```

Responsibilities:

* Query the retriever
* Analyze retrieved evidence
* Produce task results
* Update task status
* Store findings in state

---

## RAG System

The RAG system functions as a knowledge library.

It does not reason.

It only retrieves relevant information.

Reasoning happens inside the Executor.

### Workflow

```text
Query
 ↓
Embedding
 ↓
FAISS Search
 ↓
Top K Chunks
 ↓
Metadata Lookup
 ↓
Results
```

---

## Reflector

Evaluates research completeness.

The reflector is not responsible for fact-checking.

Instead, it answers:

```text
Do we have enough information
to answer the research goal?
```

Output:

```python
Reflection(
    passed=True,
    feedback="..."
)
```

or

```python
Reflection(
    passed=False,
    feedback="Missing information..."
)
```

---

## Replanner

Triggered when reflection fails.

Responsibilities:

* Analyze reflection feedback
* Generate additional research tasks
* Avoid duplicate tasks
* Improve research coverage

Workflow:

```text
Research Gap
 ↓
New Tasks
 ↓
Executor
```

---

## Report Generator

Produces the final research report.

Typical report structure:

* Overview
* Key Findings
* Trade-offs
* Recommendations

The report is generated using completed task results stored in state.

---

# Knowledge Base

The knowledge base consists of PDF documents stored in:

```text
data/documents/
```

Example content:

* Operating Systems
* DBMS
* Computer Networks
* Software Engineering
* System Design
* Big Data
* OOP
* Mobile Application Development
* Theory of Computation

---

# Embeddings

Model:

```text
all-MiniLM-L6-v2
```

Library:

```text
sentence-transformers
```

Embeddings are generated locally.

No external embedding APIs are used.

---

# Chunking Strategy

Library:

```text
RecursiveCharacterTextSplitter
```

Configuration:

```python
chunk_size = 1000
chunk_overlap = 200
```

Chunking occurs page-by-page to preserve source and page metadata.

---

# Vector Database

Library:

```text
FAISS
```

Files:

```text
data/vectordb/

knowledge_base.faiss
metadata.pkl
```

A single global vector index is maintained.

The current implementation rebuilds the index during ingestion.

Incremental indexing is intentionally deferred to keep focus on agent architecture.

---

# Metadata Structure

```python
{
    "id": 0,
    "source": "document.pdf",
    "page": 12,
    "text": "..."
}
```

This enables future support for citations and source attribution.

---

# Research Workflow

```text
Goal
 ↓
Planner
 ↓
Tasks

LOOP

Execute Pending Tasks
 ↓
Reflect

PASS?
├── YES
│     ↓
│ Report Generator
│
└── NO
      ↓
 Replanner
      ↓
 Execute Again
```

Exit conditions:

```python
reflection.passed
```

or

```python
state.replan_count >= state.max_replans
```

or

```python
no_new_tasks_generated
```

---

# Sample Results

### Successful Queries

* How do applications interact with the kernel?
* How does an Android application communicate with a database server?
* What happens when a user logs into a web application?

### Knowledge Gap Detection

The system correctly identified insufficient information for:

* Kafka vs Pulsar
* Scalable URL Shortener Design

Instead of hallucinating answers, the workflow:

```text
Research
 ↓
Reflection
 ↓
Gap Detection
 ↓
Replanning
 ↓
Still Insufficient
 ↓
Fail Gracefully
```

This behavior validates the reflection and replanning architecture.

---

# Key Lessons Learned

### 1. State Is Everything

The most important architectural component is the shared state.

State enables agent coordination without direct communication.

### 2. RAG Is Not An Agent

RAG retrieves information.

The Executor performs reasoning.

### 3. Reflection Drives Quality

Many failures originate from poor evaluation criteria rather than poor execution.

Well-designed reflection significantly improves research quality.

### 4. Replanning Requires Reflection

Without reflection, replanning has no signal.

Reflection provides the feedback loop needed to generate meaningful follow-up tasks.

### 5. Knowledge Coverage Becomes the Bottleneck

Once the architecture stabilizes, system quality becomes increasingly dependent on knowledge base coverage rather than agent logic.

---

# Future Improvements

Future evolution should be driven by observed limitations rather than feature accumulation.

Potential directions:

* Source citations in reports
* Multi-step retrieval
* Hybrid search
* Web search integration
* Improved reflection heuristics
* Retrieval quality improvements
* Memory (only when a real limitation appears)

---

# Tech Stack

* Python
* OpenAI API
* FAISS
* Sentence Transformers
* LangChain Text Splitters
* Dataclasses
* PDF Processing Libraries

---

# Project Philosophy

The purpose of this repository is not to build the most powerful agent.

The purpose is to understand how agent systems evolve.

Every architectural component exists because a limitation was encountered in a previous version.

The project emphasizes learning through implementation, iteration, failure analysis, and architectural evolution.
