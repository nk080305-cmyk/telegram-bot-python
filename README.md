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

**🟢 Bot is operational / Бот работает**

### ✅ Completed
- Single consolidated `bot.py` using `pyTelegramBotAPI`
- Conversation flow with input validation
- Car catalogue — 10 brands, budget + owner-count filtering
- Case-insensitive brand matching via `normalize_brand()`
- `/help`, `/cancel`, `/restart` commands
- Unit tests (14 tests, all passing)
- Docker deployment (`Dockerfile` + `docker-compose.yml`)
- Interactive `setup.sh` quickstart script

## Contributing

Feel free to open issues and submit pull requests!
