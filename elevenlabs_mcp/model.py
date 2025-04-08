from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Literal, Any


class McpVoice(BaseModel):
    id: str
    name: str
    category: str
    fine_tuning_status: Optional[Dict] = None
    llm: str


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


class ConversationListItem(BaseModel):
    agent_id: str
    conversation_id: str
    start_time_unix_secs: int
    call_duration_secs: int
    message_count: int
    status: Literal['in-progress', 'processing', 'done', 'failed']
    call_successful: Optional[Literal['success', 'failure', 'unknown']] = None
    agent_name: str | None


class ListConversationsResponse(BaseModel):
    conversations: List[ConversationListItem]
    has_more: bool
    next_cursor: str | None


class ToolCall(BaseModel):
    request_id: str
    tool_name: str
    params_as_json: str
    tool_has_been_called: bool
    type: Optional[str] = None


class ToolResult(BaseModel):
    request_id: str
    tool_name: str
    result_value: str
    is_error: bool
    tool_has_been_called: bool
    type: Optional[str] = None


class TranscriptEntry(BaseModel):
    role: Literal['user', 'agent']
    time_in_call_secs: float # API shows integer, but float might be safer
    message: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_results: Optional[List[ToolResult]] = None
    # Skipping feedback, llm_override, conversation_turn_metrics, rag_retrieval_info for now


class ConversationError(BaseModel):
    code: int
    reason: Optional[str] = None


class ConversationMetadata(BaseModel):
    start_time_unix_secs: int
    call_duration_secs: float # API shows integer, but float might be safer
    cost: Optional[int] = None
    error: Optional[ConversationError] = None
    main_language: Optional[str] = None
    # Skipping deletion_settings, feedback, auth_method, charging, phone_call, rag_usage etc.


class AgentAnalysis(BaseModel):
    call_successful: Literal['success', 'failure', 'unknown']
    transcript_summary: str
    # Skipping evaluation_criteria_results, data_collection_results for now


class ConversationDetails(BaseModel):
    agent_id: str
    conversation_id: str
    status: Literal['in-progress', 'processing', 'done', 'failed']
    transcript: List[TranscriptEntry]
    metadata: ConversationMetadata
    analysis: Optional[AgentAnalysis] = None
    # Skipping conversation_initiation_client_data
