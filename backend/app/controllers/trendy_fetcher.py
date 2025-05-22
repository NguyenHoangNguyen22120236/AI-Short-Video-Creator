from services.trend_fetcher import TrendFetcherService

class TrendyFetcherController:
    def __init__(self, ):
        pass

    async def fetch_trends(self, location):
        try:
            trend_fetcher_service = TrendFetcherService()
            trendy_topics = trend_fetcher_service.fetch_trends(location=location)
        except Exception as e:
            print(f"Error fetching trends: {e}")
            return {'error': 'Failed to fetch trendy topics'}, 500
        
        return {'trendy_topics': trendy_topics}, 200

    