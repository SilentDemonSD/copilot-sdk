#!/usr/bin/env python3
"""
Multiple Sessions - Demonstrates managing multiple independent conversations.

This example shows how to create and manage multiple conversation sessions
simultaneously, each with its own context and history.
"""

import asyncio

from copilot import CopilotClient


async def main():
    client = CopilotClient()
    await client.start()

    # Create multiple independent sessions
    session1 = await client.create_session()
    session2 = await client.create_session()
    session3 = await client.create_session({"model": "claude-sonnet-4"})

    print("Created 3 independent sessions")

    # Each session maintains its own conversation history
    # Send initial context to each session
    await session1.send({"prompt": "You are helping with a Python project"})
    await session2.send({"prompt": "You are helping with a TypeScript project"})
    await session3.send({"prompt": "You are helping with a Go project"})

    print("Sent initial context to all sessions")

    # Follow-up messages stay in their respective contexts
    # Use send_and_wait to ensure each response completes
    await session1.send_and_wait({"prompt": "How do I create a virtual environment?"})
    await session2.send_and_wait({"prompt": "How do I set up tsconfig?"})
    await session3.send_and_wait({"prompt": "How do I initialize a module?"})

    print("Sent follow-up questions to each session")

    # Clean up all sessions
    await session1.destroy()
    await session2.destroy()
    await session3.destroy()
    await client.stop()

    print("All sessions destroyed successfully")


if __name__ == "__main__":
    asyncio.run(main())
