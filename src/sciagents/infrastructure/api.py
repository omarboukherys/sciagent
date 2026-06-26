from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from sciagents.application.conversation_service.generate_response import generate_response, stream_response
from sciagents.domain.scientist_factory import ScientistFactory

app=FastAPI(title="SciAgents API")

class ChatRequest(BaseModel):
    scientist_id: str
    message: str
    thread_id: str = "default"

class ChatResponse(BaseModel):
    resposnse: str

@app.get("/scientists")
async def list_scientists():
    """Return the list of available scientists ids."""
    return {"scientists": ScientistFactory.get_available_scientists()}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a messaeg to a scientis and get his/ her reply."""
    reply=await generate_response(
        scientist_id=request.scientist_id,
        message=request.message,
        thread_id=request.thread_id,
    )

    return ChatResponse(resposnse=reply)

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """Stream a scientist's reply token-by-token over a WebSocket."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()

            async for token in stream_response(
                scientist_id=data["scientist_id"],
                message=data["message"],
                thread_id=data.get("thread_id", "default"),
            ):
                await websocket.send_json({"token": token})

            await websocket.send_json({"done": True})
    except WebSocketDisconnect:
        pass