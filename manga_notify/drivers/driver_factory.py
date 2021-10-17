import typing

from . import driver
from . import mangakakalot_bs
from . import mangasee_rss


class DriverFactory:
    """
    Produces driver instace by its type
    """

    def list(self) -> typing.List[str]:
        return [
            driver.DriverType.MangaseeRss,
            driver.DriverType.MangakakalotBs,
        ]

    def get(self, driver_type: str) -> driver.Driver:
        if driver_type == driver.DriverType.MangaseeRss:
            return mangasee_rss.MangaseeRss()
        if driver_type == driver.DriverType.MangakakalotBs:
            return mangakakalot_bs.MangakakalotBs()
        raise ValueError(f"Unknow driver {driver_type}")
