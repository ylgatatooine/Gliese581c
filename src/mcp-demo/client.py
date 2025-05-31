from fastapi import FastAPI, Request
from pydantic import BaseModel
from schema import MCPMessage, MCPResponse
import openai
import uvicorn
import os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")


SYSTEM_PROMPT = """
You are a helpful agent. You must always respond in this exact JSON format:

{
  "thought": "<your thinking here>",
  "action": "<the action you plan to take>",
  "observation": "<what you learned or result of the action>"
}

Do not use code blocks. Do not return any extra explanation. Only return the JSON object.
"""


@app.post("/respond")
async def respond(request: Request):
    msg = MCPMessage(**(await request.json()))
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": msg.role, "content": msg.content}
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.7,
    )

    raw_reply = completion.choices[0].message.content
    print(f"[Client] Raw LLM Output:\n{raw_reply}")

    try:
        parsed = eval(raw_reply)
        return MCPResponse(**parsed)
    except Exception as e:
        return {"error": "Failed to parse LLM response", "raw": raw_reply}

if __name__ == "__main__":
    uvicorn.run(app, port=8001)