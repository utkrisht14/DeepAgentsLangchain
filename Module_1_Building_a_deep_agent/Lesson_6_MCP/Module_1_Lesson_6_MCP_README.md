# Module 1 — Building a Deep Agent
## Lesson 6 — MCP (Model Context Protocol)

> **Purpose:** Focused notes on MCP, how it works, and especially how MCP is different from normal tool calling.
>
> This lesson assumes I already understand basic tool calling from Lesson 5.

---

# 1. What Is MCP?

**MCP** stands for:

```text
Model Context Protocol
```

It is an **open standard** for connecting AI applications to external systems.

An MCP server can expose things such as:

```text
Tools
Resources
Prompts
```

An AI application connects to that server through an MCP client.

Mental model:

```text
AI Application
      ↓
MCP Client
      ↓
MCP Protocol
      ↓
MCP Server
      ↓
External System
```

Examples of external systems:

```text
GitHub
Database
Filesystem
Slack
Internal APIs
Documentation
CRM
Cloud services
```

---

# 2. Why MCP Exists

Before MCP, every AI application could integrate external systems differently.

Example:

```text
Application A
→ Custom GitHub integration

Application B
→ Different GitHub wrapper

Application C
→ Another GitHub connector
```

This creates repeated integration work.

MCP introduces a common contract.

Instead:

```text
GitHub MCP Server
        ↓
Any compatible MCP Client
        ↓
AI Application
```

So MCP provides a **standard connection layer** between AI applications and external capabilities.

---

# 3. The Most Important Mental Model

MCP is similar in spirit to a common adapter standard.

Think:

```text
USB
```

A USB device follows a standard connection format.

The computer does not need a completely different physical interface for every device.

Similarly:

```text
MCP Server
=
Standardized AI integration endpoint
```

An MCP-compatible AI application can connect to different MCP servers through the same protocol.

---

# 4. MCP Is Not an Agent Framework

MCP does **not** provide:

```text
Agent reasoning
Planning
Agent memory
Subagents
LangGraph state
Agent loops
```

MCP mainly solves:

```text
How does the AI application communicate with external capabilities?
```

So:

```text
Deep Agents
=
Agent harness

MCP
=
Integration protocol
```

---

# 5. MCP Architecture

The basic architecture has three important concepts:

```text
Host
Client
Server
```

---

# 6. MCP Host

The **host** is the AI application that wants to use MCP.

Examples could include:

```text
Deep Agent application
IDE assistant
Desktop AI application
Custom AI application
```

The host contains or manages one or more MCP clients.

Mental model:

```text
Deep Agent App
=
MCP Host
```

---

# 7. MCP Client

The **MCP client** connects the host to an MCP server.

Responsibilities include:

```text
Connect to server
Negotiate protocol/capabilities
Discover available tools
Read resources
Load prompts
Send tool requests
Receive results
```

Mental model:

```text
MCP Client
=
Connector used by the AI application
```

---

# 8. MCP Server

The **MCP server** exposes capabilities.

It can provide:

```text
Tools
Resources
Prompts
```

For example:

```text
GitHub MCP Server
    ├── search_repository
    ├── create_issue
    ├── read_file
    └── list_pull_requests
```

The server contains the actual implementation or connection to the external system.

---

# 9. Complete Architecture

```text
                 USER
                  │
                  ▼
             DEEP AGENT
                  │
                  ▼
              MCP CLIENT
                  │
          MCP PROTOCOL
                  │
                  ▼
              MCP SERVER
                  │
                  ▼
           EXTERNAL SYSTEM
```

Example:

```text
User:
"Create a GitHub issue."

Deep Agent
    ↓
MCP Client
    ↓
GitHub MCP Server
    ↓
GitHub API
```

---

# 10. MCP Server Capabilities

The three core server-facing concepts I should know are:

```text
Tools
Resources
Prompts
```

They are different.

---

# 11. MCP Tools

MCP tools represent **actions or callable functions**.

Examples:

```text
search_code
create_issue
query_database
send_message
get_weather
```

Tools are normally used by the **model**.

Mental model:

```text
Model decides:
"I need this action."

      ↓

MCP Tool
```

