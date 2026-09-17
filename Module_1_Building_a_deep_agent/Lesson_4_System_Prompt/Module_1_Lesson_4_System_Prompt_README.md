# Module 1 — Building a Deep Agent
## Lesson 4 — The System Prompt

> **Purpose:** Short notes on what the system prompt is, what it controls, and how to write it well for a Deep Agent.

---

# 1. What Is a System Prompt?

A **system prompt** is the high-level instruction given to the model that defines how the agent should behave.

Think of it as:

```text
System Prompt
=
Role
+
Rules
+
Behavior
+
Task guidance
```

It gives the model context before it handles the user's request.

---

# 2. System Prompt vs User Prompt

## System Prompt

Defines the agent's permanent behavior.

Example idea:

```text
You are a research assistant.
Use tools when needed.
Keep answers concise.
```

## User Prompt

Defines the current task.

Example idea:

```text
Compare Python and Java for backend development.
```

So:

```text
System Prompt
=
How the agent should behave

User Prompt
=
What the user wants now
```

---

# 3. Why the System Prompt Matters

The model uses the system prompt to understand:

- its role
- its goals
- important constraints
- expected behavior
- when to use tools
- how to format the response

A clearer system prompt usually leads to more consistent agent behavior.

---

# 4. How Deep Agents Uses It

The custom system prompt is passed through:

```text
create_deep_agent(
    system_prompt=...
)
```

Deep Agents then combines it with any relevant harness/profile instructions before sending the final system instructions to the model.

Mental model:

```text
My System Prompt
      +
Deep Agents / Profile Instructions
      ↓
Final Instructions Sent to Model
```

---

# 5. Important Current Behavior

Deep Agents now keeps its default authored prompt intentionally lean.

This means:

> My own `system_prompt` should clearly describe the agent-specific behavior I need.

I should not assume that a large default prompt will define my application's role automatically.

---

# 6. What Should Go in a System Prompt?

A good system prompt usually contains only what the agent needs.

Useful sections:

```text
Role
Goal
Important rules
Tool-use guidance
Output style
Constraints
```

Example structure:

```text
Role:
You are a technical learning assistant.

Goal:
Explain AI concepts clearly.

Rules:
- Use simple language.
- Be concise.
- Do not invent facts.

Output:
Use short structured answers.
```

---

# 7. Keep It Specific

Weak:

```text
You are helpful.
```

Better:

```text
You are an AI learning assistant.
Explain technical concepts in simple language.
Keep answers concise and structured.
```

The second version gives the model clearer direction.

---

# 8. Keep It Actionable

Instructions should tell the model what to do.

Good:

```text
Use the search tool when current information is required.
```

Less useful:

```text
Be intelligent and careful.
```

Actionable instructions are easier for the model to follow.

---

# 9. Keep It Concise

Do not put unnecessary information into the system prompt.

Why?

Because the system prompt uses context-window space.

A useful rule:

> Include instructions the model actually needs to perform the task.

Avoid:

```text
Long explanations
Repeated instructions
Obvious information
Unrelated background
```

---

# 10. Avoid Repeating Tool Descriptions

If a tool already has a clear name, description, and schema, I usually do not need to repeat all of that inside the system prompt.

Better:

```text
Use the weather tool when weather information is required.
```

Instead of explaining every tool parameter again.

---

# 11. Avoid Conflicting Instructions

Bad example:

```text
System:
Always keep answers under 3 lines.

User:
Give me a detailed 2-page explanation.
```

Conflicting instructions make behavior less predictable.

I should design prompts so that:

```text
Role
Rules
User task
```

work together.

---

# 12. System Prompt Priority

At a high level, system-level instructions have higher priority than normal user instructions.

So if the user asks the model to ignore a system rule, the system instruction should still guide the behavior.

Mental model:

```text
System Instructions
      ↓
User Instructions
```

---

# 13. Do Not Put Secrets in the Prompt

The system prompt should not contain secrets such as:

```text
API keys
Passwords
Private credentials
Tokens
```

Prompts are instructions, not secret storage.

---

# 14. Good System Prompt Checklist

Before using a system prompt, ask:

