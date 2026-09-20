"""
Module 3 - Lesson 1C
Summarization + Offload Combined Demo

Purpose:
    Demonstrate BOTH forms of context management together:

    1. Large tool-result offloading
       - Huge tool output is stored under /large_tool_results/...

    2. Conversation summarization + history offloading
       - Older messages are summarized.
       - Their full original history is archived under
         /conversation_history/...

Scenario:
    A product-research assistant works through a long project discussion
    and also receives a very large survey archive.
"""

from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from deepagents.middleware.summarization import SummarizationMiddleware
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv

load_dotenv()

# =========================================================
# Helper function
# =========================================================

def print_final_answer(result):
    message = result["messages"][-1]
    content = message.content

    if isinstance(content, str):
        print(content)
        return

    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])


# =========================================================
# 1. Workspace
# =========================================================

workspace = Path(__file__).parent / "combined_context_workspace"
workspace.mkdir(exist_ok=True)

# =========================================================
# 2. Backend
# =========================================================
#
# Both kinds of offloaded data can be inspected here:
#
# /large_tool_results/
# /conversation_history/
# =========================================================

backend = FilesystemBackend(
    root_dir=workspace,
    virtual_mode=True
)

# =========================================================
# 3. Large research tool
# =========================================================

@tool
def load_market_research_archive(product: str) -> str:
    """
    Return a large archive of market-research observations.
    """

    rows = []

    for i in range(2500):
        rows.append(
            f"Observation {i:04d} | Product={product} | "
            "Users prioritize reliability, simple onboarding, "
            "clear reporting, export options, and responsive support. "
            "Enterprise users frequently mention auditability."
        )

    return "\n".join(rows)

# =========================================================
# 4. Deep Agents summarization middleware
# =========================================================
#
# IMPORTANT:
# This is Deep Agents' middleware.
#
# When the trigger is reached it:
#
# 1. Offloads the full older history to the backend.
# 2. Generates a compact summary.
# 3. Keeps that summary + recent messages in active context.
#
# Small trigger values are used only so the behavior is
# easy to observe in this learning demo.
# =========================================================

summarization = SummarizationMiddleware(
    model="openai:gpt-5.5",
    backend=backend,
    trigger=("messages", 6),
    keep=("messages", 2)
)

# =========================================================
# 5. Checkpointer
# =========================================================

checkpointer = InMemorySaver()

# =========================================================
# 6. Create Deep Agent
# =========================================================

agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[load_market_research_archive],
    backend=backend,
    middleware=[summarization],
    checkpointer=checkpointer,
    system_prompt="""
     You are a product-research assistant.

    Remember important project requirements across turns.

    When market research is requested, use
    load_market_research_archive.

    Never reproduce the full research archive.
    Keep normal answers short.
    """
)

# =========================================================
# 7. One continuing thread
# =========================================================

config = {
    "configurable": {
        "thread_id": "combined-context-demo"
    }
}

# =========================================================
# 8. Several meaningful turns
# =========================================================

turns = [
    "The project is called Aurora Dashboard.",
    (
        "Load the market research archive for Aurora Dashboard. "
        "Just confirm when it is available."
    ),
    "Our primary customers are property managers.",
    "The launch deadline is 15 December.",
    "The total implementation budget is €25,000.",
    (
        "Give me a short final project brief containing the project name, "
        "target customer, deadline, budget, and the main themes you retained "
        "from the research."
    ),
]


for number, user_message in enumerate(turns, start=1):

    print(f"\n========== TURN {number} ==========\n")
    print(f"USER: {user_message}\n")

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        },
        config=config
    )

    print("AGENT: ")
    print_final_answer(result)


# =========================================================
# 9. Show any large-tool-result offload references
# =========================================================

print("\n========== TOOL RESULT OFFLOAD NOTICES ==========\n")

for message in result["messages"]:
    if isinstance(message, ToolMessage):

        content = str(message.content)

        if "large_tool_results" in content:
            print(content[:1200])
            print("\n" + "-" * 70)


# =========================================================
# 10. Show final active messages
# =========================================================
#
# Older raw conversation should be represented by a
# summarization message rather than every original message.
# =========================================================

print("\n========== FINAL ACTIVE MESSAGE STATE ==========\n")

for index, message in enumerate(result["messages"], start=1):

    source = message.additional_kwargs.get("lc_source")

    print(
        f"{index}. {type(message).__name__}"
        + (f"  [source={source}]" if source else "")
    )

    content = message.content

    if isinstance(content, str):
        print(content.replace("\n", " ")[:350])
    else:
        print("[structured content]")

    print("-" * 70)

# =========================================================
# 11. Inspect backend files
# =========================================================

print("\n========== BACKEND FILES ==========\n")

all_files = [path for path in workspace.rglob("*") if path.is_file()]

if not all_files:
    print("No backend files found.")
else:
    for path in all_files:
        print(path.relative_to(workspace))
        print(f"Size: {path.stat().st_size:,} bytes")
        print("-" * 70)


# =========================================================
# 12. Categorize what we expect
# =========================================================

large_results = [
    p for p in all_files
    if "large_tool_results" in p.parts
]

history_files = [
    p for p in all_files
    if "conversation_history" in p.parts
]

print("\n========== SUMMARY ==========\n")

print(
    f"Large tool-result files: {len(large_results)}"
)

print(
    f"Conversation-history archive files: {len(history_files)}"
)

print(
    "\nKEY IDEA:\n"
    "Large individual tool output was OFFLOADED to storage.\n"
    "Older conversation history was OFFLOADED and then SUMMARIZED.\n"
    "The model continues with a smaller active context."
)
