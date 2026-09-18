from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------
# 1. Create Checkpointer
# ---------------------------------------------------------

checkpointer = InMemorySaver()


# ---------------------------------------------------------
# 2. Create Deep Agent
# ---------------------------------------------------------

agent = create_deep_agent(
    model="openai:gpt-5.5",

    checkpointer=checkpointer,

    system_prompt="""
    You are a simple conversational assistant.

    Remember information from earlier messages
    in the same conversation thread.

    Keep answers short.
    """
)


# ---------------------------------------------------------
# 3. Create Thread Configuration
# ---------------------------------------------------------

config = {
    "configurable": {
        "thread_id": "conversation-1"
    }
}


# ---------------------------------------------------------
# 4. First Message
# ---------------------------------------------------------

print("\n========== TURN 1 ==========\n")

result_1 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "My favorite programming language is Python."
            }
        ]
    },
    config=config
)


final_message_1 = result_1["messages"][-1]

if isinstance(final_message_1.content, str):
    print(final_message_1.content)

else:
    for block in final_message_1.content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])


# ---------------------------------------------------------
# 5. Second Message — Same Thread
# ---------------------------------------------------------

print("\n========== TURN 2 ==========\n")

result_2 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is my favorite programming language?"
            }
        ]
    },
    config=config
)


final_message_2 = result_2["messages"][-1]

if isinstance(final_message_2.content, str):
    print(final_message_2.content)

else:
    for block in final_message_2.content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])


# ---------------------------------------------------------
# 6. Display Message History
# ---------------------------------------------------------

print("\n========== MESSAGE HISTORY ==========\n")

for message in result_2["messages"]:

    print(f"{type(message).__name__}:")

    if isinstance(message.content, str):
        print(message.content)

    else:
        for block in message.content:
            if isinstance(block, dict) and block.get("type") == "text":
                print(block["text"])

    print("-" * 50)