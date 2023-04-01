# flake8: noqa: E402
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

import asyncio
import argparse

from . import bot
from . import jobs
from . import custom


async def main():
    parser = argparse.ArgumentParser('Manga notify')
    parser.add_argument('mode', metavar='MODE', help='Run mode: bot or jobs')
    parser.add_argument('--user-id', nargs='?', help='UserId for send_message mode')
    parser.add_argument('--message', nargs='?', help='message for send_message mode')
    args = parser.parse_args()

    if args.mode == 'bot':
        await bot.dp.start_polling()
    elif args.mode == 'jobs':
        await jobs.run()
    elif args.mode == 'send_message':
        await custom.send_message(args.user_id, args.message)
    else:
        logging.fatal(f'Unknown mode: {args.mode}')
        exit(1)


if __name__ == '__main__':
    asyncio.run(main())
