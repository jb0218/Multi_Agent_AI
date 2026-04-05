from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.agents.graph import agent
from app.config import settings

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

@router.post("/chat")
async def chat(request: ChatRequest):
    """Chat with AI agent"""
    if not settings.openai_api_key:
        raise HTTPException(400, "OpenAI API key required")
    
    # Simple in-memory config (no Redis needed)
    config = {"configurable": {"thread_id": request.thread_id or "default"}}
    
    try:
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": request.message}]
        }, config)
        
        response = result["messages"][-1]
        return {
            "response": response.content,
            "thread_id": config["configurable"]["thread_id"],
            "tool_calls": getattr(response, "tool_calls", [])
        }
    except Exception as e:
        raise HTTPException(500, f"Agent error: {str(e)}")

@router.get("/test")
async def test():
    """Test agent works"""
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": "Say hello"}]
    })
    return {"status": "ok", "response": result["messages"][-1].content}