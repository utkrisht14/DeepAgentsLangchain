# Module 4 — Delegation
## Lesson 3 — Dynamic Subagents

> **Goal:** Understand how Deep Agents can orchestrate subagents dynamically from interpreter code instead of relying on one model-chosen delegation at a time.

---

# 1. What Are Dynamic Subagents?

Dynamic subagents let the main agent dispatch subagents from the **interpreter** using code.

Instead of:

```text
Model
  ↓
task(...)
  ↓
One subagent
```

the agent can use interpreter logic such as:

```text
Loop
Branch
Fan-out
Parallel calls
Result aggregation
```

to coordinate multiple subagent calls.

---

# 2. Important Clarification

Dynamic subagents do **not necessarily mean creating brand-new agent definitions at runtime**.

Usually, the subagents are already configured.

What becomes dynamic is:

```text
Which subagent is called
How many times it is called
Which inputs it receives
Whether calls run in loops or batches
How results are combined
```

---

# 3. Why Use Dynamic Subagents?

They are useful when a task contains many independent items.

Example:

```text
Review 20 support tickets
        ↓
Interpreter loop
        ↓
Call triage subagent for each ticket
        ↓
Collect results
        ↓
Produce summary
```

This is more efficient than asking the model to choose one delegation at a time.

---

# 4. Interpreter Requirement

Dynamic subagents depend on the interpreter.

Conceptually:

```text
Main Agent
    ↓
Interpreter
    ↓
task(...)
    ↓
Subagents
```

In Python, current Deep Agents uses the QuickJS interpreter integration.

---

# 5. `task()` Inside Interpreter Code

When subagents and interpreter middleware are enabled, the interpreter exposes:

```text
task()
```

Conceptually:

```javascript
const result = await task({
    description: "Analyse this item",
    subagentType: "risk-analyst"
});
```

The call runs the selected subagent and returns its result.

---

# 6. Dynamic Fan-Out

One powerful pattern is fan-out.

Example:

```text
Input items
   ↓
Interpreter loop
   ↓
 ┌────────────┬────────────┬────────────┐
 ↓            ↓            ↓            ↓
Task 1       Task 2       Task 3       Task 4
 ↓            ↓            ↓            ↓
Subagent     Subagent     Subagent     Subagent
   \           |           |          /
             Results
                ↓
           Main Agent
```

This is useful when the subtasks are independent.

---

# 7. Dynamic Branching

Interpreter logic can choose different specialists.

Example:

```text
If task is financial
→ budget-agent

If task is technical
→ engineering-agent

If task is legal
→ compliance-agent
```

The routing logic happens in code.

---

# 8. Static Delegation vs Dynamic Delegation

## Static / Normal Delegation

```text
Model
↓
Chooses task tool
↓
Calls one subagent
↓
Receives result
```

Good for:

```text
One or a few direct delegations
```

## Dynamic Subagents

```text
Model
↓
Interpreter
↓
Code decides many task() calls
↓
Subagents
↓
Results collected
```

Good for:

```text
Large batches
Loops
Fan-out
Multi-perspective analysis
Structured orchestration
```

---

# 9. Why This Is Better for Large Workflows

Without dynamic orchestration:

```text
Model
↓
task
↓
Model
↓
task
↓
Model
↓
task
```

With dynamic subagents:

```text
Model
↓
Interpreter
↓
task()
task()
task()
task()
↓
Collect results
↓
Model
```

This reduces repeated model-controlled routing steps.

---

# 10. Relation to Programmatic Tool Calling

Dynamic subagents are similar to Programmatic Tool Calling.

```text
PTC
→ interpreter calls tools.*

Dynamic Subagents
→ interpreter calls task()
```

They can also be combined:

```text
Interpreter
   ↓
tools.* to discover/filter inputs
   ↓
task() to delegate analysis
```

---

# 11. Persistence

With interpreter:

```text
mode="thread"
```

interpreter variables can persist across turns in the same thread.

This can support multi-turn orchestration workflows.

---

# 12. When Should I Use Dynamic Subagents?

Use them when:

```text
There are many independent items
The task needs loops or branching
Multiple perspectives are needed
Work should fan out across specialists
Results need programmatic aggregation
```

For one simple delegation, normal `task` calling is easier.

---

# 13. Simple Mental Model

Think of:

```text
Normal delegation
=
Manager assigns one task manually

Dynamic subagents
=
Manager writes a workflow that assigns many tasks automatically
```

---

# 14. Current Status

Dynamic subagents currently use the interpreter runtime and are marked as:

```text
Beta
```

So APIs and lifecycle behavior may still change.

For Python, the current interpreter integration requires:

```text
Python 3.11+
langchain-quickjs >= 0.2.0
```

---

# 15. Five Things to Remember

1. **Dynamic subagents are orchestrated from interpreter code.**
2. **Configured subagents are still the workers; the orchestration becomes dynamic.**
3. **Interpreter code can use loops, branches, batches, and `task()`.**
4. **They are most useful for large or repetitive delegation workflows.**
5. **For one simple delegation, normal subagent calling is usually better.**

---

# 16. One-Line Summary

> **Dynamic subagents let a Deep Agent use interpreter code to programmatically dispatch, coordinate, and combine many subagent calls in a flexible workflow.**

---

# References

- Dynamic Subagents  
  https://docs.langchain.com/oss/deepagents/dynamic-subagents

- Deep Agents Subagents  
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/subagents.py