---

# 12. MCP Resources

Resources expose **data or context** that an application can read.

Examples:

```text
File contents
Database schema
Documentation
Configuration
Repository information
Knowledge documents
```

Mental model:

```text
Resource
=
Information exposed by the MCP server
```

Resources are often URI-addressable.

Example idea:

```text
file://...
repo://...
docs://...
```

The exact URI design depends on the server.

---

# 13. MCP Prompts

MCP servers can also expose reusable **prompt templates**.

A prompt can represent:

```text
Code review template
Summarization template
Incident-analysis template
Research template
```

Prompts are usually user/application-selectable templates.

Mental model:

```text
Prompt
=
Reusable conversation template provided by server
```

---

# 14. Tools vs Resources vs Prompts

Easy memory:

```text
Tool
=
Do something

Resource
=
Read something

Prompt
=
Reusable instruction template
```

---

# 15. MCP Is More Than Tools

This is important.

Many beginners think:

```text
MCP = remote tools
```

That is incomplete.

MCP can expose:

```text
Tools
Resources
Prompts
Server capabilities
Other protocol features
```

So MCP is a broader protocol than only tool execution.

---

# 16. How Deep Agents Uses MCP

In the LangChain ecosystem, MCP servers can be connected through MCP adapters.

Conceptually:

```text
MCP Server
    ↓
MCP Client
    ↓
LangChain MCP Adapter
    ↓
LangChain Tools
    ↓
Deep Agent
```

This means MCP tools become tools that the Deep Agent can use.

---

# 17. The Critical Point: MCP Tools Become Normal Agent Tools

This is the most important idea in this lesson.

After MCP tool discovery:

```text
MCP Tool
    ↓
Converted / adapted
    ↓
LangChain Tool
    ↓
Passed to Deep Agent
```

From the model's perspective, it is still using a normal tool-calling mechanism.

So the runtime flow is still:

```text
Model
  ↓
Tool Call
  ↓
Runtime
  ↓
MCP-backed Tool
  ↓
MCP Client
  ↓
MCP Server
  ↓
Result
  ↓
Model
```

---

# 18. Tool Calling vs MCP

This distinction must be very clear.

## Tool Calling

Tool calling is an **LLM/agent interaction pattern**.

It answers:

> How does the model request that a tool be used?

Flow:

```text
Model
  ↓
Structured Tool Call
  ↓
Runtime
  ↓
Tool
```

---

## MCP

MCP is an **integration protocol**.

It answers:

> How does the application discover, connect to, and invoke capabilities provided by an external server?

Flow:

```text
Application
  ↓
MCP Client
  ↓
MCP Server
  ↓
External Capability
```

---

# 19. One-Line Difference

```text
Tool Calling
=
How the model asks to use a tool
```

```text
MCP
=
How external tools/resources/prompts are exposed and connected in a standard way
```

---

# 20. They Work Together

They are not replacements for each other.

Correct mental model:

```text
MCP
provides the tool

Tool Calling
lets the model use the tool
```

Example:

```text
GitHub MCP Server
      ↓
Exposes create_issue tool
      ↓
LangChain loads tool
      ↓
Model sees create_issue
      ↓
Model generates tool call
      ↓
Runtime calls MCP tool
```

---

# 21. Normal Custom Tool Calling

Without MCP:

```text
Deep Agent
    ↓
Custom Python Tool
    ↓
Python Function / API
```

Example architecture:

```text
Model
  ↓
Tool Call
  ↓
LangChain Runtime
  ↓
Python Function
  ↓
External API
```

---

# 22. MCP Tool Calling

With MCP:

```text
Deep Agent
    ↓
LangChain MCP Adapter
    ↓
MCP Client
    ↓
MCP Server
    ↓
External System
```

The model still performs tool calling.

Only the **source and connection mechanism of the tool** has changed.

---

# 23. Side-by-Side Comparison

