# Module 1 — Building a Deep Agent
## Lesson 2 — Running a Deep Agent

> **Purpose:** My study notes for understanding how a Deep Agent is created, invoked, executed, and how input/output move through the LangChain + LangGraph runtime.
>
> This lesson focuses only on **running a Deep Agent**. Model selection, prompts, tools, MCP, threads, checkpointers, and HITL are covered in later lessons.

---

# 1. Learning Objectives

By the end of this lesson, I should understand:

- the difference between **creating** and **running** a Deep Agent
- what `create_deep_agent()` does
- what `invoke()` does
- what the `messages` input means
- how the agent loop works
- why one agent run can contain several model/tool calls
- what **agent state** means
- why the result is not just a plain string
- how to locate the final AI response
- why message content may sometimes be structured
- what LangChain, LangGraph, and Deep Agents each do during a run

---

# 2. Main Idea

The basic lifecycle is:

```text
Configure agent
      ↓
create_deep_agent(...)
      ↓
Runnable agent is created
      ↓
agent.invoke(...)
      ↓
User message enters runtime
      ↓
Model reasons
      ↓
Tools may be called
      ↓
State is updated
      ↓
Loop continues
      ↓
Final state is returned
```

The key difference:

```text
create_deep_agent()
=
BUILD / CONFIGURE

agent.invoke(...)
=
RUN
```

---

# 3. Construction vs Execution

Deep Agents has two useful phases to understand.

## Phase 1 — Construction

Construction happens when the application calls:

```text
create_deep_agent(...)
```

At this stage Deep Agents prepares things such as:

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
Profiles
HITL configuration
```

Then it delegates agent construction to LangChain.

Mental model:

```text
Application
    ↓
create_deep_agent()
    ↓
Deep Agents Harness
    ↓
LangChain create_agent()
    ↓
Compiled LangGraph Agent
```

No user task has to be executed yet.

---

## Phase 2 — Execution

Execution starts when the agent receives a task.

Conceptually:

```text
agent.invoke(...)
```

Then LangGraph drives the runtime:

```text
Initial State
    ↓
Model Call
    ↓
Need Tool?
  /       \
No        Yes
│          │
│          ↓
│       Tool Call
│          ↓
│       Tool Result
│          ↓
│       Update State
│          ↓
│       Model Again
│
↓
Final Response
    ↓
Final State
```

---

# 4. What Does `create_deep_agent()` Return?

It does **not** return only an LLM.

It returns a runnable agent graph.

Mental model:

```text
create_deep_agent()
        ↓
Deep Agents configuration
        ↓
LangChain agent
        ↓
Compiled LangGraph graph
```

This is why the created agent can use LangGraph features such as:

- state
- streaming
- checkpoints
- persistence
- interrupts
- resumability

We will study several of these later.

---

# 5. Creating the Agent Does Not Run the User Task

Important:

```text
create_deep_agent(...)
```

means:

```text
Prepare the agent
```

It does **not** mean:

```text
Solve the user's request
```

A useful analogy:

```text
create_deep_agent()
=
Hire and prepare the worker

invoke()
=
Give the worker a task
```

---

# 6. What Is `invoke()`?

> `invoke()` runs the agent using the input state provided by the application.

Mental model:

```text
Input State
    ↓
invoke()
    ↓
Agent Runtime
    ↓
Final State
```

So:

```text
invoke()
=
Start one agent execution
```

---

# 7. What Do We Give to `invoke()`?

The most common starting input contains:

```text
messages
```

Conceptually:

```text
messages:
- user request
```

The runtime works with a conversation history rather than only a raw text string.

---

# 8. Why `messages`?

Agents may need to maintain a sequence such as:

```text
Human Message
      ↓
AI Message / Tool Call
      ↓
Tool Result
      ↓
AI Message
      ↓
Another Tool Call
      ↓
Tool Result
      ↓
