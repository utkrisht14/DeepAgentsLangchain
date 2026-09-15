# Module 1 — Building a Deep Agent
## Lesson 1 — Deep Agents Overview

> **Purpose:** Learning notes for understanding what Deep Agents are, why they exist, where they fit in the LangChain ecosystem, and the main capabilities we will study in later lessons.

---

## 1. Learning Objectives

By the end of this lesson, you should be able to explain:

- What a **Deep Agent** is.
- Why Deep Agents are useful for **long-horizon, multi-step tasks**.
- Where Deep Agents fit relative to **LangChain** and **LangGraph**.
- What an **agent harness** means.
- The main capabilities included in Deep Agents.
- When to use Deep Agents instead of a simpler LangChain agent.
- The basic shape of a Deep Agent program.

---

# 2. What is a Deep Agent?

A **Deep Agent** is an opinionated, batteries-included **agent harness** in the LangChain ecosystem.

It is designed for tasks where an agent may need to:

1. Understand a complex goal.
2. Break the goal into smaller tasks.
3. Use tools.
4. Work with files.
5. Manage a large amount of context.
6. Delegate work to subagents.
7. Remember useful information.
8. Ask for human approval when necessary.
9. Continue working across many steps.

A Deep Agent still uses the familiar **LLM → tool call → tool result → LLM** agent loop.

The difference is that Deep Agents provide many additional capabilities around that loop automatically.

---

# 3. The Most Important Definition

> **Deep Agents are an agent harness built on LangChain agents and the LangGraph runtime, designed for complex, multi-step work.**

The word **deep** does **not** mean:

- Deep Learning
- A deeper neural network
- More model layers

It refers to the ability of an agent to perform **deeper, longer, multi-step work**.

---

# 4. What is an Agent Harness?

An LLM by itself can generate text.

A normal agent adds things such as:

```text
LLM
 ↓
Reason about task
 ↓
Choose a tool
 ↓
Execute tool
 ↓
Observe result
 ↓
Continue
```

But complex real-world tasks require much more infrastructure.

For example:

```text
User Goal
   ↓
Plan the task
   ↓
Track progress
   ↓
Use tools
   ↓
Save intermediate information
   ↓
Manage context
   ↓
Delegate subtasks
   ↓
Execute code if required
   ↓
Ask for approval if required
   ↓
Combine results
   ↓
Final answer
```

The collection of infrastructure surrounding the model and agent loop is the **agent harness**.

Deep Agents provide this harness with useful defaults already included.

---

# 5. LangChain vs LangGraph vs Deep Agents

A useful mental model is:

```text
┌────────────────────────────────────┐
│            Deep Agents             │
│                                    │
│ Planning                           │
│ Filesystem                         │
│ Context Management                 │
│ Skills                             │
│ Memory                             │
│ Subagents                          │
│ Human-in-the-Loop                  │
│ Execution Environment              │
└─────────────────┬──────────────────┘
                  │
                  ▼
┌────────────────────────────────────┐
│          LangChain Agents          │
│                                    │
│ Model                              │
│ Tools                              │
│ System Prompt                      │
│ Middleware                         │
│ Agent / Tool Calling Loop          │
└─────────────────┬──────────────────┘
                  │
                  ▼
┌────────────────────────────────────┐
│             LangGraph              │
│                                    │
│ State                              │
│ Threads                            │
│ Checkpoints                        │
│ Persistence                        │
│ Streaming                          │
│ Interrupt / Resume                 │
│ Durable Execution                  │
└────────────────────────────────────┘
```

### LangGraph

LangGraph is the lower-level **runtime and orchestration layer**.

It is useful when you need very fine control over:

- states
- nodes
- edges
- workflow transitions
- persistence
- interrupts
- custom deterministic + agentic workflows

### LangChain Agent

LangChain provides the standard agent abstraction.

Conceptually:

```python
agent = create_agent(
    model=model,
    tools=tools
)
```

This is a good choice when the task is relatively simple and you mainly need:

