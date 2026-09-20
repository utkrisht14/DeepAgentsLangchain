# Module 2 — Execution Environment
## Lesson 3 — Sandboxes and LocalShell

> **Goal:** Understand the difference between isolated sandbox execution and running shell commands directly on the local machine.

---

# 1. What Is a Sandbox?

A **sandbox** is an isolated environment where a Deep Agent can work with files and run commands without getting unrestricted access to the host machine.

Mental model:

```text
Deep Agent
    ↓
Sandbox Backend
    ↓
Isolated Environment
    ↓
Files + Commands
```

This is useful when the agent needs to:

```text
Run Python scripts
Execute shell commands
Install temporary packages
Process files
Test generated code
```

---

# 2. Why Use a Sandbox?

Running agent-generated commands directly on the host machine can be risky.

A sandbox adds isolation.

```text
Agent command
    ↓
Sandbox
    ↓
Limited environment
```

instead of:

```text
Agent command
    ↓
My actual computer
```

This is the safer choice for production or untrusted code execution.

---

# 3. Sandbox Backend

A sandbox-capable backend implements command execution in addition to filesystem operations.

It can support tools such as:

```text
read_file
write_file
edit_file
glob
grep
execute
```

The important extra capability is:

```text
execute
```

which lets the agent run shell commands.

---

# 4. What Is LocalShellBackend?

`LocalShellBackend` gives the Deep Agent:

```text
Real local filesystem access
+
Local shell command execution
```

Example idea:

```python
from deepagents.backends import LocalShellBackend

backend = LocalShellBackend(
    root_dir="./workspace"
)
```

Now the agent can run commands directly on the host operating system.

---

# 5. LocalShell Is NOT a Sandbox

This is the most important point.

```text
LocalShellBackend
≠
Sandbox
```

Commands run directly on the host machine using the current user's permissions.

So the agent may potentially:

```text
Read local files
Modify local files
Run programs
Install packages
Start processes
Access secrets
Use network commands
```

There is no real isolation.

---

# 6. Sandbox vs LocalShell

| Sandbox | LocalShellBackend |
|---|---|
| Isolated environment | Runs on host machine |
| Safer for generated code | Higher risk |
| Good for production | Better for trusted local development |
| Limits damage to host | Commands can affect real system |
| `execute` runs inside sandbox | `execute` runs locally |

---

# 7. The `execute` Tool

When the backend supports the sandbox execution protocol, Deep Agents can expose:

```text
execute
```

Example:

```text
User asks agent to analyze data
        ↓
Agent writes analyze.py
        ↓
Agent calls execute
        ↓
python analyze.py
        ↓
Command output returned
```

If the backend does not support execution, `execute` cannot successfully run shell commands.

---

# 8. LocalShell Example Flow

```text
Deep Agent
    ↓
execute("python script.py")
    ↓
LocalShellBackend
    ↓
Operating System Shell
    ↓
script.py runs on my computer
```

This is powerful, but it must be trusted.

---

# 9. Sandbox Example Flow

```text
Deep Agent
    ↓
execute("python script.py")
    ↓
Sandbox Backend
    ↓
Isolated Container / VM / Remote Sandbox
    ↓
script.py runs there
```

The host machine remains separated from the execution environment.

---

# 10. `root_dir`

`LocalShellBackend` can use a working directory:

```python
backend = LocalShellBackend(
    root_dir="./workspace"
)
```

Filesystem tools can be rooted there.

However, this does **not** make shell execution secure.

Shell commands are still executed on the host machine.

---

# 11. Security Warning

With `LocalShellBackend`, an agent may execute arbitrary commands.

Therefore it should only be used when:

```text
I trust the agent
I trust the input
The environment is controlled
The machine contains no sensitive data
```

For risky workflows, use an isolated sandbox instead.

---

# 12. HITL with LocalShell

A strong safeguard is Human-in-the-Loop.

Example:

```text
Agent wants to run command
        ↓
Human reviews
        ↓
Approve / Reject
```

HITL is helpful, but it does not replace sandbox isolation.

---

# 13. When Should I Use Each?

Use a sandbox when:

```text
Running generated code
Handling untrusted input
Production execution
Need isolation
```

Use LocalShell when:

```text
Local development
Trusted personal coding assistant
Controlled environment
I intentionally want access to local tools/files
```

---

# 14. Simple Mental Model

```text
Sandbox
=
Agent gets its own computer-like workspace
```

```text
LocalShell
=
Agent is allowed to use my computer's shell
```

That is the easiest distinction to remember.

---

# 15. Five Things to Remember

1. **A sandbox isolates file and command execution from the host machine.**
2. **A sandbox-capable backend provides the `execute` capability.**
3. **`LocalShellBackend` runs commands directly on the local host.**
4. **LocalShell is powerful but not isolated or safe for untrusted workloads.**
5. **Use sandboxing for production or generated/untrusted code whenever possible.**

---

# 16. One-Line Summary

> **A sandbox gives the Deep Agent an isolated place to run commands, while LocalShellBackend gives the agent direct access to the host machine's filesystem and shell.**

---

# References

- Deep Agents LocalShellBackend  
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/backends/local_shell.py

- Deep Agents Backend Protocol  
  https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/backends/protocol.py

- Deep Agent from Scratch — Sandbox  
  https://github.com/langchain-ai/docs/blob/main/src/oss/langchain/deep-agent-from-scratch.mdx
