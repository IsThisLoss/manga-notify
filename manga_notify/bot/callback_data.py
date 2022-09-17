import base64
import dataclasses
import json
import typing
import functools

from aiogram import types


def _encode(data: str) -> str:
    return base64.b64encode(data.encode()).decode()


def _decode(raw: str) -> str:
    return base64.b64decode(raw.encode()).decode()


class Methods:
    UNSUBSCRIBE = 'unsubscribe'
    LATER = 'LATER'


@dataclasses.dataclass
class CallbackData:
    method: str
    payload: dict

    def serialize(self) -> str:
        return _encode(f'{self.method}\n{json.dumps(self.payload)}')


# FIXME: Cache parsed data because
# we have to parse is twice.
# To match callback and inside callback
@functools.lru_cache(maxsize=10)
def parse(raw: str) -> typing.Optional[CallbackData]:
    decoded = _decode(raw)
    pos = decoded.find('\n')
    if not pos:
        return None
    method = decoded[:pos]
    payload = json.loads(decoded[pos+1:])
    return CallbackData(
        method=method,
        payload=payload,
    )


def create_matcher(
    target: str,
) -> typing.Callable[[types.CallbackQuery], bool]:
    def matcher(callback_query: types.CallbackQuery) -> bool:
        data = parse(callback_query.data)
        if not data:
            return False
        return data.method == target
    return matcher
