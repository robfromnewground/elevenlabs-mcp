from pydantic import BaseModel


class McpVoice(BaseModel):
    id: str
    name: str
    voice_id: str
    category: str
