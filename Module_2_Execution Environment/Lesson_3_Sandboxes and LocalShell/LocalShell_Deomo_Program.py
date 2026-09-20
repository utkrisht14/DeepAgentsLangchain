from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

from dotenv import load_dotenv

load_dotenv()

# =========================================================
# LESSON 3A — LOCAL SHELL DEMO
# =========================================================

# IMPORTANT:
# LocalShellBackend is NOT a sandbox.

# Files are created on YOUR computer and commands are
# executed directly using your operating system shell.
# =========================================================

load_dotenv()

# ---------------------------------------------------------
# 1. Create a dedicated local workspace
# ---------------------------------------------------------
# This folder will be created beside this Python file.
# The file created by the agent will physically appear here.
# ---------------------------------------------------------

workspace = Path(__file__).parent / "local_shell_workspace"
workspace.mkdir(exist_ok=True)

# ---------------------------------------------------------
# 2. Create LocalShellBackend
# ---------------------------------------------------------

# root_dir:
#   The working directory for the agent.

# virtual_mode=True:
#   Agent paths such as /calculate.py map inside root_dir
#   for filesystem tools.

# inherit_env=True:
#   Shell commands inherit your normal environment.

# WARNING:
# Shell execution itself is NOT isolated.

# ---------------------------------------------------------

backend = LocalShellBackend(
    root_dir=workspace,
    virtual_mode=True,
    inherit_env=True
)

# ---------------------------------------------------------
# 3. Create the Deep Agent
# ---------------------------------------------------------

agent = create_deep_agent(
    model="openai:gpt-5.5",
    backend=backend,
    system_prompt="""
    You are a simple Python coding assistant.

    When asked to create and run Python code:

    1. Use write_file to create the Python file.
    2. Use execute to run it.
    3. Report the command output.

    Keep the final answer short.

    Do not intentionally modify anything outside
    the assigned workspace.
    """,
)

# ---------------------------------------------------------
# 4. Ask the agent to create and execute a Python program
# ---------------------------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Create /calculate.py. "
                    "The program should calculate the sum of numbers "
                    "from 1 to 10 and print the result. "
                    "Then execute the Python file and tell me the output."
                )
            }
        ]
    }
)

# ---------------------------------------------------------
# 5. Show which tools the agent used
# ---------------------------------------------------------

print("\n========== LOCAL SHELL TOOL CALLS ==========\n")

for message in result["messages"]:
    if hasattr(message, "tool_calls") and message.tool_calls:
        for tool_call in message.tool_calls:
            print(f"Tool Name: {tool_call['name']}")
            print(f"Tool Input: {tool_call['args']}")
            print("-" * 50)

# ---------------------------------------------------------
# 6. Print final response
# ---------------------------------------------------------

print("\n========== FINAL ANSWER ==========\n")

final_answer = result["messages"][-1]
content = final_answer.content

if isinstance(content, str):
    print(content)

else:
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])


# ---------------------------------------------------------
# 7. Show physical file location
# ---------------------------------------------------------

print("\n========== REAL LOCAL FILE ==========\n")
print(workspace / "calculate.py")

# =========================================================
# EXECUTION FLOW
# =========================================================
#
# Deep Agent
#     ↓
# write_file
#     ↓
# LocalShellBackend
#     ↓
# REAL file on your computer
#
# Deep Agent
#     ↓
# execute
#     ↓
# Your Windows shell
#     ↓
# Python runs on YOUR computer
# =========================================================

