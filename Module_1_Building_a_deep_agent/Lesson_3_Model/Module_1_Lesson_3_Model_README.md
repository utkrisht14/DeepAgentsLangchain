# Module 1 — Building a Deep Agent
## Lesson 3 — Model

> **Purpose:** My study notes for understanding the role of the **model** inside a Deep Agent.
>
> This lesson only focuses on the model. It does **not** go deeply into tools, MCP, memory, backends, subagents, or HITL.

---

# 1. Learning Objectives

By the end of this lesson, I should understand:

- what the **model** is in a Deep Agent
- why the model is the decision-making component
- how a model is passed to `create_deep_agent()`
- what the `provider:model` format means
- why tool-calling support matters
- why different models can behave differently
- what factors matter when choosing a model
- why the model should now be specified explicitly

---

# 2. What Is the Model?

The **model** is the LLM used by the Deep Agent.

Examples of model providers include:

```text
OpenAI
Anthropic
Google
Other LangChain-supported providers
```

The model is responsible for:

```text
Understanding the user request
        ↓
Reasoning about the task
        ↓
Deciding whether a tool is needed
        ↓
Choosing the tool
        ↓
Using tool results
        ↓
Generating the final answer
```

So the model is the main **decision-making component** of the agent.

---

# 3. Model vs Agent

These are not the same thing.

```text
MODEL
=
LLM that reasons and makes decisions
```

```text
AGENT
=
Model
+
Tools
+
Instructions
+
State
+
Runtime
+
Harness capabilities
```

So:

> The model is one component inside the Deep Agent.

---

# 4. Simple Mental Model

```text
User Request
      ↓
Deep Agent
      ↓
Model
      ↓
What should I do next?
      │
      ├── Answer directly
      │
      └── Request a tool
```

The model decides the next action.

---

# 5. What the Model Does During an Agent Run

A Deep Agent may call the model several times.

Example:

```text
User
 ↓
Model
 ↓
Tool Call
 ↓
Tool Result
 ↓
Model
 ↓
Another Tool Call
 ↓
Tool Result
 ↓
Model
 ↓
Final Answer
```

So:

```text
One agent run
may contain
many model calls
```

---

# 6. How a Model Is Given to Deep Agents

The model is passed through the `model` parameter of:

```text
create_deep_agent(...)
```

Conceptually:

```text
create_deep_agent(
    model = ...
)
```

Deep Agents then resolves the model and uses it when constructing the LangChain agent.

---

# 7. Two Common Ways to Specify a Model

There are two main approaches.

## Option 1 — Model String

Conceptually:

```text
provider:model
```

Example format:

```text
openai:model-name
```

This lets LangChain identify:

```text
Provider
+
Model name
```

---

## Option 2 — Model Object

Instead of a string, I can create a chat-model object first.

Conceptually:

```text
Create model object
       ↓
Configure it
       ↓
Pass object to Deep Agent
```

This is useful when I need more control over model settings.

---

# 8. `provider:model` Format

A model string generally follows:

```text
provider:model
```

Example idea:

```text
openai:some-model
anthropic:some-model
```

The first part identifies:

```text
Provider
```

The second part identifies:

```text
Specific model
```

This is a convenient LangChain model-resolution format.

---

# 9. Why Explicit Model Selection Matters

Current Deep Agents behavior expects me to specify the model explicitly.

Older versions allowed:

```text
model=None
```

and Deep Agents could fall back to a default model.

That fallback behavior is deprecated.

So my mental rule should be:

> **Always choose the model explicitly when creating a Deep Agent.**

This makes the application clearer and avoids depending on hidden defaults.

---

# 10. Why Tool Calling Matters

Deep Agents are agentic systems.

The model often needs to do more than generate text.

It may need to request:

```text
Search
API call
Database lookup
File operation
Subagent task
Other tool
```

For this reason, the model should support **tool calling**.

---

# 11. What Is Tool Calling?