| Topic | Normal Tool Calling | MCP |
|---|---|---|
| Main purpose | Let model request a tool | Standardize external capability integration |
| Who uses it? | Model + agent runtime | Host/client/server applications |
| Requires server? | No | Yes, MCP server |
| Can use local Python function? | Yes | Server exposes capability |
| Tool discovery | Usually defined directly in app | Can be discovered from server |
| Standard protocol | Not required | Yes |
| Supports resources | Not inherently | Yes |
| Supports prompts | Not inherently | Yes |
| Can work remotely | Yes, if custom coded | Yes, protocol supports remote server |
| Model still tool-calls? | Yes | Yes |
| Reusable across applications | Depends on implementation | Strong design goal |

---

# 24. Example Without MCP

Suppose I want weather information.

I create:

```text
get_weather()
```

inside my application.

Architecture:

```text
Deep Agent
    ↓
get_weather tool
    ↓
Weather API
```

The application owns the tool implementation.

---

# 25. Example With MCP

Now imagine a weather MCP server already exists.

Architecture:

```text
Deep Agent
    ↓
MCP Client
    ↓
Weather MCP Server
    ↓
Weather API
```

I do not need to manually recreate the weather integration inside every AI application.

---

# 26. Why MCP Is Useful

Main advantages:

```text
Standardization
Reusability
Tool discovery
Separation of concerns
Interoperability
Remote capability access
```

---

# 27. Standardization

Without MCP:

```text
Every integration may use a different interface.
```

With MCP:

```text
Servers follow a common protocol.
```

This simplifies integration.

---

# 28. Reusability

One MCP server can potentially serve many compatible hosts.

Example:

```text
GitHub MCP Server
   ├── Deep Agent App
   ├── IDE Agent
   ├── Desktop Agent
   └── Another AI Client
```

The GitHub integration does not need to be rewritten for every host.

---

# 29. Separation of Concerns

The agent application does not need to contain every integration implementation.

Instead:

```text
Agent Application
=
Reasoning + orchestration
```

```text
MCP Server
=
External capability integration
```

This creates cleaner architecture.

---

# 30. Dynamic Discovery

An MCP client can ask a server what capabilities it exposes.

Conceptually:

```text
Client
  ↓
"What tools do you have?"
  ↓
Server
  ↓
Tool List
```

The application can then load those tools.

This is different from manually hardcoding every tool definition in the application.

---

# 31. Capability Negotiation

When client and server connect, they can determine what features each side supports.

Examples:

```text
Tools
Resources
Prompts
Other protocol capabilities
```

This is part of MCP's client-server architecture.

---

# 32. MCP Transport

The client and server need a way to communicate.

Common MCP transports include:

```text
stdio
HTTP / Streamable HTTP
```

---

# 33. stdio Transport

`stdio` means:

```text
Standard Input / Standard Output
```

Usually:

```text
Host application
      ↓
Starts local MCP server process
      ↓
Communicates through stdin/stdout
```

Good for:

```text
Local tools
Developer machines
Local server processes
```

Mental model:

```text
Same machine
Host ↔ Local process
```

---

# 34. HTTP Transport

An MCP server can also run remotely over HTTP.

Mental model:

```text
Deep Agent App
      ↓
Network
      ↓
Remote MCP Server
```

This is useful for:

```text
Cloud services
Shared MCP servers
Enterprise integrations
Remote APIs
```

---

# 35. Local vs Remote MCP Server

## Local MCP Server

```text
Agent
  ↓
stdio
  ↓
Local Server Process
```

## Remote MCP Server

```text
Agent
  ↓
HTTP
  ↓
Remote Server
```

The protocol concepts are similar; the transport changes.

---

# 36. Current MCP Protocol

The current MCP specification is:

```text
2026-07-28
```

A major change in this version is that the core protocol is now designed around a **stateless request/response model**, which makes remote deployments easier to scale.

For this lesson, I do not need to memorize protocol internals.

Important takeaway:

> MCP is an actively evolving standard, so I should prefer current SDK/documentation examples.

---

# 37. MCP Client in LangChain

LangChain provides MCP adapters.

A commonly used class is:

```text
MultiServerMCPClient
```

Its purpose is to connect to one or more MCP servers.

Conceptually:

```text
MultiServerMCPClient
   ├── GitHub Server
   ├── Weather Server
   └── Database Server
```

---

