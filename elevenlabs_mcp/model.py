from pydantic import BaseModel


class McpVoice(BaseModel):
    id: str
    name: str
    category: str
