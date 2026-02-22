# Car Recommendation Telegram Bot 🚗

> **Русский / Russian** — see [Быстрый старт](#быстрый-старт) below.

## Overview

A Telegram bot that helps users find car recommendations based on their budget,
the number of previous owners, and preferred brand.

---

## ⚠️ Security — keep your token private / Безопасность

**Never share your `API_TOKEN` with anyone — including AI assistants.**
Anyone who has your token can fully control your bot.
The token lives only in your local `.env` file, which is listed in `.gitignore`
and is never committed to Git.

---

## Quickstart (English)

### Prerequisites
- Python 3.10+ **or** Docker

### Option A — plain Python (recommended)

```bash
# 1. Clone the repo
git clone https://github.com/nk080305-cmyk/telegram-bot-python.git
cd telegram-bot-python

# 2. Run the interactive setup script
bash setup.sh
```

`setup.sh` will:
- Ask you for your Telegram bot token (get one from [@BotFather](https://t.me/botfather))
- Write it to `.env`
- Install Python dependencies
- Start the bot

### Option B — Docker

```bash
git clone https://github.com/nk080305-cmyk/telegram-bot-python.git
cd telegram-bot-python
cp .env.example .env          # then open .env and paste your token
docker compose up --build -d  # build and run in the background
```

Stop the bot:
```bash
docker compose down
```

### Manual setup (step by step)

1. **Get a bot token** — open Telegram, find [@BotFather](https://t.me/botfather), send `/newbot`, follow the prompts. Copy the token it gives you.
2. **Create `.env`:**
   ```bash
   cp .env.example .env
   # open .env with any text editor and replace "your_bot_token_here"
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run:**
   ```bash
   python bot.py
   ```

---

## Быстрый старт (Русский)

### Требования
- Python 3.10+ **или** Docker

### Вариант А — обычный Python (рекомендуется)

```bash
# 1. Скачать репозиторий
git clone https://github.com/nk080305-cmyk/telegram-bot-python.git
cd telegram-bot-python

# 2. Запустить скрипт установки
bash setup.sh
```

Скрипт сам спросит токен, запишет `.env`, установит зависимости и запустит бота.

### Вариант Б — Docker

```bash
cp .env.example .env          # вставьте токен в файл .env
docker compose up --build -d  # собрать образ и запустить в фоне
```

### Пошагово

1. **Получить токен** — откройте Telegram, найдите [@BotFather](https://t.me/botfather), отправьте `/newbot`, следуйте инструкциям. Скопируйте выданный токен.
2. **Создать `.env`:**
   ```bash
   cp .env.example .env
   # откройте .env любым редактором и замените "your_bot_token_here" на ваш токен
   ```
3. **Установить зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Запустить:**
   ```bash
   python bot.py
   ```

---

## Run tests

```bash
pytest test_bot.py -v
```

---

## Features / Возможности

- Multi-step conversation: budget → previous owners → brand → recommendations
- Budget filtering with used-car discount (15 % per extra owner, capped at 75 %)
- Case-insensitive brand matching (toyota / TOYOTA / Toyota all work)
- Input validation with helpful error messages
- `/help`, `/start`, `/restart`, `/cancel` commands

## Usage

Send `/start` (or `/help`) to the bot in Telegram and follow the prompts.

---

## Current Status / Текущий этап

> **Project stage / Этап проекта: MVP — feature-complete, ready for testing**
>
> The core functionality is fully implemented and covered by automated tests.
> The next step is connecting a live car-listings data source.
>
> **Этап проекта: MVP — базовый функционал реализован, готово к тестированию**
>
> Основной функционал полностью реализован и покрыт автоматическими тестами.
> Следующий шаг — подключение реальной базы данных или внешнего API с объявлениями.

### Roadmap / Дорожная карта

| # | Feature / Функция | Status / Статус |
|---|---|---|
| 1 | Core bot (`bot.py`) with `pyTelegramBotAPI` | ✅ Done |
| 2 | Multi-step conversation: budget → owners → brand | ✅ Done |
| 3 | Car catalogue — 10 brands, budget + owner-count filtering | ✅ Done |
| 4 | Case-insensitive brand matching (`normalize_brand()`) | ✅ Done |
| 5 | Input validation with helpful error messages | ✅ Done |
| 6 | `/help`, `/cancel`, `/restart` commands | ✅ Done |
| 7 | Unit tests (14 tests, all passing) | ✅ Done |
| 8 | Docker deployment (`Dockerfile` + `docker-compose.yml`) | ✅ Done |
| 9 | Interactive `setup.sh` quickstart script | ✅ Done |
| 10 | Integration with a real car-listings database / external API | ⬜ Planned |
| 11 | Inline keyboard buttons for brand selection | ⬜ Planned |
| 12 | Persistent conversation state (Redis / SQLite) | ⬜ Planned |
| 13 | Structured logging | ⬜ Planned |
| 14 | Webhook mode for production | ⬜ Planned |
| 15 | Russian-language bot messages (i18n) | ⬜ Planned |
| 16 | Additional filters: year range and mileage | ⬜ Planned |
| 17 | CI/CD pipeline (GitHub Actions) | ⬜ Planned |

---

## What's next / Что осталось сделать

### 🔴 High priority

1. **Real data source** (replaces the hardcoded catalogue)
   Connect to a live car-listings API or database so prices and
   availability are always up to date.
   *Подключить реальную базу данных или внешний API с актуальными объявлениями.*

2. **Inline keyboard buttons for brand selection**
   Replace free-text brand input with Telegram inline keyboard buttons
   so the user can simply tap a brand name.
   *Заменить ввод марки текстом на кнопки Telegram-клавиатуры.*

3. **Persistent conversation state**
   `user_state` is currently an in-memory dict — all sessions are lost
   on restart.  Replace with SQLite or Redis so conversations survive
   restarts.
   *`user_state` хранится в памяти и теряется при перезапуске.
   Заменить на SQLite или Redis.*

### 🟡 Medium priority

4. **Structured logging**
   Add Python `logging` (or `structlog`) to `bot.py` so errors and
   warnings are captured and easy to diagnose in production.
   *Добавить логирование (`logging` / `structlog`) для отладки в продакшне.*

5. **Webhook mode for production**
   The bot currently uses long-polling (`infinity_polling()`).
   Add an optional webhook mode (e.g. via `aiohttp` or `Flask`) for
   lower latency and better scalability.
   *Добавить режим webhook для продакшн-развёртывания.*

6. **Russian-language bot messages (i18n)**
   The README is bilingual, but the bot only speaks English.
   Add locale detection (or a `/lang` command) and translate all
   bot messages to Russian.
   *Добавить русскоязычные ответы бота (определение языка или команда `/lang`).*

### 🟢 Low priority

7. **Additional search filters**
   Extend the conversation with optional year-range and maximum-mileage
   filters so users can narrow down results further.
   *Добавить фильтры по году выпуска и максимальному пробегу.*

8. **CI/CD pipeline (GitHub Actions)**
   Add a workflow that runs `pytest` automatically on every push /
   pull request.
   *Настроить GitHub Actions: запуск тестов при каждом push / pull request.*

## Contributing

Feel free to open issues and submit pull requests!
