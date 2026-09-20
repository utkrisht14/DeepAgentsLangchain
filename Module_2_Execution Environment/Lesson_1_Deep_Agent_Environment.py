from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from langchain_core.messages import ToolMessage
from dotenv import load_dotenv

# ---------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------

load_dotenv()

# ---------------------------------------------------------
# 2. Create the execution backend
# ---------------------------------------------------------

# StateBackend stores files inside the LangGraph agent state.

# IMPORTANT:
# These are virtual files.
# They are NOT created inside your Windows project folder.
# ---------------------------------------------------------

backend = StateBackend()

# ---------------------------------------------------------
# 3. Create the Deep Agent
# ---------------------------------------------------------

# By providing StateBackend, Deep Agents automatically gives
# the agent filesystem capabilities such as:
#
# - write_file
# - read_file
# - edit_file
# - ls
# - glob
# - grep
#
# StateBackend does NOT provide shell execution.
# ---------------------------------------------------------

agent = create_deep_agent(
    model = "openai:gpt-5.5",
    backend = backend,

    system_prompt = """
    You are a learning assistant.

    When the user asks you to work with files,
    use the available filesystem tools.

    Follow the user's instructions carefully.
    Keep the final answer short.
    """
)

# ---------------------------------------------------------
# 4. Give the Agent a Task
# ---------------------------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Create a file called /learning_notes.txt. "
                    "Write these three lines into it:\n"
                    "Deep Agent uses an execution environment.\n"
                    "A backend controls where files are stored.\n"
                    "StateBackend stores files in agent state.\n\n"
                    "After creating the file, read it back "
                    "and tell me what it contains."
                )
            }
        ]
    }
)


# ---------------------------------------------------------
# 5. Display Tool Execution
# ---------------------------------------------------------
# This lets us see which filesystem tools the agent used.
# ---------------------------------------------------------

print("\n========== EXECUTION ==========\n")

for message in result["messages"]:

    # AI messages may contain tool calls
    if hasattr(message, "tool_calls") and message.tool_calls:

        for tool_call in message.tool_calls:

            print(
                f"Agent called tool: "
                f"{tool_call['name']}"
            )

            print(
                f"Arguments: ",
                f"{tool_call['args']}"
            )

            print("-" * 50)

    # ToolMessage contains the result returned by the tool
    if isinstance(message, ToolMessage):

        print(f"Tool result ({message.name}):")

        print(message.content)

        print("-" * 50)


# ---------------------------------------------------------
# 6. Print Final Agent Response
# ---------------------------------------------------------


print("\n========== FINAL ANSWER ==========\n")

final_message = result["messages"][-1]

content = final_message.content

# AIMessage.content may be a string
if isinstance(content, str):
    print(content)


# Or it may contain structured content blocks
else:
    for block in content:

        if (
                isinstance(block, dict)
                and block.get("type") == "text"
        ):
            print(block["text"])


