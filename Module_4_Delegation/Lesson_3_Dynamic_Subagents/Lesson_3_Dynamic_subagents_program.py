import asyncio

from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware
from dotenv import load_dotenv


load_dotenv()


# =========================================================
# MODULE 4 — LESSON 3
# DYNAMIC SUBAGENTS DEMO
# =========================================================


# ---------------------------------------------------------
# 1. Define a specialist subagent
# ---------------------------------------------------------
#
# This subagent analyses ONE customer-support ticket.
#
# The main agent can dynamically call this same subagent
# many times from JavaScript.
# ---------------------------------------------------------

ticket_analyst = {

    "name": "ticket-analyst",

    "description": (
        "Analyse one customer-support ticket, determine its "
        "priority, identify the issue, and recommend the next action."
    ),

    "model": "openai:gpt-5.5",

    "tools": [],

    "system_prompt": """
    You are a customer-support ticket analyst.

    For every ticket:

    1. Give priority: Low, Medium, or High.
    2. Briefly identify the issue.
    3. Recommend one next action.

    Keep the response concise.
    """
}


# ---------------------------------------------------------
# 2. Create interpreter middleware
# ---------------------------------------------------------
#
# Dynamic subagents require the interpreter.
#
# Inside this interpreter, Deep Agents makes the
# JavaScript function task() available automatically
# because subagents are configured.
# ---------------------------------------------------------

interpreter = CodeInterpreterMiddleware()


# ---------------------------------------------------------
# 3. Create main agent
# ---------------------------------------------------------

agent = create_deep_agent(

    model="openai:gpt-5.5",

    subagents=[
        ticket_analyst
    ],

    middleware=[
        interpreter
    ],

    system_prompt="""
    You are a customer-support manager.

    When the user asks for a workflow involving multiple tickets:

    - Use the interpreter.
    - Dynamically dispatch one ticket-analyst subagent per ticket.
    - Use task() from JavaScript.
    - Process independent tickets in parallel when possible.
    - Combine the subagent results into one short summary.

    Do not analyse all tickets yourself.
    """
)


# =========================================================
# Helper function
# =========================================================

def print_final_answer(result):

    final_message = result["messages"][-1]
    content = final_message.content

    if isinstance(content, str):

        print(content)

    else:

        for block in content:

            if (
                isinstance(block, dict)
                and block.get("type") == "text"
            ):

                print(block["text"])


# =========================================================
# Main program
# =========================================================

async def main():

    # -----------------------------------------------------
    # 4. Batch of real-life support tickets
    # -----------------------------------------------------

    user_request = """
    Run a workflow to analyse these customer-support tickets:

    Ticket 1:
    "I cannot log in after changing my password this morning."

    Ticket 2:
    "Our production dashboard has stopped showing new customer data."

    Ticket 3:
    "Please tell me how I can download last month's invoice."

    Analyse every ticket independently and give me a final table
    containing:
    - ticket number
    - priority
    - issue
    - recommended action
    """


    # -----------------------------------------------------
    # 5. Run the agent asynchronously
    # -----------------------------------------------------
    #
    # The interpreter supports async task() calls,
    # therefore ainvoke() is the appropriate execution path.
    # -----------------------------------------------------

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_request
                }
            ]
        }
    )


    # -----------------------------------------------------
    # 6. Show main-agent tool calls
    # -----------------------------------------------------
    #
    # IMPORTANT:
    #
    # With normal delegation we normally see:
    #
    #     task
    #
    # as the main tool call.
    #
    # With dynamic subagents we should normally see:
    #
    #     eval
    #
    # because task() is being called FROM INSIDE
    # the JavaScript interpreter.
    # -----------------------------------------------------

    print(
        "\n========== MAIN AGENT TOOL CALLS ==========\n"
    )


    for message in result["messages"]:

        if (
            hasattr(message, "tool_calls")
            and message.tool_calls
        ):

            for tool_call in message.tool_calls:

                print(
                    f"Tool Name: {tool_call['name']}"
                )

                print(
                    f"Tool Input: {tool_call['args']}"
                )

                print("-" * 70)


    # -----------------------------------------------------
    # 7. Final answer
    # -----------------------------------------------------

    print(
        "\n========== FINAL TICKET REPORT ==========\n"
    )

    print_final_answer(result)


# =========================================================
# Start program
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())