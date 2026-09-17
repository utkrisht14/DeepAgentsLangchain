# Module 1 — Building a Deep Agent
## Lesson 5 — Tools

> **Purpose:** Short notes on what tools are, how the model chooses them, and how tools fit into a Deep Agent.

---

# 1. What Is a Tool?

A **tool** is a function or capability that the model can ask the agent runtime to execute.

Examples:

```text
Search the web
Query a database
Call an API
Calculate something
Read a file
Send a request
Look up information
```

A tool allows the agent to do something beyond normal text generation.

---

# 2. Why Tools Are Needed

An LLM knows how to generate text, but it cannot directly perform external actions.

For example, the model cannot directly:

```text
Query my database
Call my company's API
Read a live weather service
Execute my Python function
```

Instead:

```text
Model
  ↓
Requests Tool
  ↓
Runtime Executes Tool
  ↓
Tool Returns Result
  ↓
Model Uses Result
```

---

# 3. Model vs Tool

This distinction is important.

```text
MODEL
=
Decides what should be done
```

```text
TOOL
=
Performs a specific action
```

Example:

```text
Model:
"I need today's weather."

Tool:
get_weather("Amsterdam")
```

---

# 4. Tool Calling Flow

The basic flow is:

```text
User Request
      ↓
Model
      ↓
Need a tool?
    /      \
   No      Yes
   │        │
   ▼        ▼
Answer   Tool Call
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
           ▼
         Model
           │
           ▼
      Final Answer
```

---

# 5. The Model Does Not Execute the Tool

The model only generates a structured request.

Conceptually:

```text
Tool:
get_weather

Arguments:
city = "Amsterdam"
```

The actual tool is executed by the agent runtime.

So:

```text
Model
=
Requests action

Runtime
=
Executes action
```

---

# 6. How Tools Are Added to a Deep Agent

Custom tools are supplied when creating the Deep Agent.

Conceptually:

```text
create_deep_agent(
    tools = [...]
)
```

The model can then see those tools during execution.

---

# 7. What the Model Knows About a Tool

The model normally receives information such as:

```text
Tool name
Tool description
Argument schema
```

The model uses this information to decide:

```text
Should I use this tool?

Which tool should I use?

What arguments should I provide?
```

---

# 8. Tool Name

The tool name should clearly describe its purpose.

Good:

```text
get_weather
search_customer
calculate_tax
```

Weak:

```text
tool1
helper
do_task
```

A clear name makes tool selection easier for the model.

---

# 9. Tool Description

The description explains **when and why** the tool should be used.

Good idea:

```text
Use this tool to retrieve the current weather for a city.
```

Poor idea:

```text
Weather function.
```

The description is important because the model uses it when choosing between tools.

---

# 10. Tool Arguments

Tools can accept structured arguments.

Example conceptually:

```text
Tool:
get_weather

Arguments:
city
country
```

The model must generate valid values for those arguments.

---

# 11. Argument Schema

The argument schema tells the model:

```text
Which parameters exist
What types they have
Which ones are required
```

Example idea:

```text
city: string
days: integer
```

A clear schema reduces incorrect tool calls.

---

# 12. Tool Result

After execution, the tool returns a result.

Example:

```text
Tool Call:
get_weather("Amsterdam")

Tool Result:
18°C, partly cloudy
```

The model then receives this result and decides what to do next.

---

# 13. The Tool Result Is Not Automatically the Final Answer

Important:

```text
Tool Result
≠
Final Response
```

Normally:

```text
Tool Result
      ↓
Model
      ↓
Final User-Friendly Answer
```

The model interprets the raw tool output before responding.

---

# 14. A Tool Should Have One Clear Responsibility

Good tool:

```text
get_course_duration(course_name)
```

Less ideal tool:

```text
search_database_send_email_create_report(...)
```

A focused tool is easier for the model to understand and use correctly.

---

# 15. Tools Should Return Useful Information

A tool result should be:

```text
Clear
Relevant
Structured enough to understand
Not unnecessarily large
```

Bad tool outputs make the model's job harder.

---

# 16. Tool Selection Is Done by the Model

If several tools are available:

```text
weather_tool
calculator
customer_search
```

the model decides which one is appropriate.

Example:

```text
"What is the weather in Helsinki?"

→ weather_tool
```

```text
"What is 35 × 19?"

→ calculator
```

---

