# Deep Agents Ecosystem — Foundation Notes

> **Purpose of these notes**
>
> I am using this file as my **master reference for the complete Deep Agents ecosystem** before going lesson-by-lesson through the LangChain Academy course.
>
> This file is not tied to one lesson. It explains the main terms, layers, components, and how they connect.
>
> **No program examples are included here.**
>
> Last reviewed against the official LangChain Deep Agents documentation: **15 September 2026**.

---

# 1. My One-Line Understanding

> **Deep Agents is an opinionated agent harness built on top of LangChain agents and the LangGraph runtime for building agents that can handle long, multi-step, context-heavy tasks.**

Important:

- Deep Agents is **not another LLM**.
- Deep Agents is **not a replacement for LangChain**.
- Deep Agents is **not a replacement for LangGraph**.
- Deep Agents still uses the normal **model → tool call → tool result → model** loop.
- It adds a richer working environment around that loop.

---

# 2. The Complete Stack

My mental model:

```text
Application / User Interface
          │
          ▼
┌───────────────────────────────┐
│          Deep Agents          │
│      Opinionated Harness      │
│                               │
│ Filesystem                    │
│ Context Management            │
│ Subagents                     │
│ Skills                        │
│ Memory                        │
│ Summarization                 │
│ HITL                          │
│ Backends                      │
│ Optional Planning             │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       LangChain Agents        │
│                               │
│ Model                         │
│ Tools                         │
│ System Prompt                 │
│ Messages                      │
│ Middleware                    │
│ Agent Loop                    │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│          LangGraph            │
│            Runtime            │
│                               │
│ State                         │
│ Threads                       │
│ Checkpoints                   │
│ Persistence                   │
│ Interrupt / Resume            │
│ Streaming                     │
│ Durable Execution             │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Models + External Systems     │
│                               │
│ OpenAI / Anthropic / Google   │
│ APIs                          │
│ Databases                     │
│ MCP Servers                   │
│ Local / Remote Services       │
└───────────────────────────────┘
```

Around this stack:

```text
LangSmith
   │
   ├── Tracing
   ├── Debugging
   ├── Evaluation
   ├── Monitoring
   └── Deployment
```

---

# 3. Layer-by-Layer Responsibility

| Layer | Main responsibility |
|---|---|
| **LLM / Model** | Reasoning and deciding what to say or which tool to call |
| **LangChain** | Agent abstraction: model + tools + middleware + agent loop |
| **LangGraph** | Runtime: state, checkpoints, streaming, interrupts, resumability |
| **Deep Agents** | Opinionated harness for complex agentic work |
| **LangSmith** | Tracing, testing, evaluation, monitoring, deployment |

The most important distinction:

```text
LangGraph = Runtime
LangChain = Agent framework
Deep Agents = Agent harness
LangSmith = Observability + Evaluation + Deployment
```

---

# 4. What is an Agent?

A normal LLM mainly does:

```text
Input
  ↓
Model
  ↓
Output
```

An agent adds the ability to make decisions and take actions.

```text
User Request
     ↓
Model
     ↓
Do I need a tool?
   /        \
 No          Yes
 │            │
Answer      Tool Call
              │
              ▼
          Tool Result
              │
              ▼
             Model
              │
              ▼
           Continue
```

The loop can repeat many times.

The agent decides:

- whether it has enough information
- whether it should call a tool
- which tool should be used
- what arguments should be passed
- whether another tool call is required
- when the task is complete

---

# 5. What is an Agent Harness?

## Simple definition

> An **agent harness** is the supporting infrastructure around the LLM agent loop that helps the agent perform real work reliably.

The LLM is like the **worker**.

The harness provides the worker with:

```text
Instructions
Tools
Workspace
Files
Memory
Task delegation
Context management
Execution environment
Safety controls
Progress tracking
Persistence
```

A simple agent may only have:

```text
Model
+
Prompt
+
Tools
```

A Deep Agent can have:

```text
Model
+
Prompt
+
Tools
+
Filesystem
+
Context Management
+
Subagents
+
Memory
+
Skills
+
Execution Environment
+
HITL
+
Middleware
+
Persistence
```

That surrounding system is the **harness**.

---

# 6. Why Deep Agents Exist

A normal tool-calling agent is enough for small tasks.

Example type of task:

```text
Question
  ↓
One tool
  ↓
Answer
```

Complex tasks create additional problems.

## Problem 1 — Too many steps

The agent may need to perform many actions.

Possible issues:

- forgetting the original goal
- repeating work
- stopping too early
- losing track of progress

Deep Agents can use planning and structured workflows.

## Problem 2 — Context becomes too large

A long task may contain:

```text
Many user messages
+
Many tool calls
+
Large tool results
+
Files
+
Research
+
Intermediate results
```

The model context can become overloaded.

Deep Agents provides mechanisms such as:

- summarization
- context offloading
- filesystem
- subagent isolation
- skills
- memory
- prompt caching

## Problem 3 — One agent should not do everything

Complex work may contain specialized tasks.

```text
Supervisor
   │
   ├── Research specialist
   ├── Coding specialist
   ├── Data specialist
   └── Review specialist
```

Deep Agents provides subagent delegation.

## Problem 4 — The agent needs somewhere to work

Real agents may need to:

- read files
- write files
- search files
- modify files
- execute commands
- run code
- store intermediate results

Deep Agents provides execution environments and filesystem backends.

## Problem 5 — Some actions need human control

Examples:

- delete a file
- send an email
- modify production data
- run an expensive operation
- execute a dangerous command

Deep Agents integrates with LangGraph interrupts for human approval.

---

# 7. What `create_deep_agent()` Really Does

I should think of `create_deep_agent()` as the **assembly point**.

It brings together:

```text
Model
System Prompt
Tools
Middleware
Backend
Subagents
Skills
Memory
Checkpointer
Store
HITL configuration
Permissions
Profiles
```

Then internally Deep Agents relies on:

```text
LangChain create_agent()
        ↓
LangGraph runtime
```

So:

> `create_deep_agent()` does not create a new kind of runtime. It configures a powerful LangChain agent harness that runs on LangGraph.

---

