from deepagents import create_deep_agent
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# MODULE 4 — LESSON 1
# DELEGATION DEMO
# =========================================================

# ---------------------------------------------------------
# 1. Define the specialist subagent
# ---------------------------------------------------------
#
# This agent has one specific responsibility:
# analyse project risks.
#
# By default, the subagent works in isolated context.
# It receives the delegated task rather than the complete
# conversation of the main agent.
# ---------------------------------------------------------

risk_analyst = {

"name": "risk-analyst",

    "description": (
        "Analyse project plans and identify important "
        "delivery, technical, and operational risks."
    ),

    "model": "openai:gpt-5.5",

    "tools": [],

    "system_prompt": """
    You are a project risk analyst.

    When given a project plan:

    1. Identify the three most important risks.
    2. Explain each risk briefly.
    3. Suggest one mitigation for each risk.

    Keep your response concise.
    """
}

# ---------------------------------------------------------
# 2. Create the main agent
# ---------------------------------------------------------
#
# The main agent behaves like a project manager.
#
# It can delegate work to the risk-analyst through
# Deep Agents' built-in task tool.
# ---------------------------------------------------------

agent = create_deep_agent(

    model = "openai:gpt-5.5",

    subagents = [risk_analyst],

    system_prompt="""
    You are a project manager.

    When the user asks you to review a project plan,
    delegate the risk analysis to the risk-analyst.

    After receiving the subagent's report:

    - use its findings,
    - give the user a short final recommendation.

    Do not perform the risk analysis yourself.
    """

)


# ---------------------------------------------------------
# 3. User gives a real-life project scenario
# ---------------------------------------------------------

user_request = """
We are planning to launch a new customer dashboard in 6 weeks.

The development is around 70% complete.

Two developers are still working on critical features,
testing has not started yet, and one external API
integration is still unfinished.

Review this plan and tell me what we should focus on.
"""

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": user_request
            }
        ]
    }
)

# ---------------------------------------------------------
# 4. Show delegation
# ---------------------------------------------------------
#
# The main agent should call the built-in `task` tool
# and delegate work to risk-analyst.
# ---------------------------------------------------------

print("\n========== DELEGATION ==========\n")

for message in result["messages"]:
    if (hasattr(message, "tool_calls") and message.tool_calls):
        for tool_call in message.tool_calls:
            print(f"Tool Name: {tool_call['name']}")
            print(f"Tool Input: {tool_call['args']}")
            print("-" * 50)


# ---------------------------------------------------------
# 5. Print final main-agent answer
# ---------------------------------------------------------

print("\n========== FINAL ANSWER ==========\n")

final_message = result["messages"][-1]

content = final_message.content

if isinstance(content, str):
    print(content)

else:
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])