Tool calling means the model can produce a structured request such as:

```text
Use Tool X
with these arguments
```

Conceptually:

```text
Model
  ↓
Tool Call Request
  ↓
Runtime
  ↓
Tool Executes
  ↓
Tool Result
  ↓
Model
```

The model does **not** directly execute the tool.

It requests the tool.

---

# 12. Model Responsibility vs Runtime Responsibility

This distinction is important.

## Model

Decides:

```text
Do I need a tool?
Which tool?
What arguments?
What should I do after the result?
```

## Runtime

Handles:

```text
Actually executing the tool
Returning the result
Updating state
Calling the model again
```

So:

```text
Model
=
Decision maker

Runtime
=
Executor / coordinator
```

---

# 13. Why Different Models Behave Differently

Even with:

```text
Same system prompt
Same tools
Same user request
```

different models may produce different behavior.

For example:

```text
Model A
→ chooses the correct tool immediately

Model B
→ answers without the tool

Model C
→ uses several unnecessary tool calls
```

This happens because models differ in their capabilities.

---

# 14. Important Model Capabilities

When choosing a model for a Deep Agent, I should mainly consider:

```text
Tool calling quality
Reasoning ability
Instruction following
Context window
Latency
Cost
Reliability
```

---

# 15. Tool Calling Quality

A good agent model should be able to:

```text
Recognize when a tool is required
Choose the correct tool
Provide valid arguments
Use the tool result correctly
Avoid unnecessary calls
```

This is very important for Deep Agents.

---

# 16. Reasoning Ability

Complex Deep Agent tasks may involve:

```text
Many steps
Several tools
Ambiguous information
Long context
Planning
Delegation
```

A stronger reasoning model may perform these tasks more reliably.

---

# 17. Instruction Following

The model must follow instructions from:

```text
System prompt
User request
Tool descriptions
Harness instructions
```

Poor instruction following can cause:

```text
Wrong tool usage
Ignoring constraints
Incorrect output format
Stopping too early
```

---

# 18. Context Window

The context window controls how much information the model can consider at one time.

The context can include:

```text
System prompt
Message history
Tool definitions
Tool results
Loaded files
Memory
Skills
Summaries
```

A larger context window can help with long tasks.

But Deep Agents also uses context-management techniques, so simply choosing the largest context window is not the whole solution.

---

# 19. Latency

Latency means:

```text
How long the model takes to respond
```

This matters because one Deep Agent run may call the model multiple times.

Example:

```text
5 model calls
×
model response time
=
total agent latency
```

A very slow model can make an agent feel slow.

---

# 20. Cost

Agent workflows may make several model calls.

Therefore model cost matters.

Conceptually:

```text
Cost per model call
×
Number of model calls
×
Tokens used
=
Agent cost
```

A more capable model may cost more but may also require fewer unnecessary actions.

So model selection is a tradeoff.

---

# 21. Reliability

For agents, reliability is more than:

```text
"Can the model write a good answer?"
```

It also means:

```text
Can it use tools correctly?
Can it follow schemas?
Can it continue after tool results?
Can it stay on task?
Can it finish multi-step work?
```

---

# 22. Model Selection Depends on the Task

There is no single best model for every Deep Agent.

Example:

```text
Simple assistant
→ fast / lower-cost model may be enough
```

```text
Complex research agent
→ stronger reasoning model may be better
```

```text
Coding agent
→ model strong in code/tool use may be preferable
```

So:

> Choose the model based on the task requirements.

---

# 23. Model-Agnostic Does Not Mean Identical Behavior

Deep Agents is designed to work with different model providers.

But:

```text
Same Deep Agent configuration
+
Different models
=
Potentially different behavior
```

This is normal.

Model-agnostic means:

```text
I am not locked to one provider
```

It does **not** mean:

```text
Every model performs exactly the same
```

---

# 24. Model Configuration

If I create a model object myself, I may configure model-specific settings.