# 17. A Tool Being Available Does Not Mean It Will Be Used

Tools are available capabilities.

The model may decide:

```text
I already know enough.
No tool needed.
```

So:

```text
Available Tool
≠
Automatically Called Tool
```

---

# 18. System Prompt Can Guide Tool Use

The system prompt can give rules such as:

```text
Always use the database tool for customer data.
Do not guess customer information.
```

This helps guide the model.

But:

> The tool's own name, description, and schema still need to be clear.

---

# 19. Tool Description vs System Prompt

Use the **tool description** to explain:

```text
What this tool does
When this tool is appropriate
```

Use the **system prompt** for broader rules:

```text
Never guess live data.
Use available tools when current information is required.
```

Avoid unnecessarily duplicating the same instructions everywhere.

---

# 20. Custom Tools

Custom tools are functions created for my application.

Examples:

```text
get_employee_details
search_product_catalog
calculate_shipping
lookup_booking
get_course_duration
```

These tools expose application-specific capabilities to the model.

---

# 21. Deep Agents Built-In Capabilities

Deep Agents may also expose harness capabilities such as:

```text
Filesystem operations
Subagent delegation
Execution
```

depending on its configuration and backend.

So the final tool set can include:

```text
My custom tools
+
Deep Agents harness tools
```

I do not need to study the built-in filesystem tools deeply in this lesson.

They are covered later.

---

# 22. Tools Can Come From MCP

Tools do not have to be created only as Python functions.

They can also come from an **MCP server**.

Conceptually:

```text
Deep Agent
    ↓
MCP Tool
    ↓
MCP Server
    ↓
External System
```

MCP is covered in Lesson 6.

---

# 23. Good Tool Design

A good tool should have:

```text
Clear name
Clear description
Simple arguments
Focused responsibility
Useful result
Predictable behavior
```

---

# 24. Avoid Too Many Similar Tools

If the model sees:

```text
search_customer
find_customer
lookup_customer
get_customer
```

with very similar descriptions, tool selection becomes harder.

Prefer fewer, clearly differentiated tools.

---

# 25. Avoid Ambiguous Descriptions

Bad:

```text
Use this for information.
```

Better:

```text
Use this tool to retrieve customer account details by customer ID.
```

Specific descriptions improve tool selection.

---

# 26. Avoid Unnecessary Arguments

If a tool only needs:

```text
city
```

do not require:

```text
city
country
region
language
timezone
format
mode
```

unless they are actually necessary.

Simpler schemas are easier for models to use correctly.

---

# 27. Tool Errors

Tools can fail.

Examples:

```text
Invalid argument
API unavailable
Database error
Timeout
Permission failure
```

The runtime can return error information to the agent.

The model may then:

```text
Retry
Choose another tool
Ask the user
Explain the failure
```

Exact error-handling behavior depends on the application.

---

# 28. Tools and Real-Time Information

Tools are especially important when the answer depends on current or external data.

Examples:

```text
Current weather
Live stock price
Database value
Latest booking information
Current inventory
```

The model should not rely only on its training knowledge for such information.

---

# 29. Tools and Side Effects

Some tools only read information.

Example:

```text
search_database
```

Other tools can change something.

Example:

```text
send_email
delete_file
create_booking
```

These are **side-effecting tools**.

They require more care because they can change external systems.

HITL for sensitive actions is covered later.

---

# 30. Read Tools vs Action Tools

## Read Tool

Retrieves information.

```text
get_weather
lookup_order
search_database
```

## Action Tool

Changes something.

```text
send_email
update_order
delete_record
```

Action tools usually require stricter safety controls.

---

# 31. Tool Quality Affects Agent Quality

A useful mental equation:

```text
Agent Tool Performance
=
Model Tool-Calling Ability
+
Tool Name Quality
+
Tool Description Quality
+
Argument Schema Quality
+
Tool Result Quality
```

A strong model cannot fully compensate for badly designed tools.

---

# 32. Common Mistake — Poor Tool Name

Bad:

```text
function1
```

Better:

```text
get_course_duration
```

---

# 33. Common Mistake — Weak Description

Bad:

```text
Gets data.
```

Better:

```text
Retrieves the duration of a course using its course name.
```

---

# 34. Common Mistake — Thinking the Model Runs Python Directly

Incorrect:

```text
LLM executes Python function
```

Correct:

