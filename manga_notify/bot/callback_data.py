import dataclasses
import json
import typing

from aiogram import types


@dataclasses.dataclass
class CallbackData:
    method: str
    payload: dict


    def serialize(self) -> str:
        return f'{self.method}\n{json.dumps(self.payload)}'


def _parse_method(raw: str) -> typing.Optional[str]:
    pos = raw.find('\n')
    if not pos:
        return None
    return raw[:pos]


def create_matcher(target: str) -> typing.Callable[[types.CallbackQuery], bool]:
    def matcher(callback_query: types.CallbackQuery) -> bool:
        method = _parse_method(callback_query.data)
        return method == target
    return matcher


def parse(raw: str) -> CallbackData:
    pos = raw.find('\n')
    if not pos:
        raise ValueError(f"Callback data has wrong format: {raw}")
    return json.loads(raw[pos+1:])
