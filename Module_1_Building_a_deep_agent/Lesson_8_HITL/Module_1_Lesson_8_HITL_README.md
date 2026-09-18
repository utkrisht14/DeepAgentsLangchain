# Module 1 — Building a Deep Agent
## Lesson 8 — Human-in-the-Loop (HITL)

> **Purpose:** Short notes on how Deep Agents can pause before sensitive tool actions and wait for human approval.

---

# 1. What Is HITL?

**HITL** means:

```text
Human-in-the-Loop
```

It allows a human to review an agent action before that action is executed.

Example:

```text
Agent wants to delete a file
        ↓
Execution pauses
        ↓
Human reviews
        ↓
Approve / Edit / Reject
```

---

# 2. Why HITL Is Useful

Some tools can perform sensitive actions.

Examples:

```text
Delete file
Send email
Modify database
Create payment
Run SQL
Change production data
```

For these actions, I may not want the agent to act automatically.

HITL adds a human approval step.

---

# 3. Basic HITL Flow

```text
User Request
    ↓
Agent reasons
    ↓
Agent selects sensitive tool
    ↓
Interrupt
    ↓
Execution pauses
    ↓
Human decision
    ↓
Agent resumes
```

---

# 4. What Is an Interrupt?

An **interrupt** pauses LangGraph execution.

The agent state is saved so execution can continue later.

Mental model:

```text
Running Agent
    ↓
Interrupt
    ↓
State Saved
    ↓
Wait for Human
```

---

# 5. `interrupt_on`

Deep Agents can be configured so selected tools require review.

Conceptually:

```text
interrupt_on = {
    "delete_file": True
}
```

Meaning:

```text
If agent tries delete_file
        ↓
Pause for human review
```

Tools not configured for interruption can continue normally.

---

# 6. Human Decisions

The main decisions are:

```text
approve
edit
reject
```

---

## Approve

Run the tool exactly as proposed.

```text
Agent proposal
    ↓
Approve
    ↓
Tool executes
```

---

## Edit

Modify the tool arguments before execution.

Example:

```text
Agent:
Delete file A

Human:
Change to file B

Tool executes with edited arguments
```

---

## Reject

Do not execute the proposed tool call.

```text
Agent proposal
    ↓
Reject
    ↓
Tool is skipped
```

---

# 7. HITL Needs a Checkpointer

This is very important.

When execution pauses, the agent must remember:

```text
Messages
Tool request
Current state
Where execution stopped
```

Therefore HITL requires a checkpointer.

Mental model:

```text
Interrupt
    ↓
Checkpointer saves state
    ↓
Human responds later
    ↓
State restored
```

---

# 8. HITL Needs a `thread_id`

The runtime also needs to know **which paused execution** should be resumed.

That is why we use:

```text
thread_id
```

The same thread ID must be used when resuming.

Flow:

```text
Initial Run
thread_id = "chat-1"
    ↓
Interrupt
    ↓
Checkpoint saved

Resume
thread_id = "chat-1"
    ↓
Correct state restored
```

---

# 9. Checkpointer + Thread ID

These concepts work together:

```text
thread_id
=
Which conversation/execution?

checkpointer
=
Where is its saved state?
```

For HITL:

```text
Interrupt
+
Checkpointer
+
Same thread_id
=
Resume safely
```

---

# 10. Resume

After the human decision, execution is resumed using a LangGraph `Command`.

Conceptually:

```text
Command(
    resume = human decision
)
```

The runtime restores the saved execution and continues from the interrupt.

---

# 11. Approve Flow

```text
Agent wants tool
    ↓
Interrupt
    ↓
Human: Approve
    ↓
Resume
    ↓
Tool executes
    ↓
Agent continues
```

---

# 12. Reject Flow

```text
Agent wants tool
    ↓
Interrupt
    ↓
Human: Reject
    ↓
Resume
    ↓
Tool does not execute
    ↓
Agent continues
```

---

# 13. Edit Flow

```text
Agent proposes tool arguments
    ↓
Interrupt
    ↓
Human edits arguments
    ↓
Resume
    ↓
Tool executes with edited values
```

---

# 14. HITL Is Usually Applied Selectively

Not every tool needs approval.

Example:

```text
read_file
→ No approval

search_web
→ No approval

delete_file
→ Approval required

send_email
→ Approval required
```

This keeps the workflow practical.

---

# 15. Risk-Based Configuration

A useful approach:

```text
Low-risk tool
→ No interrupt

Medium-risk tool
→ Approve / Reject

High-risk tool
→ Approve / Edit / Reject
```

---

# 16. HITL Does Not Mean the Human Writes the Whole Answer

The human normally reviews a proposed **action**.

The agent still handles:

```text
Reasoning
Tool selection
Task execution
Final response
```

The human only intervenes where required.

---

# 17. HITL vs Normal Tool Calling

Normal tool calling:

```text
Model
    ↓
Tool Call
    ↓
Tool Executes
```

HITL tool calling:

```text
Model
    ↓
Tool Call
    ↓
Interrupt
    ↓
Human Review
    ↓
Tool Executes or Is Rejected
```

---

# 18. Common Use Cases

HITL is useful for:

