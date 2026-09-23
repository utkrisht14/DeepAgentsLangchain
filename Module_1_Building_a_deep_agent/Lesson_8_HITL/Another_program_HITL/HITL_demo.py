from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from deepagents import create_deep_agent

from dotenv import load_dotenv

load_dotenv()

@tool
def delete_file(path: str) -> str:
    """Delete a file from system."""
    return f"Deleting file {path}"


@tool
def read_file(path: str) -> str:
    """ Read a file from the filesystem. """
    return f"Pretend content of {path}"


# A checkpointer is required for HITL — it's what lets the agent pause
# and pick back up later.
checkpointer = InMemorySaver()

agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[delete_file, read_file],
    interrupt_on=  {
        "delete_file": True, # sensitive -> needs human approval
        "read_file": False # harmless -> runs automatically
    },
    checkpointer=checkpointer,
    system_prompt="""
    You are a file system assistant.
    """
)

config = {
    "configurable": {
        "thread_id": "hitl-demo-1"
    }
}


def ask_human(action_requests):
    """ Show each pending tool call and collect a decision from the terminal. """

    decisions = []

    for action in action_requests:
        print(f"The agent want to call {action.tool_name} with input: {action.tool_input}")
        choice = input("Approve (y/n): ").strip().lower()
        if choice == "y":
            decisions.append({"type": "approve"})
        else:
            reason = input("Why are you rejecting? ").strip() or "No reason provided."
            decisions.append({"type": "reject", "message": reason})

    return decisions


def run(user_message: str):
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        },
        config=config,
        version="v2"
    )

    while result.interrupts:
        decisions = ask_human(result.interrupts[0].value["action_requests"])
        result = agent.invoke(
            Command(
                resume = {
                    "decisions": decisions,
                },
                config=config,
                version="v2" # ontrols the shape of what invoke() gives you back, specifically how interrupts show up
            )
        )

    print("\nFinal answer:")
    print(result.value["messages"][-1].content)


if __name__ == "__main__":
    run("Please delete the file temp.txt and then read report.txt")

