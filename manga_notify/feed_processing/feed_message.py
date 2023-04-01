import typing

from ..drivers import driver
from ..channels import channel


DEFAULT_CHUNK_SIZE = 10


class FeedMessage(channel.Message):
    def __init__(
            self,
            parsed_items: typing.List[driver.ParsingItem],
            mal_url: typing.Optional[str],
    ):
        self._parsed_items = parsed_items
        self._mal_url = mal_url

    def _serialize_one(self, parsed_item: driver.ParsingItem) -> str:
        return f'Новый выпуск [{parsed_item.name}]({parsed_item.link})'

    def _serialize_many(
        self,
        parsed_items: typing.List[driver.ParsingItem],
    ) -> str:
        result = 'Несколько новых выпусков:\n'
        for parsed_item in parsed_items:
            result += f'[{parsed_item.name}]({parsed_item.link})\n'
        return result

    def serialize(self) -> str:
        if len(self._parsed_items) == 1:
            return self._serialize_one(self._parsed_items[0])
        return self._serialize_many(self._parsed_items)

    def extra(self) -> dict:
        if self._mal_url:
            return {'mal_url': self._mal_url}
        return {}


def create_messages(
        parsed_items: typing.List[driver.ParsingItem],
        mal_url: typing.Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> typing.List[channel.Message]:
    if not parsed_items:
        return []
    result: typing.List[channel.Message] = []
    chunk_size = min(chunk_size, len(parsed_items))
    for i in range(0, len(parsed_items), chunk_size):
        result.append(FeedMessage(
            parsed_items[i:i+chunk_size],
            mal_url,
        ))
    return result
