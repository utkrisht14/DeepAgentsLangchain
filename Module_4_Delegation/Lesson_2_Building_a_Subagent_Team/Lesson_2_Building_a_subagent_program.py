from deepagents import create_deep_agent
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# MODULE 4 — LESSON 2
# BUILDING A SUBAGENT TEAM
# =========================================================

# ---------------------------------------------------------
# 1. Risk Analyst Subagent
# ---------------------------------------------------------

risk_analyst = {
"name": "risk-analyst",

    "description": (
        "Analyse project plans and identify the most important "
        "delivery, technical, and operational risks."
    ),

    "model": "openai:gpt-5.5",

    # This specialist does not need external tools.
    "tools": [],

    "system_prompt": """
    You are a project risk analyst.

    For the project information you receive:

    1. Identify the 3 biggest risks.
    2. Explain each briefly.
    3. Give one mitigation for each.

    Keep the response concise.
    """
}


# ---------------------------------------------------------
# 2. Budget Planner Subagent
# ---------------------------------------------------------

budget_planner = {

    "name": "budget-planner",

    "description": (
        "Review project budgets and suggest how available "
        "money should be allocated across project activities."
    ),

    "model": "openai:gpt-5.5",

    "tools": [],

    "system_prompt": """
    You are a project budget planner.

    Given a project budget:

    1. Suggest a simple budget allocation.
    2. Focus on development, testing, contingency,
       and launch preparation.
    3. Make sure the total allocation does not exceed
       the available budget.

    Keep the response concise.
    """
}

# ---------------------------------------------------------
# 3. Create Main Agent
# ---------------------------------------------------------
#
# Providing multiple subagents causes Deep Agents to expose
# the built-in `task` delegation tool.
# ---------------------------------------------------------

agent = create_deep_agent(

    model = "openai:gpt-5.5",

    subagents = [risk_analyst, budget_planner],

    system_prompt="""
    You are a project manager.

    When reviewing a project plan:

    - Delegate risk analysis to the risk-analyst.
    - Delegate budget planning to the budget-planner.
    - Do not perform their specialist work yourself.

    After receiving both reports, combine them into a
    short project recommendation for the user.
    """
)


# ---------------------------------------------------------
# 4. Real-Life Project Request
# ---------------------------------------------------------

user_request = """
We need to launch a customer dashboard in 4 weeks.

Current situation:

- Development is 75% complete.
- Testing has not started.
- One API integration is unfinished.
- We have 3 developers.
- Remaining project budget is €20,000.

Review the project and give me:
1. The main risks.
2. A suggested budget allocation.
3. A short recommendation on what we should focus on.
"""

# ---------------------------------------------------------
# 5. Run Main Agent
# ---------------------------------------------------------

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
# 6. Show Delegation Calls
# ---------------------------------------------------------
#
# We should see the main agent calling `task` for
# different subagent types.
# ---------------------------------------------------------

print("\n========== DELEGATION ==========\n")

for message in result["messages"]:
    if (hasattr(message, "tool_calls") and message.tool_calls):
        for tool_call in message.tool_calls:
            print(f"Tool Name: {tool_call['name']}")
            print(f"Tool Input: {tool_call['args']}")
            print("-" * 50)


# ---------------------------------------------------------
# 7. Print Final Main-Agent Response
# ---------------------------------------------------------

print("\n========== FINAL PROJECT REVIEW ==========\n")

content = result["messages"][-1].content

if isinstance(content, str):
    print(content)

else:
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])