# 38. Why Multi-Server Support Matters

A real agent may need several external systems.

Example:

```text
Research Agent
   ├── Search MCP Server
   ├── GitHub MCP Server
   └── Database MCP Server
```

A multi-server client can collect tools from these servers.

---

# 39. MCP Tool Loading

Conceptual sequence:

```text
Create MCP Client
      ↓
Connect to Server
      ↓
Discover Tools
      ↓
Load MCP Tools
      ↓
Convert to LangChain-Compatible Tools
      ↓
Pass Tools to Deep Agent
```

Then normal agent tool calling continues.

---

# 40. MCP Does Not Replace `@tool`

This is another important point.

Normal custom tool:

```text
@tool
Python Function
```

is still perfectly valid.

MCP is useful when I want:

```text
Reusable external integration
Standard client/server interface
Remote server capability
Cross-application interoperability
```

So:

```text
Custom Tool
and
MCP Tool
```

can exist together in the same Deep Agent.

---

# 41. When a Normal Tool Is Better

Use a normal custom tool when:

```text
The capability is small
It belongs directly inside my application
It is only used by one agent
I do not need a separate server
I want the simplest implementation
```

Example:

```text
calculate_discount()
```

There may be no reason to create an MCP server for such a small function.

---

# 42. When MCP Is Better

MCP becomes more useful when:

```text
Capability should be reusable
Integration is shared across applications
Tool belongs to another service/team
Server is remote
Several tools belong together
I want standardized discovery
I also need resources or prompts
```

---

# 43. Do Not Use MCP Just Because It Exists

MCP adds architecture:

```text
Client
Server
Protocol
Transport
Authentication
Deployment
```

For a tiny local function:

```text
Normal tool
```

may be much simpler.

Good engineering rule:

> Use MCP when standardization and reuse provide real value.

---

# 44. MCP Tools Still Need Good Descriptions

MCP does not solve bad tool design.

The model still needs:

```text
Clear tool name
Clear description
Clear argument schema
Useful output
```

If an MCP server exposes confusing tools, the model can still choose incorrectly.

---

# 45. MCP and Tool Count

Connecting many MCP servers can expose a large number of tools.

Example:

```text
GitHub server = 40 tools
Database server = 20 tools
Slack server = 30 tools

Total = 90 tools
```

This can create:

```text
Tool-selection confusion
More context usage
Higher complexity
```

Therefore tool organization still matters.

---

# 46. MCP and Deep Agent Subagents

Later, subagents can help separate tool domains.

Example:

```text
Main Agent
   ├── GitHub Subagent
   │      └── GitHub MCP Tools
   │
   └── Database Subagent
          └── Database MCP Tools
```

This keeps each agent's tool set more focused.

This belongs to Module 4, so I only need to know the idea for now.

---

# 47. MCP Resources vs Normal Tool Results

Suppose documentation exists on a server.

Two possible designs:

```text
Tool:
search_docs("topic")
```

or:

```text
Resource:
docs://guide
```

A tool represents an action/query.

A resource represents accessible context/data.

MCP supports both patterns.

---

# 48. MCP Prompts vs System Prompt

These are not the same thing.

## System Prompt

Core agent instructions.

```text
"You are a coding assistant."
```

## MCP Prompt

Reusable prompt/template exposed by an MCP server.

Example:

```text
review_pull_request
```

So:

```text
System Prompt
=
Agent behavior

MCP Prompt
=
Reusable server-provided prompt template
```

---

# 49. MCP Client vs MCP Server

Easy memory:

```text
CLIENT
=
Connects and requests
```

```text
SERVER
=
Exposes and responds
```

---

# 50. MCP Server vs API

An MCP server often sits **in front of** an API or system.

Example:

```text
Deep Agent
   ↓
MCP Client
   ↓
GitHub MCP Server
   ↓
GitHub API
```

The API is the underlying service interface.

The MCP server translates/exposes selected capabilities in an AI-friendly standardized format.

---

# 51. API vs MCP

## API

Designed as a general software interface.

```text
Application
  ↓
REST / GraphQL / SDK
  ↓
Service
```

## MCP

Designed specifically as a standard integration protocol for AI applications.

