from telethon.tl.types import InputMediaDocumentExternal
from telethon.events import StopPropagation
from telethon.tl.custom import Message
from telethon import events, Button
from typing import Union
import logging


Event = Union[Message, events.NewMessage.Event]


async def init(bot, cache, podcastapi):
    @bot.on(events.NewMessage(pattern="/start"))
    async def start_handler(event: Event):
        await event.respond("Hello, I'm your friendly echo bot..")
        raise StopPropagation()

    @bot.on(events.InlineQuery)
    async def inline_handler(event: Event):
        builder = event.builder

        res = []
        query = event.text.strip(" \n\r\t")
        if query:
            res_feed = await podcastapi.search_feeds(query)
            if res_feed["feeds"]:
                episodes = await podcastapi.get_episodes(res_feed["feeds"][0]["id"])
                for ep in episodes["items"][:10]:  # limit to the first 10 for now
                    if ep["enclosureLength"] / 1_000_000 >= 20.0:
                        res.append(builder.article(
                            ep["title"], url = ep["enclosureUrl"],
                            text = f"<b>{ep['title']}</b>\n\n{ep['description']}",
                            parse_mode = "html", link_preview = False,
                            buttons = Button.url("Listen", ep["enclosureUrl"]),
                        ))
                    else:
                        res.append(builder.document(ep["enclosureUrl"], text=ep["title"]))

        await event.answer(res)
