# flake8: noqa: E402
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

import signal

import asyncio
import argparse

from . import dependencies


async def run_bot():
    from . import bot

    def _sig_handler(*args):
        bot.dp.stop_polling()

    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, _sig_handler)

    await bot.dp.start_polling()


async def run_job():
    from . import jobs
    await jobs.run()


async def main():
    parser = argparse.ArgumentParser('Manga notify')
    parser.add_argument('mode', metavar='MODE', help='Run mode: bot or jobs')
    parser.add_argument('--user-id', nargs='?', help='UserId for send_message mode')
    parser.add_argument('--message', nargs='?', help='message for send_message mode')
    args = parser.parse_args()

    try:
        await dependencies.on_startup()
    except Exception as _:
        logging.exception('Failed to initialize dependencies')
        exit(2)

    try:
        if args.mode == 'bot':
            await run_bot()
        elif args.mode == 'jobs':
            await run_job()
        elif args.mode == 'send_message':
            from . import custom
            await custom.send_message(args.user_id, args.message)
        else:
            logging.fatal(f'Unknown mode: {args.mode}')
            exit(1)
    finally:
        await dependencies.on_shutdown()


if __name__ == '__main__':
    asyncio.run(main())
