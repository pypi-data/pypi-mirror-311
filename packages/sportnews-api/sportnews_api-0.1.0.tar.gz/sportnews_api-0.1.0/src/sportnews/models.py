from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class NewsArticle:
    """Represents a news article from the Sport News API."""
    
    id: str
    title: str
    link: str
    published: datetime
    description: str
    author: str
    language: str
    sport: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NewsArticle':
        """Create a NewsArticle instance from a dictionary."""
        if isinstance(data.get('published'), str):
            data['published'] = datetime.fromisoformat(data['published'].replace('Z', '+00:00'))
        return cls(**data)