Final AI Message
```

So messages are part of the agent's state.

---

# 9. Main Message Roles

The important roles are:

```text
System
Human / User
AI / Assistant
Tool
```

## System

High-level agent instructions.

## Human / User

The user's current request.

## AI / Assistant

The model's response.

It may contain:

- normal text
- tool calls
- structured content

## Tool

The result returned after a tool executes.

---

# 10. What Does the Model Receive?

At a high level, the model receives:

```text
System Instructions
+
Message History
+
Available Tool Definitions
+
Context Added by Middleware
```

Then the model decides what should happen next.

---

# 11. Tool Calling Requirement

Deep Agents normally uses models that support **tool calling**.

Why?

Because the agent may need to request actions such as:

```text
Search
Read file
Write file
Call API
Use database
Delegate to subagent
Execute command
```

The model does not directly perform the external operation.

Instead it requests a tool call.

---

# 12. Tool Calling Flow

```text
Model
  ↓
"I need Tool X"
  ↓
Structured Tool Call
  ↓
Runtime executes tool
  ↓
Tool Result
  ↓
Result added to state
  ↓
Model sees result
  ↓
Model decides next step
```

---

# 13. The Agent Loop

The core loop is:

```text
             MODEL
               │
               ▼
        Need a tool?
          /       \
        No         Yes
        │           │
        ▼           ▼
 Final Answer    Tool Call
                    │
                    ▼
                  Tool
                    │
                    ▼
               Tool Result
                    │
                    └──────→ MODEL
```

The loop continues until the model produces a final response instead of another action.

---

# 14. One `invoke()` Is Not Necessarily One Model Call

This is important.

A single agent run can be:

```text
invoke()
  ↓
Model Call 1
  ↓
Tool Call
  ↓
Model Call 2
  ↓
Tool Call
  ↓
Model Call 3
  ↓
Final Answer
```

Therefore:

```text
1 invoke()
≠
1 LLM call
```

---

# 15. One `invoke()` Can Also Use Many Tools

A run can contain:

```text
0 tools
1 tool
many tools
```

Example:

```text
User
 ↓
Model
 ↓
Tool A
 ↓
Model
 ↓
Tool B
 ↓
Model
 ↓
Final Answer
```

---

# 16. What Is Agent State?

> **State is the information carried through the agent execution.**

For now, the most important field is:

```text
messages
```

But Deep Agent state can also contain other information depending on configuration, such as:

```text
files
todos
structured response
custom state
```

---

# 17. Initial State vs Final State

At the beginning:

```text
Initial State

messages:
- Human request
```

After tool usage:

```text
Updated State

messages:
- Human request
- AI tool call
- Tool result
```

At completion:

```text
Final State

messages:
- Human request
- AI tool call
- Tool result
- AI final response
```

---

# 18. Why `invoke()` Does Not Return Only Text

A Deep Agent is a stateful system.

Therefore the result is conceptually:

```text
Final Agent State
```

not:

```text
Only Final Text
```

The final state may contain:

```text
messages
files
other state fields
```

The final answer is only one part of this state.

---

# 19. Locating the Final AI Response

In a normally completed run, the latest message is usually the final AI response.

Mental model:

```text
messages
  │
  ├── [0] Human
  ├── [1] AI Tool Call
  ├── [2] Tool Result
  └── [-1] Final AI Message
```

That is why we commonly inspect the final message after the run.

---

# 20. Important: AI Message Content Is Not Always a String

This is something I already encountered in Lesson 1.

An AI message may contain:

```text
Plain text
```

or:

```text
Structured content blocks
```

Example conceptually:

```text
[
    {
        type: "text",
        text: "Here is your answer..."
    }
]
```

This is normal.

---

# 21. Why Structured Content Exists

Modern models can return multiple kinds of content.

Examples:

```text
text
reasoning
tool-related content
images
citations
provider-specific blocks
```

LangChain therefore supports structured message content.

So:

> If `message.content` prints like a list of dictionaries, that does not automatically mean the run failed.

---

# 22. Construction and Execution Responsibilities

A useful separation:

```text
CONSTRUCTION

Resolve configuration
Assemble middleware
Prepare tools
Prepare backend
Build agent graph
```

Then:

```text
EXECUTION

Receive state
Call model
Execute requested tools
Update state
Repeat
Return state
```

---

# 23. What Deep Agents Does

Deep Agents provides the opinionated harness.

Examples:

```text
Filesystem
Subagents
Summarization
Memory
Skills
Execution Environment
HITL integration
Optional planning
```

Mental model:

```text
Deep Agents
=
How the richer agent is assembled
```

---

# 24. What LangChain Does

LangChain owns the agent abstraction.

Important pieces:

```text
Model
Tools
Middleware
Agent state schema
Model/tool interaction
```

Mental model:

```text
LangChain
=
Defines the agent structure
```

---

# 25. What LangGraph Does

LangGraph owns the runtime.

Important capabilities:

```text
State
Execution
Streaming
Checkpoints
Persistence
Interrupts
Resume
```

Mental model:

```text
LangGraph
=
Runs the stateful workflow
```

---

# 26. Complete Layering

```text
Deep Agents
    ↓
