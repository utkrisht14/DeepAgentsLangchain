# Module 3 — Context Management
## Lesson 3 — Memory

> **Goal:** Understand Deep Agents memory as durable context stored in `AGENTS.md`.

---

# 1. What Is Memory?

In this lesson, **memory** means durable agent context stored in files such as:

```text
AGENTS.md
```

It can contain:

```text
Preferences
Project conventions
Important facts
Working rules
Long-term instructions
```

The agent can load this memory again in future runs.

---

# 2. Basic Idea

```text
Run 1
User gives durable information
    ↓
Agent updates AGENTS.md
    ↓
File is saved

Run 2
Fresh agent starts
    ↓
AGENTS.md is loaded
    ↓
Agent remembers the information
```

This does not require the previous conversation messages.

---

# 3. Example

`AGENTS.md` might contain:

```markdown
# Agent Memory

## Development Preferences

- Use Python 3.13.
- Use uv for package management.
- Keep code examples simple.
```

A new agent run can use these instructions immediately.

---

# 4. Basic Configuration

Conceptually:

```python
agent = create_deep_agent(
    model="openai:gpt-5.5",
    backend=backend,
    memory=["/AGENTS.md"]
)
```

This tells the agent to load the memory file into its context.

---

# 5. What Should Go Into Memory?

Good memory content:

```text
Stable preferences
Project standards
Reusable facts
Naming conventions
Development rules
Long-term guidance
```

Avoid storing temporary information that is only useful for one conversation.

---

# 6. Memory vs Checkpointer

These are different.

## Checkpointer

```text
Remembers conversation/thread state
```

Example:

```text
Previous messages
Tool calls
Execution state
```

## AGENTS.md Memory

```text
Remembers durable knowledge across fresh runs
```

Example:

```text
Use uv
Use Python 3.13
Follow project naming rules
```

Simple difference:

```text
Checkpointer
=
Remember this conversation

Memory
=
Remember durable context
```

---

# 7. Memory vs Skills

They are also different.

## Memory

Tells the agent:

```text
What should be remembered?
```

Example:

```text
Use uv for Python package management.
```

## Skill

Tells the agent:

```text
How should a task be performed?
```

Example:

```text
How to create a Python project with uv.
```

So:

```text
Memory
=
Facts, preferences, conventions

Skills
=
Procedures and workflows
```

---

# 8. Memory Is Usually Always Relevant

Memory is generally loaded as part of the agent context.

That makes it suitable for information that should influence many future tasks.

Skills are usually more selective and are loaded only when needed.

---

# 9. Why Memory Is Useful

Without durable memory:

```text
New run
→ Agent starts without project preferences
```

With `AGENTS.md`:

```text
New run
→ Memory loaded
→ Agent immediately knows project rules
```

This improves consistency across sessions.

---

# 10. Keep Memory Small and Useful

Too much memory can increase context size and reduce quality.

Good memory should be:

```text
Stable
Relevant
Concise
Reusable
```

Avoid turning `AGENTS.md` into a full conversation log.

---

# 11. Simple Mental Model

Think of `AGENTS.md` as the agent's long-term notebook.

```text
Checkpointer
=
Conversation history

AGENTS.md
=
Long-term notebook

SKILL.md
=
How-to manual
```

---

# 12. Five Things to Remember

1. **Memory in this lesson means durable context stored in `AGENTS.md`.**
2. **It survives fresh agent runs because the file is loaded again.**
3. **It is different from checkpointer-based conversation memory.**
4. **Memory stores facts/preferences; skills store procedures.**
5. **Keep memory concise and limited to stable, reusable information.**

---

# 13. One-Line Summary

> **Deep Agents memory uses files such as `AGENTS.md` to preserve durable preferences, facts, conventions, and instructions across fresh agent runs.**

---

# References

- Deep Agents Memory Middleware  
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/memory.py

- Deep Agents GitHub  
  https://github.com/langchain-ai/deepagents
