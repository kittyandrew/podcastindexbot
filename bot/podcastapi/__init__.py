from dotenv import load_dotenv
import aiohttp
import asyncio
import hashlib
import logging
import time
import os

from .cache import lru_cache


load_dotenv()


class PodcastAPI:
    URL = "https://api.podcastindex.org/api/1.0"

    def __init__(self):
        self.key = os.getenv("API_KEY")
        self.secret = os.getenv("API_SECRET")

        self.agent = os.getenv("USER_AGENT")

        self.headers = {
            "X-Auth-Key": self.key,
            "User-Agent": self.agent,
            "X-Auth-Date": None,
            "Authorization": None,
        }

    def prepare_headers(self):
        epoch = str(int(time.time()))

        self.headers["X-Auth-Date"] = epoch
        self.headers["Authorization"] = hashlib.sha1((self.key + self.secret + epoch).encode()).hexdigest()

    @lru_cache(maxsize=8192)
    async def get(self, url: str):
        self.prepare_headers()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as r:
                return await r.json()

    async def search_feeds(self, query: str):
        logging.info("Query: %s", query)
        return await self.get(f"{self.URL}/search/byterm?q={query}")

    async def get_podcast(self, feed_id: int):
        return await self.get(f"{self.URL}/podcasts/byfeedid?id={feed_id}")

    async def get_episodes(self, feed_id: int):
        return await self.get(f"{self.URL}/episodes/byfeedid?id={feed_id}")

