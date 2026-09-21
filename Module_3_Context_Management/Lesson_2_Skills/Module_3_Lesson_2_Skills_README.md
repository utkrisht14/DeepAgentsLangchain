# Module 3 — Context Management
## Lesson 2 — Skills

> **Goal:** Understand Deep Agents skills as reusable task instructions stored in files such as `SKILL.md`.

---

# 1. What Is a Skill?

A **skill** is reusable know-how for performing a specific type of task.

It tells the agent:

```text
How should this task be done?
```

Skills are usually written as instructions in a file such as:

```text
SKILL.md
```

---

# 2. Example

A skill for creating a Word document might contain:

```markdown
# Create Word Document

1. Collect the required content.
2. Structure headings and sections.
3. Create the .docx file.
4. Apply simple formatting.
5. Save the final document.
```

The skill does not perform the action itself.

It tells the agent **how to perform it**.

---

# 3. Skill Mental Model

```text
User asks for a task
        ↓
Agent identifies relevant skill
        ↓
SKILL.md is loaded
        ↓
Agent follows the instructions
        ↓
Task is completed
```

---

# 4. Skills Are Usually Text Instructions

A skill is mainly:

```text
Instructions
Procedures
Best practices
Workflow steps
Task-specific guidance
```

It is not usually executable code by itself.

---

# 5. Skill vs Tool

These are different.

## Skill

Tells the agent:

```text
How to do something
```

Example:

```text
How to prepare a PDF report
```

## Tool

Allows the agent to:

```text
Actually perform an action
```

Example:

```text
create_pdf()
send_email()
search_database()
```

So:

```text
Skill
=
Know-how

Tool
=
Capability
```

---

# 6. Skills Can Use Tools

A skill may instruct the agent to use one or more tools.

Example:

```text
SKILL.md

1. Search the source data.
2. Calculate totals.
3. Create the report.
4. Save the file.
```

The agent may then use:

```text
search tool
calculator tool
file tool
```

The skill coordinates the workflow.

---

# 7. Skill vs Memory

This is an important distinction.

## Memory

Tells the agent:

```text
What should I remember?
```

Example:

```text
Use uv for Python projects.
```

## Skill

Tells the agent:

```text
How should I perform this task?
```

Example:

```text
How to create a Python project using uv.
```

So:

```text
Memory
=
Facts, preferences, conventions

Skill
=
Procedures and workflows
```

---

# 8. Progressive Disclosure

Skills are useful for context management because the agent does not need every workflow loaded all the time.

Conceptually:

```text
Many available skills
        ↓
Agent sees skill descriptions
        ↓
Relevant skill selected
        ↓
Detailed SKILL.md loaded
```

This is called:

```text
Progressive Disclosure
```

It helps keep the active context smaller.

---

# 9. Why Skills Are Useful

Without skills:

```text
Large system prompt
→ every workflow included all the time
```

With skills:

```text
Small general prompt
+
Relevant skill loaded only when needed
```

Benefits:

```text
Smaller context
Reusable workflows
Better organization
Easier maintenance
More consistent task execution
```

---

# 10. What Belongs in a Skill?

Good skill content includes:

```text
Step-by-step workflow
Task rules
Best practices
Required tools
Output requirements
Important constraints
```

Avoid storing unrelated project facts in a skill.

Those belong in memory instead.

---

# 11. Skills Can Be Specialized

Examples:

```text
PDF creation skill
Data analysis skill
Code review skill
Email drafting skill
Report generation skill
Deployment skill
```

Each skill should focus on one task area.

---

# 12. Keep Skills Focused

A good skill should be:

```text
Specific
Reusable
Clear
Action-oriented
Not unnecessarily long
```

One large skill covering everything is usually harder to maintain.

---

# 13. Skill vs System Prompt

System prompt:

```text
General behavior for the agent
```

Skill:

```text
Detailed instructions for one type of task
```

Example:

```text
System Prompt:
"You are a helpful AI engineering assistant."

Skill:
"How to review a LangGraph application before deployment."
```

---

# 14. Simple Mental Model

Think of:

```text
System Prompt
=
Job description

Memory
=
Notebook of important facts

Skill
=
Instruction manual

Tool
=
Equipment
```

---

# 15. Five Things to Remember

1. **A skill contains reusable instructions for how to perform a task.**
2. **Skills are commonly stored in files such as `SKILL.md`.**
3. **Skills are usually loaded only when relevant, which helps context management.**
4. **A skill provides know-how; a tool provides the actual capability.**
5. **Memory stores durable facts/preferences, while skills store procedures.**

---

# 16. One-Line Summary

> **Deep Agents skills are reusable task-specific instruction sets, typically stored in `SKILL.md`, that teach the agent how to perform a workflow without keeping every workflow permanently in active context.**

---

# References

- Deep Agents Skills Middleware  
  https://github.com/langchain-ai/deepagents

- LangChain Deep Agents Documentation  
  https://docs.langchain.com/oss/python/deepagents
