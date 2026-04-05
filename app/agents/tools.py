from langchain_core.tools import tool
import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from tenacity import retry, stop_after_attempt, wait_exponential
from fastapi import HTTPException
from app.config import settings

# Direct engine - NO dependency issues
DB_URL = str(settings.DATABASE_URL).replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(DB_URL, echo=False)

BLOCKED_WORDS = {"DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE", "TRUNCATE"}

@tool
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
async def query_database(sql: str) -> str:
    """
    Safely execute READ-ONLY SQL queries against the agent database.
    
    Args:
        sql: SQL SELECT query only (writes auto-blocked)
    
    Returns:
        JSON array of query results
    
    Examples:
        "SELECT * FROM information_schema.tables LIMIT 5"
        "SELECT current_database()"
        "SELECT version()"
    """
    sql_upper = sql.strip().upper()
    
    # Block dangerous operations
    if any(word in sql_upper for word in BLOCKED_WORDS):
        return "❌ ERROR: Write operations blocked for safety"
    
    # Ensure it's a SELECT
    if not sql_upper.startswith("SELECT"):
        return "❌ ERROR: Only SELECT queries allowed"
    
    async with engine.connect() as conn:
        conn = await conn.execution_options(isolation_level="AUTOCOMMIT")
        result = await conn.execute(text(sql))
        rows = [dict(row._mapping) for row in result.mappings()]
        return str(rows)

@tool
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
async def fetch_api(url: str) -> str:
    """
    Fetch data from public HTTP/HTTPS APIs.
    
    Args:
        url: Complete URL (https:// or http://)
    
    Returns:
        Response body as string
    
    Examples:
        "https://jsonplaceholder.typicode.com/posts/1"
        "https://api.github.com/users/octocat"
        "https://httpbin.org/json"
    """
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text