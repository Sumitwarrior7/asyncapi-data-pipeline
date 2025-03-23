import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import chromadb
import feedparser

# Constants
GITHUB_ORG = "https://api.github.com/orgs/asyncapi/repos"
BLOG_URL = "https://www.asyncapi.com/blog"  # Example, replace with actual RSS feed if available'
BLOG_RSS_URL = "https://www.asyncapi.com/rss.xml"

def fetch_blogs():
    """Fetch AsyncAPI blogs from the RSS feed and scrape full content from each blog link."""
    feed = feedparser.parse(BLOG_RSS_URL)
    blog_data = []
    
    for entry in feed.entries:
        blog_content = scrape_blog_content(entry.link)
        blog_data.append({
            "id": entry.id if "id" in entry else entry.link,
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "content": blog_content  # Scraped full content
        })
    
    return blog_data

def scrape_blog_content(url):
    """Scrape the full blog content from the given URL."""
    try:
        response = requests.get(url, timeout=10)  # Fetch the page
        response.raise_for_status()  # Raise error if request fails
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract blog content (modify selector based on actual HTML structure)
        article = soup.find("article")  # Common tag for blog content
        if not article:
            article = soup.find("div", class_="post-content")  # Another possible structure
        
        return article.get_text(strip=True) if article else "Content not found"
    
    except requests.RequestException as e:
        return f"Error fetching content: {e}"

