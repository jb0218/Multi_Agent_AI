from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.config import settings

app = FastAPI(
    title="🤖 AI Agent API", 
    version="1.0.0",
    description="LangGraph + OpenAI + Postgres Tools"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api", tags=["agent"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Agent API Ready! 🚀",
        "endpoints": {
            "health": "/health",
            "chat": "/api/chat",
            "docs": "/docs"
        },
        "openai_ready": bool(settings.openai_api_key)
    }

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": str(settings.DATABASE_URL)[:40] + "..." if settings.DATABASE_URL else "none",
        "openai_key": bool(settings.openai_api_key),
        "timestamp": "2024"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,  # Dev mode
        log_level="info"
    )