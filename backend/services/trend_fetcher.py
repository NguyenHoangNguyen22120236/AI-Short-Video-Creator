from third_party.serp_api_google_trend import SerpAPIGoogleTrend

class TrendFetcherService:
    def __init__(self, location):
        self.location = location

    def fetch_trends(self):
        serp_api_google_trend = SerpAPIGoogleTrend()
        data = serp_api_google_trend.get_trending_searches(self.location)
        
        return data