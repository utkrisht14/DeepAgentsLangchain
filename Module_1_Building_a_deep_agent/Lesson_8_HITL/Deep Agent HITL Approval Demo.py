from deepagents import create_deep_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------
# 1. Create a sensitive tool
# ---------------------------------------------------------

@tool
def submit_expense(description: str, amount: float) -> str:
    """
    Submit an expense for reimbursement.
    """

    # This is only a demo.
    # No real expense is submitted.
    return (
        f"Expense submitted successfully.\n"
        f"Description: {description}\n"
        f"Amount: €{amount:.2f}"
    )


# ---------------------------------------------------------
# 2. Create Checkpointer
# ---------------------------------------------------------

checkpointer = InMemorySaver()


# ---------------------------------------------------------
# 3. Create Deep Agent with HITL
# ---------------------------------------------------------

agent = create_deep_agent(
    model="openai:gpt-5.5",

    tools=[
        submit_expense
    ],

    checkpointer=checkpointer,

    # Pause before this tool executes
    interrupt_on={
        "submit_expense": {
            "allowed_decisions": [
                "approve",
                "reject"
            ]
        }
    },

    system_prompt="""
    You are an expense assistant.

    When the user asks to submit an expense,
    use the submit_expense tool.

    Keep the final answer short.
    """
)


# ---------------------------------------------------------
# 4. Create Thread
# ---------------------------------------------------------

config = {
    "configurable": {
        "thread_id": "expense-thread-1"
    }
}


# ---------------------------------------------------------
# 5. Start Agent
# ---------------------------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Submit an expense of €75 for "
                    "a client dinner."
                )
            }
        ]
    },
    config=config,
    version="v2"
)


# ---------------------------------------------------------
# 6. Check for HITL Interrupt
# ---------------------------------------------------------

if result.interrupts:

    print("\n========== HUMAN APPROVAL REQUIRED ==========\n")

    interrupt = result.interrupts[0]

    print(interrupt.value)

    print("\nDo you want to approve this action?")
    decision = input("Type 'approve' or 'reject': ").strip().lower()


    # -----------------------------------------------------
    # 7. Human Approves
    # -----------------------------------------------------

    if decision == "approve":

        print("\nAction approved.\n")

        result = agent.invoke(
            Command(
                resume={
                    "decisions": [
                        {
                            "type": "approve"
                        }
                    ]
                }
            ),
            config=config,
            version="v2"
        )


    # -----------------------------------------------------
    # 8. Human Rejects
    # -----------------------------------------------------

    else:

        print("\nAction rejected.\n")

        result = agent.invoke(
            Command(
                resume={
                    "decisions": [
                        {
                            "type": "reject",
                            "message": (
                                "The user rejected the expense submission. "
                                "Do not submit it."
                            )
                        }
                    ]
                }
            ),
            config=config,
            version="v2"
        )


# ---------------------------------------------------------
# 9. Print Final Response
# ---------------------------------------------------------

final_message = result.value["messages"][-1]

print("\n========== FINAL RESPONSE ==========\n")

if isinstance(final_message.content, str):
    print(final_message.content)

else:
    for block in final_message.content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])