Opinionated Harness

LangChain
    ↓
Agent Abstraction

LangGraph
    ↓
Runtime

Model + Tools
    ↓
Actual reasoning and actions
```

---

# 27. What Middleware Does During a Run

Middleware can participate around model/tool operations.

It may:

- change the model request
- inject instructions
- add or modify tools
- summarize context
- load skills
- load memory
- manage filesystem behavior
- pause sensitive actions
- repair message history

Mental model:

```text
State
  ↓
Middleware
  ↓
Prepared Model Request
  ↓
Model
```

For Lesson 2, I do not need to understand every middleware class.

I only need to remember:

> Middleware adds behavior around the agent loop.

---

# 28. Running Without a Tool

A simple run may be:

```text
User
  ↓
Model
  ↓
Final Answer
```

The harness does not force tool usage.

---

# 29. Running With a Tool

```text
User
  ↓
Model
  ↓
Tool Call
  ↓
Tool Result
  ↓
Model
  ↓
Final Answer
```

---

# 30. Running With Several Tools

```text
User
  ↓
Model
  ↓
Tool A
  ↓
Result A
  ↓
Model
  ↓
Tool B
  ↓
Result B
  ↓
Model
  ↓
Final Answer
```

---

# 31. Direct Model Call vs Agent Run

A direct model call:

```text
Prompt
  ↓
Model
  ↓
Response
```

A Deep Agent run:

```text
Goal
  ↓
Model
  ↕
Tools
  ↕
State
  ↕
Filesystem
  ↕
Subagents
  ↓
Final Result
```

This is why an agent is useful for tasks that require action and iteration.

---

# 32. Reason → Act → Observe → Repeat

A useful agent mental model:

```text
REASON
  ↓
ACT
  ↓
OBSERVE
  ↓
REASON AGAIN
```

Example:

```text
Reason:
"I need more information."

Act:
Call tool.

Observe:
Read tool result.

Reason:
"Now I can continue."
```

This loop continues until the goal is complete.

---

# 33. User Goal vs Agent Execution Path

The user often describes:

```text
WHAT they want
```

The agent decides:

```text
HOW to achieve it
```

Example:

```text
User Goal
    ↓
Agent chooses actions
    ↓
Observes results
    ↓
Chooses next action
    ↓
Final result
```

---

# 34. Agentic vs Deterministic Workflow

## Agentic

The model chooses the next step.

```text
Current State
    ↓
Model
    ↓
Choose Next Action
```

## Deterministic

The developer predefines the steps.

```text
Step 1
 ↓
Step 2
 ↓
Step 3
```

Deep Agents is mainly for agentic workflows.

LangGraph can support both styles.

---

# 35. Why Deep Agents Still Uses a Graph

I do not manually define graph nodes and edges when using the high-level Deep Agents API.

But underneath:

```text
Deep Agents
    ↓
LangChain create_agent
    ↓
LangGraph graph
```

So I get a graph runtime without manually building the graph.

---

# 36. Environment Setup

Before a hosted model can run, the application normally needs:

```text
Python environment
Deep Agents package
Provider integration
API credentials
```

Credentials should normally come from environment variables rather than being hard-coded.

Examples:

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
GOOGLE_API_KEY
```

---

# 37. Why `.env` Is Common

During local development:

```text
.env
  ↓
Environment loader
  ↓
Python process
  ↓
Model provider
```

Important:

> `.env` files containing secrets should normally be excluded from Git.

---

# 38. Model Identifier

Deep Agents can accept model identifiers in provider/model form.

Mental model:

```text
provider:model
```

This answers:

```text
Which provider?
Which model?
```

We will study model configuration properly in Lesson 3.

---

# 39. Tool Calling Is a Model Capability

Not every model behaves equally well as an agent.

Agent performance depends on things such as:

```text
Tool-calling support
Instruction following
Reasoning quality
Context window
Latency
Cost
```

