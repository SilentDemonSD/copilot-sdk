# Error Handling Patterns

Handle errors gracefully in your Copilot SDK applications.

> **Runnable example:** [recipe/error_handling.py](recipe/error_handling.py)
>
> ```bash
> cd recipe && pip install -r requirements.txt
> python error_handling.py
> ```

## Example scenario

You need to handle various error conditions like connection failures, timeouts, and invalid responses.

## Basic try-except

```python
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

        await session.send_and_wait({"prompt": "Hello!"})

        if response:
            print(response)

        await session.destroy()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await client.stop()


asyncio.run(main())
```

## Handling specific error types

```python
try:
    await client.start()
except FileNotFoundError:
    print("Copilot CLI not found. Please install it first.")
except ConnectionError:
    print("Could not connect to Copilot CLI server.")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Timeout handling

The SDK's `send_and_wait()` method accepts a timeout parameter:

```python
import asyncio

session = await client.create_session()

try:
    # Wait with timeout (30 seconds)
    await session.send_and_wait({"prompt": "Complex question..."}, timeout=30.0)
    print("Response received")
except asyncio.TimeoutError:
    print("Request timed out")
```

## Aborting a request

```python
import asyncio

session = await client.create_session()


async def abort_after_delay():
    await asyncio.sleep(5)
    await session.abort()
    print("Request aborted")


# Start the abort task
abort_task = asyncio.create_task(abort_after_delay())

# Send a long request
await session.send({"prompt": "Write a very long story..."})
```

## Graceful shutdown

```python
import asyncio
import signal

client = CopilotClient()


async def shutdown():
    print("\nShutting down...")
    errors = await client.stop()
    if errors:
        print(f"Cleanup errors: {errors}")


# Handle Ctrl+C gracefully
loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(shutdown()))
```

## Best practices

1. **Always clean up**: Use try-finally to ensure `await client.stop()` is called
2. **Handle connection errors**: The CLI might not be installed or running
3. **Use timeouts**: Pass timeout to `send_and_wait()` for long-running requests
4. **Log errors**: Capture error details for debugging
5. **Use async patterns**: The SDK is fully async - use `asyncio.run()` as entry point
