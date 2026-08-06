from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_agent_service, get_operator_user
from app.models.user import User
from app.services.agent import AgentService
from app.schemas.agent import AgentRunRequest, AgentApproveRequest, AgentRunResponse
from app.schemas.common import ErrorResponse

router = APIRouter()

@router.post(
    "/run",
    response_model=AgentRunResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse}
    }
)
async def execute_agent_workflow(
    payload: AgentRunRequest,
    current_user: User = Depends(get_operator_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """Start or run the LangGraph workflow on a customer query session."""
    config = {"configurable": {"thread_id": str(payload.thread_id)}}
    
    initial_state = {
        "query": payload.query,
        "context_chunks": [],
        "response": None,
        "escalated": False,
        "requires_approval": False,
        "approved": None,
        "feedback": None
    }
    
    # Run the graph (will pause after respond node due to interrupt_after)
    await agent_service.graph.ainvoke(initial_state, config)
    
    state = agent_service.graph.get_state(config)
    if not state or not state.values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to run agent or resolve state checkpoint."
        )
        
    values = state.values
    return AgentRunResponse(
        thread_id=payload.thread_id,
        response=values.get("response"),
        requires_approval=values.get("requires_approval", False),
        escalated=values.get("escalated", False)
    )

@router.post(
    "/approve",
    response_model=AgentRunResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse}
    }
)
async def resume_agent_approval(
    payload: AgentApproveRequest,
    current_user: User = Depends(get_operator_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """Submit human-in-the-loop approval or revision comments to resume execution."""
    config = {"configurable": {"thread_id": str(payload.thread_id)}}
    
    # Check if thread exists and is currently paused
    current_state = agent_service.graph.get_state(config)
    if not current_state or not current_state.values:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation thread state not found."
        )
        
    # Update state with approval decision and comments
    agent_service.graph.update_state(
        config,
        {
            "approved": payload.approved,
            "feedback": payload.feedback,
            "requires_approval": not payload.approved
        }
    )
    
    # Resume execution by invoking with None
    await agent_service.graph.ainvoke(None, config)
    
    # Get updated state
    updated_state = agent_service.graph.get_state(config)
    if not updated_state or not updated_state.values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to resume agent workflow or resolve state checkpoint."
        )
        
    values = updated_state.values
    return AgentRunResponse(
        thread_id=payload.thread_id,
        response=values.get("response"),
        requires_approval=values.get("requires_approval", False),
        escalated=values.get("escalated", False)
    )
