import typing

from . import chapmanganato_bs
from . import driver
from . import erai_raws_rss
from . import mangaplus
from . import readmanga_rss
from . import weebcentral


class DriverFactory:
    """
    Produces driver instace by its type
    """
    def __init__(self):
        self.readmanga = readmanga_rss.ReadmangaRss()
        self.chapmanganato = chapmanganato_bs.ChapmanganatoBs()
        self.erai_raws_rss = erai_raws_rss.EraiRawsRss()
        self.mangaplus = mangaplus.Mangaplus()
        self.weebcentral = weebcentral.WeebCentralRss()

    def _map(self) -> typing.Dict[str, driver.Driver]:
        return {
            driver.DriverType.ChapmanganatoBs: self.chapmanganato,
            driver.DriverType.EraiRawsRss: self.erai_raws_rss,
            driver.DriverType.Mangaplus: self.mangaplus,
            driver.DriverType.ReadmangaRss: self.readmanga,
            driver.DriverType.WeebCentralRss: self.weebcentral,
        }

    def find_driver(self, url: str) -> typing.Optional[str]:
        for deriver_type, drv in self._map().items():
            if drv.is_match(url):
                return deriver_type
        return None

    def get(self, driver_type: str) -> driver.Driver:
        drv = self._map().get(driver_type)
        if drv:
            return drv
        raise ValueError(f"Unknown driver {driver_type}")
