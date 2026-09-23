import asyncio
import sys


from pathlib import Path

from deepagents import create_deep_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():

    # Find our MCP server file
    server_path = Path(__file__).parent / "order_server.py"

    # Configure MCP connection
    mcp_config = {
        "orders": {
            "command": sys.executable,
            "args": [str(server_path)],
            "transport": "stdio"
        }
    }

    # Create MCP client
    mcp_client = MultiServerMCPClient(mcp_config)

    # Load MCP tools
    tools = await mcp_client.get_tools()

    print("MCP tools are available.")

    for tool in tools:
        print(f"Tool Name: {tool.name}")
        print(f"Description: {tool.description}")
        print("-" * 50)


    # Create deep agent
    agent = create_deep_agent(
        model="openai:gpt-5.5",
        tools=tools,
        system_prompt="""
        You are a customer support agent.

        Use the available order tools when you need information
        about an order.

        If the customer asks about a refund:

        1. Check the order.
        2. Check refund eligibility.
        3. If appropriate, create a support note.
        4. Explain the result clearly to the customer.

        Never invent order information.
        """
    )


    # User request
    user_message = """
    Customer John says:

    I received order ORD-101 a few days ago,
    but I don't want the laptop anymore.

    Can I return it?

    Please also record that I contacted support.
    """

    # Run deep agent
    result = await agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
    )

    # Print final answer
    final_message = result["messages"][-1]
    print(final_message.content)


if __name__ == "__main__":
    asyncio.run(main())
