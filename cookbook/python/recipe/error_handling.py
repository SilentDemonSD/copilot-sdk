#!/usr/bin/env python3
"""
Error Handling Patterns - Demonstrates error handling with the Copilot SDK.

This example shows how to properly handle errors when working with the
async Copilot SDK, including connection failures, timeouts, and cleanup.
"""

import asyncio

from copilot import CopilotClient


async def main():
    client = CopilotClient()
    response = None

    def handle_message(event):
        nonlocal response
        if event.type == "assistant.message":
            response = event.data.content

    try:
        await client.start()

        session = await client.create_session()
        session.on(handle_message)

        # Use send_and_wait for simple request-response pattern
        await session.send_and_wait({"prompt": "Hello!"})

        if response:
            print(response)

        await session.destroy()

    except FileNotFoundError:
        print("Error: Copilot CLI not found. Please install it first.")
    except ConnectionError:
        print("Error: Could not connect to Copilot CLI server.")
    except asyncio.TimeoutError:
        print("Error: Request timed out.")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
