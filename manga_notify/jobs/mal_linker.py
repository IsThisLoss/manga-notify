import logging

from .. import dependencies

from ..drivers import driver_factory
from ..external import mal


MAL_QUERY_LIMIT = 1


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
            try:
                mal_items = await my_anime_list.find(
                    feed_type=driver.feed_type(),
                    title=feed.get_title(),
                    limit=MAL_QUERY_LIMIT,
                )
                if not mal_items:
                    continue
                await db.feeds.update_mal_url(
                    feed.get_id(),
                    mal_items[0].link,
                )
            except Exception as _:  # noqa
                logging.exception(
                    'Cannot find mal title for %s',
                    feed.get_title(),
                )
