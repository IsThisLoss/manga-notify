import typing

from . import driver
from . import mangakakalot_bs
from . import mangasee_rss
from . import readmanga_rss


class DriverFactory:
    """
    Produces driver instace by its type
    """
    def __init__(self):
        self.mangasee = mangasee_rss.MangaseeRss()
        self.mangakakalot = mangakakalot_bs.MangakakalotBs()
        self.readmanga = readmanga_rss.ReadmangaRss()

    def _map(self) -> typing.Dict[str, driver.Driver]:
        return {
            driver.DriverType.MangaseeRss: self.mangasee,
            driver.DriverType.MangakakalotBs: self.mangakakalot,
            driver.DriverType.ReadmangaRss: self.readmanga,
        }

    def find_driver(self, url: str) -> typing.Optional[str]:
        for deriver_type, drv in self._map().items():
            if drv.is_match(url):
                return deriver_type
        return None

    def get(self, driver_type: str) -> driver.Driver:
        if driver_type == driver.DriverType.MangaseeRss:
            return mangasee_rss.MangaseeRss()
        if driver_type == driver.DriverType.MangakakalotBs:
            return mangakakalot_bs.MangakakalotBs()
        if driver_type == driver.DriverType.ReadmangaRss:
            return readmanga_rss.ReadmangaRss()
        raise ValueError(f"Unknown driver {driver_type}")
