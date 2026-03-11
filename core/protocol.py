from pydantic import BaseModel, Field
from typing import Literal, Optional, Any
from enum import Enum
from datetime import datetime
import uuid

class AgentRole(str, Enum):
    ARCHITECT = "architect"
    CODER = "coder"
    DEBUGGER = "debugger"
    REVIEWER = "reviewer"

class ToolType(str, Enum):
    CODE_EXEC = "code_execution"
    FILE_OPS = "file_operations"

class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ToolCall(BaseModel):
    tool_type: ToolType
    parameters: dict[str, Any]
    call_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class ToolResult(BaseModel):
    call_id: str
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float

class ThoughtProcess(BaseModel):
    observation: str
    reasoning: str
    plan: list[str]
    next_action: str

class AgentResponse(BaseModel):
    thought_process: ThoughtProcess
    tool_calls: list[ToolCall] = Field(default_factory=list)
    message: str
    requires_human_input: bool = False
    confidence: float = Field(ge=0.0, le=1.0)

class AgentConfig(BaseModel):
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: AgentRole
    model: str = "claude-sonnet-4-20250514"
    temperature: float = 0.7
    max_iterations: int = 10
    allowed_tools: list[ToolType]
    system_prompt: str

class AgentState(BaseModel):
    config: AgentConfig
    messages: list[Message] = Field(default_factory=list)
    iteration: int = 0
    status: Literal["idle", "thinking", "executing", "completed", "error"] = "idle"
    result: Optional[str] = None
