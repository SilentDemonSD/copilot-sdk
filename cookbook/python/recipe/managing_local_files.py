#!/usr/bin/env python3
"""
Managing Local Files - Demonstrates using Copilot to organize files.

This example shows how to use the Copilot SDK to intelligently organize
files in a folder based on metadata like file type, creation date, etc.
"""

import asyncio
import os

from copilot import CopilotClient


async def main():
    # Create and start client
    client = CopilotClient()
    await client.start()

    # Create session
    session = await client.create_session()

    # Event handler
    def handle_event(event):
        if event.type == "assistant.message":
            print(f"\nCopilot: {event.data.content}")
        elif event.type == "tool.execution_start":
            print(f"  → Running: {event.data.tool_name}")
        elif event.type == "tool.execution_complete":
            print(f"  ✓ Completed: {event.data.tool_call_id}")

    session.on(handle_event)

    # Ask Copilot to organize files
    # Change this to your target folder
    target_folder = os.path.expanduser("~/Downloads")

    await session.send_and_wait(
        {
            "prompt": f"""
Analyze the files in "{target_folder}" and organize them into subfolders.

1. First, list all files and their metadata
2. Preview grouping by file extension
3. Create appropriate subfolders (e.g., "images", "documents", "videos")
4. Move each file to its appropriate subfolder

Please confirm before moving any files.
"""
        }
    )

    await session.destroy()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
