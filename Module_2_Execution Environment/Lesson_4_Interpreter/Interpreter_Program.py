import asyncio

from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

# =========================================================
# MODULE 2 — LESSON 4
# INTERPRETER DEMO
# =========================================================

load_dotenv()

# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def print_final_message(result):
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


# ---------------------------------------------------------
# Main async program
# ---------------------------------------------------------

async def main():

    # =====================================================
    # 1. CHECKPOINTER
    # =====================================================
    #
    # Keeps the conversation state for this thread.
    # =====================================================

    checkpointer = InMemorySaver()

    # =====================================================
    # 2. INTERPRETER MIDDLEWARE
    # =====================================================
    #
    # mode="thread":
    #
    # JavaScript variables/functions created by eval
    # can remain available across multiple turns using
    # the SAME thread_id.
    #
    # =====================================================

    interpreter = CodeInterpreterMiddleware(
        mode="thread"
    )

    # =====================================================
    # 3. CREATE DEEP AGENT
    # =====================================================

    agent = create_deep_agent(
        model="openai:gpt-5.5",

        middleware=[interpreter],

        checkpointer=checkpointer,

        system_prompt="""
            You are a learning assistant demonstrating
            the JavaScript interpreter.

            When calculations are requested:

            - Use the eval tool.
            - Keep useful variables in the interpreter.
            - Reuse existing variables when the user
              asks a follow-up question.
            - Keep final answers short.
            """
    )

    # =====================================================
    # 4. THREAD
    # =====================================================
    #
    # The same thread_id is important because
    # mode="thread" keeps interpreter state per thread.
    #
    # =====================================================

    config = {
        "configurable": {
            "thread_id": "interpreter-thread"
        }
    }

    # =====================================================
    # TURN 1
    # =====================================================
    #
    # The agent creates a JavaScript variable:
    #
    # courseFees = [400, 700, 600]
    #
    # This variable should stay inside the interpreter.
    #
    # =====================================================

    print(
        "\n========== TURN 1 ==========\n"
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Use the interpreter. "
                        "Create a JavaScript variable called "
                        "courseFees containing [400, 700, 600]. "
                        "Calculate the total course fee. "
                        "Keep courseFees available because "
                        "I will use it again later."
                    )
                }
            ]
        },

        config=config
    )

    print_final_message(result)

    # =====================================================
    # SHOW INTERPRETER TOOL CALLS
    # =====================================================

    print(
        "\n========== TURN 1 TOOL CALLS ==========\n"
    )

    for message in result["messages"]:
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                print(f"Tool Name: {tool_call['name']}")
                print(f"Tool Input: {tool_call['args']}")
                print("-" * 50)

    # =====================================================
    # TURN 2
    # =====================================================
    #
    # IMPORTANT:
    #
    # We DO NOT provide [400, 700, 600] again.
    #
    # The agent should reuse courseFees from the
    # persistent interpreter.
    #
    # =====================================================

    print(
        "\n========== TURN 2 ==========\n"
    )

    result_2 = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Using the existing courseFees variable "
                        "already stored in the interpreter, "
                        "calculate the average fee and the "
                        "highest fee. "
                        "Do not recreate the variable."
                    )

                }
            ]
        },
    # SAME thread
    config = config
    )

    # =====================================================
    # SHOW TURN 2 TOOL CALLS
    # =====================================================

    print("\n========== TURN 2 TOOL CALLS ==========\n")

    for message in result_2["messages"]:
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                print(f"Tool Name: {tool_call['name']}")
                print(f"Tool Input: {tool_call['args']}")
                print("-" * 50)


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":
    asyncio.run(main())