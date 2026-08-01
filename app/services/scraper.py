import httpx
from bs4 import BeautifulSoup
import re

class ScraperService:
    def __init__(self):
        pass

    def crawl_website(self, url: str) -> str:
        """Crawl a website and extract raw text."""
        try:
            # Use httpx for a lightweight request
            with httpx.Client(follow_redirects=True, timeout=10.0) as client:
                response = client.get(url)
                response.raise_for_status()
                
                # Parse HTML with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script, style, header, footer, and nav elements
                for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
                    script_or_style.extract()
                
                # Extract text
                text = soup.get_text(separator=' ')
                
                # Clean up whitespace
                text = re.sub(r'\s+', ' ', text).strip()
                return text
        except Exception as e:
            raise ValueError(f"Failed to crawl website {url}: {str(e)}")

scraper_service = ScraperService()
