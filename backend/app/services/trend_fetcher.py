from app.third_party.serp_api_google_trend import SerpAPIGoogleTrend

class TrendFetcherService:
    def __init__(self):
        pass

    async def fetch_trends(self, location):
        serp_api_google_trend = SerpAPIGoogleTrend()
        data = await serp_api_google_trend.get_trending_searches(location)
        
        return [trend["query"] for trend in data]