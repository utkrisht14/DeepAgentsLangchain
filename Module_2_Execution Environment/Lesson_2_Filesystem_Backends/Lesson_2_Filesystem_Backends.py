from pathlib import Path

from deepagents import create_deep_agent

from  deepagents.backends import StateBackend, FilesystemBackend, StoreBackend
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# HELPER FUNCTION
# =========================================================
# Prints only the final response from the agent.
# =========================================================

def print_final_answer(result):

    final_message = result["messages"][-1]

    content = final_message.content

    if isinstance(content, str):
        print(content)

    else:
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                print(block["text"])


# =========================================================
# DEMO 1 — STATE BACKEND
# =========================================================

# StateBackend stores files inside LangGraph agent state.

# These are virtual files.
# They do NOT appear in the Windows project folder.

# With a checkpointer, the virtual file can survive across multiple turns of the same thread.

# =========================================================

print("\n======================================")
print("DEMO 1 — STATE BACKEND")
print("======================================\n")


state_backend = StateBackend()

state_checkpointer = InMemorySaver()

state_agent = create_deep_agent(
    model="openai:gpt-5.5",

    backend = state_backend,

    checkpointer = state_checkpointer,

    system_prompt = """
    You are a filesystem learning assistant.

    Use the available filesystem tools whenever
    the user asks you to work with files.

    Keep your final answer short
    """
)


# Same thread will be used for both calls.

state_config = {
    "configurable": {
        "thread_id": "state-backend-demo"
    }
}


# ---------------------------------------------------------
# Turn 1 — Write virtual file
# ---------------------------------------------------------

state_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Create a file called /state_note.txt "
                    "and write this text into it:\n"
                    "This file is stored inside agent state."
                )
            }
        ]
    },
    config = state_config
)

# ---------------------------------------------------------
# Turn 2 — Read same virtual file
# ---------------------------------------------------------

state_result = state_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                        "Read /state_note.txt and tell me "
                        "what it contains."
                )
            }
        ]
    },

    # Same thread ID
    config = state_config
)

print_final_answer(state_result)


# =========================================================
# DEMO 2 — FILESYSTEM BACKEND
# =========================================================

# FilesystemBackend stores REAL files on the local disk.

# We create a dedicated folder so the agent only works
# inside this demonstration directory.

# =========================================================

print("\n\n======================================")
print("DEMO 2 — FILESYSTEM BACKEND")
print("======================================\n")

# Create a real folder next to this Python file.

demo_folder = (
        Path(__file__).parent / "filesystem_demo"
)

demo_folder.mkdir(exist_ok=True)

filesystem_backend = FilesystemBackend(
    root_dir = demo_folder,

    # "/" inside the agent maps to demo_folder.
    virtual_mode= True # Treat root_dir as the agent's virtual "/" or "root" directory
                        # and keep file operations inside it.

)


filesystem_agent = create_deep_agent(
    model="openai:gpt-5.5",

    backend = filesystem_backend,

system_prompt="""
    You are a filesystem learning assistant.

    Use filesystem tools when the user asks
    you to create, read, or edit files.

    Keep your answer short.
    """
)

filesystem_result = filesystem_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content" :  "Create a file called /local_note.txt "
                    "containing:\n"
                    "This is a real file stored on disk.\n\n"
                    "Then read the file and confirm its contents."
            }
        ]
    }
)

print_final_answer(filesystem_result)

print(
    "\nReal file location:\n"
    f"{demo_folder / 'local_note.txt'}"
)

# =========================================================
# DEMO 3 — STORE BACKEND
# =========================================================

# StoreBackend stores files in a LangGraph Store.

# Unlike StateBackend, this storage is not tied to only
# one conversation thread.

# For learning, we use InMemoryStore.

# In production, a durable store/database could be used.

print("\n\n======================================")
print("DEMO 3 — STORE BACKEND")
print("======================================\n")

store = InMemoryStore() # For storage mechanism.

store_backend = StoreBackend(
    store = store, # For the actual LangGraph BaseStore where the files are saved

    # Namespace groups files inside the Store.
    # This lambda always puts files under the "filesystem-demo" namespace.
    # _runtime is provided by LangGraph but is not used here.

    # The namespace must be provided as a function that receives the LangGraph Runtime and returns a tuple of strings.
    # Providing namespace is mandatory.
    namespace = lambda _runtime : ("filesystem-demo") # Under which logical group should these files be stored?
)

store_agent = create_deep_agent(
    model="openai:gpt-5.5",

    backend = store_backend,

    # Provide the same store to the graph
    store = store,

    system_prompt="""
    You are a filesystem learning assistant.

    Use the filesystem tools when working
    with stored files.

    Keep your answers short.
    """
)

# ---------------------------------------------------------
# First conversation/thread writes the file
# ---------------------------------------------------------

store_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Create /shared_note.txt containing:\n"
                    "This file can be accessed across threads."
                )
            }
        ]
    },
    config={
        "configurable": {
            "thread_id": "thread-A"
        }
    }
)


# ---------------------------------------------------------
# Different thread reads the same StoreBackend file
# ---------------------------------------------------------

store_result = store_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Read /shared_note.txt and tell me "
                    "what it contains."
                )
            }
        ]
    },
    config = {
        "configurable": {
            "thread_id": "thread-B"
        }
    }
)

print_final_answer(store_result)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n\n======================================")
print("BACKEND SUMMARY")
print("======================================\n")

print(
    """
StateBackend
→ Virtual files
→ Stored in agent/thread state

FilesystemBackend
→ Real files
→ Stored on the local disk

StoreBackend
→ Stored in a LangGraph Store
→ Can be shared across threads
"""
)