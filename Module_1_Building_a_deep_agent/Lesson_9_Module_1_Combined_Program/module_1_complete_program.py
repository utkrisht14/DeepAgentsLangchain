import asyncio
import sys
from pathlib import Path

from deepagents import create_deep_agent

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

# Current first-party LangChain MCP integration
from langchain.mcp import MCPAdapter

# Used to save the state of our conversation thread
from langgraph.checkpoint.memory import InMemorySaver

# Used to resume execution after HITL approval/rejection
from langgraph.types import Command


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# NORMAL LANGCHAIN TOOL
# =========================================================
# This is a normal Python/LangChain tool.
# It is NOT coming from MCP.
# =========================================================

@tool
def calculate_discounted_price(
    price: float,
    discount_percent: float
) -> str:
    """
    Calculate the final price after applying a discount.
    """

    discount_amount = price * (discount_percent / 100)

    final_price = price - discount_amount

    return f"Final price after discount: €{final_price:.2f}"


# =========================================================
# SENSITIVE TOOL
# =========================================================
# This tool represents an action that changes something.
#
# Because enrollment is an action, we will protect it using
# Human-in-the-Loop approval.
# =========================================================

@tool
def enroll_student(
    student_name: str,
    course_name: str
) -> str:
    """
    Enroll a student in a course.
    """

    # Demo only.
    # No real enrollment happens.
    return (
        f"{student_name} has been successfully enrolled "
        f"in the {course_name} course."
    )


# =========================================================
# HELPER FUNCTION
# =========================================================
# Deep Agent responses can contain either:
#
# 1. A normal string
# 2. Structured content blocks
#
# This helper prints the final AI response cleanly.
# =========================================================

def print_final_response(result):

    messages = result.value["messages"]

    final_message = messages[-1]

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
# MAIN PROGRAM
# =========================================================

