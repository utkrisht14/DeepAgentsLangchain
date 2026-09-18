# Module 1 — Building a Deep Agent
## Lesson 7 — Messages, Threads, and Checkpointers

> **Purpose:** Focused notes on how Deep Agents keeps conversation state across turns using messages, threads, and checkpointers.
>
> This lesson does not go deeply into HITL, long-term memory, stores, or backends except where needed to understand persistence.

---

# 1. Main Idea

The three concepts connect like this:

```text
Messages
=
What happened in the conversation

Thread
=
Which conversation this belongs to

Checkpointer
=
How that conversation state is saved
```

Mental model:

```text
User + Agent Messages
        ↓
Stored in Agent State
        ↓
Associated with thread_id
        ↓
Saved by Checkpointer
```

---

# 2. What Is a Message?

A **message** is a unit of conversation context.

Messages represent things such as:

```text
User input
Model response
Tool call
Tool result
System instruction
```

LangChain uses message objects so the agent can keep structured conversation history.

---

# 3. Main Message Types

The most important message types are:

```text
SystemMessage
HumanMessage
AIMessage
ToolMessage
```

---

# 4. SystemMessage

A `SystemMessage` contains instructions that guide the model.

Example idea:

```text
"You are a helpful coding assistant."
```

It defines high-level behavior.

We covered this in Lesson 4.

---

# 5. HumanMessage

A `HumanMessage` represents user input.

Example:

```text
"What is LangGraph?"
```

Mental model:

```text
HumanMessage
=
User → Agent
```

---

# 6. AIMessage

An `AIMessage` represents model output.

It can contain:

```text
Text
Tool calls
Metadata
Structured content
```

Example:

```text
AI:
"I need to use the weather tool."
```

or a normal final answer.

---

# 7. ToolMessage

A `ToolMessage` contains the result of a tool execution.

Example:

```text
AIMessage:
Tool call → get_weather("Amsterdam")

ToolMessage:
18°C, cloudy
```

The tool result is then sent back to the model.

---

# 8. Message Flow During Tool Calling

```text
HumanMessage
      ↓
AIMessage
(tool call)
      ↓
ToolMessage
(tool result)
      ↓
AIMessage
(final answer)
```

This sequence becomes part of the conversation history.

---

# 9. Messages Are Part of Agent State

When I run a Deep Agent, the `messages` list is stored in the agent's state.

Conceptually:

```text
Agent State

messages:
    HumanMessage
    AIMessage
    ToolMessage
    AIMessage
```

The model can use this history when processing the next turn.

---

# 10. Why Message History Matters

Without history:

```text
Turn 1:
"My name is Alex."

Turn 2:
"What is my name?"

Agent:
Does not know.
```

With conversation history:

```text
Turn 1:
Human → "My name is Alex."

Turn 2:
Human → "What is my name?"

Previous messages available
      ↓
Agent → "Alex"
```

---

# 11. One Invocation vs Multiple Turns

A single invocation might contain:

```text
Human
AI
Tool
AI
```

But a conversation may contain several user turns:

```text
Turn 1
Human
AI

Turn 2
Human
AI

Turn 3
Human
AI
```

To connect these separate invocations, LangGraph uses **threads** and **checkpointers**.

---

# 12. What Is a Thread?

A **thread** represents one continuing conversation or execution history.

Think:

```text
Thread A
=
Conversation A
```

```text
Thread B
=
Conversation B
```

Each thread has its own state.

---

# 13. `thread_id`

A thread is identified by:

```text
thread_id
```

Conceptually:

```text
thread_id = "conversation-1"
```

The runtime uses this ID to know:

> Which saved conversation state should I load?

---

# 14. Thread Mental Model

```text
thread_id = "user-chat-123"
        ↓
Find saved state
        ↓
Load previous messages
        ↓
Add new user message
        ↓
Run agent
        ↓
Save updated state
```

---

# 15. Different Threads Are Independent

Example:

```text
Thread A
User: My favorite language is Python.
```

```text
Thread B
User: What is my favorite language?
```

Thread B should not automatically know what happened in Thread A.

Why?

Because:

```text
Thread A state
≠
Thread B state
```

---

# 16. Same Thread Continues Conversation

Example:

```text
Thread ID = "chat-1"

Turn 1:
"My favorite language is Python."
```

Later:

```text
Thread ID = "chat-1"

Turn 2:
"What is my favorite language?"
```

