from fastapi import FastAPI
from schema import MCPMessage
import uvicorn
import requests

app = FastAPI()
MCP_CLIENT_ENDPOINT = "http://localhost:8001/respond"

@app.post("/chat")
async def receive_message(msg: MCPMessage):
    print(f"[Server] Received: {msg.role} -> {msg.content}")

    response = requests.post(MCP_CLIENT_ENDPOINT, json=msg.dict())
    return response.json()

if __name__ == "__main__":
    uvicorn.run(app, port=8000)