from ..database import feed_storage


def build_feed_info(feed: feed_storage.FeedData) -> str:
    result = ''

    title = feed.get_title() or 'Неизвестный тайтол'
    result += f'{title}:\n'
    result += f'- `{feed.get_url()}`'

    mal_url = feed.get_mal_url()
    if mal_url:
        result += f'\n- [MAL]({mal_url})'

    result += '\n'
    return result
