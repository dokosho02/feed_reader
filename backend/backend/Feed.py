import asyncio
import aiohttp
import feedparser

async def get_feed_async(feed_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(feed_url) as response:
            if response.status == 200:
                data = await response.text()
                feed = feedparser.parse(data)
                return feed
            else:
                raise Exception(f"Error fetching feed: {response.status}")

async def main():
    url = "http://www.solidot.org/index.rss"
    try:
        entries = await get_feed_entries_async(url)
        if entries and entries.entries:
            print(entries.entries[0].title)
        else:
            print("No entries found in the feed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
