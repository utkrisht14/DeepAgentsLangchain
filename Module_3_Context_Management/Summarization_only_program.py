"""
Module 3 - Lesson 1A
Summarization Only Demo

Purpose:
    Demonstrate context summarization WITHOUT Deep Agents conversation-history
    offloading.

Important:
    Deep Agents normally installs its own SummarizationMiddleware, which also
    offloads old conversation history.

    In this demo we pass LangChain's base SummarizationMiddleware. Because it
    has the same middleware name, it replaces the Deep Agents default
    summarization middleware.

Scenario:
    A project assistant remembers important requirements from a long
    conversation even after older messages are summarized.
"""

from deepagents import create_deep_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv

load_dotenv()

# =========================================================
# Helper: print final model response
# =========================================================

def print_final_answer(result):
    message = result["messages"][-1]
    content = message.content

    if isinstance(content, str):
        print(content)
    else:
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                print(block["text"])


# =========================================================
# 1. Create checkpointer
# =========================================================
# We use the same thread across several separate invocations.
# =========================================================

checkpointer = InMemorySaver()

# =========================================================
# 2. Summarization-only middleware
# =========================================================
#
# trigger=("messages", 6)
#     Start summarizing once the conversation reaches
#     approximately 6 messages.
#
# keep=("messages", 2)
#     Keep the newest 2 messages unchanged.
#
# This is LANGCHAIN's middleware, not Deep Agents'
# backend-aware summarization middleware.
# Therefore this demo does not archive the old history
# to /conversation_history.
# =========================================================

summarization = SummarizationMiddleware(
    model="openai:gpt-5.5",
    trigger=("messages", 6),
    keep=("messages", 2)
)

# =========================================================
# 3. Create Deep Agent
# =========================================================

agent = create_deep_agent(
    model="openai:gpt-5.5",
    middleware = [summarization],
    checkpointer = checkpointer,
    system_prompt="""
    You are a project-planning assistant.

    Remember the important project requirements from earlier turns.
    Keep each response short.
    """,
)

# =========================================================
# 4. Same conversation thread
# =========================================================

config = {
    "configurable": {
        "thread_id": "summarization-only-demo"
    }
}

# =========================================================
# 5. Build a conversation long enough to summarize
# =========================================================

turns = [
    "Our project is called Aurora Analytics.",
    "The launch deadline is 15 December.",
    "The maximum budget is €25,000.",
    "The dashboard must support English and Finnish.",
    (
        "Now summarize the key project requirements I gave you. "
        "Do not invent anything."
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
# 6. Inspect the final active message state
# =========================================================
#
# After summarization, older raw messages should no longer
# all be present in the active context. A summary message
# represents the compressed older history.
# =========================================================

print("\n========== ACTIVE MESSAGE STATE ==========\n")

for index, message in enumerate(result["messages"], start=1):

    source = message.additional_kwargs.get("lc_source")

    print(
        f"{index}. {type(message).__name__}"
        + (f"  [source={source}]" if source else "")
    )

    content = message.content

    if isinstance(content, str):
        preview = content.replace("\n", " ")[:300]
        print(preview)
    else:
        print("[structured content]")

    print("-" * 60)


print(
"\nKEY IDEA:\n"
"Old conversation detail was compressed into a shorter summary.\n"
"No conversation-history archive was intentionally created in this demo."
)
