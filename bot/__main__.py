from telethon import TelegramClient
import asyncio

from . import SESSION_NAME, API_HASH, API_ID, BOT_TOKEN
from .podcastapi import PodcastAPI
from .modules import init


class TelethonManager:
    def __init__(self):
        self.client = TelegramClient(session=SESSION_NAME, api_hash=API_HASH, api_id=API_ID)
        self.cache = dict()
        self.podcastapi = PodcastAPI()

        ## register handlers
        init(self.client, self.cache, self.podcastapi)

        ## register background events

        # Start
        self.client.start(bot_token=BOT_TOKEN)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    TelethonManager()
