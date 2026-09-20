# Module 2 — Execution Environment
## Lesson 2 — Filesystem Backends

> **Goal:** Understand how Deep Agents decides where files are stored and accessed.

---

# 1. What Is a Filesystem Backend?

A **filesystem backend** is the storage layer used by Deep Agents for file operations.

The agent may use tools such as:

```text
ls
read_file
write_file
edit_file
glob
grep
```

The backend decides where those files actually live.

Mental model:

```text
Deep Agent
    ↓
Filesystem Tool
    ↓
Backend
    ↓
Actual Storage
```

---

# 2. Why Backends Matter

The same agent code can use different storage strategies.

For example:

```text
StateBackend
→ files live in agent/thread state

FilesystemBackend
→ files live on the local disk

StoreBackend
→ files live in a durable LangGraph store
```

So the backend changes the **storage location**, not the basic file tools the agent sees.

---

# 3. StateBackend

`StateBackend` stores files inside LangGraph agent state.

```text
StateBackend
→ virtual files
→ thread-scoped
```

Important points:

- Files are not normal files in my project folder.
- They can persist across turns when checkpointing is used.
- They are not automatically shared across different threads.

This is the default backend when no backend is provided.

Example idea:

```python
backend = StateBackend()
```

Use it when I want a safe, temporary workspace for one conversation.

---

# 4. FilesystemBackend

`FilesystemBackend` works with real files on the local filesystem.

```text
FilesystemBackend
→ actual disk files
```

Example:

```python
backend = FilesystemBackend(
    root_dir="C:/my/project"
)
```

Now file operations can read and write real files under that directory.

Use it for:

```text
Local development
Coding assistants
Working with project files
```

Be careful because the agent is accessing real files.

---

# 5. StoreBackend

`StoreBackend` stores files in a LangGraph store.

```text
StoreBackend
→ durable storage
→ can be shared across threads
```

This is useful for information that should survive beyond one conversation.

Example use cases:

```text
Long-term instructions
Persistent notes
Reusable memories
Shared agent files
```

---

# 6. ContextHubBackend

`ContextHubBackend` stores files durably in a LangSmith Context Hub repository.

Conceptually:

```text
Deep Agent
    ↓
ContextHubBackend
    ↓
LangSmith Context Hub
```

This is useful when I want durable agent context without managing my own storage backend.

---

# 7. CompositeBackend

`CompositeBackend` lets different paths use different backends.

Example idea:

```text
/workspace/*
→ StateBackend

/memories/*
→ StoreBackend
```

Mental model:

```text
One Agent
   ↓
CompositeBackend
   ↓
Different paths routed
to different storage systems
```

This is useful when temporary files and long-term files need different storage.

---

# 8. Backend Comparison

| Backend | Where Files Live | Persistence |
|---|---|---|
| `StateBackend` | Agent state | Usually thread-scoped |
| `FilesystemBackend` | Local disk | Persists on disk |
| `StoreBackend` | LangGraph store | Durable across threads |
| `ContextHubBackend` | LangSmith Context Hub | Durable |
| `CompositeBackend` | Multiple backends | Depends on route |

---

# 9. Backend vs Checkpointer

These are different concepts.

```text
Backend
=
Where files are stored

Checkpointer
=
How graph/thread state is saved
```

For example:

```text
StateBackend
+
Checkpointer
```

allows virtual files stored in agent state to persist across turns in the same thread.

---

# 10. Backend vs Sandbox

A filesystem backend answers:

> Where are my files?

A sandbox answers:

> Where can commands/code safely execute?

Some sandbox backends provide both:

```text
Filesystem
+
execute
```

We cover that in Lesson 3.

---

# 11. Which Backend Should I Choose?

Simple rule:

```text
Temporary thread workspace
→ StateBackend

Real local project files
→ FilesystemBackend

Long-term cross-thread storage
→ StoreBackend

LangSmith-managed durable context
→ ContextHubBackend

Mixed storage needs
→ CompositeBackend
```

---

# 12. Security Note

More direct filesystem access means more risk.

```text
StateBackend
→ isolated virtual files

FilesystemBackend
→ real machine files
```

So local filesystem access should only be used when I trust the environment and the agent behavior.

---

# 13. Five Things to Remember

1. **Backends decide where Deep Agent files are stored.**
2. **The same file tools can work with different backend implementations.**
3. **`StateBackend` is thread-scoped and virtual.**
4. **`FilesystemBackend` accesses real local files.**
5. **`CompositeBackend` can route different paths to different storage systems.**

---

# 14. One-Line Summary

> **A filesystem backend is the storage layer behind Deep Agents file tools, controlling whether files live in agent state, local disk, durable storage, or a combination of these.**

---

# References

- Deep Agents Backends  
  https://docs.langchain.com/oss/python/deepagents/backends

- Deep Agents GitHub  
  https://github.com/langchain-ai/deepagents
