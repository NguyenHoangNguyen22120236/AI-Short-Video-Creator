from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()

serp_api_key = os.getenv("SERP_API_KEY")

class SerpAPIGoogleTrend():
    def __init__(self):
        pass
    
    def get_trending_searches(self, location):
        params = {
            "engine": "google_trends_trending_now",
            "geo": location,
            "api_key": serp_api_key
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        trending_searches = results["trending_searches"]
        
        return trending_searches
    