```text
Model + Prompt + Tools + Agent Loop
```

### Deep Agents

Deep Agents sit at a higher level.

Conceptually:

```python
agent = create_deep_agent(...)
```

You still have:

```text
Model
Tools
System Prompt
```

but the harness can additionally provide capabilities such as:

```text
Planning
Filesystem
Context management
Subagents
Skills
Memory
Execution environments
Human-in-the-loop
```

---

# 6. Why Do Deep Agents Exist?

Consider this request:

> Research five AI companies, analyze their products, compare their pricing, inspect recent developments, save your research, and produce a detailed report.

A simple agent could theoretically perform this task.

But problems quickly appear.

## Problem 1 — Long Tasks Need Planning

The agent may need to perform many operations.

Without planning, it may:

- forget parts of the task
- repeat work
- stop too early
- perform steps in a poor order

Deep Agents can use task planning to manage this.

Conceptually:

```text
TODO

[ ] Research Company A
[ ] Research Company B
[ ] Research Company C
[ ] Compare pricing
[ ] Compare products
[ ] Synthesize findings
[ ] Write report
```

## Problem 2 — Context Windows Become Large

Imagine a research agent performs:

```text
20 searches
10 webpage reads
5 document reads
multiple tool calls
```

Putting every result into the main conversation can create **context bloat**.

Deep Agents can use:

- filesystem storage
- summarization
- context offloading
- subagents

to keep the useful context manageable.

We will study this deeply in **Module 3 — Context Management**.

## Problem 3 — One Agent Should Not Do Everything

Some tasks naturally contain specialized subtasks.

Example:

```text
Main Research Agent
        │
        ├── Financial Research Agent
        │
        ├── Competitor Research Agent
        │
        └── Technical Research Agent
```

The main agent acts more like a coordinator.

Deep Agents support this through **delegation and subagents**.

We will study this in **Module 4 — Delegation**.

## Problem 4 — Agents Need Somewhere to Work

Complex agents may need to:

```text
read files
write files
edit files
search files
execute programs
run shell commands
store intermediate results
```

Deep Agents provide abstractions for execution environments and filesystem backends.

We will study this in **Module 2 — Execution Environment**.

---

# 7. Core Capabilities of Deep Agents

Deep Agents combine several capabilities into one harness.

## 7.1 Planning

Deep Agents can break large goals into smaller tasks and track progress.

A built-in planning mechanism can maintain TODO-style tasks.

Example:

```text
Goal:
Create a competitor analysis report.

Plan:
1. Identify competitors
2. Research each competitor
3. Compare features
4. Compare pricing
5. Summarize strengths/weaknesses
6. Generate report
```

## 7.2 Tools

Deep Agents can use normal LangChain tools.

Examples:

```text
Web search
Database query
Weather API
Calculator
REST API
Python function
Internal company API
```

They can also work with tools exposed through **MCP**.

Tools are covered later in Module 1.

## 7.3 Filesystem

Deep Agents can work with a virtual filesystem.

Typical operations include:

```text
ls
read_file
write_file
edit_file
glob
grep
```

The filesystem can be used as a form of **working memory**.

Instead of keeping a massive result in the prompt:

```text
Huge research result
        ↓
conversation context
```

the agent can do:

```text
Huge research result
        ↓
/research/company_a.md
        ↓
Read only when needed
```

## 7.4 Context Management

Long-running agents need to control what information remains inside the model's context window.

Deep Agents support techniques such as:

```text
Summarization
      +
Offloading
      +
Filesystem
      +
Subagent isolation
```

The goal is:

> Give the model the **right context**, not necessarily **all context**.

## 7.5 Subagents

A Deep Agent can delegate tasks to specialized agents.

Example:

```text
Supervisor Agent
      │
      ├── Research Subagent
      │
      ├── Coding Subagent
      │
      └── Analysis Subagent
```

A major advantage is **context isolation**.

The subagent can perform many internal tool calls while the parent agent receives mainly the final useful result.

## 7.6 Skills

