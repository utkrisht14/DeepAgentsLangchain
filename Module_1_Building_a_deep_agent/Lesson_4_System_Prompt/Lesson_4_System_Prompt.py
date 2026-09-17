from deepagents import create_deep_agent
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
# 1. Define the system prompt
# ---------------------------------------------------------

system_prompt = """
You are a Python learning assistant.

Rules:
- Explain concepts in simple words.
- Keep the answer short.
- Use exactly 3 bullet points.
- Do not use complex terminology unless necessary.
"""


# ---------------------------------------------------------
# 2. Create the Deep Agent
# ---------------------------------------------------------

agent = create_deep_agent(
    model="openai:gpt-5.5",
    system_prompt=system_prompt
)

# ---------------------------------------------------------
# 3. Give the agent a task
# ---------------------------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
            "role": "user",
            "content": "Explain what a Python decorator is."
            }
        ]
    }
)


# ---------------------------------------------------------
# 4. Get the final response
# ---------------------------------------------------------

final_message = result["messages"][-1]


# ---------------------------------------------------------
# 5. Print only the text
# ---------------------------------------------------------

print("\n========== FINAL RESPONSE ==========\n")

if isinstance(final_message.content, str):
    print(final_message.content)

else:
    for block in final_message.content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])