Examples can include:

```text
Model name
Temperature
Timeout
Retries
Provider-specific options
```

Not every provider supports exactly the same parameters.

For this lesson, the important point is:

> A model object gives me more explicit control than only supplying a model string.

---

# 25. Temperature

Temperature generally influences output randomness.

Mental model:

```text
Lower temperature
→ more consistent / less random
```

```text
Higher temperature
→ more varied / creative
```

For many agentic tasks, consistency is often more useful than creativity.

But exact behavior depends on the model/provider.

---

# 26. Model Choice and Tools

The model must understand the available tool descriptions.

Conceptually it receives:

```text
Tool name
Tool description
Argument schema
```

Then it decides:

```text
Should I call this tool?
```

So agent performance depends on both:

```text
Model quality
+
Tool definition quality
```

---

# 27. Model Choice and System Prompt

The system prompt tells the model how to behave.

So:

```text
Model
+
System Prompt
=
Reasoning behavior shaped by instructions
```

A strong model can still perform poorly if instructions are unclear.

We study the system prompt in Lesson 4.

---

# 28. Model Choice and Deep Agents Harness

Deep Agents can adjust parts of the harness based on the selected model/provider.

The project supports model/provider-specific **harness profiles**.

At a high level, these can tune things such as:

```text
Prompt instructions
Tool descriptions
Middleware choices
Subagent behavior
```

I do not need to master profiles in this lesson.

The only important idea is:

> Deep Agents may adapt some harness behavior to the selected model family.

---

# 29. What Happens When Deep Agents Resolves a Model

Conceptually:

```text
Model input
   ↓
Resolve model
   ↓
Identify provider/model
   ↓
Apply relevant harness configuration
   ↓
Pass model into LangChain agent
```

Then that model is used during agent execution.

---

# 30. Common Beginner Mistake — Not Specifying a Model

Older examples may rely on a default model.

Current best practice:

```text
Specify the model explicitly.
```

This avoids deprecated behavior and makes the code clearer.

---

# 31. Common Beginner Mistake — Choosing a Model Without Tool Calling

A normal chat model may be good at text generation but unsuitable for agent workflows if it cannot reliably call tools.

For Deep Agents, I should verify:

```text
Does this model support tool calling?
```

---

# 32. Common Beginner Mistake — Thinking the Model Executes Tools

Incorrect:

```text
Model executes Python/API
```

Correct:

```text
Model requests tool
Runtime executes tool
```

---

# 33. Common Beginner Mistake — Assuming Bigger Always Means Better

A larger or more expensive model is not automatically the best choice.

I should consider:

```text
Task complexity
Tool-use quality
Latency
Cost
Reliability
```

---

# 34. Common Beginner Mistake — Comparing Models Only by Answer Quality

For agent use, I also need to evaluate:

```text
Tool selection
Tool arguments
Multi-step completion
Instruction following
Recovery after tool results
```

Agent performance is broader than normal chatbot performance.

---

# 35. Practical Model Selection Checklist

When selecting a model for a Deep Agent, ask:

- Does it support tool calling?
- Is it strong enough for the task?
- Does it follow instructions well?
- Is the context window sufficient?
- Is the latency acceptable?
- Is the cost acceptable?
- Is it reliable over multiple steps?
- Does the provider integrate well with LangChain?

---

# 36. My Simple Decision Rule

```text
Simple task
↓
Use a capable fast model

Complex multi-step task
↓
Use stronger reasoning/tool-use model

High-volume application
↓
Balance quality + cost + latency
```

---

# 37. Model and Agent Performance

A useful mental equation:

```text
Agent Quality
=
Model Quality
+
Prompt Quality
+
Tool Quality
+
Context Quality
+
Runtime Design
```

So the model is important, but it is not the only factor.

---

# 38. Interview-Level Explanation

If someone asks:

### "What is the role of the model in a Deep Agent?"

My answer:

