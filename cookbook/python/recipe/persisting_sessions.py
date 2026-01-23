#!/usr/bin/env python3
"""
Session Persistence - Demonstrates saving and resuming conversation sessions.

This example shows how to create sessions with custom IDs and resume them
later, allowing conversations to persist across application restarts.
"""

import asyncio

from copilot import CopilotClient


async def main():
    client = CopilotClient()
    await client.start()

    # Create session with a memorable ID
    session = await client.create_session(
        {
            "session_id": "user-123-conversation",
        }
    )

    await session.send_and_wait({"prompt": "Let's discuss TypeScript generics"})
    print(f"Session created: {session.session_id}")

    # Destroy session but keep data on disk
    await session.destroy()
    print("Session destroyed (state persisted)")

    # Resume the previous session
    resumed = await client.resume_session("user-123-conversation")
    print(f"Resumed: {resumed.session_id}")

    await resumed.send_and_wait({"prompt": "What were we discussing?"})

    # Get session message history
    messages = await resumed.get_messages()
    print(f"Session has {len(messages)} messages")

    # List all available sessions
    sessions = await client.list_sessions()
    print("Available sessions:")
    for s in sessions:
        print(f"  - {s['session_id']}: {s.get('summary', 'No summary')}")

    await resumed.destroy()

    # Delete session permanently (removes all data from disk)
    await client.delete_session("user-123-conversation")
    print("Session deleted permanently")

    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
