# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference: Common Commands

```bash
# Development environment
make start-dev-env           # Start PostgreSQL and Redis for local development
make down-dev-env            # Stop services

# Running the application
make run-bot                 # Start Telegram bot (polling mode)
make run-jobs                # Start background job worker

# Code quality checks (run before submitting PRs)
make flake8-check            # Run flake8 linter
make mypy-check              # Run type checker
make tests                   # Run test suite

# Run a single test
. ./tests/init_env.sh && python -m pytest tests/path/to/test.py::test_name -v
```

## Project Architecture

### Overview
A Telegram bot that notifies users about new manga chapters. The system has three main components:

1. **Telegram Bot** (`manga_notify/bot/`) - Interactive Telegram bot using aiogram
2. **Feed Processing** (`manga_notify/feed_processing/`) - Parses manga feeds and detects new chapters
3. **Background Jobs** (`manga_notify/jobs/`) - Async job queue using arq (Redis-based)

### Run Modes
The application supports different execution modes via `python -m manga_notify <mode>`:
- `bot` - Polling mode (default Telegram bot)
- `bot-webhook` - Webhook mode for production (sets Telegram webhook)
- `jobs` - Background worker that runs scheduled jobs (feed parsing, message sending)
- `send_message` - One-off command to send message to user

### Drivers (Feed Parsers)
Located in `manga_notify/drivers/`. Each driver handles a specific manga source:
- **RSS-based**: `mangasee_rss.py`, `readmanga_rss.py`, `erai_raws_rss.py`, `weebcentral.py`
- **BeautifulSoup-based**: `mangakakalot_bs.py`, `chapmanganato_bs.py`, `sovet_romantica_bs.py`, `animejoy_bs.py`
- **Special protocol**: `mangaplus/` (Google's MangaPlus protobuf API)

The `driver.py` defines the Driver base class. Each driver implements:
- `is_match(url)` - Checks if URL matches this source
- `feed_type()` - Returns driver identifier string
- `parse(feed_data)` - Fetches latest chapters and returns `ParsingResult` with new items

### Feed Processing Pipeline
`feed_processing/feed_processor.py` orchestrates the parsing flow:
1. Selects appropriate driver based on feed URL
2. Calls driver's `parse()` method
3. Converts new chapters to `feed_message.Message` objects
4. Sends messages to all subscribed channels (currently only Telegram)
5. Updates stored feed metadata (etag, timestamps, etc.)

### Database
- PostgreSQL with migrations in `postgres/migrations/`
- SQL queries in `manga_notify/database/sql/` (used with aiosql)
- Two main storage modules:
  - `feed_storage.py` - Stores feed metadata and chapter history
  - `user_storage.py` - Stores user subscriptions and preferences

### Bot: Command Flows
- `basic_commands.py` - `/start`, `/help`, `/list` commands
- `subscription_flow.py` - Subscribe/unsubscribe flows (conversational)
- `mal_search_flow.py` - MyAnimeList search integration

Uses FSM (Finite State Machine) with Redis storage for managing conversation state.

### Settings & Configuration
- `settings.py` - Pydantic settings with environment variable support
- Required env vars: `TG_TOKEN`, `PARSING_INTERVAL` (in minutes)
- Optional: Redis credentials, PostgreSQL connection string, webhook config, erai_raws token, HTTP timeout

## Development Guidelines

### Adding a New Manga Source
1. Create a new driver in `manga_notify/drivers/` (follow existing drivers as template)
2. Implement the `Driver` interface
3. Register in `driver_factory.py` - add entry to `_DRIVERS`
4. Add driver type to `DriverType` enum in `driver.py`

### Database Migrations
Use yandex-pgmigrate (already in dev dependencies):
1. Create migration file in `postgres/migrations/` with naming: `V###__description.sql`
2. Run: `python -m yandex_pgmigrate migrate --target-version <VERSION>`

### Testing
- Tests mirror source structure under `tests/` directory
- Use `aioresponses` for mocking HTTP requests
- Use `pytest-asyncio` for async test fixtures
- Initialize test environment with: `. ./tests/init_env.sh`

### Type Checking
Full mypy coverage expected. Pay attention to:
- Optional types for nullable values
- Async function return types
- Type hints in driver implementations

## Async Architecture Notes
The entire codebase is async-first:
- Bot uses aiogram's async handlers
- All driver parsing is async (HTTP requests)
- Database operations via asyncpg
- Job queue is async via arq
- Use `asyncio.gather()` for parallel operations, avoid blocking calls

## Known Integration Points
- **arq**: Redis-backed task queue for background jobs. Jobs defined in `manga_notify/jobs/`. Cron schedule calculated dynamically in `gen_minutes()`.
- **aiogram**: Telegram bot framework. Routers define command handlers, FSM for conversation state.
- **aiosql**: SQL queries loaded from `.sql` files in `database/sql/`.
- **pydantic**: Data validation for driver results and configuration.