# 8. Construction Phase vs Execution Phase

A Deep Agent has two useful phases to understand.

## Phase 1 — Construction

This happens when the agent is created.

Deep Agents resolves:

- model
- provider/model profile
- system prompt
- middleware stack
- backend
- tools
- subagents
- skills
- memory
- permissions
- HITL configuration

Then it builds the runnable agent.

## Phase 2 — Execution

This happens when the agent receives a request.

```text
User message
     ↓
LangGraph runtime
     ↓
Prepare state
     ↓
Middleware processes request
     ↓
Model call
     ↓
Tool call if needed
     ↓
Tool result added to state
     ↓
Model called again
     ↓
Repeat until complete
```

---

# 9. Model

The **model** is the LLM doing the reasoning.

Examples of model providers:

- OpenAI
- Anthropic
- Google
- OpenRouter
- Fireworks
- Baseten
- Ollama
- self-hosted models

Deep Agents is designed to be **model-agnostic**.

Main requirement:

> The model should support tool calling for the normal Deep Agents workflow.

---

# 10. System Prompt

The **system prompt** defines the agent's high-level behavior.

It can describe:

- role
- goals
- constraints
- workflow
- preferred behavior
- tool-use rules
- domain instructions
- response style

Mental model:

```text
System Prompt
=
Permanent instructions for this agent
```

The user message is different:

```text
User Message
=
Current task
```

---

# 11. Messages

Messages are the conversation records used by the agent.

Common message types conceptually:

```text
System instructions
Human message
AI message
Tool-call message
Tool-result message
```

A long-running agent may accumulate:

```text
Human
  ↓
AI
  ↓
Tool Call
  ↓
Tool Result
  ↓
AI
  ↓
Tool Call
  ↓
Tool Result
  ↓
AI
```

These messages are part of the agent's runtime state.

---

# 12. State

## Simple definition

> **State is the information LangGraph carries while the agent runs.**

State can contain things such as:

- messages
- todo items
- temporary data
- file information
- interrupt information
- custom application fields

Mental model:

```text
State
=
Current working condition of the agent
```

State changes during execution.

---

# 13. Thread

A **thread** identifies one continuing conversation/execution history.

Think:

```text
Thread A
User conversation A
Agent state A
Checkpoints A
Files scoped to A
```

and:

```text
Thread B
User conversation B
Agent state B
Checkpoints B
Files scoped to B
```

They are separate.

## Important

A thread is not the same as memory.

```text
Thread
=
One conversation/execution history

Memory
=
Information intended to survive and be useful beyond one thread
```

---

# 14. Checkpointer

## Simple definition

> A **checkpointer** saves LangGraph state so an agent can continue or resume later.

Think of it like:

```text
Game Save
```

At different points:

```text
Agent State
   ↓
Checkpoint
   ↓
Saved
```

Later:

```text
Checkpoint
   ↓
Restore
   ↓
Continue execution
```

Checkpoints are important for:

- conversation persistence
- resuming interrupted agents
- human-in-the-loop
- recovering long-running workflows
- maintaining thread state

---

# 15. Thread + Checkpointer Together

Mental model:

```text
thread_id
    │
    ▼
Identifies conversation
    │
    ▼
Checkpointer
    │
    ▼
Loads/saves state for that thread
```

For HITL resume, the same thread identity must be used so the runtime knows which interrupted execution to continue.

---

# 16. Store

A **Store** is different from a checkpointer.

## Checkpointer

Mainly concerned with:

```text
Graph execution state
Conversation state
Resume points
Interrupt state
```

## Store

Mainly concerned with:

```text
Long-term data
Cross-thread data
Persistent application information
Memory
```

Mental model:

```text
Checkpointer
=
Save the running workflow

Store
=
Save information for longer-term reuse
```

---

# 17. Tools

A tool is an action the model can choose to call.

Examples:

- search
- query database
- call REST API
- calculate
- send message
- read file
- write file
- execute code

The model does not directly execute the external action itself.

Instead:

```text
Model decides:
"I need tool X"
      ↓
Agent runtime executes tool X
      ↓
Tool returns result
      ↓
Model sees result
```

---

# 18. Built-in Tools vs Custom Tools

## Custom tools

Created for my application.

Examples:

- company database search
- booking system lookup
- weather API
- internal analytics
- custom business operation

## Harness-provided tools

Deep Agents can expose tools through built-in capabilities.

Filesystem operations include:

- `ls`
- `read_file`
- `write_file`
- `edit_file`
- `delete`
- `glob`
- `grep`

Depending on the backend, it may also expose:

- `execute`

Subagent support exposes:

- `task`

Optional planning can expose:

- `write_todos`

---

# 19. MCP

MCP = **Model Context Protocol**.

## Simple definition

> MCP is a standard way for an AI application to connect to external tools, resources, and systems.

MCP does **not** replace Deep Agents.

They solve different problems.

```text
Deep Agents
=
How the agent organizes and performs complex work

MCP
=
How external capabilities are exposed to the agent in a standard way
```

---

# 20. API vs Tool vs MCP

## API

An external service interface.

```text
Weather API
Database API
GitHub API
```

## Tool

An agent-facing action.

A tool may internally call an API.

```text
Agent
  ↓
Tool
  ↓
API
```

## MCP Server

A standardized server that can expose capabilities to an MCP client.

```text
Agent Application
      ↓
MCP Client
      ↓
MCP Server
      ↓
External System
```

---

# 21. Middleware

This is one of the most important concepts.

## Simple definition

> **Middleware is code that can intercept and modify what happens around model calls or tool execution.**

Think of middleware as layers placed around the agent loop.

```text
Agent Request
     ↓
Middleware A
     ↓
Middleware B
     ↓
Model
     ↓
Middleware B
     ↓
Middleware A
     ↓
Result
```

Middleware can influence the agent before or after important operations.

---

# 22. Why Middleware Is Different from a Tool

A tool runs when the **model chooses to call it**.

```text
Model
  ↓
"I want Tool X"
  ↓
Tool runs
```

Middleware can participate automatically without the model explicitly selecting it.

```text
Agent is about to call model
      ↓
Middleware intercepts
      ↓
Changes prompt / tools / context / state
      ↓
Model call continues
```

