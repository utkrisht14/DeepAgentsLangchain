import asyncio
import sys

from pathlib import Path
from dotenv import load_dotenv

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter


load_dotenv()


async def main():

    # 1. Find our MCP server file
    server_path = Path(__file__).parent / "order_server.py"


    # 2. Configure MCP connection
    mcp_config = {
        "mcpServers": {
            "orders": {
                "command": sys.executable,
                "args": [str(server_path)],
                "transport": "stdio",
            }
        }
    }


    # 3. Connect to MCP server through MCPAdapter
    async with MCPAdapter(mcp_config) as adapter:

        # 4. Load MCP tools as LangChain tools
        tools = await adapter.list_tools()

        print("MCP tools are available.\n")

        for tool in tools:
            print(f"Tool Name: {tool.name}")
            print(f"Description: {tool.description}")
            print("-" * 50)


        # 5. Create Deep Agent
        agent = create_deep_agent(
            model="openai:gpt-5.5",
            tools=tools,
            system_prompt="""
            You are a customer support agent.

            Use the available order tools whenever you need
            information about an order.

            If the customer asks about a refund:

            1. Check the order.
            2. Check refund eligibility.
            3. If appropriate, create a support note.
            4. Explain the result clearly to the customer.

            Never invent order information.
            """
        )


        # 6. User request
        user_message = """
        Customer John says:

        I received order ORD-101 a few days ago,
        but I don't want the laptop anymore.

        Can I return it?

        Please also record that I contacted support.
        """


        # 7. Run Deep Agent
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )


        # 8. Print final answer
        final_message = result["messages"][-1]

        print("\nFINAL ANSWER:\n")

        content = final_message.content

        if isinstance(content, str):
            print(content)

        else:
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    print(block["text"])


if __name__ == "__main__":
    asyncio.run(main())