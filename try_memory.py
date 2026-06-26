import asyncio

from sciagents.application.conversation_service.generate_response import generate_response

async def main():
    tid="v2-test-1"
    r1= await generate_response("curie", "My name is omar. what did you discover ?", tid)
    print("R1:", r1, "\n")
    r2=await generate_response("curie", "what is my name ?", tid)
    print("R2:",r2)

asyncio.run(main())