So:

```text
Tool
=
Something the model chooses to use

Middleware
=
Infrastructure that can modify/control the agent workflow
```

---

# 23. What Middleware Can Do

Middleware can:

- inject system-prompt instructions
- modify model requests
- dynamically add/remove tools
- validate tool calls
- summarize messages
- manage memory
- load skills
- enforce permissions
- implement HITL
- cache prompts
- repair tool-call history
- add custom state
- implement retry logic
- log or monitor execution

This makes middleware one of the main extension points of Deep Agents.

---

# 24. Deep Agents Middleware Stack

Deep Agents automatically assembles middleware.

The exact stack depends on configuration and model profile.

A useful mental model:

```text
Skills Middleware           optional
        ↓
Filesystem Middleware
        ↓
Subagent Middleware
        ↓
Summarization Middleware
        ↓
Patch Tool Calls Middleware
        ↓
Async Subagent Middleware   optional
        ↓
My Custom Middleware        optional
        ↓
Provider/Profile Middleware
        ↓
Prompt Caching Middleware
        ↓
Memory Middleware           optional
        ↓
HITL Middleware             optional
```

I do **not** need to memorize every position now.

What matters is:

> Deep Agents is powerful largely because it assembles useful middleware around a standard LangChain agent.

---

# 25. Important Built-in Middleware Concepts

## FilesystemMiddleware

Responsible for filesystem-related agent capabilities.

It can expose operations such as:

```text
read
write
edit
list
search
delete
```

It works through a backend.

## SubAgentMiddleware

Provides delegation capabilities.

It enables the main agent to hand a task to another agent.

## SummarizationMiddleware

Helps control context growth.

It can summarize older conversation history when context becomes large.

## PatchToolCallsMiddleware

Helps repair message history when tool calls are incomplete or interrupted.

This is useful around interruption/resume workflows.

## SkillsMiddleware

Makes skill metadata/instructions available to the agent.

Skills can be loaded progressively when required.

## MemoryMiddleware

Loads persistent memory/instructions into the agent context.

## HumanInTheLoopMiddleware

Pauses selected tool operations for human review.

## TodoListMiddleware

Provides structured planning through a todo list.

Important current behavior:

> Starting with Deep Agents v0.7, task planning is **opt-in**, not automatically enabled by default.

---

# 26. Planning

Planning helps an agent organize long tasks.

Conceptually:

```text
Goal
  ↓
Break into tasks
  ↓
Track status
  ↓
Complete tasks
  ↓
Final result
```

Possible task states:

```text
pending
in_progress
completed
```

Planning is useful for:

- long tasks
- complicated workflows
- weaker models that benefit from explicit structure
- showing progress in a UI

Planning is not always necessary.

A simple task may not benefit from a todo list.

---

# 27. Execution Environment

The execution environment answers:

> **Where and how can the agent actually perform work?**

Deep Agents execution environment includes several layers:

```text
Tools
+
Virtual Filesystem
+
Filesystem Permissions
+
Optional Code Execution
```

---

# 28. Virtual Filesystem

Deep Agents gives agents a filesystem-style interface.

The model can conceptually work with paths such as:

```text
/research/
/notes/
/workspace/
/memories/
```

Important:

> A virtual path does not automatically mean a physical file exists on my computer.

The actual storage location depends on the **backend**.

This explains why a file can exist inside Deep Agent state but not appear in PyCharm or Windows Explorer.

---

# 29. Backend

## Simple definition

> A **backend determines where the agent's filesystem data lives and which execution capabilities are available.**

The same filesystem interface can point to different storage systems:

```text
State
Local disk
Persistent store
Sandbox
Remote system
```

---

# 30. StateBackend

This is the default backend.

Mental model:

```text
Virtual File
    ↓
LangGraph State
```

Characteristics:

- thread-scoped
- stored in graph state
- files can persist across turns when a checkpointer is used
- files are not automatically shared across different threads
- files are not physical local files by default

Use case:

```text
Temporary working files for one agent thread
```

---

# 31. FilesystemBackend

Mental model:

```text
Virtual Filesystem
      ↓
Real Filesystem Directory
```

Characteristics:

- can work with files on disk
- can be rooted to a specific directory
- useful for coding agents or file workflows
- requires careful security boundaries

Use case:

```text
Agent works with a real project directory
```

---

# 32. StoreBackend

Mental model:

```text
Virtual Filesystem
      ↓
LangGraph Store
      ↓
Persistent Cross-Thread Data
```

Useful for:

- long-term memory
- reusable instructions
- persistent knowledge
- data shared across executions

---

# 33. CompositeBackend

A CompositeBackend acts like a **router**.

Different virtual paths can go to different storage systems.

Conceptually:

```text
/workspace/
      ↓
Local Filesystem

/memories/
      ↓
Persistent Store

/temp/
      ↓
State Backend
```

This is useful because not all agent files should have the same lifetime.

---

# 34. ContextHubBackend

A backend option for durable context stored through LangSmith Context Hub.

This belongs more to advanced/production use.

For my current course:

> Know that Deep Agents can use multiple storage backends. I do not need to master Context Hub yet.

---

# 35. Sandbox

## Simple definition

> A sandbox is an isolated environment where the agent can execute commands/code without directly using the host environment.

Mental model:

```text
My Computer
    │
    └── Isolated Sandbox
            │
            ├── Files
            ├── Shell
            ├── Commands
            └── Code execution
```

Why useful:

- safety
- reproducibility
- isolated dependencies
- coding agents
- testing
- package installation
- shell commands

---

# 36. LocalShell

LocalShell lets the agent execute shell commands on the **host machine**.

Mental model:

```text
Agent
  ↓
LocalShell
  ↓
My actual computer
```

This is powerful but less isolated.

Important:

> Local shell execution should be used carefully because the agent can act directly on the host environment.

---

# 37. Sandbox vs LocalShell

| Sandbox | LocalShell |
|---|---|
| Isolated | Runs on host |
| Safer boundary | Higher risk |
| Separate environment | Uses local environment |
| Good for untrusted execution | Better for controlled development |
| Can install/run code safely | Can modify real host files/processes |