Skills are reusable sets of:

```text
instructions
domain knowledge
workflows
best practices
```

that an agent can load when required.

Instead of placing every possible instruction into one enormous system prompt, specialized knowledge can be activated when needed.

## 7.7 Memory

Deep Agents can work with persistent memory.

This can allow useful information to survive beyond one immediate interaction.

Conceptually:

```text
Thread 1
   ↓
save useful information
   ↓
Persistent Store
   ↓
Thread 2
   ↓
retrieve information
```

Memory will be covered in Module 3.

## 7.8 Human-in-the-Loop (HITL)

Some actions should not happen automatically.

For example:

```text
Delete file
Send email
Execute sensitive command
Make payment
Modify production data
```

A Deep Agent can pause before the action:

```text
Agent wants to execute action
           ↓
        INTERRUPT
           ↓
     Human reviews
       /       \
   Approve     Reject
      ↓           ↓
   Continue     Change path
```

This capability comes from the LangGraph runtime underneath the agent.

## 7.9 Execution Environment

Some agents need more than API tools.

They may need to:

```text
run Python
run shell commands
create files
execute tests
install packages
analyze datasets
build software
```

Deep Agents can work with different execution backends, including isolated sandbox environments.

This is the focus of Module 2.

---

# 8. Deep Agent Architecture

A simplified architecture is:

```text
                         USER
                           │
                           ▼
                 ┌─────────────────┐
                 │   Deep Agent    │
                 │   Coordinator   │
                 └────────┬────────┘
                          │
              ┌───────────┼────────────┐
              │           │            │
              ▼           ▼            ▼
           Planning     Tools      Filesystem
              │           │            │
              └───────────┼────────────┘
                          │
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
             Subagents        Context Mgmt
                 │                 │
                 └────────┬────────┘
                          │
                          ▼
                     Final Result
```

Underneath this sits the LangGraph runtime:

```text
Deep Agent Harness
       ↓
LangChain Agent
       ↓
LangGraph Runtime
```

---

# 9. A Deep Agent is Still an Agent

Do not imagine Deep Agents as a completely different AI architecture.

At the center is still approximately this loop:

```text
User Message
     ↓
LLM
     ↓
Does the model need a tool?
     │
 ┌───┴────┐
 │        │
No       Yes
 │        │
 ▼        ▼
Answer   Tool Call
          ↓
      Tool Result
          ↓
          LLM
```

Deep Agents add powerful infrastructure **around this loop**.

This is an important concept.

---

# 10. Simple Agent vs Deep Agent

| Capability | Simple LangChain Agent | Deep Agent |
|---|---|---|
| LLM | ✅ | ✅ |
| System Prompt | ✅ | ✅ |
| Tools | ✅ | ✅ |
| Tool-calling loop | ✅ | ✅ |
| Planning | Can be built | Built-in support |
| Filesystem | Can be added | Built-in support |
| Context management | Manual/custom | Built-in mechanisms |
| Subagents | Can be built | Built-in support |
| Skills | Manual/custom | Supported |
| Persistent memory | Can be added | Supported |
| HITL | Possible with LangGraph | Integrated with LangGraph |
| Long multi-step work | Possible | Main design goal |

---

# 11. When Should You Use Deep Agents?

Deep Agents are especially useful for tasks such as:

### Research Agents

```text
Research topic
→ search many sources
→ delegate research
→ store findings
→ compare evidence
→ create report
```

### Coding Agents

```text
Inspect repository
→ modify files
→ run tests
→ inspect failures
→ fix code
→ verify result
```

### Data Analysis Agents

```text
Load data
→ execute code
→ inspect outputs
→ create intermediate files
→ analyze results
→ produce report
```

### Complex Business Agents

```text
Read documents
→ query systems
→ create plan
→ call APIs
→ ask for approval
→ perform action
→ generate summary
```

---

# 12. When Deep Agents May Be Overkill

Suppose your application is:

```text
User: What is the weather in Amsterdam?

Agent:
1. Call weather tool
2. Return answer
```

