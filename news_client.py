# news_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NewsAPIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("NEWSAPI_KEY")
        if not self.api_key:
            raise ValueError("API key is missing.")
        self.base_url = "https://newsapi.org/v2"

    def get_top_headlines(self, **params):
        return self._make_request("/top-headlines", params)

    def get_everything(self, **params):
        return self._make_request("/everything", params)

    def _make_request(self, endpoint, params):
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": self.api_key}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "message": str(e), "articles": []}
