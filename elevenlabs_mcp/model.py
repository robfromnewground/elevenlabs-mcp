from pydantic import BaseModel


class McpVoice(BaseModel):
    id: str
    name: str
    category: str


class ConvAiAgentListItem(BaseModel):
    name: str
    agent_id: str


class ConvaiAgent(BaseModel):
    name: str
    agent_id: str
    system_prompt: str
    voice_id: str | None
    language: str
    llm: str
