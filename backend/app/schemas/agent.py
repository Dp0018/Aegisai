import uuid
from typing import Optional
from pydantic import BaseModel, Field

class AgentRunRequest(BaseModel):
    """Pydantic request body for starting or executing an agent run."""
    query: str = Field(..., description="The query string to send to the agent workflow")
    thread_id: uuid.UUID = Field(..., description="Unique thread ID for tracking conversation checkpoint memory")

class AgentApproveRequest(BaseModel):
    """Pydantic request body for human-in-the-loop review approval or redraft feedback."""
    thread_id: uuid.UUID = Field(..., description="The ID of the paused thread to resume")
    approved: bool = Field(..., description="Set to true if approved, false if feedback/redraft is requested")
    feedback: Optional[str] = Field(None, description="Optional revision comments if approved is false")

class AgentRunResponse(BaseModel):
    """Pydantic response schema summarizing the current state of the agent run."""
    thread_id: uuid.UUID = Field(..., description="Thread ID session index")
    response: Optional[str] = Field(None, description="The drafted response or status message")
    requires_approval: bool = Field(False, description="Flag indicating if the draft is currently paused for operator approval")
    escalated: bool = Field(False, description="Flag indicating if the query was escalated")
