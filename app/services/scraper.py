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
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1"
            }
            response = httpx.get(url, headers=headers, follow_redirects=True, timeout=30.0)
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
