import asyncio
import sys
from pathlib import Path

from deepagents import create_deep_agent
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from langchain_mcp_adapters.client import MultiServerMCPClient

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


load_dotenv()


# =========================================================
# 1. NORMAL CUSTOM TOOL
# =========================================================

@tool
def calculate_discounted_price(price: float, discount_percent:float) -> str:
    """
    Calculate a discounted course price.
    """

    discount = price * discount_percent / 100
    final_price = price - discount

    return f"Final price after discount is: {final_price:.2f}"


# =========================================================
# 2. SENSITIVE TOOL — WILL REQUIRE HITL
# =========================================================

@tool
def enroll_student(student_name: str, course_name: str) -> str:
    """
    Enroll a student in a course.
    """

    return (
        f"{student_name} has been successfully enrolled "
        f"in {course_name}."
    )


# =========================================================
# Helper function to display final response
# =========================================================

def print_final_response(result):

    final_message = result.value["messages"][-1]

    if isinstance(final_message.content, str):
        print(final_message.content)

    else:
        for block in final_message.content:
            if isinstance(block, dict) and block.get("type") == "text":
                print(block["text"])


# =========================================================
# Main Program
# =========================================================

async def main():

    # -----------------------------------------------------
    # 3. MCP SERVER CONFIGURATION
    # -----------------------------------------------------

    server_path = Path(__file__).parent / "course_mcp_server.py"

    mcp_client = MultiServerMCPClient(
        {
            "courses": {
                "command": sys.executable,
                "args": [str(server_path)],
                "transport": "stdio"
            }
        }
    )

    # -----------------------------------------------------
    # 4. GET MCP TOOLS
    # -----------------------------------------------------

    mcp_tools = await mcp_client.get_tools()

    print("\n========== MCP TOOLS ==========\n")

    for tool in mcp_tools:
        print(tool.name)

    # -----------------------------------------------------
    # 5. MODEL
    # -----------------------------------------------------

    model = init_chat_model(
        "openai:gpt-5.5",
        temperature=0
    )

    # -----------------------------------------------------
    # 6. CHECKPOINTER
    # -----------------------------------------------------

    checkpointer = InMemorySaver()

    # -----------------------------------------------------
    # 7. SYSTEM PROMPT
    # -----------------------------------------------------

    system_prompt = """
        You are a course assistant.

        Rules:

        1. Use get_course_details when course duration
           or course fee is requested.

        2. Use calculate_discounted_price when the user
           asks for a discounted price.

        3. Use enroll_student when the user asks to enroll.

        4. Never invent course information.

        5. Keep answers short and clear.
        """

    # -----------------------------------------------------
    # 8. CREATE DEEP AGENT
    # -----------------------------------------------------

    agent = create_deep_agent(
        model = model,

        tools = [
            *mcp_tools,
            calculate_discounted_price,
            enroll_student
        ],

        system_prompt = system_prompt,

        checkpointer = checkpointer,

        # HITL
        interrupt_on = {
            "enroll_student": {
                "allowed_decisions": [
                    "approve",
                    "reject"
                ]
            }
        }
    )

    # -----------------------------------------------------
    # 9. THREAD
    # -----------------------------------------------------

    config = {
        "configurable": {
            "thread_id": "course-conversation-1"
        }
    }