Because the same thread is used, the previous conversation state can be restored.

---

# 17. Thread Is Not the Same as User

A user may have several conversations.

Example:

```text
User = Alex

Thread 1
→ Python discussion

Thread 2
→ Travel discussion

Thread 3
→ Finance discussion
```

So:

```text
user_id
≠
thread_id
```

A thread normally represents one conversation/session, not necessarily one person.

---

# 18. Why Threads Are Useful

Threads allow:

```text
Conversation continuity
Separate chat sessions
Independent agent workflows
Resuming previous work
HITL resume
State inspection
```

---

# 19. What Is a Checkpointer?

A **checkpointer** saves the state of a LangGraph execution.

Simple definition:

> A checkpointer stores snapshots of a thread's graph state so the thread can be continued later.

Mental model:

```text
Agent State
     ↓
Checkpointer
     ↓
Saved Checkpoint
```

---

# 20. What Is a Checkpoint?

A **checkpoint** is a saved snapshot of graph state at a particular point in execution.

It may include state such as:

```text
Messages
Conversation history
Interrupt information
Other graph state
```

So:

```text
Checkpointer
=
Mechanism that saves

Checkpoint
=
Saved snapshot
```

---

# 21. Thread + Checkpointer

These two concepts work together.

```text
thread_id
    ↓
Identifies conversation
    ↓
Checkpointer
    ↓
Loads/saves state for that thread
```

Without the thread ID, the checkpointer would not know which conversation state belongs to which execution.

---

# 22. Full Conversation Flow

```text
First User Message
       ↓
thread_id = "chat-1"
       ↓
Agent Runs
       ↓
Messages Added to State
       ↓
Checkpointer Saves State
```

Later:

```text
Second User Message
       ↓
thread_id = "chat-1"
       ↓
Checkpointer Loads State
       ↓
Previous Messages Available
       ↓
New Message Added
       ↓
Agent Runs
       ↓
Updated State Saved Again
```

---

# 23. Without a Checkpointer

Suppose:

```text
Invocation 1:
"My name is Sam."
```

Then a separate invocation:

```text
Invocation 2:
"What is my name?"
```

Without persistence, the second invocation may only receive the new message.

Conceptually:

```text
Run 1
State created
Run finishes
State disappears
```

---

# 24. With a Checkpointer

Now:

```text
Run 1
State created
      ↓
Checkpoint saved
```

Then:

```text
Run 2
Same thread_id
      ↓
Checkpoint loaded
      ↓
Previous messages restored
```

This enables short-term conversational memory.

---

# 25. Checkpointer = Thread-Scoped Memory

A useful way to think about it:

```text
Checkpointer
=
Short-term memory for one thread
```

It preserves the state of that conversation.

Important:

> This is different from long-term memory shared across threads.

---

# 26. Checkpointer vs Long-Term Memory

## Checkpointer

Scope:

```text
One thread
```

Used for:

```text
Conversation continuity
Resume
HITL
Fault recovery
State history
```

## Long-Term Store

Scope:

```text
Across threads
```

Used for things like:

```text
User preferences
Persistent facts
Shared knowledge
```

So:

```text
Checkpointer
=
Remember this conversation

Store
=
Remember information beyond this conversation
```

Stores are not the main topic of this lesson.

---

# 27. Messages + Threads + Checkpointers

The full relationship:

```text
MESSAGES
    ↓
Stored in graph STATE
    ↓
State belongs to THREAD
    ↓
THREAD identified by thread_id
    ↓
CHECKPOINTER saves STATE
```

---

# 28. Basic Thread Configuration

Conceptually, a LangGraph invocation can include:

```text
configurable:
    thread_id
```

Mental model:

```text
Agent Input
+
Thread Configuration
```

The input contains:

```text
new messages
```

The config tells the runtime:

```text
which saved conversation to use
```

---

# 29. Why `thread_id` Is Not Put Inside the User Message

The thread ID is runtime configuration.

It is not conversation content.

Wrong mental model:

```text
User message:
"My thread ID is abc."
```

Correct mental model:

```text
User message
+
Runtime config:
thread_id = "abc"
```

---

# 30. New Thread

If I use a new thread ID:

```text
thread_id = "chat-2"
```

LangGraph treats it as a separate conversation.

Conceptually:

```text
chat-1
→ existing history

chat-2
→ fresh history
```

---

# 31. Same Thread

If I reuse:

```text
thread_id = "chat-1"
```

