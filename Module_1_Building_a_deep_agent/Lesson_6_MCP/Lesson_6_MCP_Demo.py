import asyncio
import sys
from pathlib import Path

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------
# 1. Main async function
# ---------------------------------------------------------

async def main():
    server_path = Path(__file__).parent / "course_mcp_server.py"

    # -----------------------------------------------------
    # 2. Configure the MCP Server
    # -----------------------------------------------------

    mcp_config = {
        "mcpServers": {
            "courses": {
                "command":sys.executable,
                "args": [str(server_path)],
            }
        }
    }

    # -----------------------------------------------------
    # 3. Connect to MCP Server
    # -----------------------------------------------------

    async with MCPAdapter(mcp_config) as adapter:

        # Discover tools exposed by MCP servers
        tools = await adapter.list_tools()

        # -------------------------------------------------
        # 4. Display MCP tools discovered
        # -------------------------------------------------

        print("\n========== MCP TOOLS DISCOVERED ==========\n")

        for tool in tools:
            print(f"Tool Name: {tool.name}")
            print(f"Description: {tool.description}")
            print("-" * 50)

        # -------------------------------------------------
        # 5. Create Deep Agent using MCP tools
        # -------------------------------------------------

        agent = create_deep_agent(
            model="openai:gpt-5.5",

            tools=tools,

            system_prompt="""
            You are a course information assistant.

            When the user asks about course duration or price,
            use the available course-information tool.

            Keep the final answer short and clear.
            
            """

        )

        # -------------------------------------------------
        # 6. Run the Deep Agent
        # -------------------------------------------------

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
            }
        )

        # -------------------------------------------------
        # 7. Print final answer
        # -------------------------------------------------

        final_message = result["messages"][-1]

        print("\n========== FINAL ANSWER ==========\n")

        if isinstance(final_message.content, str):
            print(final_message.content)

        else:
            for block in final_message.content:
                if (
                    isinstance(block, dict)
                    and block.get("type") == "text"
                ):
                    print(block["text"])


# ---------------------------------------------------------
# 8. Start program
# ---------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())