```text
AI Host
  ↓
MCP Client
  ↓
MCP Server
  ↓
Service/API
```

MCP can internally use an API.

---

# 52. Tool vs API vs MCP

This distinction is useful.

```text
API
=
Underlying software interface
```

```text
Tool
=
Agent-callable capability
```

```text
MCP
=
Standard protocol used to expose/connect capabilities to AI applications
```

Example:

```text
GitHub REST API
      ↓
GitHub MCP Server
      ↓
create_issue MCP Tool
      ↓
Deep Agent
```

---

# 53. Tool Calling vs Function Calling

In practice these terms are often related.

Historically many systems said:

```text
Function Calling
```

Modern agent frameworks often use:

```text
Tool Calling
```

Tool calling is broader because a tool may represent:

```text
Function
API
MCP action
Database operation
Search capability
```

---

# 54. MCP Security

MCP servers can expose powerful capabilities.

Examples:

```text
Delete files
Create GitHub issue
Send Slack message
Modify database
Access private documents
```

So security matters.

Important considerations:

```text
Authentication
Authorization
Permissions
Server trust
Tool scope
Sensitive data
Human approval
```

---

# 55. Trust Boundary

When connecting to an MCP server, I am trusting that server to expose capabilities and data correctly.

Mental model:

```text
My Agent
   ↓
Trust Boundary
   ↓
MCP Server
```

I should know:

```text
Who operates the server?
What data can it access?
What actions can it perform?
```

---

# 56. Authentication

Remote MCP servers may require authentication.

Examples can include:

```text
OAuth
Bearer credentials
Provider-specific authentication
```

The MCP ecosystem includes authorization mechanisms for secure remote access.

Exact authentication setup depends on the server.

---

# 57. MCP Does Not Automatically Make a Tool Safe

Important:

```text
MCP Tool
≠
Safe Tool
```

A tool exposed through MCP can still:

```text
Delete data
Send messages
Spend money
Modify systems
```

Sensitive tools may still require:

```text
Permissions
HITL
Validation
Access control
```

---

# 58. MCP Error Handling

An MCP tool can fail for different reasons.

Examples:

```text
Tool execution error
Server error
Transport error
Authentication failure
Invalid arguments
```

LangChain MCP adapters can return normal MCP tool execution errors back to the model so the agent may self-correct.

Transport/session failures are different and may raise runtime errors.

---

# 59. MCP Discovery Does Not Mean the Model Sees Everything Automatically

The application decides what MCP tools/resources/prompts it loads and exposes.

Conceptually:

```text
MCP Server
    ↓
Many capabilities
    ↓
Application selects/loads
    ↓
Agent sees selected capabilities
```

This is useful for controlling tool scope.

---

# 60. MCP and Context

Every tool definition consumes some context.

If many MCP tools are loaded:

```text
More tool descriptions
      ↓
More tokens
      ↓
Potentially harder selection
```

So:

> Connecting more MCP servers is not automatically better.

---

# 61. Normal Tool Calling Flow

```text
USER
 │
 ▼
MODEL
 │
 ▼
Tool Call
 │
 ▼
LANGCHAIN RUNTIME
 │
 ▼
CUSTOM PYTHON TOOL
 │
 ▼
RESULT
 │
 ▼
MODEL
```

---

# 62. MCP Tool Calling Flow

```text
USER
 │
 ▼
MODEL
 │
 ▼
Tool Call
 │
 ▼
LANGCHAIN RUNTIME
 │
 ▼
LANGCHAIN MCP TOOL ADAPTER
 │
 ▼
MCP CLIENT
 │
 ▼
MCP SERVER
 │
 ▼
EXTERNAL SYSTEM
 │
 ▼
RESULT
 │
 ▼
MODEL
```

---

# 63. Main Difference Visually

Without MCP:

```text
Model
 ↓
Tool
 ↓
Local/Application Implementation
```

With MCP:

```text
Model
 ↓
Tool
 ↓
MCP Client
 ↓
MCP Server
 ↓
External Implementation
```

The model's tool-calling behavior is still fundamentally the same.

---

# 64. The Best Sentence to Remember

