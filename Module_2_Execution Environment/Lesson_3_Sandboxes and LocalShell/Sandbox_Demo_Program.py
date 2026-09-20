import os
import posixpath
import shlex
import subprocess
import tempfile
import uuid
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends.sandbox import BaseSandbox
from deepagents.backends.protocol import (
    ExecuteResponse,
    FileUploadResponse,
    FileDownloadResponse,
)

from dotenv import load_dotenv


load_dotenv()


# =========================================================
# LESSON 3B — DOCKER SANDBOX
# =========================================================
#
# This is a REAL sandbox example.
#
# The agent does NOT execute Python directly on Windows.
#
# Instead:
#
# Deep Agent
#     ↓
# DockerSandbox
#     ↓
# Docker container
#     ↓
# Python executes inside Linux container
#
# =========================================================


class DockerSandbox(BaseSandbox):

    # =====================================================
    # 1. CREATE DOCKER CONTAINER
    # =====================================================

    def __init__(self):

        self.container_name = (
            f"deep-agent-sandbox-{uuid.uuid4().hex[:8]}"
        )

        print(
            f"\nCreating Docker sandbox: "
            f"{self.container_name}"
        )

        subprocess.run(
            [
                "docker",
                "run",
                "-d",

                # Automatically remove container when stopped
                "--rm",

                "--name",
                self.container_name,

                # Disable network access for this simple demo
                "--network",
                "none",

                # Basic resource limits
                "--memory",
                "256m",

                "--cpus",
                "1",

                "--pids-limit",
                "64",

                # Work inside this directory
                "-w",
                "/workspace",

                # Python Linux image
                "python:3.12-slim",

                # Keep container alive
                "sh",
                "-lc",
                "tail -f /dev/null",
            ],
            check=True,
            capture_output=True,
            text=True,
        )


    # =====================================================
    # 2. SANDBOX ID
    # =====================================================

    @property
    def id(self) -> str:

        return self.container_name


    # =====================================================
    # 3. EXECUTE COMMAND INSIDE SANDBOX
    # =====================================================
    #
    # This is the important sandbox operation.
    #
    # docker exec means:
    #
    # Run this command INSIDE the running container.
    #
    # =====================================================

    def execute(
        self,
        command: str,
        *,
        timeout: int | None = None,
    ) -> ExecuteResponse:

        try:

            # timeout=0 means no timeout
            actual_timeout = (
                None
                if timeout == 0
                else timeout or 120
            )

            result = subprocess.run(
                [
                    "docker",
                    "exec",
                    self.container_name,
                    "sh",
                    "-lc",
                    command,
                ],
                capture_output=True,
                text=True,
                timeout=actual_timeout,
            )

            output = (
                (result.stdout or "")
                +
                (result.stderr or "")
            )

            return ExecuteResponse(
                output=output,
                exit_code=result.returncode,
                truncated=False,
            )

        except subprocess.TimeoutExpired:

            return ExecuteResponse(
                output="Command timed out.",
                exit_code=124,
                truncated=False,
            )


    # =====================================================
    # 4. UPLOAD FILES INTO SANDBOX
    # =====================================================
    #
    # Required by the current BaseSandbox API.
    #
    # Input:
    #
    # [
    #     ("/workspace/file.txt", b"Hello")
    # ]
    #
    # We temporarily save the bytes on the host and then use:
    #
    # docker cp
    #
    # to copy them into the container.
    #
    # =====================================================

    def upload_files(
        self,
        files: list[tuple[str, bytes]],
    ) -> list[FileUploadResponse]:

        responses = []

        for path, content in files:

            # Sandbox paths should be absolute.
            if not path.startswith("/"):

                responses.append(
                    FileUploadResponse(
                        path=path,
                        error="invalid_path",
                    )
                )

                continue


            temp_path = None

            try:

                # -----------------------------------------
                # Make sure parent directory exists
                # inside Docker.
                # -----------------------------------------

                parent = posixpath.dirname(path)

                self.execute(
                    f"mkdir -p {shlex.quote(parent)}"
                )


                # -----------------------------------------
                # Create temporary host file
                # -----------------------------------------

                with tempfile.NamedTemporaryFile(
                    delete=False
                ) as temp_file:

                    temp_file.write(content)

                    temp_path = temp_file.name


                # -----------------------------------------
                # Copy host file → Docker container
                # -----------------------------------------

                result = subprocess.run(
                    [
                        "docker",
                        "cp",
                        temp_path,
                        (
                            f"{self.container_name}:"
                            f"{path}"
                        ),
                    ],
                    capture_output=True,
                    text=True,
                )


                if result.returncode == 0:

                    responses.append(
                        FileUploadResponse(
                            path=path,
                            error=None,
                        )
                    )

                else:

                    responses.append(
                        FileUploadResponse(
                            path=path,
                            error=(
                                result.stderr.strip()
                                or "upload_failed"
                            ),
                        )
                    )


            except Exception as error:

                responses.append(
                    FileUploadResponse(
                        path=path,
                        error=str(error),
                    )
                )


            finally:

                # Delete temporary host file.
                if (
                    temp_path
                    and os.path.exists(temp_path)
                ):

                    os.remove(temp_path)


        return responses


    # =====================================================
    # 5. DOWNLOAD FILES FROM SANDBOX
    # =====================================================
    #
    # Required by BaseSandbox.
    #
    # Uses:
    #
    # docker cp
    #
    # Container → temporary host location
    #
    # =====================================================

    def download_files(
        self,
        paths: list[str],
    ) -> list[FileDownloadResponse]:

        responses = []


        for path in paths:

            if not path.startswith("/"):

                responses.append(
                    FileDownloadResponse(
                        path=path,
                        content=None,
                        error="invalid_path",
                    )
                )

                continue


            try:

                with tempfile.TemporaryDirectory() as temp_dir:

                    destination = (
                        Path(temp_dir)
                        / "downloaded_file"
                    )


                    # -------------------------------------
                    # Copy Docker file → temporary host file
                    # -------------------------------------

                    result = subprocess.run(
                        [
                            "docker",
                            "cp",
                            (
                                f"{self.container_name}:"
                                f"{path}"
                            ),
                            str(destination),
                        ],
                        capture_output=True,
                        text=True,
                    )


                    if result.returncode != 0:

                        responses.append(
                            FileDownloadResponse(
                                path=path,
                                content=None,
                                error="file_not_found",
                            )
                        )

                        continue


                    # -------------------------------------
                    # Check if requested path was directory
                    # -------------------------------------

                    if destination.is_dir():

                        responses.append(
                            FileDownloadResponse(
                                path=path,
                                content=None,
                                error="is_directory",
                            )
                        )

                        continue


                    # -------------------------------------
                    # Read downloaded bytes
                    # -------------------------------------

                    content = destination.read_bytes()


                    responses.append(
                        FileDownloadResponse(
                            path=path,
                            content=content,
                            error=None,
                        )
                    )


            except Exception as error:

                responses.append(
                    FileDownloadResponse(
                        path=path,
                        content=None,
                        error=str(error),
                    )
                )


        return responses


    # =====================================================
    # 6. DESTROY SANDBOX
    # =====================================================

    def close(self):

        print(
            f"\nDestroying Docker sandbox: "
            f"{self.container_name}"
        )

        subprocess.run(
            [
                "docker",
                "rm",
                "-f",
                self.container_name,
            ],
            capture_output=True,
            text=True,
        )