We will study this in Lesson 3.

---

# 40. Deep Agent Execution Can Use Built-in Capabilities

Depending on configuration/backend, the run may involve:

```text
Filesystem operations
Subagents
Summarization
Execution
Memory
Skills
HITL
```

These can happen within the same overall agent run.

---

# 41. Planning Is Optional

Current Deep Agents behavior:

```text
write_todos planning
=
Optional
```

I should not assume every Deep Agent automatically creates a todo list.

Planning can be added when useful.

---

# 42. Files May Live in Agent State

If the default state-backed filesystem is used:

```text
/report.md
```

may exist inside agent state rather than on my real Windows disk.

This explains the Lesson 1 behavior I observed.

Detailed filesystem backends belong to Module 2.

---

# 43. Backend Still Matters During Execution

If the agent requests a filesystem action:

```text
Agent
  ↓
Filesystem Middleware
  ↓
Backend
  ↓
Actual storage location
```

Examples of storage can later include:

```text
State
Local filesystem
Persistent store
Sandbox
```

---

# 44. A Run Can Delegate to a Subagent

Conceptually:

```text
Main Agent
   ↓
Delegated Task
   ↓
Subagent
   ↓
Subagent Result
   ↓
Main Agent
```

This can happen inside one main invocation.

We study delegation in Module 4.

---

# 45. A Long Run Can Trigger Summarization

Conceptually:

```text
Message history grows
      ↓
Context becomes large
      ↓
Summarization middleware
      ↓
Older history compressed
      ↓
Execution continues
```

This belongs to Module 3.

---

# 46. A Run Can Pause for HITL

Conceptually:

```text
Agent proposes sensitive action
       ↓
Interrupt
       ↓
Execution pauses
       ↓
Human reviews
       ↓
Resume
```

This belongs to Lesson 8.

---

# 47. A Run Can Be Persistent Later

For Lesson 2, I focus on one invocation.

Later:

```text
thread_id
+
checkpointer
```

can connect several invocations into one continuing conversation.

That belongs to Lesson 7.

---

# 48. `invoke()` vs Streaming

## Invoke

```text
Start execution
      ↓
Run completes
      ↓
Receive final state
```

## Streaming

```text
Start execution
      ↓
Receive intermediate updates
      ↓
Tool activity
      ↓
Model output
      ↓
Final update
```

For this lesson, `invoke()` is the main concept.

---

# 49. Why Streaming Exists

Agent runs may take longer because they can contain:

```text
Multiple model calls
Multiple tools
Subagents
External APIs
```

Streaming helps applications show progress while work is happening.

We do not need to master it yet.

---

# 50. LangSmith Tracing

LangSmith can make the internal run visible.

A trace can show:

```text
User Input
   ↓
Model Call
   ↓
Tool Call
   ↓
Tool Result
   ↓
Model Call
   ↓
Final Output
```

This is useful for:

- debugging
- learning
- evaluation
- latency inspection
- token/cost inspection

---

# 51. Terminal Output vs Agent Output

Important distinction:

```text
Everything printed in terminal
≠
Agent final answer
```

The terminal may also show:

```text
Python process path
Warnings
Debug logs
Tracebacks
Exit code
```

The real agent output comes from the returned state/messages.

---

# 52. Exit Code 0

If Python reports:

```text
Process finished with exit code 0
```

it generally means:

```text
The Python program completed without an uncaught exception.
```

It does **not** mean:

```text
The agent's answer was definitely correct.
```

---

# 53. Execution Success vs Task Success

## Execution Success

```text
Program ran
No runtime error
```

## Task Success

```text
Agent correctly completed the user's request
```

An agent can execute successfully but still give a weak or incorrect answer.

This is why evaluation matters.

---

# 54. Same Input May Produce Different Runs

LLM-based agents are not always deterministic.

Differences can come from:

- model stochasticity
- changing tool data
- search results
- provider changes
- model updates
- different context

Therefore:

```text
Same request
may produce
slightly different execution paths
```

---

# 55. Cost and Latency

One direct model request may require:

```text
1 model call
```

One agent run may require:

```text
Model
Tool
Model
Tool
Model
Subagent
Model
```

Therefore agent runs can have higher:

```text
Latency
Token usage
API cost
```

This is normal for more capable workflows.

---

