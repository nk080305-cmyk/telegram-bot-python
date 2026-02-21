# Car Search Telegram Bot

## Overview
This bot helps users find cars for sale by allowing them to search through various listings within Telegram.

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/nk080305-cmyk/telegram-bot-python.git
   cd telegram-bot-python
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up the Telegram Bot:**
   - Create a new bot by chatting with [BotFather](https://telegram.me/botfather) on Telegram.
   - Save the token provided by BotFather.
4. **Configure the bot:**
   - Create a `.env` file from the example:
     ```bash
     cp .env.example .env
     ```
   - Replace `your_bot_token_here` with the token from BotFather.
5. **Run the bot:**
   ```bash
   python bot.py
   ```
6. **Run tests:**
   ```bash
   pytest test_bot.py -v
   ```

## Docker Deployment

Build and run with a single command:

```bash
cp .env.example .env          # add your API_TOKEN
docker compose up --build -d  # build image and start in background
```

Stop the bot:

```bash
docker compose down
```

## Features
- Multi-step conversation: budget → previous owners → brand → recommendations
- Budget filtering with used-car discount (15 % per extra owner, capped at 75 %)
- Case-insensitive brand matching
- Input validation with helpful error messages
- `/help`, `/start`, `/restart`, `/cancel` commands

## Usage
- Start the bot by sending `/start` or type `/help` to see all available commands.
- Follow the prompts to search for cars.

## Current Status / Текущий этап

### ✅ Completed
- Consolidated all three bot implementations into a single `bot.py` using `pyTelegramBotAPI`
- Conversation flow: budget → number of previous owners → car brand → recommendations
- Input validation: budget must be a positive integer; owner count must be a non-negative integer
- Car catalogue with price data for 10 brands (Toyota, BMW, Mercedes, Audi, Honda, Hyundai, Volkswagen, Ford, Mazda, Renault)
- Budget filtering: only shows models the user can afford
- Used-car discount: 15 % price reduction per previous owner when filtering (capped at 75 %)
- Case-insensitive brand matching: "bmw", "BMW", "Bmw" all resolve to BMW correctly
- API token loaded from `.env` file via `python-dotenv`
- `/cancel`, `/restart`, `/help` commands supported
- Unit tests (`test_bot.py`) covering all recommendation logic paths
- Docker deployment via `Dockerfile` + `docker-compose.yml`

### ⬜ Pending
- Integration with a real car listings database or external API

## Contributing
Feel free to open issues and submit pull requests to enhance the bot!