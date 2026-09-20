"""
Module 3 - Lesson 1B
Offload Only Demo

Purpose:
    Demonstrate Deep Agents automatically moving an oversized TOOL RESULT
    out of the active model context and into backend storage.

This is NOT conversation summarization.

Scenario:
    A research tool returns a very large collection of survey comments.
    Keeping the complete tool output in the model context would waste tokens,
    so Deep Agents stores the full output in the filesystem and leaves a
    smaller preview/reference in the ToolMessage.
"""

from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool

from dotenv import load_dotenv

load_dotenv()

# =========================================================
# 1. Workspace used for offloaded content
# =========================================================

workspace = Path(__file__).parent / "offload_only_workspace"
workspace.mkdir(exist_ok=True)

# =========================================================
# 2. Real filesystem backend
# =========================================================

# virtual_mode=True means an agent path such as:
#
#     /large_tool_results/...
#
# maps under our workspace folder.
# =========================================================

backend = FilesystemBackend(
    root_dir=workspace,
    virtual_mode=True
)

# =========================================================
# 3. A deliberately large tool result
# =========================================================
#
# Deep Agents currently offloads oversized tool results.
# We create >80,000 characters so this example reliably
# exceeds the typical large-result threshold.
# =========================================================

@tool
def get_customer_survey_archive(product: str) -> str:
    """
    Return a large archive of customer survey comments for a product.
    """

    comments = []

    for i in range(2500):
        comments.append(
            f"Survey {i:04d} | Product={product} | "
            "Customers value reliability, clear documentation, "
            "fast onboarding, and responsive support. "
            "Some users also request better reporting and exports."
        )

        return "\n".join(comments)


# =========================================================
# 4. Disable automatic conversation summarization
# =========================================================
#
# create_deep_agent normally has Deep Agents'
# SummarizationMiddleware.
#
# Passing LangChain's middleware with the same name replaces it.
#
# trigger=None means automatic summarization is disabled.
#
# This lets us isolate TOOL-RESULT OFFLOADING.
# =========================================================

no_auto_summary = SummarizationMiddleware(
    model="openai:gpt-5.5",
    trigger=None,
)

agent = create_deep_agent(
    model="openai:gpt-5.5",
    backend=backend,
    middleware=[no_auto_summary],
    tools=[get_customer_survey_archive],
    system_prompt="""
    You are a research assistant.

    When asked about the survey archive:
    1. Call get_customer_survey_archive.
    2. Do not reproduce the entire archive.
    3. Give only a short confirmation that the archive was received.
    """
)

# =========================================================
# 6. Run the research request
# =========================================================

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                 "content": (
                    "Load the customer survey archive for Aurora Dashboard. "
                    "After loading it, briefly confirm that you received it."
                ),
            }
        ]
    }
)

# =========================================================
# 7. Inspect ToolMessage
# =========================================================
#
# Instead of containing the whole huge tool result,
# the ToolMessage should contain an offload notice,
# preview, and filesystem path.
# =========================================================

print("\n========== TOOL MESSAGE ==========\n")

for message in result["messages"]:
    if isinstance(message, ToolMessage):
        print(f"Tool: {message.name}")
        print()
        print(message.content)
        print("\n" + "-" * 70)


# =========================================================
# 8. Show files physically created by offloading
# =========================================================

print("\n========== OFFLOADED FILES ==========\n")

found = False

for path in workspace.rglob("*"):

    if path.is_file():

        found = True

        print(path)

        # Show size so we can see that the full result
        # is much larger than the preview in the message.
        print(f"Size: {path.stat().st_size:,} bytes")
        print("-" * 70)


if not found:
    print(
        "No offloaded file was found. "
        "If your Deep Agents version uses a different threshold, "
        "increase the number of generated survey comments."
    )


# =========================================================
# 9. Final answer
# =========================================================

print("\n========== FINAL ANSWER ==========\n")

final_message = result["messages"][-1]

if isinstance(final_message.content, str):
    print(final_message.content)
else:
    for block in final_message.content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])


print(
    "\nKEY IDEA:\n"
    "The full oversized TOOL RESULT was moved out of active context.\n"
    "The model received a much smaller reference/preview instead."
)