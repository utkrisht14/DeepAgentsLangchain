from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
# 1. Create and configure the model
# ---------------------------------------------------------

model = init_chat_model(
    "openai:gpt-5.5",
    temperature=0
)


# ---------------------------------------------------------
# 2. Create the Deep Agent using the model object
# ---------------------------------------------------------

agent = create_deep_agent(
    model,
    system_prompt="""
    You are an AI learning assistant.

    Explain technical concepts in simple words.
    Keep answers short and structured.
    """
)


# ---------------------------------------------------------
# 3. Prepare the user request
# ---------------------------------------------------------

input_state= {
    "messages": [
        {
            "role": "user",
            "content": "Explain the difference between an AI model and an AI agent in 3 simple points."
        }
    ]
}


# ---------------------------------------------------------
# 4. Run the agent
# ---------------------------------------------------------

result = agent.invoke(input_state)

# ---------------------------------------------------------
# 5. Get the final AI message
# ---------------------------------------------------------

final_message = result["messages"][-1]


# ---------------------------------------------------------
# 6. Display only the text content
# ---------------------------------------------------------

print("\n========== FINAL RESPONSE ==========\n")

if isinstance(final_message.content, str):
    print(final_message.content)

else:
    for block in final_message.content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])
