import unittest
from pathlib import Path
import sys
import os
from datetime import datetime, timedelta

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from sportnews import SportNewsAPI, SportNewsAPIError

class TestSportNewsAPI(unittest.TestCase):
    def setUp(self):
        """Initialize the API client before each test execution."""
        self.api = SportNewsAPI(
            api_key='sk_pro_5d24de40-c254-464c-85aa-09a3aeeb616e',
            base_url='https://fastapi-app-505935705476.northamerica-northeast1.run.app/api/v1'  # Update this to your actual API endpoint
        )

    def test_get_latest_news(self):
        """Verify the retrieval and structure of latest news articles."""
        news = self.api.get_latest_news(limit=10, language='en')
        
        self.assertLessEqual(len(news), 10)
        
        if news:
            article = news[0]
            self.assertIsInstance(article.title, str)
            self.assertIsInstance(article.published, datetime)
            self.assertIsInstance(article.description, str)
            self.assertIsInstance(article.language, str)
            self.assertIsInstance(article.sport, str)
            
            print(f"\nTest Article Details:")
            print(f"Title: {article.title}")
            print(f"Published: {article.published}")
            print(f"Description: {article.description}")
            print(f"Sport: {article.sport}")
            print(f"Language: {article.language}")

    def test_search_news(self):
        """Verify the search functionality with specific criteria."""
        search_results = self.api.search_news(
            query="football",
            from_date=datetime.utcnow() - timedelta(days=7),
            language="en",
            size=5
        )
        
        self.assertIn('total', search_results)
        self.assertIn('items', search_results)
        self.assertLessEqual(len(search_results['items']), 5)

    def test_language_validation(self):
        """Verify handling of invalid language parameters."""
        with self.assertRaises(ValueError) as context:
            self.api.get_latest_news(language='invalid_language')
        
        self.assertIn("Invalid language code", str(context.exception))

    def test_connection_error(self):
        """Verify proper handling of connection errors."""
        invalid_api = SportNewsAPI(
            api_key='sk_pro_5d24de40-c254-464c-85aa-09a3aeeb616e',
            base_url='http://invalid-url'
        )
        
        with self.assertRaises(SportNewsAPIError):
            invalid_api.get_latest_news()

if __name__ == '__main__':
    unittest.main()