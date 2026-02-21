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
   - Create a `.env` file in the project root with your token:
     ```
     API_TOKEN=your_bot_token_here
     ```
5. **Run the bot:**
   ```bash
   python bot.py
   ```

## Features
- Search for available cars based on user input.
- Receive real-time notifications for new car listings.
- Filter results based on user preferences.

## Usage
- Start the bot by sending `/start` command. 
- Follow the prompts to search for cars.

## Current Status / Текущий этап

### ✅ Completed
- Consolidated all three bot implementations into a single `bot.py` using `pyTelegramBotAPI`
- Conversation flow: budget → number of previous owners → car brand → recommendations
- Input validation: budget must be a positive integer; owner count must be a non-negative integer
- Car catalogue with price data for 10 brands (Toyota, BMW, Mercedes, Audi, Honda, Hyundai, Volkswagen, Ford, Mazda, Renault)
- Budget filtering: only shows models the user can afford
- Used-car discount: 15 % price reduction per previous owner when filtering
- API token loaded from `.env` file via `python-dotenv`
- `/cancel` and `/restart` commands supported

### ⬜ Pending
- Integration with a real car listings database or external API
- Unit tests and integration tests
- Deployment configuration (e.g., Docker, systemd service, or cloud hosting)

## Contributing
Feel free to open issues and submit pull requests to enhance the bot!