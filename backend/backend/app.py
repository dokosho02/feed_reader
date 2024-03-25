from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from .Feed import get_feed_async  # 导入异步函数

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的跨域请求
    allow_credentials=True,
    allow_methods=["GET"],  # 只允许 GET 请求
    allow_headers=["*"],
)

# RSS feed URLs
RSS_FEED_URLS = [
    "http://www.solidot.org/index.rss",
    "https://rsshub.app/huxiu/article",
    "https://rsshub.app/bbc/world-asia",
    "https://feeds.feedblitz.com/baeldung/kotlin",
    "https://rsshub.app/nhk/news_web_easy",
    "https://biz.trans-suite.jp/feed"
]

@app.get('/data')
async def get_feeds():
    all_feeds = []
    for url in RSS_FEED_URLS:
        # 使用 feedparser 获取 RSS 订阅源信息
        feed = await get_feed_async(url)
        all_feeds.append(feed)
    return all_feeds

if __name__ == '__main__':
    asyncio.run(app.run_task())  # 使用 asyncio.run() 运行应用程序
"""
poetry run uvicorn backend.app:app --reload --port 10000
"""