the runtime can continue the existing conversation state.

So:

```text
Same thread_id
=
Continue conversation
```

```text
Different thread_id
=
Start separate conversation
```

---

# 32. In-Memory Checkpointer

A common development checkpointer is:

```text
InMemorySaver
```

It stores checkpoints in RAM.

Useful for:

```text
Learning
Testing
Local development
Short-lived applications
```

---

# 33. Limitation of In-Memory Persistence

If the process stops:

```text
Python process ends
      ↓
RAM cleared
      ↓
Checkpoints lost
```

So an in-memory checkpointer does not survive application restarts.

---

# 34. Persistent Checkpointers

For persistence across process restarts, a durable checkpointer can be used.

Examples include:

```text
SQLite
PostgreSQL
```

Conceptually:

```text
Agent
   ↓
Persistent Checkpointer
   ↓
Database / Disk
```

---

# 35. In-Memory vs Persistent

| In-Memory | Persistent |
|---|---|
| Stored in RAM | Stored on disk/database |
| Lost on process restart | Survives restart |
| Easy for learning | Better for real applications |
| Fast/simple | Requires storage setup |

---

# 36. Checkpointing Happens During Execution

A checkpointer does not only save the final answer.

LangGraph can save graph state as execution progresses.

Conceptually:

```text
State A
 ↓
Checkpoint

State B
 ↓
Checkpoint

State C
 ↓
Checkpoint
```

This supports features such as resumability and inspection.

---

# 37. Why Checkpoints Matter Beyond Chat History

Checkpoints enable:

```text
Conversation continuity
Human-in-the-loop
Resume after interruption
Fault recovery
State history
Time travel/debugging
```

For this lesson, the main focus is:

```text
Conversation continuity
```

HITL comes in Lesson 8.

---

# 38. Message History Growth

As a conversation gets longer:

```text
messages
    ↓
More messages
    ↓
More context
```

This can increase:

```text
Token usage
Latency
Context size
```

Deep Agents later uses context-management techniques to handle long threads.

That belongs to Module 3.

---

# 39. Message Object vs Plain String

LangChain uses structured message objects.

Why?

Because a message can contain more than text:

```text
Role
Text
Images
Tool calls
Metadata
Usage data
Message ID
```

So:

```text
Message
≠
Just a string
```

---

# 40. Message Content Can Be Structured

An `AIMessage` can contain:

```text
Plain string
```

or:

```text
Structured content blocks
```

It may also contain:

```text
tool_calls
usage_metadata
response_metadata
```

This is why printing `.content` does not always produce only plain text.

---

# 41. Tool Calls Are Stored in AI Messages

When the model decides to use a tool:

```text
AIMessage
    ↓
tool_calls
```

The actual tool result then appears as:

```text
ToolMessage
```

So message history contains the full agent interaction.

---

# 42. Tool Call IDs

A tool call has an ID.

The corresponding `ToolMessage` references the same ID.

Mental model:

```text
AIMessage
tool_call_id = 123
       ↓
Tool executes
       ↓
ToolMessage
tool_call_id = 123
```

This lets the runtime match:

```text
Tool request
↔
Tool response
```

---

# 43. Conversation State Example

A typical state might look conceptually like:

```text
Thread: chat-1

messages:

1. HumanMessage
   "What's the weather?"

2. AIMessage
   Tool Call → get_weather

3. ToolMessage
   "18°C"

4. AIMessage
   "The weather is 18°C."

5. HumanMessage
   "Should I take a jacket?"

6. AIMessage
   "Yes..."
```

All of this belongs to the same thread.

---

# 44. Thread State Is More Than Messages

A thread may contain state beyond messages.

Examples:

```text
files
todos
interrupt state
custom fields
```

The checkpointer saves graph state, not only chat text.

This is why it is more accurate to say:

```text
Checkpointer saves thread state
```

rather than:

```text
Checkpointer saves messages only
```

---

# 45. Deep Agents and Messages

Deep Agents extends the normal LangChain agent state.

Messages remain the main conversation channel.

Deep Agents may also store extra harness state.

Important mental model:

```text
Messages
=
Conversation portion of agent state
```

---

# 46. Deep Agents and Long Threads

Deep Agents supports long-running work.

As threads get longer, storing full duplicated message history in every checkpoint would be inefficient.

Current Deep Agents uses a delta-based message state design so checkpoint growth is more efficient over long threads.

For this lesson, I do not need implementation details.