# =========================================================
# CREATE THE SANDBOX
# =========================================================

sandbox = DockerSandbox()


try:

    # =====================================================
    # CREATE DEEP AGENT
    # =====================================================
    #
    # Since DockerSandbox implements BaseSandbox,
    # Deep Agents gets filesystem functionality plus
    # the execute capability.
    #
    # =====================================================

    agent = create_deep_agent(

        model="openai:gpt-5.5",

        backend=sandbox,

        system_prompt="""
        You are a simple Python coding assistant.

        You are working inside an isolated Docker sandbox.

        When asked to create and execute Python code:

        1. Use write_file to create the Python file.

        2. Store files inside /workspace.

        3. Use execute to run the Python file.

        4. Read the execution output.

        5. Keep your final answer short.
        """
    )


    # =====================================================
    # GIVE AGENT A TASK
    # =====================================================

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Create a Python file at "
                        "/workspace/calculate.py. "
                        "The program should calculate "
                        "the sum of numbers from 1 to 10 "
                        "and print the result. "
                        "Then execute the program and "
                        "tell me the output."
                    )
                }
            ]
        }
    )


    # =====================================================
    # SHOW TOOL CALLS
    # =====================================================

    print(
        "\n========== SANDBOX TOOL CALLS ==========\n"
    )

    for message in result["messages"]:

        if (
            hasattr(message, "tool_calls")
            and message.tool_calls
        ):

            for tool_call in message.tool_calls:

                print(
                    f"Tool: {tool_call['name']}"
                )

                print(
                    f"Arguments: {tool_call['args']}"
                )

                print("-" * 50)


    # =====================================================
    # PRINT FINAL AGENT ANSWER
    # =====================================================

    print(
        "\n========== FINAL ANSWER ==========\n"
    )


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


    # =====================================================
    # DIRECTLY VERIFY SANDBOX
    # =====================================================
    #
    # This confirms:
    #
    # - Current directory is /workspace
    # - Python exists inside Docker
    # - calculate.py exists inside Docker
    # - calculate.py produces 55
    #
    # =====================================================

    print(
        "\n========== DIRECT DOCKER CHECK ==========\n"
    )


    check = sandbox.execute(
        "pwd && "
        "python --version && "
        "echo '--- calculate.py ---' && "
        "cat /workspace/calculate.py && "
        "echo '\n--- result ---' && "
        "python /workspace/calculate.py"
    )


    print(check.output)


finally:

    # =====================================================
    # ALWAYS CLEAN UP
    # =====================================================

    sandbox.close()