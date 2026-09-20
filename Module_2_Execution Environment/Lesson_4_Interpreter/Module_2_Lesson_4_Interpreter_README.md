# Module 2 — Execution Environment
## Lesson 4 — Interpreter

> **Goal:** Understand what the Deep Agents interpreter is, why it is useful, and how it differs from normal shell execution.

---

# 1. What Is the Interpreter?

The **Interpreter** gives a Deep Agent a persistent code execution environment.

In current Deep Agents, this is commonly provided through:

```python
CodeInterpreterMiddleware
```

with a QuickJS-based JavaScript runtime.

Mental model:

```text
Deep Agent
    ↓
Interpreter Middleware
    ↓
Persistent REPL
    ↓
Run code
```

---

# 2. Why Use an Interpreter?

Normal tool calling works well for one action at a time.

But sometimes the agent needs to:

```text
Loop over data
Filter results
Aggregate values
Reuse variables
Call several tools
Perform calculations between tool calls
```

The interpreter lets the agent do this inside one code execution step.

---

# 3. Interpreter vs `execute`

These are different.

## `execute`

Runs a shell command.

Example:

```text
python script.py
ls
git status
```

Usually provided by:

```text
LocalShellBackend
Sandbox Backend
```

## Interpreter

Runs code inside a REPL-like environment.

Example:

```javascript
const values = [10, 20, 30];
values.reduce((a, b) => a + b, 0);
```

So:

```text
execute
=
Shell / process execution

Interpreter
=
Persistent code workspace
```

---

# 4. Persistent REPL

A major feature of the interpreter is that variables can remain available across multiple interpreter calls.

Example:

```javascript
const price = 600;
```

Later:

```javascript
price * 0.9
```

The interpreter can reuse the earlier variable.

This makes it useful for multi-step reasoning.

---

# 5. Thread Isolation

Interpreter state is associated with the conversation thread.

Conceptually:

```text
Thread A
→ its own interpreter variables

Thread B
→ separate interpreter variables
```

So two threads should not automatically share interpreter state.

---

# 6. Basic Setup

The interpreter can be added as middleware.

Example:

```python
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openai:gpt-5.5",
    middleware=[
        CodeInterpreterMiddleware()
    ]
)
```

This adds an interpreter tool, typically:

```text
eval
```

The model can use it when code execution is useful.

---

# 7. Why `ainvoke()` Is Preferred

The interpreter can expose async bridges, especially when programmatic tool calling is enabled.

So the recommended execution style is:

```python
result = await agent.ainvoke(...)
```

rather than:

```python
agent.invoke(...)
```

---

# 8. Programmatic Tool Calling (PTC)

One powerful feature is **Programmatic Tool Calling**.

PTC lets interpreter code call selected agent tools directly.

Conceptually:

```text
Interpreter code
    ↓
tools.search(...)
tools.lookup(...)
tools.calculate(...)
```

This avoids sending every individual tool call back through the model.

---

# 9. Why PTC Helps

Without PTC:

```text
Model
↓
Tool 1
↓
Model
↓
Tool 2
↓
Model
↓
Tool 3
```

With PTC:

```text
Model
↓
Interpreter
↓
Tool 1
Tool 2
Tool 3
↓
Interpreter processes results
↓
Model receives final result
```

This can reduce model round trips.

---

# 10. PTC Is Explicit

Programmatic Tool Calling is not automatically enabled for every tool.

It uses an allowlist.

Example idea:

```python
CodeInterpreterMiddleware(
    ptc=["search_web"]
)
```

Only approved tools are available from interpreter code.

---

# 11. Interpreter vs Sandbox

These concepts are related but different.

```text
Interpreter
=
How code is evaluated

Sandbox
=
Where execution is isolated
```

An interpreter may itself use a restricted runtime.

A sandbox focuses on protecting the host environment.

---

# 12. Interpreter vs Tool

A normal tool is a predefined capability:

```python
calculate_price()
```

The interpreter is more general.

It allows the model to dynamically write code such as:

```javascript
const total = prices
    .filter(x => x > 100)
    .reduce((a, b) => a + b, 0);
```

So:

```text
Tool
=
Predefined operation

Interpreter
=
General code execution environment
```

---

# 13. Good Use Cases

The interpreter is useful for:

```text
Loops
Filtering
Aggregation
Data transformation
Parallel tool calls
Multi-step calculations
Dynamic subagent orchestration
Reusing intermediate variables
```

---

# 14. When I Probably Do Not Need It

For simple tasks like:

```text
Call one API
Read one file
Calculate one number
Send one request
```

a normal tool call is usually simpler.

---

# 15. Security

Interpreter execution should still be treated carefully.

Important controls include:

```text
Restricted runtime
Timeouts
Memory limits
Explicit tool allowlists
Thread isolation
```

Programmatic access to sensitive tools should not be enabled casually.

---

# 16. Interpreter and Dynamic Subagents

Later in the course, dynamic subagents can use the interpreter.

The interpreter can run orchestration code such as:

```text
Loop over tasks
    ↓
Call task(...)
    ↓
Collect subagent results
    ↓
Combine results
```

We will cover that in Module 4.

---

# 17. Simple Mental Model

Think of the interpreter as a small notebook or REPL available to the agent.

```text
Model
=
Decides what calculation/workflow is needed

Interpreter
=
Runs that calculation/workflow as code
```

---

# 18. Five Things to Remember

1. **The interpreter gives the agent a persistent code execution environment.**
2. **It is different from shell `execute`; interpreter code runs inside a REPL.**
3. **Variables can be reused across interpreter calls within the same thread.**
4. **PTC lets interpreter code call selected agent tools directly.**
5. **Use `ainvoke()` when interpreter async bridges are involved.**

---

# 19. One-Line Summary

> **The Deep Agents interpreter is a persistent code workspace that lets the agent perform calculations, loops, data processing, and approved tool orchestration without requiring a separate model round trip for every step.**

---

# References

- Deep Agents QuickJS Interpreter  
  https://github.com/langchain-ai/deepagents/tree/main/libs/partners/quickjs

- Dynamic Subagents  
  https://github.com/langchain-ai/docs/blob/main/src/oss/deepagents/dynamic-subagents.mdx

- Deep Agents GitHub  
  https://github.com/langchain-ai/deepagents
