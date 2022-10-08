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


async def main():
    parser = argparse.ArgumentParser('Manga notify')
    parser.add_argument('mode', metavar='MODE', help='Run mode: bot or jobs')
    args = parser.parse_args()

    if args.mode == 'bot':
        await bot.dp.start_polling()
    elif args.mode == 'jobs':
        await jobs.run()
    else:
        logging.fatal(f'Unknown mode: {args.mode}')
        exit(1)


if __name__ == '__main__':
    asyncio.run(main())
