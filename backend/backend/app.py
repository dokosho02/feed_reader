from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from .Feed import get_feed_async

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow cross-origin requests from all sources
    allow_credentials=True,
    allow_methods=["GET"],  # only GET requests are allowed
    allow_headers=["*"],
)

# RSS feed URLs
RSS_FEED_URLS = [
    "http://www.solidot.org/index.rss",
    "https://rsshub.app/huxiu/article",
    "https://rsshub.app/bbc/world-asia",
    "https://feeds.feedblitz.com/baeldung/kotlin",
    "https://rsshub.app/nhk/news_web_easy",
    "https://biz.trans-suite.jp/feed",
    "http://www.ithome.com/rss/",
    "https://chinadigitaltimes.net/chinese/feed",
    "https://rsshub.app/bing",
    "https://www.ruanyifeng.com/blog/atom.xml",

]

@app.get('/data')
async def get_feeds():
    all_feeds = []
    for url in RSS_FEED_URLS:
        feed = await get_feed_async(url)
        all_feeds.append(feed)
    return all_feeds

if __name__ == '__main__':
    asyncio.run(app.run_task())
"""
poetry run uvicorn backend.app:app --reload --port 10000
"""