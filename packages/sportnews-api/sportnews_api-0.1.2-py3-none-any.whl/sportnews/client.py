import requests
from typing import Optional, List, Dict, Any
from datetime import datetime
from .exceptions import SportNewsAPIError
from .models import NewsArticle

class SportNewsAPI:
    """Client for interacting with the Sport News API."""
    
    VALID_LANGUAGES = ['en', 'fr', 'es', 'it', 'de']
    
    def __init__(self, api_key: str, base_url: str = "https://api.sportnews.com/v1"):
        """Initialize the Sport News API client."""
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        })

    def get_latest_news(
        self,
        limit: int = 10,
        language: Optional[str] = None,
        sport: Optional[str] = None
    ) -> List[NewsArticle]:
        """Retrieve the latest sports news articles."""
        if language and language not in self.VALID_LANGUAGES:
            raise ValueError(f"Invalid language code. Must be one of: {', '.join(self.VALID_LANGUAGES)}")

        endpoint = f"{self.base_url}/news"
        params = {
            'size': min(limit, 100),
            'page': 1
        }
        
        if language:
            params['language'] = language
        if sport:
            params['sport'] = sport

        response = self._make_request('GET', endpoint, params=params)
        return [NewsArticle.from_dict(item) for item in response['items']]

    def search_news(
        self,
        query: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        language: Optional[str] = None,
        sport: Optional[str] = None,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        """Search for news articles with specific criteria."""
        if language and language not in self.VALID_LANGUAGES:
            raise ValueError(f"Invalid language code. Must be one of: {', '.join(self.VALID_LANGUAGES)}")

        endpoint = f"{self.base_url}/news/search"
        params = {
            'query': query,
            'page': page,
            'size': size
        }

        if language:
            params['language'] = language
        if sport:
            params['sport'] = sport
        if from_date:
            params['from_date'] = from_date.isoformat()
        if to_date:
            params['to_date'] = to_date.isoformat()

        response = self._make_request('GET', endpoint, params=params)
        response['items'] = [NewsArticle.from_dict(item) for item in response['items']]
        return response

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an HTTP request to the API."""
        try:
            response = self.session.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SportNewsAPIError(f"API request failed: {str(e)}")