> **The model is the decision-making component of the Deep Agent. It interprets the user request, follows the system instructions, decides whether tools are needed, generates structured tool calls, uses tool results, and determines when the task is complete. Deep Agents can work with different LangChain-supported tool-calling models, and the model can be provided as either a provider/model string or a configured chat-model object.**

---

# 39. Interview Question — Why Does Tool Calling Matter?

> Deep Agents perform actions through tools. The model must be able to reliably decide when a tool is needed, choose the correct tool, and generate valid arguments for it.

---

# 40. Interview Question — Does Deep Agents Require One Specific Provider?

> No. Deep Agents is model-agnostic and can use different LangChain-supported providers, although behavior and performance can vary between models.

---

# 41. Interview Question — Does the Model Execute the Tool?

> No. The model generates the tool-call request. The agent runtime executes the tool and returns the result to the model.

---

# 42. Interview Question — Why Might Two Models Behave Differently?

> Models differ in reasoning ability, instruction following, tool-calling quality, context capacity, latency, and other provider/model characteristics.

---

# 43. Revision Cheat Sheet

```text
MODEL
=
LLM used by the Deep Agent
```

```text
Main job:
Understand
Reason
Choose action
Request tools
Use results
Answer
```

```text
Deep Agents model input:
provider:model
OR
configured model object
```

```text
Important capabilities:
Tool calling
Reasoning
Instruction following
Context
Reliability
```

```text
Important tradeoffs:
Quality
Cost
Latency
```

---

# 44. Five Things I Should Remember

1. **The model is the decision-making component of a Deep Agent.**

2. **Deep Agents should now be created with an explicitly selected model.**

3. **A model can be supplied as a provider/model string or as a configured model object.**

4. **Tool-calling quality is especially important for agentic workflows.**

5. **Different models can produce different agent behavior even with the same tools and prompt.**

---

# 45. Self-Check Questions

Before moving to Lesson 4, I should be able to answer:

1. What is the model's role inside a Deep Agent?
2. Is a model the same thing as an agent?
3. What does `provider:model` mean?
4. What are the two common ways to provide a model?
5. Why should the model now be specified explicitly?
6. Why is tool calling important?
7. Who executes the actual tool?
8. Why might two models behave differently?
9. What factors matter when selecting a model?
10. Why is the most expensive model not automatically the best choice?
11. What does context window mean?
12. Why do cost and latency matter more in agents than in one-shot model calls?
13. What is the purpose of a model object?
14. What does model-agnostic mean?
15. What should I evaluate besides final answer quality?

---

# 46. One-Line Summary

> **The model is the reasoning and decision-making engine inside a Deep Agent; it understands the task, decides which actions or tools are needed, processes their results, and produces the final response.**

---

# 47. Final Mental Model

```text
              USER REQUEST
                    │
                    ▼
               DEEP AGENT
                    │
                    ▼
                  MODEL
                    │
           What should I do?
              /           \
             /             \
            ▼               ▼
      Answer directly     Use Tool
                              │
                              ▼
                         Tool Request
                              │
                              ▼
                           Runtime
                              │
                              ▼
                            Tool
                              │
                              ▼
                         Tool Result
                              │
                              └──────→ MODEL
                                         │
                                         ▼
                                   Final Answer
```

---

# 48. Official References

- Deep Agents GitHub README  
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/README.md

- Deep Agents `create_deep_agent()` implementation  
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/graph.py

- Deep Agents Architecture  
  https://github.com/langchain-ai/deepagents/blob/main/libs/ARCHITECTURE.md

- LangChain Academy — Introduction to Deep Agents  
  https://academy.langchain.com/courses/take/foundation-introduction-to-deepagents/

---

# 49. Next Step

Next lesson:

> **Module 1 — Lesson 4: The System Prompt**

There I should focus on:

```text
What the system prompt is
How it shapes model behavior
How Deep Agents combines instructions
What belongs in a system prompt
What should not be placed there
```
