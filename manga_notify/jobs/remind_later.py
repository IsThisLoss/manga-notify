from .. import dependencies


async def job(ctx, user_id: str, message_id: int):
    deps: dependencies.Dependencies = ctx['deps']
    bot = deps.get_bot()
    await bot.send_message(
        user_id,
        'Напоминаю',
        reply_to_message_id=message_id
    )
