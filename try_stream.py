import asyncio
from sciagents.application.conversation_service.generate_response import stream_response


async def main():
    async for token in stream_response("feynman", "What is light?", "stream-v2-1"):
        print(token, end="", flush=True)
    print()


asyncio.run(main())