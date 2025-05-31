from pydantic import BaseModel
from typing import Literal

class MCPMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class MCPResponse(BaseModel):
    thought: str
    action: str
    observation: str