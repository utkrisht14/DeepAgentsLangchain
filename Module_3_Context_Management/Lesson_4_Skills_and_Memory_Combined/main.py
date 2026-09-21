from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from dotenv import load_dotenv

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

# =========================================================
# 1. PROJECT DIRECTORY
# =========================================================

project_dir = Path(__file__).parent

# =========================================================
# 2. FILESYSTEM BACKEND
# =========================================================
#
# The agent needs filesystem access so it can:
#
# - Read AGENTS.md
# - Discover skills
# - Read the relevant SKILL.md
#
# =========================================================

backend = FilesystemBackend(
    root_dir=".",
    virtual_mode=True
)

# =========================================================
# 3. CREATE DEEP AGENT
# =========================================================

agent = create_deep_agent(
    model="openai:gpt-5.5",

    backend=backend,

    memory = ["./AGENTS.md"],  # AGENTS.md is loaded as persistent context.
                              # The agent therefore always knows our communication preferences.

    skills = ["/skills"],  # Deep Agents discovers skills in this directory.
                          # The full professional-email SKILL.md is loaded only when the task is relevant.

    system_prompt="""
    You are a workplace assistant.

    Use the available memory and relevant skills
    when completing user requests.

    Return only the final requested content.
    """
)

# =========================================================
# 4. REAL-LIFE TASK
# =========================================================

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Write an email to my manager explaining that "
                    "the project report will be delivered tomorrow "
                    "instead of today because I need one more day "
                    "to validate the results."
                )
            }
        ]
    }
)

# =========================================================
# 5. PRINT FINAL ANSWER
# =========================================================

final_message = result["messages"][-1]

content = final_message.content

if isinstance(content, str):

    print(content)

else:

    for block in content:

        if (
            isinstance(block, dict)
            and block.get("type") == "text"
        ):

            print(block["text"])