You probably do **not** need a Deep Agent.

A normal LangChain agent may be enough.

Another example:

```text
User question
     ↓
Retrieve documents
     ↓
Generate answer
```

A simple RAG application may also not require the full Deep Agent harness.

---

# 13. Rule of Thumb

Use:

```text
Simple Tool Calling
        ↓
LangChain Agent
```

when your application is relatively small and straightforward.

Use:

```text
Complex
Multi-step
Long-running
Context-heavy
Delegation-heavy
        ↓
Deep Agents
```

when you want the agent harness capabilities out of the box.

Use:

```text
Highly custom workflow
Deterministic + agentic control
Custom state transitions
        ↓
LangGraph
```

when you need to design the workflow itself.

---

# 14. Small Implementation Preview

> We will study running a Deep Agent properly in **Lesson 2**.  
> For Lesson 1, this example is only meant to show the basic API shape.

Install:

```bash
pip install -U deepagents langchain-openai
```

Set your API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-api-key"
```

Minimal example:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="openai:gpt-5.5",
    system_prompt="You are a helpful learning assistant."
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Explain why context management is important for AI agents."
            }
        ]
    }
)

print(result["messages"][-1].content)
```

At a high level:

```text
create_deep_agent(...)
        ↓
Deep Agent is created
        ↓
agent.invoke(...)
        ↓
User message enters agent
        ↓
Model reasons and uses harness capabilities if needed
        ↓
Final response
```

Do not worry yet about every parameter.

Upcoming lessons will separately cover:

```text
Model
System Prompt
Tools
MCP
Messages
Threads
Checkpointer
HITL
```

---

# 15. The Five Modules — Big Picture

Our learning path is:

```text
MODULE 1
Building a Deep Agent
        ↓
Learn the main building blocks

MODULE 2
Execution Environment
        ↓
Learn where/how the agent works and executes

MODULE 3
Context Management
        ↓
Learn how long-running agents control information

MODULE 4
Delegation
        ↓
Learn how agents delegate to subagents

MODULE 5
Putting It All Together
        ↓
Build a complete Deep Agent project
```

---

# 16. Important Terminology

| Term | Meaning |
|---|---|
| **Agent** | An LLM-driven system capable of choosing actions/tools |
| **Agent Harness** | Infrastructure surrounding the agent loop that helps the agent work effectively |
| **Deep Agent** | LangChain's batteries-included harness for complex multi-step agents |
| **Tool** | A function/capability the model can invoke |
| **Tool Calling** | The model deciding that a tool should be executed |
| **Filesystem** | Storage the agent can use for files and working context |
| **Backend** | Implementation of storage/execution used by the agent |
| **Context** | Information currently available to the model |
| **Context Management** | Controlling what information enters/stays in the model context |
| **Subagent** | Another agent delegated a specific task |
| **Skill** | Reusable instructions/workflow/domain capability loaded when needed |
| **Memory** | Information persisted for later use |
| **Thread** | A continuing conversation/execution identity |
| **Checkpointer** | Saves workflow state so execution can be resumed |
| **HITL** | Human-in-the-loop approval or intervention |
| **MCP** | Model Context Protocol; a standard way to expose external tools/context to agents |

---

# 17. Deep Agents and MCP

Do not confuse these two.

### MCP answers:

> **How can an agent connect to external tools and services in a standardized way?**

### Deep Agents answers:

> **How can an agent organize and execute complex, long-running work?**

They can be used together:

```text
Deep Agent
    │
    ├── Planning
    ├── Filesystem
    ├── Context Management
    ├── Subagents
    │
    └── Tools
          │
          ├── Normal Python Tool
          ├── REST API Tool
          └── MCP Tools
                 │
                 ├── GitHub
                 ├── Database
                 └── Other MCP Servers
```

We will study MCP in Module 1, Lesson 6.

---

# 18. Deep Agents and Context Engineering

One of the most important themes of Deep Agents is **context engineering**.