Just remember:

> Deep Agents still relies on LangGraph state/checkpointing for persistence.

---

# 47. Thread vs Session

These words are sometimes used informally in similar ways.

But in LangGraph:

```text
thread_id
```

is the important runtime identifier for persisted graph state.

A UI may call it:

```text
Chat
Conversation
Session
```

but the LangGraph persistence concept is:

```text
Thread
```

---

# 48. Thread vs Run

These are different.

## Run

One execution of the agent.

```text
invoke()
```

## Thread

A series of related runs.

```text
Run 1
Run 2
Run 3
```

all using:

```text
same thread_id
```

So:

```text
Thread
=
Container for multiple related runs
```

---

# 49. One Thread Can Have Many Runs

Example:

```text
Thread: chat-1

Run 1
User asks question

Run 2
User asks follow-up

Run 3
User clarifies

Run 4
Agent resumes after interruption
```

All belong to the same persisted thread state.

---

# 50. One Run Does Not Necessarily Need Persistence

For a simple one-off request:

```text
User
 ↓
Agent
 ↓
Answer
```

a checkpointer may not be necessary.

Use persistence when the application needs:

```text
Multiple turns
Resume
HITL
State history
```

---

# 51. When I Need a Checkpointer

Use a checkpointer when:

```text
Conversation must continue across invocations
Agent must resume later
HITL is required
Execution state matters after interruption
I want thread history
```

---

# 52. When I Might Not Need One

For:

```text
One-shot task
Stateless request
Simple batch job
```

I may not need persisted thread state.

---

# 53. Common Mistake — Same Conversation, Different Thread IDs

Example:

```text
Turn 1:
thread_id = "1"

Turn 2:
thread_id = "2"
```

The second turn starts a different thread.

Therefore previous state is not loaded.

Correct:

```text
Turn 1:
thread_id = "1"

Turn 2:
thread_id = "1"
```

---

# 54. Common Mistake — Expecting InMemorySaver to Survive Restart

Wrong expectation:

```text
Close Python
Restart tomorrow
Conversation still exists
```

With an in-memory checkpointer:

```text
Process stops
→ state lost
```

Use persistent storage if restart persistence is required.

---

# 55. Common Mistake — Confusing Thread Memory With Long-Term Memory

Thread persistence:

```text
Conversation A remembers earlier turns.
```

Long-term memory:

```text
Conversation B knows a saved preference from Conversation A.
```

These are different.

---

# 56. Common Mistake — Manually Re-Sending Full History With a Checkpointer

If the checkpointer already restores the thread state, the application should generally send the **new turn**, not manually duplicate the whole saved history.

Otherwise history may be duplicated.

Mental model:

```text
Checkpointer
=
Loads old state

Application
=
Adds new message
```

---

# 57. Common Mistake — Thinking `thread_id` Is Memory

The thread ID does not itself contain information.

It is only an identifier.

```text
thread_id
=
Lookup key
```

The checkpointer holds the actual saved state.

---

# 58. Common Mistake — Thinking Checkpointer Saves to Disk Automatically

Not necessarily.

Storage depends on the checkpointer implementation.

```text
InMemorySaver
→ RAM

SqliteSaver
→ SQLite

PostgresSaver
→ PostgreSQL
```

---

# 59. Practical Mental Model

Think of a messaging app.

```text
Messages
=
Chat messages

Thread
=
One chat conversation

thread_id
=
Chat conversation ID

Checkpointer
=
Storage system saving the chat state
```

This is one of the easiest ways to remember the concepts.

---

# 60. Another Analogy — Game Save

```text
Agent State
=
Current game state

Thread
=
One game save slot

thread_id
=
Save slot ID

Checkpointer
=
Save system

Checkpoint
=
One saved snapshot
```

---

# 61. Interview-Level Explanation

If asked:

### "What are messages, threads, and checkpointers in LangGraph/Deep Agents?"

A good answer:

> **Messages are the structured conversation events exchanged between the user, model, and tools. A thread identifies one continuing graph conversation or execution history using a `thread_id`. A checkpointer persists snapshots of that thread's graph state, allowing later invocations using the same thread ID to restore previous state and continue the conversation.**

---

# 62. Interview Question — What Does a Thread ID Do?

> It identifies which persisted thread state LangGraph should load and update for an invocation.

---

# 63. Interview Question — Does a Checkpointer Only Store Messages?

