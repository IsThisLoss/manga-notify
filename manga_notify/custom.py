import logging
import typing

from . import dependencies


async def send_message(
    user_id: typing.Optional[str],
    message: typing.Optional[str],
):
    if not user_id or not message:
        logging.critical(
            'Wrong usage, user_id and message should ne passed',
        )
        exit(1)
    deps = dependencies.get()
    queues = await deps.get_queues()
    await queues.enqueue_job(
        'send_telegram_message',
        user_id,
        message,
        extra={},
    )
    logging.info('Done')