A capable agent does not simply need a powerful model.

It needs:

```text
Right model
    +
Right instructions
    +
Right tools
    +
Right information
    +
Right amount of context
    +
Right time
```

This becomes increasingly important as the task becomes longer.

A useful principle:

> **The goal is not to give the model all available information. The goal is to give it the information it needs to make the next good decision.**

---

# 19. Key Mental Model

Think of a basic LLM as a smart worker.

```text
LLM
=
Smart Worker
```

A LangChain agent gives the worker tools.

```text
LLM + Tools
=
Worker with equipment
```

A Deep Agent gives the worker something closer to a complete working environment.

```text
Deep Agent
=
Worker
+ Tools
+ Workspace
+ Notes
+ Task List
+ Specialists
+ Memory
+ Execution Environment
+ Safety / Approval Mechanisms
```

This is why the term **agent harness** is useful.

---

# 20. Common Misconceptions

### ❌ Deep Agents use a special "deep" neural network

No.

They can use different tool-calling LLMs.

### ❌ Deep Agents replace LangGraph

No.

Deep Agents use LangGraph underneath for runtime capabilities.

### ❌ Deep Agents replace LangChain

No.

Deep Agents are built using LangChain agent building blocks.

### ❌ Every AI agent should be a Deep Agent

No.

Simple applications may be better implemented with a normal LangChain agent or a custom LangGraph workflow.

### ❌ Subagents automatically mean multiple independent AI systems

Not necessarily.

Subagents are an architectural pattern for delegating work and isolating context. Their exact model, tools, prompts, and behavior are configurable.

---

# 21. Interview-Level Explanation

If someone asks:

### "What are Deep Agents in LangChain?"

A strong short answer is:

> **Deep Agents are LangChain's batteries-included agent harness for building long-horizon, multi-step agents. They run on the LangGraph runtime and provide built-in capabilities such as planning, filesystem-based context management, subagent delegation, skills, memory, execution environments, and human-in-the-loop workflows.**

---

# 22. Revision Cheat Sheet

Remember:

```text
Deep Agents
    =
Agent Harness
    +
LangChain Agent
    +
LangGraph Runtime
```

Main purpose:

```text
Complex
Long-horizon
Multi-step
Agentic work
```

Main capabilities:

```text
Planning
Filesystem
Context Management
Execution
Subagents
Skills
Memory
HITL
Tools / MCP
```

Architecture:

```text
Deep Agents
    ↓
LangChain Agent
    ↓
LangGraph
```

Use Deep Agents when:

```text
task complexity ↑
number of steps ↑
context size ↑
need for delegation ↑
need for persistence ↑
```

---

# 23. Self-Check Questions

Before moving to Lesson 2, you should be able to answer:

1. What is a Deep Agent?
2. What does **agent harness** mean?
3. Does Deep Agents replace LangGraph?
4. What is the relationship between Deep Agents, LangChain, and LangGraph?
5. Why are files useful for long-running agents?
6. Why are subagents useful?
7. What problem does context management solve?
8. What is HITL?
9. What is the difference between MCP and Deep Agents?
10. When would a normal LangChain agent be preferable to a Deep Agent?

---

# 24. One-Line Summary

> **Deep Agents provide a batteries-included harness on top of LangChain and LangGraph so an agent can plan, manage context, use a workspace, delegate work, remember information, execute actions, and handle complex multi-step tasks more reliably.**

---

## Official References

- LangChain Deep Agents Overview: https://docs.langchain.com/oss/python/deepagents/overview
- Deep Agents Quickstart: https://docs.langchain.com/oss/python/deepagents/quickstart
- LangChain / LangGraph / Deep Agents concepts: https://docs.langchain.com/oss/python/concepts/products
- Deep Agents GitHub repository: https://github.com/langchain-ai/deepagents
- LangChain Academy: https://academy.langchain.com/courses/take/foundation-introduction-to-deepagents/

---

**Next:** Module 1 — Lesson 2: **Running a Deep Agent**
