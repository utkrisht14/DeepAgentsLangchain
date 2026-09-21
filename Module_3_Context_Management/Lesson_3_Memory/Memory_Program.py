from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# MODULE 3 — MEMORY DEMO
# =========================================================
#
# IMPORTANT:
#
# This is AGENTS.md memory.
#
# It is NOT:
#
# - message history
# - checkpointer memory
# - StoreBackend memory
# - temporary filesystem state
#
# AGENTS.md contains durable context/instructions that are
# automatically loaded into the agent's system context.
# =========================================================

# ---------------------------------------------------------
# 1. Project directory
# ---------------------------------------------------------

project_dir = Path(__file__).parent


# ---------------------------------------------------------
# 2. Make sure AGENTS.md exists
# ---------------------------------------------------------

memory_file = project_dir / "AGENTS.md"

if not memory_file.exists():
    memory_file.write_text(
        """# Agent Memory
    
        ## Project
    
        This project is for learning Deep Agents.
        """,
        encoding="utf-8"
    )


# ---------------------------------------------------------
# 3. Filesystem backend
# ---------------------------------------------------------
#
# The MemoryMiddleware uses this backend to read AGENTS.md.
#
# virtual_mode=True means:
#
# /AGENTS.md
#
# maps to:
#
# <project folder>/AGENTS.md
# ---------------------------------------------------------

backend = FilesystemBackend(
    root_dir=project_dir,
    virtual_mode=True
)

# =========================================================
# HELPER FUNCTION
# =========================================================

def print_final_answer(result):

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


# =========================================================
# RUN 1 — TEACH THE AGENT SOMETHING
# =========================================================

print("\n========== RUN 1: SAVE MEMORY ==========\n")

agent_1 = create_deep_agent(
    model="openai:gpt-5.5",
    backend=backend,
    memory=["./AGENTS.md"], # Deep Agents loads this file into the agent context.

    system_prompt="""
    You are a Deep Agents learning assistant.

    Keep answers short.

    If the user gives you a durable project preference
    and asks you to remember it, update AGENTS.md.
    """
)

result_1 = agent_1.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Remember this project preference: "
                    "we use Python 3.13 and uv as the package manager. "
                    "All future Python setup examples should use uv. "
                    "Save this as durable memory."
                )
            }
        ]
    }
)

print_final_answer(result_1)

# =========================================================
# SHOW AGENTS.md AFTER RUN 1
# =========================================================

print("\n========== AGENTS.md AFTER RUN 1 ==========\n")

print(memory_file.read_text(encoding="utf-8"))


# =========================================================
# RUN 2 — CREATE A COMPLETELY NEW AGENT
# =========================================================
#
# Notice:
#
# We are NOT using a checkpointer.
#
# We are NOT passing previous messages.
#
# This is a fresh agent instance.
#
# The only way it knows the preference is AGENTS.md.
# =========================================================

print("\n========== RUN 2: RECALL MEMORY ==========\n")

agent_2 = create_deep_agent(
    model="openai:gpt-5.5",
    backend=backend,
    memory=["./AGENTS.md"],
    system_prompt="""
    You are a Deep Agents learning assistant.

    Answer based on the persistent agent memory
    when relevant.

    Keep answers short.
    """
)

result_2 = agent_2.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Which Python version and package manager "
                    "should I use for this project?"
                )
            }
        ]
    }
)

print_final_answer(result_2)
