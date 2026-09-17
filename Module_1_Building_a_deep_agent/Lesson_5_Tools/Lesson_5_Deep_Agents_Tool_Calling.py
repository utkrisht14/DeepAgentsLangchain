from deepagents import create_deep_agent
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
# 1. Create a custom tool
# ---------------------------------------------------------

@tool
def calculate_trip_cost(distance_km: float, fuel_price: float):
    """
    Calculate the approximate fuel cost for a trip.

    Assumption:
    - Vehicle fuel consumption = 8 liters per 100 km
    """

    fuel_consumption = 8 # liters per 100 km

    litres_needed = (distance_km / 100) * fuel_consumption

    total_cost = litres_needed * fuel_price

    return f"Estimated fuel cost: €{total_cost:.2f}"


# ---------------------------------------------------------
# 2. Create the Deep Agent
# ---------------------------------------------------------

agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[
        calculate_trip_cost
    ],

    system_prompt = """ 
    You are a simple travel cost assistant.

    If the user asks for fuel cost:
    - Always use the calculate_trip_cost tool.
    - Do not calculate the result yourself.
    - Return a short final answer.
    """
)

# ---------------------------------------------------------
# 3. Give the agent a task
# ---------------------------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": """
                I need to drive 350 km.

                The fuel price is €1.85 per liter.

                What will be the approximate fuel cost?
                """
            }
        ]
    }
)

# ---------------------------------------------------------
# 4. Show the execution flow
# ---------------------------------------------------------

print("\n========== AGENT EXECUTION ==========\n")

for message in result["messages"]:
    print(f"Message Type: {type(message).__name__}")

    # Show tool call
    if hasattr(message, "tool_calls") and message.tool_calls:
        print("Tool Calls:")
        print(message.tool_calls)

    # Show message content
    if message.content:
        print("Content: ")
        print(message.content)

    print("-" * 50)


# ---------------------------------------------------------
# 5. Print only final answer
# ---------------------------------------------------------

final_message = result["messages"][-1]

print("\n========== FINAL ANSWER ==========\n")

if isinstance(final_message.content, str):
    print(final_message.content)

else:
    for block in final_message.content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])