# 56. Common Mistake — Defining a System Prompt but Not Passing It

A Python variable existing does not mean the agent received it.

Conceptually:

```text
system_prompt variable
```

must actually be connected to:

```text
agent construction
```

I encountered this in Lesson 1.

---

# 57. Common Mistake — Conflicting Instructions

Example:

```text
System:
Do not save files.

User:
Save the file.
```

This creates unnecessary conflict.

Best practice:

```text
Keep system behavior and user task consistent.
```

---

# 58. Common Mistake — Assuming Message Content Is Always Text

If the provider returns structured content:

```text
message.content
```

may look like:

```text
list of content blocks
```

This is not automatically an error.

---

# 59. Common Mistake — Assuming a Virtual File Is Local

A path such as:

```text
/report.md
```

does not tell me where the data physically lives.

I must ask:

```text
Which backend is being used?
```

---

# 60. Common Mistake — Thinking `invoke()` Means One LLM Request

Wrong mental model:

```text
invoke
=
one model call
```

Correct mental model:

```text
invoke
=
one complete agent run
```

---

# 61. Common Mistake — Thinking a Tool Runs Because It Exists

A tool being available means:

```text
The model CAN use it.
```

It does not mean:

```text
The model MUST use it.
```

---

# 62. Common Mistake — Thinking the Model Executes Python

The model:

```text
requests a tool
```

The runtime:

```text
executes the tool
```

This separation is fundamental.

---

# 63. Common Mistake — Printing the Entire State to End Users

For development, full state is useful.

For a real application, the user normally needs:

```text
Final useful response
```

not:

```text
all internal messages/state
```

---

# 64. Debugging Order

If a run behaves unexpectedly, I should inspect:

```text
1. Did Python execute?
2. Is the API key loaded?
3. Is the model identifier valid?
4. Does the model support tool calling?
5. Is my system prompt actually attached?
6. Are my tools attached?
7. What exactly did the user message say?
8. Did the model call a tool?
9. What did the tool return?
10. What messages are in final state?
11. What is the final AI message?
12. What does the LangSmith trace show?
```

---

# 65. Running a Deep Agent — 8-Step Summary

```text
1. Prepare environment

2. Configure model/tools/prompt

3. Construct agent

4. Prepare input state

5. Invoke agent

6. Runtime executes model/tool loop

7. Receive final state

8. Extract/display useful output
```

---

# 66. Step 1 — Prepare Environment

Need:

```text
Python
deepagents
model provider
API credentials
```

---

# 67. Step 2 — Configure Agent

For a basic run:

```text
Model
System Prompt
Tools
```

Later I may add:

```text
Middleware
Backend
Subagents
Memory
Skills
Checkpointer
Store
HITL
```

---

# 68. Step 3 — Construct Agent

```text
Configuration
    ↓
create_deep_agent()
    ↓
Runnable Agent Graph
```

---

# 69. Step 4 — Prepare Input State

For a simple conversational run:

```text
messages
    ↓
user request
```

---

# 70. Step 5 — Invoke

```text
Initial State
    ↓
invoke()
    ↓
LangGraph starts runtime
```

---

# 71. Step 6 — Agent Loop

```text
Model
 ↕
Tools
 ↕
State
```

until the task is complete.

---

# 72. Step 7 — Final State

The agent returns the completed state.

Possible contents:

```text
messages
files
other configured state
```

---

# 73. Step 8 — Display Output

Developer view:

```text
Full state
Messages
Tool calls
Trace
```

User view:

```text
Final useful answer
```

---

# 74. Main Concepts to Lock In

## Construction

```text
Build/configure the agent
```

## Invocation

```text
Run the agent
```

## State

```text
Information carried through the run
```

## Agent Loop

```text
Model → Tool → Result → Model
```

## Final State

```text
Result of completed execution
```

---

# 75. Interview-Level Explanation

If asked:

### "How do you run a Deep Agent?"

My answer:

> **I first construct the agent with `create_deep_agent()`. This configures the Deep Agents harness and returns a runnable LangGraph-based agent. I then invoke it with an initial state, usually containing user messages. LangGraph drives the model/tool loop, updating state after model and tool operations until the model reaches a final response. The invocation returns the final agent state, from which I can access the final AI message and any other state produced during the run.**

---

# 76. Interview Question — Is One Invoke One Model Call?

