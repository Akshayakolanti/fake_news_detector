import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def scrape_news_url(url):
    """
    Extract title and main article body text from a provided news URL.
    """
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        res = requests.get(url, headers=headers, timeout=8)
        
        if res.status_code != 200:
            return {'error': f'HTTP Error {res.status_code}: Could not fetch page'}
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Remove script and style tags
        for script in soup(['script', 'style', 'header', 'footer', 'nav']):
            script.decompose()
            
        # Extract title
        title = ""
        if soup.find('h1'):
            title = soup.find('h1').get_text().strip()
        elif soup.title:
            title = soup.title.get_text().strip()
            
        # Extract body paragraphs
        paragraphs = soup.find_all('p')
        body_text = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30])
        
        domain = urllib.parse.urlparse(url).netloc
        
        if not body_text and not title:
            return {'error': 'Could not extract meaningful news content from this page.'}
            
        full_content = f"{title}. {body_text}" if title else body_text
        
        return {
            'url': url,
            'domain': domain,
            'title': title or 'Extracted News Article',
            'text': full_content[:3000],  # cap at 3k chars
            'word_count': len(full_content.split())
        }
    except Exception as e:
        return {'error': f'Failed to scrape URL: {str(e)}'}

if __name__ == '__main__':
    res = scrape_news_url("https://en.wikipedia.org/wiki/Artificial_intelligence")
    print("Scraped title:", res.get('title'))