---

# 38. Interpreter

The interpreter is different from shell execution.

Deep Agents can use an in-process JavaScript interpreter based on QuickJS.

Purpose:

- loops
- branching
- batching
- deterministic transformations
- programmatic tool calling
- dynamic subagent orchestration

It is lighter than a sandbox.

---

# 39. Interpreter vs Sandbox

## Interpreter

```text
Scoped programmable environment
No normal operating-system shell
Good for logic/orchestration
```

## Sandbox

```text
Operating-system-like isolated environment
Shell commands
Files
Dependencies
Tests
CLIs
```

So:

```text
Interpreter
=
Programmatic control

Sandbox
=
Execution environment
```

---

# 40. Filesystem Permissions

Permissions control what built-in filesystem tools are allowed to access.

Possible intentions:

```text
Allow read from /docs/
Deny access to /.env
Allow writes only to /workspace/
Require approval for sensitive paths
```

Permissions help enforce:

- security boundaries
- least privilege
- project isolation
- protection of secrets

---

# 41. Context Management

Context management answers:

> **What information should the model see right now?**

This is one of the most important problems in agent engineering.

A model has a finite context window.

A long-running agent may generate huge amounts of information.

The goal is not:

```text
Give the model everything
```

The goal is:

```text
Give the model the right information
at the right time
```

---

# 42. Context Engineering

Context engineering is broader than prompt engineering.

Prompt engineering asks:

```text
How should I phrase instructions?
```

Context engineering asks:

```text
What information should the model receive?
When?
In what form?
How much?
From where?
```

A good agent depends on:

```text
Right model
+
Right prompt
+
Right tools
+
Right memories
+
Right skills
+
Right retrieved data
+
Right amount of history
```

---

# 43. Four Main Context Problems

## 1. Context overload

Too much information.

## 2. Irrelevant context

Information exists but does not help the current decision.

## 3. Missing context

The model lacks necessary information.

## 4. Context decay

Important details get buried in a very long conversation.

Deep Agents provides multiple strategies to manage these problems.

---

# 44. Summarization

Summarization compresses older conversation history.

Instead of:

```text
100 detailed messages
```

the agent may keep:

```text
Recent detailed messages
+
Summary of older history
```

This reduces token usage.

Mental model:

```text
Old Messages
     ↓
Summarizer
     ↓
Compact Summary
```

---

# 45. Context Offloading

Offloading means moving large information out of the active model context.

Concept:

```text
Huge tool result
      ↓
Store in filesystem
      ↓
Keep reference/path in context
```

Later the agent can read it when required.

This helps prevent context bloat.

---

# 46. Summarization vs Offloading

## Summarization

```text
Large information
      ↓
Smaller representation
```

Information is compressed.

## Offloading

```text
Large information
      ↓
Stored elsewhere
      ↓
Loaded only when needed
```

Information is moved out of active context.

---

# 47. Skills

## Simple definition

> A skill is a reusable package of specialized instructions, workflows, and supporting resources that an agent can load when needed.

A skill can represent knowledge such as:

```text
How to write a legal memo
How to review Python code
How to create a financial report
How to operate a specific internal workflow
```

Skills are usually organized around a `SKILL.md`.

---

# 48. Progressive Disclosure

Skills are designed around **progressive disclosure**.

Instead of loading every skill completely into the system prompt:

```text
All skills
All instructions
All files
      ↓
Massive context
```

the agent first knows lightweight metadata.

Then:

```text
Task requires Skill X
      ↓
Load full Skill X
```

This saves context.

---

# 49. Skill vs Tool

## Skill

Teaches the agent **how to do something**.

```text
Instructions
Workflow
Best practices
Domain knowledge
```

## Tool

Lets the agent **perform an action**.

```text
Search
Query
Send
Read
Write
Execute
```

Easy memory:

```text
Skill = Know-how
Tool = Capability/action
```

---

# 50. Skill vs System Prompt

## System Prompt

Always part of the agent's base instructions.

## Skill

Can be loaded only when relevant.

So:

```text
System Prompt
=
Core behavior

Skill
=
Optional specialized behavior
```

---

# 51. Memory

## Simple definition

> Memory is persistent context that should remain useful across conversations or executions.

Examples:

- project conventions
- coding preferences
- company rules
- user preferences
- persistent instructions
- learned corrections

Deep Agents can use memory files such as `AGENTS.md`.

---

# 52. Memory vs Thread

This distinction is essential.

```text
Thread
=
One continuing conversation

Memory
=
Information that may survive across threads
```

---

# 53. Memory vs Skill

## Memory

Information remembered about:

- user
- project
- organization
- prior feedback
- conventions

## Skill

Reusable knowledge for performing a type of task.

Easy memory:

```text
Memory
=
What should I remember?

Skill
=
How should I do this kind of task?
```

---

# 54. Memory vs Checkpointer

```text
Checkpointer
=
Resume this specific workflow/thread

Memory
=
Carry useful information across workflows/threads
```

---

# 55. Retrieval

Retrieval means finding relevant information from an external knowledge source.

Examples:

- vector database
- document store
- search system
- knowledge base

Retrieval is usually **on-demand**.

Memory and skills are different concepts even though all contribute context.

---

# 56. Prompt Caching

Some model providers can cache repeated static prompt sections.

Useful repeated content may include:

- base system instructions
- memory
- skill content

Purpose:

- lower latency
- lower cost
- avoid repeatedly processing identical prompt tokens

This is mostly an optimization layer.

For learning priority:

> Understand the idea, but it is not a foundation requirement before Lesson 2.

---

# 57. Delegation

Delegation means:

> The main agent gives part of the work to another agent.

Mental model:

```text
Main Agent
    │
    ├── Task A → Subagent
    ├── Task B → Subagent
    └── Task C → Subagent
```

The main agent remains responsible for the overall goal.

---

# 58. Why Subagents Are Important

Subagents help with:

- context isolation
- specialization
- parallel work
- model specialization
- keeping supervisor context clean

Without subagents:

```text
Main Agent Context
  +
Every search
  +
Every file
  +
Every intermediate result
  =
Context bloat
```

