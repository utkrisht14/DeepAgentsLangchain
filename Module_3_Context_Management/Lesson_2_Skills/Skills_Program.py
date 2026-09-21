from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from dotenv import load_dotenv

load_dotenv()

agent = create_deep_agent(
    model="openai:gpt-5.5",
    backend = FilesystemBackend(
        root_dir=".",
        virtual_mode=True
    ),
    skills = ["./skills"]
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": """
                    Write an email to my manager saying that
                    I have completed the API implementation
                    and will start testing tomorrow.
                """
            }
        ]
    }
)

print(result["messages"][-1].content)