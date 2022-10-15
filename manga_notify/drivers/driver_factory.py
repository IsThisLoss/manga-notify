import typing

from . import driver
from . import mangakakalot_bs
from . import sovet_romantica_bs
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
        self.sovet_romantica = sovet_romantica_bs.SovetRomanticaBs()

    def _map(self) -> typing.Dict[str, driver.Driver]:
        return {
            driver.DriverType.MangakakalotBs: self.mangakakalot,
            driver.DriverType.MangaseeRss: self.mangasee,
            driver.DriverType.ReadmangaRss: self.readmanga,
            driver.DriverType.SovetRomanticaBs: self.sovet_romantica,
        }

    def find_driver(self, url: str) -> typing.Optional[str]:
        for deriver_type, drv in self._map().items():
            if drv.is_match(url):
                return deriver_type
        return None

    def get(self, driver_type: str) -> driver.Driver:
        if driver_type == driver.DriverType.MangaseeRss:
            return self.mangasee
        if driver_type == driver.DriverType.MangakakalotBs:
            return self.mangakakalot
        if driver_type == driver.DriverType.ReadmangaRss:
            return self.readmanga
        if driver_type == driver.DriverType.SovetRomanticaBs:
            return self.sovet_romantica
        raise ValueError(f"Unknow driver {driver_type}")
