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
   - Update the configuration file with your token.
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
- Basic bot structure created (`bot.py`, `car_bot.py`, `main.py`)
- Conversation flow implemented: budget → number of owners → car brand
- Sample car recommendation logic added (Toyota, BMW, Mercedes, Audi, Honda, Hyundai, Volkswagen, Ford, Mazda, Renault)

### 🔄 In Progress
- Consolidating three bot implementations into a single, clean `bot.py`
- Moving API tokens out of source code and into environment variables (`.env` file)

### ⬜ Pending
- Integration with a real car listings database or external API
- Input validation (e.g., numeric budget, valid owner count)
- Unit tests and integration tests
- Deployment configuration (e.g., Docker, systemd service, or cloud hosting)

## Contributing
Feel free to open issues and submit pull requests to enhance the bot!