With subagents:

```text
Main Agent
   ↓
Delegates research
   ↓
Subagent performs many tool calls
   ↓
Returns concise report
   ↓
Main Agent receives report only
```

---

# 59. Supervisor / Main Agent

The main agent often behaves like a supervisor.

Responsibilities:

- understand overall goal
- decide what should be delegated
- choose subagent
- combine results
- maintain overall task direction
- produce final answer

---

# 60. General-Purpose Subagent

Deep Agents can provide a general-purpose subagent.

Its role:

```text
Handle complex delegated tasks
without requiring a specialized custom agent
```

Important idea:

> It gives context isolation even when specialized behavior is not required.

---

# 61. Custom Subagent

A custom subagent can have its own:

- name
- description
- system prompt
- model
- tools
- middleware
- skills
- permissions

Use custom subagents when different roles need different capabilities.

---

# 62. Subagent Context Isolation

Default isolated subagent model:

```text
Parent Agent
     │
     ├── Gives task description
     │
     ▼
Subagent gets fresh context
     │
     ├── Performs work
     ├── Calls tools
     └── Produces report
     │
     ▼
Parent receives final result
```

This is sometimes called **context quarantine**.

---

# 63. Forked Subagents — Advanced

A forked subagent can continue from the parent's existing conversation context rather than starting with only a fresh task description.

Use when:

```text
Subagent must continue an investigation
that the parent has already started
```

This is more advanced than the normal isolated subagent pattern.

---

# 64. Dynamic Subagents

Dynamic subagents allow the agent to orchestrate delegation programmatically.

Instead of manually making a few normal subagent tool calls, the agent can use interpreter logic for:

- loops
- batches
- branches
- many parallel items
- recursive analysis

Useful for:

```text
Review every file
Process many tickets
Analyze many documents
Run multiple perspectives
```

Current status:

> Dynamic subagents depend on interpreter functionality that is still considered beta.

---

# 65. Async Subagents — Advanced

Normal synchronous delegation:

```text
Main Agent
   ↓
Subagent runs
   ↓
Main Agent waits
   ↓
Result returns
```

Async delegation allows longer-running workstreams that can proceed more independently.

Useful for:

- long-running tasks
- parallel workstreams
- steering while work is running
- cancellation

This is advanced compared with the normal course foundation.

---

# 66. Planning vs Delegation

These are related but different.

## Planning

```text
What tasks need to be done?
```

## Delegation

```text
Who should do each task?
```

---

# 67. Human-in-the-Loop — HITL

HITL means the agent pauses and asks a human before certain actions.

Mental model:

```text
Agent wants action
      ↓
Interrupt
      ↓
Human Review
   /   |   \
Approve Edit Reject
      ↓
Agent continues
```

---

# 68. Why HITL Is Needed

Agents can make mistakes.

Some actions have consequences.

Use HITL for:

- destructive operations
- expensive API calls
- production changes
- sending communications
- financial actions
- sensitive data operations
- interactive debugging

---

# 69. Interrupt

An interrupt pauses LangGraph execution.

```text
Running Agent
     ↓
Interrupt
     ↓
State saved
     ↓
Human decision
     ↓
Resume
```

This is a LangGraph runtime capability used by Deep Agents.

---

# 70. HITL + Checkpointer

A checkpointer is required for normal resumable HITL workflows because the runtime must save where execution stopped.

```text
Agent
  ↓
Interrupt
  ↓
Checkpoint
  ↓
Human decision
  ↓
Load checkpoint
  ↓
Resume
```

---

# 71. HITL + Thread ID

The thread identifies which interrupted workflow should be resumed.

```text
thread_id
   ↓
Find saved checkpoint
   ↓
Resume correct execution
```

So these concepts connect:

```text
HITL
+
Interrupt
+
Checkpointer
+
Thread ID
```

---

# 72. Steering

Steering means controlling or influencing agent behavior during execution.

HITL is one steering mechanism.

Other steering concepts can include:

- permissions
- human feedback
- runtime guidance
- approvals
- rejection
- modifying proposed actions

---

# 73. Profiles

Profiles are an advanced customization mechanism.

A harness profile can tune Deep Agents behavior for a particular provider or model.

Possible profile changes:

- base system prompt
- prompt suffix
- tool descriptions
- excluded tools
- additional middleware
- subagent behavior

Reason:

> Different model families may work better with slightly different harness instructions or tool descriptions.

---

# 74. Provider Profile vs Harness Profile

At a high level:

## Provider profile

Concerned more with how the model/provider client is resolved.

## Harness profile

Concerned with how the Deep Agent harness should behave for that model/provider.

This is an advanced customization topic.

---

# 75. Model-Agnostic Does Not Mean Model-Identical

Deep Agents can work with multiple providers.

Models differ in:

- tool calling quality
- context limits
- reasoning ability
- instruction following
- latency
- cost
- structured output behavior

Therefore:

```text
Same harness
≠
Identical behavior from every model
```

---

# 76. Streaming

Streaming lets the application observe the agent while it is running.

Possible streamed information:

- model messages
- tool calls
- tool results
- state values
- subagent activity

This is useful for user interfaces and debugging.

---

# 77. Tracing

Tracing records what happened during an agent run.

A trace can help answer:

- Which model call happened?
- Which tool was called?
- What arguments were passed?
- Which subagent ran?
- Where did the agent fail?
- How many tokens were used?
- How long did each step take?

LangSmith is the main LangChain ecosystem tool for this.

---

# 78. LangSmith

LangSmith is not Deep Agents itself.

It supports the broader development lifecycle.

Main uses:

```text
Tracing
Debugging
Evaluation
Monitoring
Testing
Deployment
```

Mental model:

```text
Deep Agent
   ↓
Does the work

LangSmith
   ↓
Helps me observe and improve the work
```

---

# 79. Evaluation

An agent should not be judged only by:

```text
"It looked good once."
```

Evaluation asks:

- Did it complete the task?
- Did it use correct tools?
- Was the answer accurate?
- Did it follow policy?
- Did it delegate appropriately?
- Did it avoid unnecessary calls?
- Was it reliable across many test cases?

---

# 80. Observability

