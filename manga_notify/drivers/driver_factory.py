import typing

from . import driver
# from . import animejoy_bs
from . import chapmanganato_bs
from . import erai_raws_rss
from . import mangakakalot_bs
from . import mangasee_rss
from . import readmanga_rss
from . import sovet_romantica_bs
from . import mangaplus


class DriverFactory:
    """
    Produces driver instace by its type
    """
    def __init__(self):
        self.mangasee = mangasee_rss.MangaseeRss()
        self.mangakakalot = mangakakalot_bs.MangakakalotBs()
        self.readmanga = readmanga_rss.ReadmangaRss()
        self.sovet_romantica = sovet_romantica_bs.SovetRomanticaBs()
        # FIXME: Now it is protected by cloudflare
        # self.animejoy = animejoy_bs.AnimeJoyBs()
        self.chapmanganato = chapmanganato_bs.ChapmanganatoBs()
        self.erai_raws_rss = erai_raws_rss.EraiRawsRss()
        self.mangaplus = mangaplus.Mangaplus()

    def _map(self) -> typing.Dict[str, driver.Driver]:
        return {
            driver.DriverType.MangakakalotBs: self.mangakakalot,
            driver.DriverType.MangaseeRss: self.mangasee,
            driver.DriverType.ReadmangaRss: self.readmanga,
            driver.DriverType.SovetRomanticaBs: self.sovet_romantica,
            # FIXME: Now it is protected by cloudflare
            # driver.DriverType.AnimeJoyBs: self.animejoy,
            driver.DriverType.ChapmanganatoBs: self.chapmanganato,
            driver.DriverType.EraiRawsRss: self.erai_raws_rss,
            driver.DriverType.Mangaplus: self.mangaplus,
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
