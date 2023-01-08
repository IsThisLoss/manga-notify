import typing

from . import driver
from . import animejoy_bs
from . import mangakakalot_bs
from . import mangasee_rss
from . import readmanga_rss
from . import sovet_romantica_bs


class DriverFactory:
    """
    Produces driver instace by its type
    """
    def __init__(self):
        self.mangasee = mangasee_rss.MangaseeRss()
        self.mangakakalot = mangakakalot_bs.MangakakalotBs()
        self.readmanga = readmanga_rss.ReadmangaRss()
        self.sovet_romantica = sovet_romantica_bs.SovetRomanticaBs()
        self.animejoy = animejoy_bs.AnimeJoyBs()

    def _map(self) -> typing.Dict[str, driver.Driver]:
        return {
            driver.DriverType.MangakakalotBs: self.mangakakalot,
            driver.DriverType.MangaseeRss: self.mangasee,
            driver.DriverType.ReadmangaRss: self.readmanga,
            driver.DriverType.SovetRomanticaBs: self.sovet_romantica,
            driver.DriverType.AnimeJoyBs: self.animejoy,
        }

    def find_driver(self, url: str) -> typing.Optional[str]:
        for deriver_type, drv in self._map().items():
            if drv.is_match(url):
                return deriver_type
        return None

    def get(self, driver_type: str) -> driver.Driver:
        driver = self._map().get(driver_type)
        if driver:
            return driver
        raise ValueError(f"Unknow driver {driver_type}")