Observability means being able to understand what the agent is doing at runtime.

This includes:

- traces
- tool calls
- errors
- timing
- token usage
- subagent activity
- interruptions
- state changes

For production agents, observability is essential.

---

# 81. MCP in the Deep Agents Ecosystem

MCP belongs at the tool/integration boundary.

```text
Deep Agent
   │
   ├── Normal Tool
   ├── Custom API Tool
   └── MCP Tool
          │
          ▼
      MCP Server
          │
          ▼
      External System
```

Deep Agents does not require MCP.

MCP is one way to supply capabilities.

---

# 82. ACP — Agent Client Protocol

ACP is a protocol used for connecting agent systems to compatible clients/editors.

Think:

```text
Agent
  ↕
ACP
  ↕
Editor / Client
```

This is not required for basic Deep Agents development.

---

# 83. A2A — Agent-to-Agent

A2A refers to communication between separate agent systems.

Conceptually:

```text
Agent System A
      ↕
     A2A
      ↕
Agent System B
```

This is different from Deep Agents' internal subagent delegation.

---

# 84. AG-UI

AG-UI belongs to the agent-to-user-interface communication space.

Think:

```text
Agent Backend
      ↕
     AG-UI
      ↕
Frontend
```

This is not required for the Academy foundation modules.

---

# 85. Frontend vs Agent Runtime

The frontend is what the user interacts with.

Examples:

- web app
- chat UI
- terminal UI
- IDE extension

The agent runtime is where the agent logic executes.

```text
Frontend
   ↓
Deep Agent
   ↓
LangGraph Runtime
```

---

# 86. Deep Agents Code / `dcode`

Deep Agents Code is a prebuilt coding-agent product built on the Deep Agents SDK.

Think:

```text
deepagents SDK
=
Building blocks

Deep Agents Code / dcode
=
A ready-made coding agent built with those blocks
```

This is useful as a reference implementation but is not required for learning the SDK fundamentals.

---

# 87. Managed Deep Agents

Managed Deep Agents belongs to the deployment/managed ecosystem.

For now:

> Know it exists, but focus first on understanding the SDK and runtime architecture.

---

# 88. Deep Agents Core Capability Categories

The ecosystem can be remembered in four major categories:

```text
1. Execution Environment
2. Context Management
3. Delegation
4. Steering
```

---

# 89. Category 1 — Execution Environment

Contains:

```text
Tools
MCP
Virtual Filesystem
Backends
Permissions
Sandboxes
LocalShell
Interpreter
Streaming
```

Question it answers:

> Where and how can the agent take action?

---

# 90. Category 2 — Context Management

Contains:

```text
System Prompt
Messages
Summarization
Offloading
Skills
Memory
Retrieval
Prompt Caching
Context Engineering
```

Question it answers:

> What information should the agent know right now?

---

# 91. Category 3 — Delegation

Contains:

```text
Planning
Subagents
General-Purpose Subagent
Custom Subagents
Forked Subagents
Dynamic Subagents
Async Subagents
```

Question it answers:

> How should complex work be divided?

---

# 92. Category 4 — Steering

Contains:

```text
HITL
Interrupts
Approvals
Permissions
Human feedback
Runtime guidance
```

Question it answers:

> How do humans keep control over agent behavior?

---

# 93. How Everything Connects

Full mental model:

```text
USER
 │
 ▼
Messages
 │
 ▼
Deep Agent Harness
 │
 ├──────────── System Prompt
 │
 ├──────────── Skills
 │
 ├──────────── Memory
 │
 ├──────────── Middleware
 │
 ├──────────── Planning
 │
 ├──────────── Filesystem
 │                 │
 │                 ▼
 │              Backend
 │                 │
 │      ┌──────────┼───────────┐
 │      ▼          ▼           ▼
 │    State      Local       Store
 │
 ├──────────── Tools
 │                 │
 │       ┌─────────┴─────────┐
 │       ▼                   ▼
 │   Custom Tools           MCP
 │
 ├──────────── Subagents
 │                 │
 │                 ▼
 │          Isolated Context
 │
 ├──────────── Summarization
 │
 └──────────── HITL
                   │
                   ▼
               Interrupt
                   │
                   ▼
              Human Review

Everything runs on:

LANGGRAPH
 │
 ├── State
 ├── Threads
 ├── Checkpoints
 ├── Streaming
 └── Resume

Observed through:

LANGSMITH
 │
 ├── Trace
 ├── Debug
 ├── Evaluate
 └── Monitor
```

---

# 94. Full Agent Lifecycle

## Step 1 — Agent is constructed

```text
Model selected
System prompt prepared
Tools registered
Middleware assembled
Backend resolved
Subagents configured
Memory/skills configured
Runtime created
```

## Step 2 — User starts a thread

```text
User message
   ↓
thread_id
```

## Step 3 — State is prepared

```text
Messages
Files
Todos
Runtime information
```

## Step 4 — Context is prepared

Middleware may add:

```text
System instructions
Memory
Skill metadata
Tool descriptions
Summaries
```

## Step 5 — Model decides next action

Possible choices:

```text
Answer directly
Call tool
Read/write file
Delegate subtask
Update todo list
```

## Step 6 — Tool executes

Tool result enters agent state.

## Step 7 — Context is managed

If context becomes large:

```text
Summarize
Offload
Delegate
Retrieve only relevant information
```

## Step 8 — Sensitive action may interrupt

```text
Proposed action
      ↓
HITL
      ↓
Approve / edit / reject
```

## Step 9 — Checkpointer preserves progress

Runtime state can be resumed if necessary.

## Step 10 — Final response

The model returns the completed result.

---

# 95. Course Mapping — Module 1

## Lesson 1 — Deep Agents Overview

```text
Deep Agent
Agent Harness
LangChain
LangGraph
Core capabilities
```

## Lesson 2 — Running a Deep Agent

```text
Create agent
Invoke agent
Input
Output
Basic execution flow
```

## Lesson 3 — Model

```text
LLM
Provider
Tool calling
Model configuration
```

## Lesson 4 — System Prompt

```text
Agent role
Instructions
Constraints
Behavior
```

## Lesson 5 — Tools