> **MCP standardizes where tools come from and how an AI application connects to them; tool calling is how the model decides to use those tools.**

---

# 65. Common Misconception — MCP Replaces Tool Calling

Wrong:

```text
Either Tool Calling
OR
MCP
```

Correct:

```text
MCP provides tool
+
Tool calling uses tool
```

---

# 66. Common Misconception — MCP Is Only for Remote Servers

Not true.

MCP servers can run:

```text
Locally using stdio
```

or:

```text
Remotely using HTTP
```

---

# 67. Common Misconception — MCP Is Only About Tools

Not true.

MCP can expose:

```text
Tools
Resources
Prompts
```

---

# 68. Common Misconception — Every Function Should Become an MCP Server

Not true.

For simple application-local logic:

```text
Normal custom tool
```

is usually easier.

---

# 69. Common Misconception — MCP Server Is the LLM

No.

```text
MCP Server
=
Capability provider
```

```text
LLM
=
Reasoning model
```

The MCP server usually has no responsibility for deciding when its tool should be used.

---

# 70. Common Misconception — MCP Client Is the Agent

No.

```text
MCP Client
=
Protocol connector
```

```text
Deep Agent
=
Reasoning/orchestration system
```

---

# 71. Common Misconception — MCP Tools Use a Different Agent Loop

No.

Once loaded as LangChain tools, MCP tools participate in the same familiar loop:

```text
Model
 ↓
Tool Call
 ↓
Tool Result
 ↓
Model
```

---

# 72. When I Should Use a Normal Tool

Use a normal tool when:

```text
Simple function
Application-specific logic
No reuse needed
No separate server needed
Fastest implementation desired
```

---

# 73. When I Should Consider MCP

Consider MCP when:

```text
Integration is reusable
External system already has MCP server
Many related capabilities are exposed
Multiple AI applications need the integration
Remote service is involved
Standard discovery is useful
Resources/prompts are useful too
```

---

# 74. MCP in the LangChain Ecosystem

Useful mental stack:

```text
Deep Agents
      ↓
LangChain Agent
      ↓
LangChain MCP Adapter
      ↓
MCP Client
      ↓
MCP Server
```

LangChain's MCP adapter converts MCP capabilities into forms LangChain agents understand.

---

# 75. `MultiServerMCPClient`

A useful LangChain integration component is:

```text
MultiServerMCPClient
```

Purpose:

```text
Connect to multiple MCP servers
Load tools
Load resources
Load prompts
Retrieve server information
```

For this lesson, the main thing to remember is:

> It acts as the bridge between MCP servers and LangChain-compatible capabilities.

---

# 76. MCP and Deep Agents

Conceptually:

```text
MCP Client
    ↓
Get MCP Tools
    ↓
Pass Tools to create_deep_agent()
    ↓
Deep Agent uses them
```

So Deep Agents does not need a special new reasoning mechanism for MCP.

It simply receives MCP-backed tools through LangChain-compatible adapters.

---

# 77. Interview-Level Explanation

If asked:

### "What is MCP?"

A good answer:

> **MCP, or Model Context Protocol, is an open standard that allows AI applications to connect to external systems through a common client-server protocol. MCP servers can expose tools, resources, and prompts, while MCP clients discover and consume those capabilities.**

---

# 78. Interview Question — How Is MCP Different From Tool Calling?

A strong answer:

> **Tool calling is the mechanism by which an LLM decides to invoke a tool and supplies arguments. MCP is a protocol used by the application to discover and connect to externally provided tools, resources, and prompts. MCP tools still use the normal tool-calling loop once they are loaded into the agent.**

---

# 79. Interview Question — Does MCP Replace LangChain Tools?

> No. LangChain MCP adapters convert MCP tools into LangChain-compatible tools, which can then be passed to a LangChain or Deep Agent like other tools.

---

# 80. Interview Question — What Are MCP Client and Server?

> The MCP client is the connector inside the AI host that communicates using the MCP protocol. The MCP server exposes tools, resources, prompts, and other supported capabilities.

---

# 81. Interview Question — Why Use MCP Instead of a Python Tool?

