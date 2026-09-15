from deepagents import create_deep_agent
from langchain_core.tools import tool
from langchain.agents.middleware import TodoListMiddleware
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------
# 1. Custom Tool
# ---------------------------------------------------------

@tool
def get_city_information(city: str) -> str:
    """Return basic travel information about a city."""

    city_data = {
        "Amsterdam": """
        Amsterdam:
        - Famous for canals, museums, cycling and historic architecture.
        - Popular places: Rijksmuseum, Jordaan, Vondelpark.
        - Good activities: canal cruise, cycling, museum visits.
        """,

        "Paris": """
        Paris:
        - Famous for art, architecture and food.
        - Popular places: Eiffel Tower, Louvre, Montmartre.
        - Good activities: museum visits, Seine walk, cafes.
        """,

        "Rovaniemi": """
        Rovaniemi:
        - Located in Finnish Lapland.
        - Popular for Arctic nature and Santa Claus Village.
        - Good activities: hiking, Northern Lights tours and nature trips.
        """
    }

    return city_data.get(
        city,
        f"No information is currently available for {city}."
    )


# ---------------------------------------------------------
# 2. System Prompt
# ---------------------------------------------------------

system_prompt = """
You are a weekend travel planner assistant.

Follow these steps:

1. Create a small todo list.
2. Use get_city_information to get information about the city.
3. Create a simple Saturday and Sunday itinerary.
4. Return the complete itinerary directly to the user.

Do not save or write anything to a file.
Keep the itinerary practical and concise.
"""


# ---------------------------------------------------------
# 3. Create Deep Agent
# ---------------------------------------------------------

agent = create_deep_agent(
    model="openai:gpt-5.5",

    tools=[
        get_city_information
    ],

    middleware=[
        TodoListMiddleware()
    ],

    system_prompt=system_prompt
)


# ---------------------------------------------------------
# 4. Give Agent a Task
# ---------------------------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": """
                I want to spend a weekend in Rovaniemi.

                Create a simple Saturday and Sunday itinerary.
                Return the itinerary directly in your response.
                """
            }
        ]
    }
)


# ---------------------------------------------------------
# 5. Print Only Final Text
# ---------------------------------------------------------

final_message = result["messages"][-1]

content = final_message.content

if isinstance(content, str):
    print(content)

else:
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])