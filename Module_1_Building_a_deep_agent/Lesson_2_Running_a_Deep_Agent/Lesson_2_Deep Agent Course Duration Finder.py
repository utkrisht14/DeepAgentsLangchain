from deepagents import create_deep_agent
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
# 1. Create a simple tool
# ---------------------------------------------------------

@tool
def get_course_duration(course_name: str) -> str:
    """
    Return the approximate duration of a course.
    """

    courses = {
        "Python": "8 weeks",
        "Machine Learning": "12 weeks",
        "Deep Learning": "10 weeks",
        "Agentic AI": "6 weeks"
    }

    return courses.get(
        course_name,
        f"No duration information found for {course_name}."
    )


# ---------------------------------------------------------
# 2. Create the Deep Agent
# ---------------------------------------------------------


agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[get_course_duration],
    system_prompt="""
    You are a learning assistant.

    When the user asks about a course:
    - Use the available tool to find the course duration.
    - Return a short and clear answer.
    """
)


# ---------------------------------------------------------
# 3. Prepare input
# ---------------------------------------------------------

input_state = {
    "messages": [
        {
            "role": "user",
            "content": "How long does the Agentic AI course take?"
        }
    ]
}

# ---------------------------------------------------------
# 4. Run the Deep Agent
# ---------------------------------------------------------

result = agent.invoke(input_state)

# ---------------------------------------------------------
# 5. Display complete execution messages
# ---------------------------------------------------------

print("\n========== AGENT EXECUTION ==========\n")

for message in result["messages"]:
    print(f"Message Type: {type(message).__name__}")

    # Show tool calls if present
    if hasattr(message, "tool_calls") and message.tool_calls:
        print("Tool Calls:")
        print(message.tool_calls)

    # Show message content
    if message.content:
        print("Content: ")
        print(message.content)

    print("-" * 50)


# ---------------------------------------------------------
# 6. Display only final answer
# ---------------------------------------------------------

final_message = result["messages"][-1]

print("\n========== FINAL ANSWER ==========\n")

if isinstance(final_message.content, str):
    print(final_message.content)
else:
    for block in final_message.content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])