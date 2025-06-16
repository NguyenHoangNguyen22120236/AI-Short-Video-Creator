from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.controllers.trendy_fetcher import TrendyFetcherController

trendy_fetcher_router = APIRouter()
trendy_fetcher_controller = TrendyFetcherController()

@trendy_fetcher_router.get("/fetch_trends")
async def fetch_trends(
    location: str = Query("US", description="Location for trending topics")
):
    trendy_topics, status_code = await trendy_fetcher_controller.fetch_trends(location=location)
    
    return JSONResponse(content=trendy_topics, status_code=status_code)