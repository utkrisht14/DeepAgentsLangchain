# Module 4 — Delegation
## Lesson 1 — Delegation

> **Goal:** Understand how a Deep Agent delegates work to a subagent and why delegation helps with complex tasks.

---

# 1. What Is Delegation?

**Delegation** means the main agent gives part of a task to another agent.

Mental model:

```text
User
  ↓
Main Agent
  ↓
Delegates subtask
  ↓
Subagent
  ↓
Returns result
  ↓
Main Agent combines result
```

The main agent stays responsible for the final answer.

---

# 2. Why Use Delegation?

Delegation is useful when a task is:

```text
Complex
Multi-step
Context-heavy
Better handled by a specialist
Easy to split into independent parts
```

Instead of one agent doing everything, the work can be divided.

---

# 3. Subagents

A **subagent** is another agent invoked by the main agent for a specific task.

A subagent can have its own:

```text
System prompt
Tools
Model
Skills
Permissions
Specialized role
```

Example:

```text
Main Agent
    ↓
Research Subagent
    ↓
Research result
```

---

# 4. The `task` Tool

Deep Agents exposes delegation through a tool commonly called:

```text
task
```

The main agent uses this tool when it decides another agent should handle a subtask.

Conceptually:

```text
Main Agent
    ↓
task(...)
    ↓
Subagent
    ↓
Result
```

The model itself decides when delegation is useful.

---

# 5. What Is Passed to a Subagent?

The main agent should send a clear task description.

Example:

```text
Research the main advantages of electric vehicles.
Return 3 concise points with evidence.
```

The delegated prompt should include:

```text
What to do
Relevant context
Expected output
Constraints
```

A vague delegated task usually produces a weaker result.

---

# 6. Isolated Context

By default, a subagent works with an isolated context.

That means it usually receives only the delegated task, not the entire parent conversation.

```text
Main Agent Context
        ↓
Delegated Task Only
        ↓
Subagent Context
```

This is useful because the subagent does not need all of the main agent's history.

It helps reduce context pressure.

---

# 7. Delegation as Context Management

Delegation is not only about specialization.

It also helps context management.

Example:

```text
Main Agent
    ↓
Large research task
    ↓
Subagent handles detailed research
    ↓
Returns concise report
    ↓
Main Agent receives only useful result
```

The detailed intermediate work stays mostly inside the subagent.

---

# 8. Main Agent vs Subagent

## Main Agent

Responsible for:

```text
Understanding user request
Breaking down the task
Choosing when to delegate
Combining results
Giving final answer
```

## Subagent

Responsible for:

```text
Completing delegated task
Using its tools
Returning a useful result
```

---

# 9. Delegation Does Not Mean Parallelism

Delegation and parallel execution are different concepts.

```text
Delegation
=
Give work to another agent

Parallelism
=
Run multiple tasks at the same time
```

Delegated tasks may run sequentially or concurrently.

We will cover multi-subagent teams in Lesson 2.

---

# 10. When Should I Delegate?

Delegate when:

```text
The subtask is complex
A specialist can do it better
The task requires a lot of context
The result can be summarized cleanly
The task can be separated from the main workflow
```

Do not delegate very small tasks unnecessarily.

---

# 11. Good Delegation Example

User asks:

```text
Compare Python, Java, and Go for backend development.
```

The main agent could delegate:

```text
Subagent 1
→ Research Python

Subagent 2
→ Research Java

Subagent 3
→ Research Go
```

Then:

```text
Main Agent
→ Compare the reports
→ Give final answer
```

---

# 12. Poor Delegation Example

For a simple question:

```text
What is 10 + 20?
```

Creating a subagent is unnecessary.

Delegation adds overhead.

---

# 13. Delegation Flow

```text
User Request
     ↓
Main Agent
     ↓
Identifies subtask
     ↓
Calls task tool
     ↓
Subagent created
     ↓
Subagent performs work
     ↓
Subagent returns final report
     ↓
Main Agent continues
     ↓
Final answer to user
```

---

# 14. Important Point

The subagent's response is normally returned to the main agent.

The main agent should then:

```text
Understand it
Combine it with other information
Present the final answer
```

The subagent is helping the main agent, not replacing it.

---

# 15. Simple Mental Model

Think of a manager and specialist.

```text
Main Agent
=
Manager

Subagent
=
Specialist

task tool
=
Delegation request
```

The manager decides what work to delegate and uses the specialist's result.

---

# 16. Five Things to Remember

1. **Delegation means giving a subtask to another agent.**
2. **Deep Agents exposes delegation through the `task` tool.**
3. **Subagents normally work with isolated context.**
4. **Delegation helps both specialization and context management.**
5. **The main agent remains responsible for combining results and answering the user.**

---

# 17. One-Line Summary

> **Delegation lets a Deep Agent hand complex or specialized subtasks to isolated subagents, receive their results, and use those results to complete the larger task.**

---

# References

- Deep Agents Subagent Middleware  
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/subagents.py

- Deep Agents GitHub  
  https://github.com/langchain-ai/deepagents