```text
Custom tools
Tool calling
Tool results
Built-in tools
```

## Lesson 6 — MCP

```text
MCP Client
MCP Server
External capabilities
Standardized integration
```

## Lesson 7 — Messages, Threads and Checkpointer

```text
Messages
State
Thread
thread_id
Checkpoint
Persistence
Resume
```

## Lesson 8 — HITL

```text
Interrupt
Human review
Approve
Edit
Reject
Resume
```

---

# 96. Course Mapping — Module 2

Execution Environment:

```text
Virtual Filesystem
Backends
StateBackend
FilesystemBackend
StoreBackend
CompositeBackend
Sandbox
LocalShell
Interpreter
Permissions
```

---

# 97. Course Mapping — Module 3

Context Management:

```text
Context Engineering
Summarization
Offloading
Skills
Progressive Disclosure
Memory
Persistent Context
```

---

# 98. Course Mapping — Module 4

Delegation:

```text
Supervisor
Subagents
General-Purpose Agent
Specialized Agent
Context Isolation
Dynamic Subagents
Parallel Work
```

---

# 99. Course Mapping — Module 5

Everything combines:

```text
Model
+
Prompt
+
Tools
+
MCP
+
State
+
Threads
+
Checkpoints
+
Filesystem
+
Backends
+
Context Management
+
Skills
+
Memory
+
Subagents
+
HITL
```

---

# 100. Concepts I Should Know Before Lesson 2

I do not need to master everything in this README immediately.

## Must understand now

- Agent
- Agent loop
- Agent harness
- Deep Agents
- LangChain
- LangGraph
- Model
- System prompt
- Tool
- Middleware
- State
- Basic idea of backend

## Can learn properly later

- MCP
- Threads
- Checkpointer
- HITL
- Filesystem backends
- Sandboxes
- Interpreter
- Skills
- Memory
- Subagents

## Advanced

- Profiles
- Composite routing
- Dynamic subagents
- Async subagents
- ACP
- A2A
- AG-UI
- production deployment

---

# 101. The Most Important Differences

## Deep Agent vs Normal LangChain Agent

```text
Normal LangChain Agent
=
Lightweight agent harness

Deep Agent
=
More opinionated, batteries-included harness
for long-horizon work
```

## Deep Agents vs LangGraph

```text
Deep Agents
=
Ready-made agent architecture

LangGraph
=
Runtime and custom orchestration framework
```

## Tool vs Middleware

```text
Tool
=
Model chooses to call it

Middleware
=
Automatically surrounds/intercepts agent operations
```

## State vs Memory

```text
State
=
Current runtime information

Memory
=
Persistent useful information
```

## Checkpointer vs Memory

```text
Checkpointer
=
Resume execution

Memory
=
Remember knowledge/preferences
```

## Thread vs Memory

```text
Thread
=
One conversation/execution identity

Memory
=
Cross-thread reusable context
```

## Backend vs Filesystem

```text
Filesystem
=
Interface the agent sees

Backend
=
Where that filesystem data actually lives
```

## Sandbox vs LocalShell

```text
Sandbox
=
Isolated execution

LocalShell
=
Host-machine execution
```

## Skill vs Tool

```text
Skill
=
Know-how

Tool
=
Action
```

## Skill vs Memory

```text
Skill
=
How to perform a type of task

Memory
=
What should be remembered
```

## MCP vs Deep Agents

```text
MCP
=
Integration protocol

Deep Agents
=
Agent harness
```

## Planning vs Delegation

```text
Planning
=
What work needs doing?

Delegation
=
Who should do it?
```

---

# 102. Why Middleware Matters So Much

My key understanding:

> Deep Agents is not powerful because of one magical class. It is powerful because it assembles a useful **middleware stack**, filesystem abstraction, context-management system, delegation system, and LangGraph runtime around a normal tool-calling model.

So when I see:

```text
Middleware
```

I should think:

```text
Behavior added around the agent loop
```

Examples:

```text
Filesystem behavior
Summarization behavior
Subagent behavior
Memory injection
Skills loading
Human approval
Prompt caching
```

---

# 103. Why Backend Matters So Much

When I see a path such as:

```text
/notes/report.md
```

I should **not** immediately assume:

```text
This file exists on my Windows disk.
```

I should ask:

> Which backend is being used?

Because:

```text
StateBackend
→ file lives in state

FilesystemBackend
→ file may live on disk

StoreBackend
→ file/data may live in durable store

Sandbox
→ file lives in sandbox environment
```

---

# 104. Why Context Management Matters So Much

A long-running agent's biggest challenge is not only intelligence.

It is also:

```text
What should the model remember?
What should it forget?
What should be summarized?
What should be stored?
What should be retrieved?
What should be delegated?
```

That is why modern agent engineering is heavily about **context engineering**.

---

# 105. Why Subagents Are Also a Context Tool

Subagents are not only about "multiple agents".

They are also a context-management technique.

```text
Heavy work
   ↓
Subagent context
   ↓
Detailed intermediate information stays there
   ↓
Compact final result
   ↓
Main-agent context remains clean
```

This is a very important mental model.

---

# 106. Why HITL Belongs to the Runtime

HITL needs:

```text
Pause
Save state
Wait for decision
Resume
```

These are runtime capabilities.

That is why Deep Agents relies on LangGraph for interruption and resumability.

---

# 107. What Makes Deep Agents "Deep"

"Deep" does not mean deep neural networks.

It means the agent is designed for:

```text
Long horizon
Many steps
Large context
Tool use
File use
Delegation
Persistent work
Execution
Human steering
```

---

# 108. Deep Agents Design Principles

The project describes itself around ideas such as:

## Opinionated

Useful defaults are included.

## Extensible

Pieces can be replaced or customized.

## Model-agnostic

Different tool-calling models can be used.

## Production-oriented

Built on LangGraph and integrates with LangSmith.

---

# 109. When I Should Use Deep Agents

Good fit:

- research agents
- coding agents
- data-analysis agents
- long document workflows
- multi-step business processes
- agents that need files
- agents that need delegation
- agents that need memory
- agents that need HITL
- agents operating over many tool calls

---