```text
Sending messages
Deleting data
Database updates
Production changes
Financial actions
Running dangerous commands
Publishing content
Changing external systems
```

---

# 19. Common Mistake — No Checkpointer

Without a checkpointer, the agent cannot safely pause and later resume its execution state.

Rule:

> HITL requires checkpointing.

---

# 20. Common Mistake — Different Thread ID on Resume

If I pause with:

```text
thread_id = "chat-1"
```

and resume with:

```text
thread_id = "chat-2"
```

the runtime is looking at a different thread.

Use the same ID.

---

# 21. Common Mistake — Interrupting Everything

If every tool requires approval:

```text
Agent becomes slow
User must approve constantly
```

Use HITL only where human review adds real value.

---

# 22. Common Mistake — Assuming Approval Makes the Action Safe

Approval is one safety layer.

I may still need:

```text
Permissions
Validation
Authentication
Argument checking
Access control
```

HITL does not replace normal security controls.

---

# 23. HITL and Lesson 7

Lesson 7 concepts are directly used here.

```text
Messages
    ↓
Thread
    ↓
Checkpointer
    ↓
Interrupt
    ↓
Human Decision
    ↓
Resume
```

So Lesson 7 is the persistence foundation for Lesson 8.

---

# 24. Simple Mental Model

Think of an approval workflow:

```text
Employee proposes action
    ↓
Manager reviews
    ↓
Approve / Change / Reject
    ↓
Employee continues
```

The agent is the employee.

The human reviewer is the manager.

---

# 25. Interview-Level Explanation

If asked:

### "What is HITL in Deep Agents?"

A good answer:

> **Human-in-the-loop allows Deep Agents to pause before selected tool operations so a human can approve, edit, or reject the proposed action. It uses LangGraph interrupts, requires a checkpointer to persist the paused state, and resumes using the same `thread_id`.**

---

# 26. Interview Question — Why Is a Checkpointer Required?

> Because the agent must save its execution state when it pauses and restore that state when the human decision arrives.

---

# 27. Interview Question — Why Is `thread_id` Required?

> It identifies the exact paused conversation/execution that should be resumed.

---

# 28. Interview Question — What Can the Human Do?

The main decisions are:

```text
Approve
Edit
Reject
```

Depending on the configured policy, only selected decisions may be allowed.

---

# 29. Revision Cheat Sheet

```text
HITL
=
Human review before sensitive action
```

```text
interrupt_on
=
Which tools require review
```

```text
Interrupt
=
Pause execution
```

```text
Checkpointer
=
Save paused state
```

```text
thread_id
=
Identify paused thread
```

```text
Command(resume=...)
=
Continue execution
```

---

# 30. Core Flow

```text
Model chooses tool
        ↓
Tool matches interrupt policy
        ↓
Interrupt
        ↓
Checkpoint saved
        ↓
Human reviews
        ↓
Approve / Edit / Reject
        ↓
Resume with same thread_id
        ↓
Agent continues
```

---

# 31. Five Things to Remember

1. **HITL adds human approval before selected agent actions.**
2. **`interrupt_on` decides which tools require review.**
3. **An interrupt pauses execution before the sensitive action runs.**
4. **A checkpointer and the same `thread_id` are required to resume safely.**
5. **The human can approve, edit, or reject the proposed action depending on configuration.**

---

# 32. Self-Check Questions

Before finishing Module 1, I should be able to answer:

1. What does HITL mean?
2. Why is HITL useful?
3. What is an interrupt?
4. What does `interrupt_on` control?
5. What are the main human decisions?
6. Why is a checkpointer needed?
7. Why must the same `thread_id` be used?
8. What does resume mean?
9. How is HITL different from normal tool calling?
10. Should every tool require HITL?

---

# 33. One-Line Summary

> **HITL lets a Deep Agent pause before sensitive tool actions, save its state, wait for a human decision, and then safely resume the same thread.**

---

# 34. Final Mental Model

```text
                 USER
                  │
                  ▼
                AGENT
                  │
                  ▼
             TOOL REQUEST
                  │
          Sensitive action?
             /        \
           No          Yes
           │            │
           ▼            ▼
      Tool Executes   INTERRUPT
                        │
                        ▼
                  CHECKPOINTER
                        │
                     Save State
                        │
                        ▼
                  HUMAN REVIEW
                /       |       \
          Approve      Edit     Reject
                \       |       /
                        ▼
                      RESUME
                        │
                Same thread_id
                        │
                        ▼
                 Agent Continues
```

---

# 35. Official References

- Deep Agents Human-in-the-Loop  
  https://docs.langchain.com/oss/python/deepagents/human-in-the-loop

- LangChain Human-in-the-Loop  
  https://docs.langchain.com/oss/python/langchain/human-in-the-loop

- LangGraph Interrupts / Persistence  
  https://docs.langchain.com/oss/python/langgraph/interrupts

- Deep Agents GitHub  
  https://github.com/langchain-ai/deepagents

---

# 36. Module 1 Complete

After this lesson, Module 1 has covered:

```text
Deep Agents Overview
Running a Deep Agent
Model
System Prompt
Tools
MCP
Messages / Threads / Checkpointer
HITL
```

Next:

> **Module 2 — Execution Environment**
