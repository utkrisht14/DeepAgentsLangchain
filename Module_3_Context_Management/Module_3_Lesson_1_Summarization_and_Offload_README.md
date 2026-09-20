# Module 3 — Context Management
## Lesson 1 — Summarization and Offload

> **Goal:** Understand how Deep Agents manage long conversations when the context window starts getting full.

---

# 1. Why Context Management Is Needed

As an agent works for a long time, its message history keeps growing.

```text
More messages
    ↓
More tokens
    ↓
Larger context
    ↓
Higher cost / latency
    ↓
Eventually context limit
```

Deep Agents uses context-management techniques such as:

```text
Summarization
Offload
```

---

# 2. What Is Summarization?

**Summarization** compresses older conversation history into a shorter summary.

Instead of keeping every old message in active context:

```text
Old Message 1
Old Message 2
Old Message 3
Old Message 4
```

the agent may replace them with:

```text
Summary:
"The user is building a Deep Agents project and has already
implemented MCP, HITL, filesystem backends, and sandboxes."
```

This reduces the number of tokens sent to the model.

---

# 3. What Happens During Summarization?

Conceptually:

```text
Conversation grows
      ↓
Token threshold reached
      ↓
Older messages selected
      ↓
LLM creates summary
      ↓
Old messages removed from active context
      ↓
Summary inserted
      ↓
Recent messages kept
```

So the model still knows the important history without seeing every old message.

---

# 4. Summarization Middleware

Deep Agents uses summarization middleware.

Conceptually:

```python
SummarizationMiddleware(
    model=...,
    backend=...,
    trigger=...,
    keep=...
)
```

Important settings:

```text
trigger
→ When summarization should happen

keep
→ How much recent context should remain unchanged
```

---

# 5. Example

Before summarization:

```text
Message 1
Message 2
Message 3
Message 4
Message 5
Message 6
Message 7
Message 8
```

After summarization:

```text
Summary of Messages 1–5

Message 6
Message 7
Message 8
```

The model receives much less context.

---

# 6. What Is Offload?

**Offload** means moving detailed information out of the active model context and storing it somewhere else.

Example:

```text
Large conversation history
        ↓
Backend storage
```

The information is no longer sent to the model on every request.

But it can still be stored for later inspection or retrieval.

---

# 7. Why Offload?

The model's context window is limited.

Some information may be useful to preserve, but not useful enough to keep sending on every model call.

So:

```text
Active Context
=
Only information needed now

Offloaded Storage
=
Detailed information kept outside context
```

---

# 8. Deep Agents Summarization + Offload

In current Deep Agents, summarization and offloading work together.

When old messages are summarized:

```text
Old Messages
      ↓
Full history offloaded to backend
      ↓
Short summary generated
      ↓
Summary stays in active context
```

So the detailed history is preserved externally while the model sees the compressed version.

Current Deep Agents stores offloaded conversation history under a path such as:

```text
/conversation_history/...
```

---

# 9. Summarization vs Offload

| Summarization | Offload |
|---|---|
| Compresses information | Moves information out of active context |
| Keeps a shorter representation | Keeps full detailed data externally |
| Summary stays visible to model | Offloaded content is not always sent to model |
| Reduces token usage | Reduces active context size |
| Useful for conversation history | Useful for large/detailed data |
| Loses some detail through compression | Preserves original detail externally |

---

# 10. The Most Important Difference

```text
Summarization
=
Keep the meaning, reduce the size
```

```text
Offload
=
Keep the full data, move it somewhere else
```

---

# 11. They Are Complementary

They are not competing approaches.

A strong pattern is:

```text
Detailed history
      ↓
Offload full history
      ↓
Create short summary
      ↓
Put summary in context
```

So:

```text
Offload preserves detail
+
Summarization preserves useful meaning
```

---

# 12. Simple Analogy

Imagine studying from a large textbook.

## Summarization

You write:

```text
1-page revision notes
```

instead of carrying the whole chapter in your head.

## Offload

You keep the full textbook on your shelf.

You do not carry it everywhere, but it is still available if needed.

---

# 13. When Summarization Is Best

Use summarization when:

```text
Conversation is becoming long
Old details can be compressed
Model still needs the main context
Token usage is growing
```

---

# 14. When Offload Is Best

Use offload when:

```text
Information is large
Exact details should be preserved
Data does not need to stay in active context
Information may be needed later
```

---

# 15. What Should Stay in Active Context?

Usually keep:

```text
Current user request
Recent conversation
Current task state
Important constraints
Recent tool results
Compact summary of older history
```

Move less-active detail outside the context.

---

# 16. Context Management Mental Model

```text
                FULL HISTORY
                     │
                     ▼
              Context gets large
                     │
              ┌──────┴──────┐
              ▼             ▼
        Summarization     Offload
              │             │
      Short useful      Full detail
         summary        stored outside
              │             │
              └──────┬──────┘
                     ▼
              Smaller context
                     ▼
                   Model
```

---

# 17. Summarization Is Not Perfect Memory

A summary may lose small details.

Example:

Original:

```text
User prefers Python 3.12,
uses uv,
runs Windows,
and wants comments in all code.
```

Poor summary:

```text
User is learning Python.
```

Some useful detail was lost.

That is why summarization quality matters.

---

# 18. Offload Does Not Automatically Mean Recall

Offloaded data existing somewhere does not necessarily mean the model is seeing it.

The information may need to be:

```text
Read
Retrieved
Loaded
Referenced
```

before it becomes active context again.

---

# 19. Automatic vs On-Demand Summarization

Deep Agents can summarize automatically when context reaches a configured threshold.

It can also expose a compaction tool so summarization can be triggered intentionally.

Conceptually:

```text
Automatic
→ Context threshold reached

Manual / Tool-based
→ Agent decides to compact now
```

---

# 20. Five Things to Remember

1. **Summarization compresses old context into a shorter representation.**
2. **Offload moves detailed information outside the active model context.**
3. **Summarization reduces tokens but may lose detail.**
4. **Offload preserves full detail but the model may need to retrieve it later.**
5. **Deep Agents can combine both: offload full history and keep a summary in context.**

---

# 21. Interview-Level Answer

### What is the difference between summarization and offloading?

> **Summarization reduces context size by replacing older information with a compact representation. Offloading removes detailed information from the model's active context and stores it externally. In Deep Agents they can work together: the full conversation history is offloaded while a summary remains in the model context.**

---

# 22. One-Line Summary

> **Summarization keeps a compressed version of information in context, while offloading keeps the full information outside the context window.**

---

# References

- Deep Agents Summarization Middleware  
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/summarization.py

- Deep Agents Architecture  
  https://github.com/langchain-ai/deepagents/blob/main/libs/ARCHITECTURE.md

- Deep Agents GitHub  
  https://github.com/langchain-ai/deepagents