> No. One invocation may contain multiple model calls and multiple tool calls.

---

# 77. Interview Question — Who Executes the Tool?

> The model requests the tool call, but the runtime executes the actual tool and returns the result to the model through state/messages.

---

# 78. Interview Question — Why Is the Result a State Object?

> Because the Deep Agent is a stateful runtime, not a simple text-in/text-out model call. The final answer is only one part of the final state.

---

# 79. Interview Question — What Does LangGraph Do?

> LangGraph runs the stateful execution loop and provides capabilities such as state, streaming, checkpoints, persistence, interrupts, and resumability.

---

# 80. Interview Question — What Does Deep Agents Add?

> Deep Agents adds an opinionated harness around the LangChain agent, including capabilities such as filesystem access, context management, subagents, memory, skills, execution environments, and HITL integration.

---

# 81. Revision Cheat Sheet

```text
CREATE
create_deep_agent()
      ↓
Runnable Deep Agent

INPUT
messages
      ↓
Initial State

RUN
invoke()
      ↓
LangGraph Runtime

LOOP
Model ↔ Tools
      ↓
State Updated

OUTPUT
Final State
      ↓
Latest AI Message
```

---

# 82. Five Sentences I Should Remember

1. **`create_deep_agent()` constructs the agent; `invoke()` runs it.**

2. **One `invoke()` can contain several model calls and tool calls.**

3. **The model requests tool actions, while the runtime executes them.**

4. **The returned result is the final agent state, not only a plain text answer.**

5. **Deep Agents provides the harness, LangChain provides the agent abstraction, and LangGraph provides the runtime.**

---

# 83. Self-Check Questions

Before moving to Lesson 3, I should be able to answer:

1. What is the difference between construction and execution?
2. What does `create_deep_agent()` return conceptually?
3. What does `invoke()` do?
4. Why do we use `messages`?
5. What are the main message roles?
6. What is agent state?
7. Why is the final result not just text?
8. Can one invocation contain multiple model calls?
9. Can one invocation contain multiple tool calls?
10. Who chooses which tool to call?
11. Who actually executes the tool?
12. What happens after the tool returns?
13. What does Deep Agents provide?
14. What does LangChain provide?
15. What does LangGraph provide?
16. Why can AI message content be structured?
17. What is the difference between execution success and task success?
18. How is `invoke()` different from streaming?
19. Why is LangSmith useful when debugging?
20. Why should I first understand one simple invocation before adding threads/checkpointers?

---

# 84. One-Line Summary

> **Running a Deep Agent means invoking a LangGraph-based agent with initial state, letting the runtime coordinate the model, tools, middleware, and state until the task finishes, and then receiving the final agent state.**

---

# 85. Final Mental Model

```text
                     USER
                      │
                      ▼
                 INPUT STATE
                 (messages)
                      │
                      ▼
               DEEP AGENT HARNESS
                      │
                      ▼
                  LANGCHAIN
                      │
                      ▼
                  LANGGRAPH
                      │
                      ▼
                    MODEL
                      │
                Need action?
                /         \
              No           Yes
              │             │
              ▼             ▼
         Final Answer    Tool Call
                            │
                            ▼
                           Tool
                            │
                            ▼
                       Tool Result
                            │
                            └────→ MODEL
                      │
                      ▼
                  FINAL STATE
                      │
                      ▼
                 APPLICATION
```

---

# 86. Official References

- Deep Agents Quickstart  
  https://docs.langchain.com/oss/python/deepagents/quickstart

- Deep Agents Overview  
  https://docs.langchain.com/oss/python/deepagents/overview

- Deep Agents GitHub  
  https://github.com/langchain-ai/deepagents

- Deep Agents Architecture  
  https://github.com/langchain-ai/deepagents/blob/main/libs/ARCHITECTURE.md

- LangChain Academy — Introduction to Deep Agents  
  https://academy.langchain.com/courses/take/foundation-introduction-to-deepagents/

---

# 87. Next Step

After understanding these notes, I should do one small practical demonstration where I:

```text
Create a Deep Agent
      ↓
Give it one user request
      ↓
Run it with invoke()
      ↓
Inspect the messages
      ↓
Observe any tool call
      ↓
Print only the final response
```

After that:

> **Module 1 — Lesson 3: Model**
