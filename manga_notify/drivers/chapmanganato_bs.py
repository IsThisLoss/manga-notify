from . import mangakakalot_bs


class ChapmanganatoBs(mangakakalot_bs.MangakakalotBs):
    def is_match(self, url: str) -> bool:
        return 'chapmanganato' in url

    def chapter_list_class(self) -> str:
        return 'panel-story-chapter-list'
