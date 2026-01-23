# Working with Multiple Sessions

Manage multiple independent conversations simultaneously.

> **Runnable example:** [recipe/multiple_sessions.py](recipe/multiple_sessions.py)
>
> ```bash
> cd recipe && pip install -r requirements.txt
> python multiple_sessions.py
> ```

## Example scenario

You need to run multiple conversations in parallel, each with its own context and history.

## Python

```python
import asyncio
from copilot import CopilotClient


async def main():
    client = CopilotClient()
    await client.start()

    # Create multiple independent sessions
    session1 = await client.create_session()
    session2 = await client.create_session()
    session3 = await client.create_session({"model": "claude-sonnet-4"})

    # Each session maintains its own conversation history
    await session1.send({"prompt": "You are helping with a Python project"})
    await session2.send({"prompt": "You are helping with a TypeScript project"})
    await session3.send({"prompt": "You are helping with a Go project"})

    # Follow-up messages stay in their respective contexts
    await session1.send_and_wait({"prompt": "How do I create a virtual environment?"})
    await session2.send_and_wait({"prompt": "How do I set up tsconfig?"})
    await session3.send_and_wait({"prompt": "How do I initialize a module?"})

    # Clean up all sessions
    await session1.destroy()
    await session2.destroy()
    await session3.destroy()
    await client.stop()


asyncio.run(main())
```

## Custom session IDs

Use custom IDs for easier tracking:

```python
session = await client.create_session({
    "session_id": "user-123-chat",
})

print(session.session_id)  # "user-123-chat"
```

## Listing sessions

```python
# List all available sessions
sessions = await client.list_sessions()
for session_info in sessions:
    print(f"Session: {session_info['session_id']}")
    print(f"  Modified: {session_info['modified_time']}")
```

## Deleting sessions

```python
# Delete a specific session permanently
await client.delete_session("user-123-chat")
```

## Use cases

- **Multi-user applications**: One session per user
- **Multi-task workflows**: Separate sessions for different tasks
- **A/B testing**: Compare responses from different models
