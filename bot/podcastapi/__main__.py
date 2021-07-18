from . import PodcastAPI
import sys


async def main():
    query = " ".join(sys.argv[1:]).strip(" \n\r\t")
    if not query:
        return

    p = PodcastAPI()
    r = await p.search_feeds(query)

    feed_id = r["feeds"][0]["id"]
    r = await p.get_episodes(feed_id)

    import pprint
    pprint.pprint(r)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
