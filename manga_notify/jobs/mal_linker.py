from .. import dependencies

from ..drivers import driver_factory
from ..external import mal


async def job(ctx: dict):
    """
    Tries to find MAL page for feeds
    """

    deps: dependencies.Dependencies = ctx['deps']
    drivers = driver_factory.DriverFactory()
    my_anime_list = mal.MyAnimeList()

    async with deps.get_db() as db:
        feeds = await db.feeds.find_without_mal_link()
        for feed in feeds:
            driver = drivers.get(feed.get_driver())
            mal_url = await my_anime_list.find(
                driver.feed_type(),
                feed.get_title(),
            )
            if mal_url:
                await db.feeds.update_mal_url(feed.get_id(), mal_url)