> MCP is useful when the capability should be standardized, reusable, shared across applications, remotely hosted, or bundled with related tools/resources/prompts. For small application-local logic, a normal Python tool can be simpler.

---

# 82. Interview Question — Can MCP Servers Be Local?

> Yes. They can run locally using transports such as stdio, or remotely using HTTP-based transports.

---

# 83. Interview Question — Is MCP Only Tools?

> No. MCP supports tools, resources, prompts, and other protocol capabilities.

---

# 84. Revision Cheat Sheet

```text
MCP
=
Model Context Protocol
```

Purpose:

```text
Standard connection between
AI applications
and
external systems
```

Architecture:

```text
Host
 ↓
Client
 ↓
MCP Protocol
 ↓
Server
```

Server can expose:

```text
Tools
Resources
Prompts
```

---

# 85. Tool Calling vs MCP Cheat Sheet

```text
TOOL CALLING

Model
 ↓
Choose Tool
 ↓
Provide Arguments
```

```text
MCP

Application
 ↓
Connect to Server
 ↓
Discover/Access Capabilities
```

Together:

```text
MCP provides the tool
      ↓
Model tool-calls the tool
```

---

# 86. Five Things to Remember

1. **MCP is a protocol, not an agent framework.**
2. **An MCP server can expose tools, resources, and prompts.**
3. **The MCP client connects the AI application to the MCP server.**
4. **MCP tools become normal LangChain-compatible tools for the agent.**
5. **Tool calling is how the model uses a tool; MCP is how the application connects to standardized external capabilities.**

---

# 87. Self-Check Questions

Before moving to Lesson 7, I should be able to answer:

1. What does MCP stand for?
2. Why was MCP created?
3. What is an MCP host?
4. What is an MCP client?
5. What is an MCP server?
6. What can an MCP server expose?
7. What is the difference between a tool and a resource?
8. What is an MCP prompt?
9. What is the difference between MCP and tool calling?
10. Does MCP replace tool calling?
11. Does MCP replace LangChain tools?
12. What happens to an MCP tool in LangChain?
13. What is `MultiServerMCPClient` conceptually used for?
14. What is the difference between stdio and HTTP transport?
15. When should I use a normal custom tool instead of MCP?
16. When is MCP a better architectural choice?
17. Is an MCP server the LLM?
18. Is an MCP client the agent?
19. Can MCP servers run locally?
20. Why can loading too many MCP tools be a problem?

---

# 88. One-Line Summary

> **MCP is a standardized client-server protocol for exposing tools, resources, and prompts to AI applications, while tool calling is the mechanism the model uses to decide when and how to invoke an available tool.**

---

# 89. Final Mental Model

```text
                   USER
                    │
                    ▼
                DEEP AGENT
                    │
                    ▼
                   MODEL
                    │
             Need a tool?
              /        \
            No          Yes
            │            │
            ▼            ▼
         Answer      Tool Call
                         │
                         ▼
                LANGCHAIN RUNTIME
                         │
                         ▼
                  MCP-BACKED TOOL
                         │
                         ▼
                    MCP CLIENT
                         │
                         ▼
                    MCP SERVER
                         │
                         ▼
                 EXTERNAL SYSTEM
                         │
                         ▼
                      RESULT
                         │
                         └────────→ MODEL
```

---

# 90. Official References

- MCP Official Website / Specification  
  https://modelcontextprotocol.io/

- MCP 2026-07-28 Specification Release  
  https://blog.modelcontextprotocol.io/posts/2026-07-28/

- MCP Python SDK  
  https://py.sdk.modelcontextprotocol.io/

- LangChain MCP Adapters  
  https://github.com/langchain-ai/langchain-mcp-adapters

- Deep Agents GitHub  
  https://github.com/langchain-ai/deepagents

- LangChain Academy — Introduction to Deep Agents  
  https://academy.langchain.com/courses/take/foundation-introduction-to-deepagents/

---

# 91. Next Lesson

> **Module 1 — Lesson 7: Messages, Threads and Checkpointer**

Next I should learn:

```text
Messages
Conversation state
Thread ID
Persistence
Checkpointer
Resume
How multiple agent turns are connected
```