> No. It stores graph state snapshots. Messages are an important part of that state, but other state fields can also be persisted.

---

# 64. Interview Question — Why Use a Checkpointer?

> To preserve thread-scoped state across invocations and support conversation continuity, resume, HITL, state history, and fault recovery.

---

# 65. Interview Question — Is InMemorySaver Persistent?

> It persists state only while the Python process is running. The data is lost when the process stops.

---

# 66. Interview Question — Checkpointer vs Store?

> A checkpointer persists graph state for one thread and acts as short-term thread memory. A store is used for long-term data that can be accessed across threads.

---

# 67. Revision Cheat Sheet

```text
MESSAGE
=
One conversation event
```

```text
THREAD
=
One continuing conversation
```

```text
thread_id
=
Identifier for the conversation
```

```text
CHECKPOINT
=
Saved snapshot of graph state
```

```text
CHECKPOINTER
=
Mechanism that saves and loads checkpoints
```

---

# 68. Core Flow

```text
New Message
    ↓
thread_id
    ↓
Checkpointer loads existing state
    ↓
Agent processes message
    ↓
State changes
    ↓
Checkpointer saves updated state
```

---

# 69. Same vs Different Thread

```text
Same thread_id
=
Continue conversation
```

```text
Different thread_id
=
Separate conversation
```

---

# 70. Persistence Levels

```text
InMemorySaver
=
Persists while process lives
```

```text
SQLite / PostgreSQL Checkpointer
=
Can persist across restarts
```

---

# 71. Five Things to Remember

1. **Messages are structured conversation events.**
2. **A thread represents one continuing conversation or execution history.**
3. **`thread_id` tells LangGraph which thread state to load.**
4. **A checkpointer saves and restores thread-scoped graph state.**
5. **Checkpointer memory is thread-scoped; long-term cross-thread memory is a different concept.**

---

# 72. Self-Check Questions

Before moving to Lesson 8, I should be able to answer:

1. What is a message?
2. What are the main message types?
3. What is stored inside an `AIMessage`?
4. What is a `ToolMessage`?
5. Why do tool calls have IDs?
6. What is a thread?
7. What is `thread_id`?
8. What happens if I change the thread ID?
9. What is a checkpointer?
10. What is a checkpoint?
11. Why do threads need a checkpointer for persistence?
12. What does `InMemorySaver` do?
13. Does `InMemorySaver` survive process restarts?
14. What is the difference between a thread and a run?
15. What is the difference between a checkpointer and long-term memory?
16. Does a checkpointer store only messages?
17. Why should I avoid manually duplicating history when using a checkpointer?
18. When do I need a persistent checkpointer?
19. What happens when I reuse the same thread ID?
20. How do messages, threads, and checkpointers connect?

---

# 73. One-Line Summary

> **Messages contain the conversation, a thread groups related agent runs using a `thread_id`, and a checkpointer saves that thread's graph state so the conversation can continue later.**

---

# 74. Final Mental Model

```text
                    USER
                     │
                     ▼
               HumanMessage
                     │
                     ▼
              thread_id = X
                     │
                     ▼
               CHECKPOINTER
                     │
              Load Thread State
                     │
                     ▼
                  AGENT
                     │
            ┌────────┴────────┐
            ▼                 ▼
        AIMessage         ToolMessage
            │                 │
            └────────┬────────┘
                     │
                     ▼
               Updated State
                     │
                     ▼
               CHECKPOINTER
                     │
                     ▼
               Save Checkpoint
                     │
                     ▼
              Future Invocation
                     │
              Same thread_id
                     │
                     ▼
               Continue Thread
```

---

# 75. Official References

- LangChain Messages  
  https://docs.langchain.com/oss/python/langchain/messages

- LangGraph Persistence  
  https://docs.langchain.com/oss/python/langgraph/persistence

- Deep Agents Architecture  
  https://github.com/langchain-ai/deepagents/blob/main/libs/ARCHITECTURE.md

- Deep Agents GitHub  
  https://github.com/langchain-ai/deepagents

- LangChain Academy — Introduction to Deep Agents  
  https://academy.langchain.com/courses/take/foundation-introduction-to-deepagents/

---

# 76. Next Lesson

> **Module 1 — Lesson 8: Human-in-the-Loop (HITL)**

Next I should learn:

```text
Interrupt
Pause execution
Human review
Approve
Edit
Reject
Resume
Why checkpointer + thread_id are required for resumable HITL
```