```text
LLM requests function
Runtime executes function
```

---

# 35. Common Mistake — Forcing Tool Use for Everything

Not every question needs a tool.

If the model can answer directly:

```text
No tool may be required.
```

Tools should exist because the agent needs external capability, not just because tools are possible.

---

# 36. Common Mistake — Too Many Overlapping Tools

Too many similar tools can confuse the model.

Prefer:

```text
Small set
+
Clear responsibilities
```

---

# 37. Common Mistake — Returning Huge Tool Outputs

Large tool outputs can consume context.

Prefer returning:

```text
Only information needed by the agent
```

Context management becomes more important in later modules.

---

# 38. Practical Tool Checklist

Before giving a tool to the agent, ask:

- Is the name clear?
- Is the description specific?
- Are the arguments simple?
- Are argument types clear?
- Does it have one main responsibility?
- Is the output useful?
- Could the model confuse it with another tool?
- Does it cause side effects?
- Does it need additional safety controls?

---

# 39. Interview-Level Explanation

If asked:

### "What is a tool in a Deep Agent?"

A good answer:

> **A tool is a function or capability that the model can request when it needs to perform an external action or retrieve information. The model chooses the tool and generates its arguments, while the agent runtime executes it and returns the result to the model. Tool names, descriptions, schemas, and outputs are important because they directly affect how reliably the model uses the tool.**

---

# 40. Interview Question — Who Chooses the Tool?

> The model chooses which available tool to call based on the user request, system instructions, and tool descriptions.

---

# 41. Interview Question — Who Executes the Tool?

> The agent runtime executes the tool. The model only generates the tool-call request.

---

# 42. Interview Question — Why Is the Tool Description Important?

> The model uses the description to understand what the tool does and when it should be used.

---

# 43. Interview Question — Is the Tool Result the Final Answer?

> Usually no. The tool result is returned to the model, which uses it to continue reasoning or generate the final response.

---

# 44. Revision Cheat Sheet

```text
TOOL
=
External capability available to the model
```

Basic flow:

```text
Model
  ↓
Tool Call
  ↓
Runtime
  ↓
Tool
  ↓
Tool Result
  ↓
Model
```

Good tools have:

```text
Clear name
Clear description
Simple schema
Focused purpose
Useful output
```

---

# 45. Five Things to Remember

1. **Tools let the agent access capabilities outside normal text generation.**
2. **The model chooses the tool; the runtime executes it.**
3. **Tool names and descriptions strongly affect tool selection.**
4. **Tool arguments should be simple and clearly defined.**
5. **The tool result normally goes back to the model before the final answer is produced.**

---

# 46. Self-Check Questions

Before moving to Lesson 6, I should be able to answer:

1. What is a tool?
2. Why does an agent need tools?
3. Who chooses which tool to use?
4. Who executes the tool?
5. What information does the model receive about a tool?
6. Why is the tool description important?
7. What is an argument schema?
8. Is a tool result always the final user response?
9. Why should a tool have one clear responsibility?
10. What is the difference between a read tool and an action tool?
11. Why can too many similar tools be a problem?
12. How can the system prompt guide tool usage?
13. Can Deep Agent tools come from MCP?
14. Why should large tool outputs be avoided?
15. What makes a good tool?

---

# 47. One-Line Summary

> **A tool gives the Deep Agent an external capability: the model decides when and how to call it, the runtime executes it, and the result is returned to the model for the next decision or final response.**

---

# 48. Final Mental Model

```text
               USER
                 │
                 ▼
               MODEL
                 │
          Need external help?
            /          \
          No            Yes
          │              │
          ▼              ▼
       Answer         Choose Tool
                         │
                         ▼
                    Tool Arguments
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
                         ▼
                       Model
                         │
                         ▼
                   Final Answer
```

---

# 49. Official References

- Deep Agents README  
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/README.md

- Deep Agents Architecture  
  https://github.com/langchain-ai/deepagents/blob/main/libs/ARCHITECTURE.md

- LangChain Academy — Introduction to Deep Agents  
  https://academy.langchain.com/courses/take/foundation-introduction-to-deepagents/

---

# 50. Next Lesson

> **Module 1 — Lesson 6: MCP**

Next I should learn:

```text
What MCP is
MCP client
MCP server
How tools are exposed through MCP
How Deep Agents can use MCP tools
MCP vs normal custom tools
```