async def main():

    # =====================================================
    # 1. FIND MCP SERVER
    # =====================================================

    server_path = (
        Path(__file__).parent
        / "course_mcp_server.py"
    )


    # =====================================================
    # 2. MCP CONFIGURATION
    # =====================================================
    # MCPAdapter will start the local MCP server using
    # the same Python environment as this program.
    #
    # We do NOT need to start course_mcp_server.py manually.
    # =====================================================

    mcp_config = {

        "mcpServers": {

            "courses": {

                "command": sys.executable,

                "args": [
                    str(server_path)
                ]
            }
        }
    }


    # =====================================================
    # 3. CONNECT TO MCP SERVER
    # =====================================================

    async with MCPAdapter(mcp_config) as adapter:

        # Discover MCP tools and convert them into
        # LangChain-compatible tools.
        mcp_tools = await adapter.list_tools()


        print(
            "\n========== MCP TOOLS DISCOVERED ==========\n"
        )

        for mcp_tool in mcp_tools:

            print(
                f"Tool Name: {mcp_tool.name}"
            )

            print(
                f"Description: {mcp_tool.description}"
            )

            print("-" * 50)


        # =================================================
        # 4. MODEL
        # =================================================
        # Lesson 3 - Model
        #
        # The model performs reasoning and decides when
        # a tool needs to be called.
        # =================================================

        model = init_chat_model(
            "openai:gpt-5.5",
            temperature=0
        )


        # =================================================
        # 5. CHECKPOINTER
        # =================================================
        # Lesson 7 - Checkpointer
        #
        # Saves conversation state for our thread.
        #
        # InMemorySaver only survives while this Python
        # process is running.
        # =================================================

        checkpointer = InMemorySaver()


        # =================================================
        # 6. SYSTEM PROMPT
        # =================================================
        # Lesson 4 - System Prompt
        # =================================================

        system_prompt = """
        You are a course information assistant.

        Follow these rules:

        1. When course duration or fee information is needed,
           use the available MCP course-information tool.

        2. When a discounted price needs to be calculated,
           use the calculate_discounted_price tool.

        3. When the user asks to enroll in a course,
           use the enroll_student tool.

        4. Use information from previous messages when
           available.

        5. Do not invent course information.

        6. Keep answers short and clear.
        """


        # =================================================
        # 7. CREATE DEEP AGENT
        # =================================================
        #
        # This combines:
        #
        # Model
        # System Prompt
        # MCP Tool
        # Normal Tool
        # HITL Tool
        # Checkpointer
        # =================================================

        agent = create_deep_agent(

            model=model,

            tools=[
                *mcp_tools,
                calculate_discounted_price,
                enroll_student
            ],

            system_prompt=system_prompt,

            checkpointer=checkpointer,


            # =============================================
            # HITL CONFIGURATION
            # =============================================
            # Lesson 8 - Human-in-the-Loop
            #
            # Before enroll_student executes, pause the
            # graph and ask the human for approval.
            # =============================================

            interrupt_on={

                "enroll_student": {

                    "allowed_decisions": [
                        "approve",
                        "reject"
                    ]
                }
            }
        )


        # =================================================
        # 8. THREAD
        # =================================================
        # Lesson 7 - Thread
        #
        # All three turns use the SAME thread_id.
        #
        # Therefore the agent can access previous messages.
        # =================================================

        config = {

            "configurable": {

                "thread_id":
                    "module-1-course-demo"
            }
        }


        # =================================================
        # TURN 1
        # =================================================
        # Demonstrates:
        #
        # Messages
        # Model
        # System Prompt
        # MCP
        # Tool Calling
        # =================================================

        print(
            "\n\n========== TURN 1 ==========\n"
        )

        print(
            "USER:\n"
            "What is the duration and fee "
            "of the Agentic AI course?\n"
        )


        result = await agent.ainvoke(

            {
                "messages": [

                    {
                        "role": "user",

                        "content": (
                            "What is the duration and fee "
                            "of the Agentic AI course?"
                        )
                    }
                ]
            },

            config=config,

            version="v2"
        )


        print("AGENT:")

        print_final_response(result)


        # =================================================
        # TURN 2
        # =================================================
        # Demonstrates:
        #
        # Same Thread
        # Checkpointer
        # Previous Messages
        # Normal LangChain Tool
        #
        # Notice that we do NOT send €600 again.
        #
        # The agent gets that context from Turn 1.
        # =================================================

        print(
            "\n\n========== TURN 2 ==========\n"
        )

        print(
            "USER:\n"
            "Using the fee you just found, "
            "what will the price be after "
            "a 10% discount?\n"
        )


        result = await agent.ainvoke(

            {
                "messages": [

                    {
                        "role": "user",

                        "content": (
                            "Using the fee you just found, "
                            "what will the price be after "
                            "a 10% discount?"
                        )
                    }
                ]
            },

            # SAME thread
            config=config,

            version="v2"
        )


        print("AGENT:")

        print_final_response(result)


        # =================================================
        # TURN 3
        # =================================================
        # Demonstrates:
        #
        # HITL
        # Interrupt
        # Checkpoint
        # Resume
        #
        # enroll_student is protected by interrupt_on.
        # =================================================

        print(
            "\n\n========== TURN 3 ==========\n"
        )

        print(
            "USER:\n"
            "Enroll Utkrisht in the "
            "Agentic AI course.\n"
        )


        result = await agent.ainvoke(

            {
                "messages": [

                    {
                        "role": "user",

                        "content": (
                            "Enroll Utkrisht in the "
                            "Agentic AI course."
                        )
                    }
                ]
            },

            config=config,

            version="v2"
        )


        # =================================================
        # 9. CHECK WHETHER EXECUTION WAS INTERRUPTED
        # =================================================

        if result.interrupts:

            print(
                "\n========== HUMAN APPROVAL REQUIRED ==========\n"
            )


            # There should be one interrupt in this demo.
            interrupt = result.interrupts[0]

            interrupt_value = interrupt.value


            # HumanInTheLoopMiddleware provides
            # action_requests describing pending tools.
            action_requests = (
                interrupt_value["action_requests"]
            )


            # Our demo contains one sensitive action.
            action = action_requests[0]


            print(
                f"Tool: {action['name']}"
            )

            print(
                f"Arguments: {action['args']}"
            )


            # =================================================
            # 10. ASK HUMAN
            # =================================================

            decision = input(
                "\nType 'approve' or 'reject': "
            ).strip().lower()


            # =================================================
            # APPROVE
            # =================================================

            if decision == "approve":

                print(
                    "\nHuman approved the action."
                )


                # Command(resume=...) continues the execution
                # from the saved checkpoint.
                #
                # IMPORTANT:
                # We use the SAME config/thread_id.
                result = await agent.ainvoke(

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


            # =================================================
            # REJECT
            # =================================================

            else:

                print(
                    "\nHuman rejected the action."
                )


                result = await agent.ainvoke(

                    Command(

                        resume={

                            "decisions": [

                                {
                                    "type": "reject",

                                    "message": (
                                        "The user rejected "
                                        "the enrollment."
                                    )
                                }
                            ]
                        }
                    ),

                    # SAME thread_id is required.
                    config=config,

                    version="v2"
                )


        # =================================================
        # 11. FINAL RESPONSE
        # =================================================

        print(
            "\n========== FINAL RESPONSE ==========\n"
        )

        print_final_response(result)


        # =================================================
        # 12. DISPLAY MESSAGE HISTORY
        # =================================================
        # This shows that all three turns belong to the
        # same conversation thread.
        # =================================================

        print(
            "\n\n========== MESSAGE HISTORY ==========\n"
        )


        for index, message in enumerate(
            result.value["messages"],
            start=1
        ):

            print(
                f"{index}. {type(message).__name__}"
            )

            content = message.content

            if isinstance(content, str):

                # Avoid printing huge empty content.
                if content.strip():

                    print(content)

            else:

                for block in content:

                    if (
                        isinstance(block, dict)
                        and block.get("type") == "text"
                    ):

                        print(
                            block["text"]
                        )

            print("-" * 50)


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())