# 110. When Deep Agents May Be Too Much

Probably unnecessary for:

- one-shot question answering
- one API call
- simple chatbot
- simple RAG query
- very deterministic small workflows
- tasks that do not need context management or delegation

In those cases a lighter LangChain agent may be simpler.

---

# 111. When I Might Use LangGraph Directly

Use LangGraph directly when:

```text
I need a custom graph
I need exact control over nodes and transitions
I need deterministic workflow stages
The standard agent loop is not the right architecture
```

Deep Agents is easier when the normal agent loop is suitable but I want a richer harness.

---

# 112. Learning Order I Will Follow

```text
1. Deep Agent overview
2. Running agent
3. Model
4. System Prompt
5. Tools
6. MCP
7. Messages / Threads / Checkpointer
8. HITL
9. Execution Environment
10. Filesystem Backends
11. Sandbox / LocalShell
12. Interpreter
13. Summarization / Offloading
14. Skills
15. Memory
16. Delegation
17. Subagent Team
18. Dynamic Subagents
19. Capstone
```

---

# 113. Quick Glossary

| Term | My simple meaning |
|---|---|
| **Agent** | LLM system that can decide and take actions |
| **Agent Loop** | Model → tool → result → model cycle |
| **Harness** | Infrastructure surrounding the agent loop |
| **Deep Agent** | Full-featured LangChain agent harness |
| **Model** | LLM that reasons and chooses actions |
| **System Prompt** | Core instructions for the agent |
| **Message** | Conversation/event information sent through the agent |
| **Tool** | Action available to the model |
| **Middleware** | Behavior/interceptor around agent/model/tool execution |
| **State** | Current runtime information |
| **Thread** | One conversation/execution identity |
| **Checkpointer** | Saves runtime state for resume |
| **Store** | Longer-term persistent data storage |
| **Filesystem** | File-like interface exposed to agent |
| **Backend** | Storage/execution implementation behind filesystem |
| **StateBackend** | Files stored in thread state |
| **FilesystemBackend** | Files stored on real filesystem |
| **StoreBackend** | Persistent store-backed files/data |
| **CompositeBackend** | Routes paths to different backends |
| **Sandbox** | Isolated code/shell environment |
| **LocalShell** | Shell execution on host machine |
| **Interpreter** | Lightweight programmable runtime |
| **Skill** | Reusable specialized instructions/workflow |
| **Memory** | Persistent reusable context |
| **Summarization** | Compress older context |
| **Offloading** | Move large context out of model window |
| **Retrieval** | Fetch relevant external knowledge |
| **Subagent** | Child agent that handles delegated work |
| **Supervisor** | Main agent coordinating subagents |
| **Planning** | Track what tasks need to be done |
| **Delegation** | Assign tasks to other agents |
| **HITL** | Human approval/intervention |
| **Interrupt** | Pause execution for external decision |
| **MCP** | Standard protocol for tools/resources |
| **LangChain** | Agent/application framework |
| **LangGraph** | Stateful agent runtime |
| **LangSmith** | Tracing/evaluation/monitoring/deployment |
| **Profile** | Model/provider-specific harness customization |
| **Streaming** | Observe agent output/events while running |
| **Tracing** | Record detailed execution history |
| **Context Engineering** | Designing what information the model sees |

---

# 114. My Final Mental Model

If I remember only one diagram, it should be this:

```text
                      USER
                       │
                       ▼
                 DEEP AGENT
                       │
      ┌────────────────┼────────────────┐
      │                │                │
      ▼                ▼                ▼
   CONTEXT          ACTIONS         DELEGATION
      │                │                │
 Prompt             Tools           Subagents
 Messages           MCP             Planning
 Skills             Files
 Memory             Execute
 Summary
 Offload
      │                │                │
      └────────────────┼────────────────┘
                       │
                  MIDDLEWARE
                       │
                       ▼
                  LANGCHAIN
                       │
                       ▼
                  LANGGRAPH
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
      State         Threads       Checkpoints
                                      │
                                      ▼
                                  Interrupt
                                      │
                                      ▼
                                     HITL

Storage / execution underneath:

Backend
 ├── State
 ├── Filesystem
 ├── Store
 ├── Composite
 ├── Sandbox
 └── LocalShell

Observation around everything:

LangSmith
 ├── Trace
 ├── Debug
 ├── Evaluate
 └── Monitor
```

---

# 115. Five Sentences I Should Be Able to Say Without Notes

1. **Deep Agents is an opinionated agent harness built on LangChain and running on LangGraph.**

2. **Middleware adds behavior around the agent loop, while a tool is something the model explicitly chooses to call.**

3. **A backend determines where the Deep Agent filesystem data lives and what execution capabilities are available.**

4. **Context management uses summarization, offloading, skills, memory, retrieval, and subagent isolation to keep the model focused.**

5. **LangGraph provides state, threads, checkpoints, streaming, interrupts, and resumability underneath Deep Agents.**

---

# 116. Official References

Primary references used for these notes:

- Deep Agents Overview  
  https://docs.langchain.com/oss/python/deepagents/overview

- Deep Agents Customization  
  https://docs.langchain.com/oss/python/deepagents/customization

- Deep Agents Backends  
  https://docs.langchain.com/oss/python/deepagents/backends

- Human-in-the-Loop  
  https://docs.langchain.com/oss/python/deepagents/human-in-the-loop

- Subagents  
  https://docs.langchain.com/oss/python/deepagents/subagents

- Deep Agents GitHub Repository  
  https://github.com/langchain-ai/deepagents

- Deep Agents Architecture  
  https://github.com/langchain-ai/deepagents/blob/main/libs/ARCHITECTURE.md

- LangChain Academy — Introduction to Deep Agents  
  https://academy.langchain.com/courses/take/foundation-introduction-to-deepagents/

---

# 117. Next Step

After I am comfortable with the foundation in this file:

> **Module 1 — Lesson 2: Running a Deep Agent**

For Lesson 2, I should focus only on:

```text
How a Deep Agent is created
How it receives input
How it runs
How messages flow
How the result is returned
```

I do **not** need to master backends, memory, skills, or subagents before moving to Lesson 2.
