# Module 4 — Delegation
## Lesson 2 — Building a Subagent Team

> **Goal:** Understand how to create multiple specialist subagents and let a main agent delegate work to the right specialist.

---

# 1. What Is a Subagent Team?

A **subagent team** is a group of specialist agents managed by one main agent.

Example:

```text
Main Agent
   ↓
 ┌───────────────┬───────────────┐
 ↓               ↓               ↓
Researcher    Risk Analyst    Writer
```

Each subagent has a specific responsibility.

---

# 2. Why Use a Team?

A team is useful when one task contains different kinds of work.

Example:

```text
Research
Analysis
Writing
Review
Planning
```

Instead of one agent doing everything, each specialist handles the part it is best suited for.

---

# 3. Main Agent Role

The main agent acts like a coordinator.

It is responsible for:

```text
Understanding the user request
Breaking the work into subtasks
Choosing the right subagent
Delegating work
Combining results
Giving the final answer
```

The main agent stays responsible for the overall task.

---

# 4. Subagent Role

Each subagent should have a clear specialty.

Example:

```text
Research Agent
→ gathers information

Risk Agent
→ identifies risks

Writer Agent
→ produces polished output
```

A focused role usually gives better results than a very broad one.

---

# 5. Defining Multiple Subagents

Conceptually:

```python
subagents = [
    researcher,
    risk_analyst,
    writer
]
```

Then:

```python
agent = create_deep_agent(
    model="openai:gpt-5.5",
    subagents=subagents
)
```

Deep Agents exposes the built-in `task` tool so the main agent can delegate to these specialists.

---

# 6. Choosing the Right Subagent

The main agent uses the subagent:

```text
name
description
```

to decide which specialist should receive the task.

Example:

```text
name:
risk-analyst

description:
Identify delivery, technical, and operational risks.
```

A good description helps the main model route work correctly.

---

# 7. Specialized Tools

Each subagent can have its own tools.

Example:

```text
Research Agent
→ web_search

Data Agent
→ database_query

Writer Agent
→ no tools
```

This follows the principle:

```text
Give each subagent only the tools it needs.
```

That keeps the team easier to control.

---

# 8. Isolated Context

Subagents normally work in isolated context.

```text
Main conversation
      ↓
Relevant delegated task
      ↓
Subagent
```

The subagent does not need the full parent conversation unless relevant context is explicitly passed.

This helps reduce context size.

---

# 9. Delegation Flow

```text
User Request
     ↓
Main Agent
     ↓
Break task into parts
     ↓
task(...)
     ↓
Choose subagent
     ↓
Subagent performs work
     ↓
Result returned
     ↓
Main Agent continues
     ↓
Final answer
```

---

# 10. Example Team

Suppose the user asks:

```text
Review our product launch plan and prepare a management summary.
```

The main agent could use:

```text
Research Agent
→ check assumptions

Risk Agent
→ identify risks

Writer Agent
→ prepare final summary
```

Then the main agent combines the results.

---

# 11. Sequential vs Parallel Delegation

Delegation can happen:

```text
Sequentially
```

Example:

```text
Research
   ↓
Risk analysis
   ↓
Writing
```

or:

```text
In parallel
```

Example:

```text
Research Agent ──┐
                 ├─→ Main Agent
Risk Agent ──────┘
```

Parallel execution is useful when subtasks are independent.

---

# 12. Good Team Design

A good team should have:

```text
Clear roles
Minimal overlap
Focused descriptions
Only required tools
Clear expected outputs
```

Avoid creating many agents with nearly identical responsibilities.

---

# 13. When Not to Use a Team

Do not create a subagent team for a simple task.

Example:

```text
"Rewrite this sentence."
```

A team would add unnecessary complexity.

Use multiple subagents when the task genuinely benefits from specialization.

---

# 14. Team vs Single Subagent

Single subagent:

```text
Main Agent
   ↓
Risk Analyst
```

Subagent team:

```text
Main Agent
   ↓
 ┌────────────┬────────────┐
 ↓            ↓            ↓
Research    Risk        Writer
```

Lesson 1 focused on delegation itself.

Lesson 2 focuses on designing multiple specialists.

---

# 15. Simple Mental Model

Think of a project manager and a specialist team.

```text
Main Agent
=
Project Manager

Subagents
=
Specialists

task tool
=
Work assignment
```

---

# 16. Five Things to Remember

1. **A subagent team contains multiple specialist agents.**
2. **The main agent decides which specialist should handle each subtask.**
3. **Each subagent should have a clear role and only the tools it needs.**
4. **Subagents normally work with isolated context.**
5. **The main agent combines subagent results into the final response.**

---

# 17. One-Line Summary

> **A subagent team lets the main Deep Agent coordinate multiple specialists, delegate the right work to each one, and combine their results into a final answer.**

---

# References

- Deep Agents Subagents
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/subagents.py

- Deep Agents GitHub
  https://github.com/langchain-ai/deepagents
