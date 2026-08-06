import uuid
import re
from typing import List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver

from app.core.config import settings
from app.services.rag import RAGService
from app.services.tools import create_support_ticket, send_smtp_email

class AgentState(TypedDict):
    """The State schema representing context data passing through the StateGraph."""
    query: str
    context_chunks: List[dict]
    response: Optional[str]
    escalated: bool
    requires_approval: bool
    approved: Optional[bool]
    feedback: Optional[str]
    next_node: Optional[str]

class AgentService:
    """Service layer coordinating Agent workflows using LangGraph StateGraph."""
    
    # Shared checkpointer across separate request lifetimes
    checkpointer = InMemorySaver()

    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service
        self.graph = self._compile_graph()

    def _compile_graph(self) -> StateGraph:
        """Construct, define transitions for, and compile the LangGraph workflow."""
        builder = StateGraph(AgentState)

        # 1. Register nodes
        builder.add_node("coordinator", self._coordinator_node)
        builder.add_node("research", self._research_node)
        builder.add_node("respond", self._respond_node)
        builder.add_node("escalate", self._escalate_node)
        builder.add_node("email_dispatch", self._email_dispatch_node)

        # 2. Set entry point
        builder.set_entry_point("coordinator")

        # 3. Define transitions
        builder.add_conditional_edges(
            "coordinator",
            lambda state: state["next_node"],
            {
                "research": "research",
                "respond": "respond",
                "escalate": "escalate"
            }
        )

        builder.add_edge("research", "respond")

        # Dynamic loop-back checking for Response Node approval checks
        builder.add_conditional_edges(
            "respond",
            self._post_respond_route,
            {
                "respond": "respond",
                "email_dispatch": "email_dispatch",
                "end": END
            }
        )
        builder.add_edge("escalate", END)
        builder.add_edge("email_dispatch", END)

        # Compile with checkpointer and HITL interrupt on response draft review
        return builder.compile(checkpointer=self.checkpointer, interrupt_after=["respond"])

    def _post_respond_route(self, state: AgentState) -> str:
        """Direct transition based on human feedback."""
        if state.get("approved") is False:
            return "respond"
        elif state.get("approved") is True:
            return "email_dispatch"
        return "end"

    async def _coordinator_node(self, state: AgentState) -> dict:
        """Evaluate input to classify routes: research, direct reply, or escalation."""
        query = state["query"].lower()

        # Immediate Escalation keywords
        escalation_keywords = ["refund", "billing", "dispute", "cancel", "chargeback", "credit card"]
        if any(k in query for k in escalation_keywords):
            return {"next_node": "escalate", "escalated": True}

        # Knowledge lookup keywords
        research_keywords = ["docs", "help", "information", "how to", "setup", "configure", "integrate", "smtp", "pinecone", "chroma", "vector"]
        if any(k in query for k in research_keywords):
            return {"next_node": "research"}

        return {"next_node": "respond"}

    async def _research_node(self, state: AgentState) -> dict:
        """Call RAG retrieval to fetch supporting documentation context."""
        query = state["query"]
        chunks = await self.rag_service.retrieve_context(query, top_k=2)
        return {"context_chunks": chunks}

    async def _respond_node(self, state: AgentState) -> dict:
        """Generate response draft. Re-evaluates draft if feedback was provided."""
        query = state["query"]
        context_chunks = state.get("context_chunks", [])
        
        # Check if we are resuming from an operator redraft feedback
        if state.get("approved") is False:
            feedback = state.get("feedback", "")
            new_draft = await self._generate_response(query, context_chunks, feedback=feedback)
            return {
                "response": new_draft,
                "requires_approval": True,
                "approved": None,  # Reset for next review cycle
                "feedback": None
            }

        # Generate original draft response
        draft = await self._generate_response(query, context_chunks)
        return {
            "response": draft,
            "requires_approval": True,
            "approved": None,
            "feedback": None
        }

    async def _escalate_node(self, state: AgentState) -> dict:
        """Handle support escalations and trigger ticket creation tool."""
        query = state["query"]
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', query)
        email = emails[0] if emails else "escalated-customer@aegisai.com"

        ticket = create_support_ticket(email=email, issue=query, priority="high")
        return {
            "escalated": True,
            "response": f"This request requires account/billing access. Escalated to support queue. Support ticket created: {ticket['ticket_id']} (Priority: {ticket['priority']})."
        }

    async def _email_dispatch_node(self, state: AgentState) -> dict:
        """Simulate SMTP dispatch once response has been approved by the operator."""
        query = state["query"]
        response = state["response"] or ""
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', query)
        email = emails[0] if emails else "customer@aegisai.com"

        send_smtp_email(to_email=email, subject="Response from AegisAI Support", body=response)
        return {
            "requires_approval": False
        }

    async def _generate_response(
        self,
        query: str,
        context_chunks: List[dict],
        feedback: Optional[str] = None
    ) -> str:
        """Call LLM or deterministic mock parser depending on environment configs."""
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "dummy_key_replace_in_env":
            if feedback:
                return f"[Mock Redraft] Grounded response to: '{query}' incorporating feedback: '{feedback}'"
            return f"[Mock Draft] Grounded response to: '{query}' based on {len(context_chunks)} source documents."
        else:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import SystemMessage, HumanMessage

            prompt = self.rag_service.build_grounded_prompt(query, context_chunks)
            messages = [SystemMessage(content=prompt)]

            if feedback:
                messages.append(HumanMessage(content=f"Please revise the draft response based on this operator feedback: {feedback}"))

            llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o", temperature=0.2)
            res = await llm.ainvoke(messages)
            return str(res.content)