- Is the agent role clear?
- Is the goal clear?
- Are the important rules explicit?
- Are instructions actionable?
- Is anything repeated?
- Is there unnecessary background?
- Are there conflicting instructions?
- Is the expected output style clear?
- Are tool-use rules included only when needed?

---

# 15. Simple Mental Model

```text
MODEL
   +
SYSTEM PROMPT
   ↓
Model understands
how it should behave
```

Then:

```text
SYSTEM PROMPT
   +
USER REQUEST
   +
TOOLS
   ↓
AGENT DECISION
```

---

# 16. System Prompt and Tool Use

The system prompt can guide tool behavior.

Example idea:

```text
Use the available database tool for account information.
Do not guess database values.
```

The model then uses this instruction when deciding whether to call the tool.

Important:

> The prompt guides tool usage, but the tool definition itself still tells the model how the tool works.

---

# 17. System Prompt and Output Style

The system prompt can also control response style.

Examples:

```text
Keep answers short.
Use bullet points.
Explain concepts for beginners.
Return JSON.
Use professional language.
```

This helps produce more consistent outputs.

---

# 18. System Prompt and Agent Role

The role helps define the agent's perspective.

Examples:

```text
Research assistant
Coding assistant
Travel planner
Data analyst
Learning assistant
```

But the role alone is not enough.

Better:

```text
Role
+
Goal
+
Rules
```

---

# 19. Common Mistakes

## Too vague

```text
You are helpful.
```

## Too long

Hundreds of unnecessary instructions.

## Too repetitive

The same rule written several times.

## Too many unrelated responsibilities

One prompt trying to make the agent expert at everything.

## Conflicting rules

Instructions that disagree with each other.

## Tool details duplicated unnecessarily

Repeating the full tool schema in the prompt.

---

# 20. Practical Rule of Thumb

A good system prompt should answer:

```text
Who are you?

What should you do?

What rules must you follow?

How should you respond?
```

If those four things are clear, the prompt is usually in good shape.

---

# 21. Interview-Level Explanation

If asked:

### "What is the system prompt in a Deep Agent?"

A good answer:

> **The system prompt defines the agent's high-level role, behavior, constraints, and task guidance. Deep Agents combines the custom system prompt with any relevant harness or model-profile instructions before sending the final system instructions to the model. A good system prompt should be concise, specific, and actionable.**

---

# 22. Revision Cheat Sheet

```text
System Prompt
=
Role
+
Goal
+
Rules
+
Behavior
```

Remember:

```text
System Prompt
→ How the agent should behave

User Prompt
→ What the user wants now
```

Good prompts are:

```text
Clear
Specific
Actionable
Concise
Non-conflicting
```

---

# 23. Five Things to Remember

1. **The system prompt defines the agent's high-level behavior.**
2. **It is different from the user's current request.**
3. **Keep it specific and actionable.**
4. **Do not overload it with unnecessary information.**
5. **Deep Agents may combine it with harness/profile instructions before the model sees it.**

---

# 24. Self-Check Questions

Before moving to Lesson 5, I should be able to answer:

1. What is a system prompt?
2. How is it different from a user prompt?
3. What should normally be included in it?
4. Why should it be concise?
5. Why should instructions be actionable?
6. How can it guide tool use?
7. What happens if instructions conflict?
8. Why should tool descriptions not be unnecessarily duplicated?
9. Can Deep Agents add other instructions around my prompt?
10. What are the four questions a good system prompt should answer?

---

# 25. One-Line Summary

> **The system prompt tells the Deep Agent's model who it is, how it should behave, what rules to follow, and how to handle the user's task.**

---

# 26. Official References

- LangChain Deep Agents implementation  
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/graph.py

- Deep Agents GitHub  
  https://github.com/langchain-ai/deepagents

- LangChain Agent Quickstart  
  https://github.com/langchain-ai/docs/blob/main/src/oss/langchain/quickstart.mdx

- LangChain Academy — Introduction to Deep Agents  
  https://academy.langchain.com/courses/take/foundation-introduction-to-deepagents/

---

# 27. Next Lesson

> **Module 1 — Lesson 5: Tools**

Next I should learn:

```text
What a tool is
How the model chooses tools
Tool descriptions
Tool arguments
Tool results
Why tool quality matters
```
