import os
import telebot
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise ValueError("API_TOKEN environment variable is not set.")

bot = telebot.TeleBot(API_TOKEN)

# Conversation states
BUDGET, OWNERS, BRAND, FEEDBACK = range(4)

# In-memory state storage: {chat_id: {'state': int, 'budget': int, 'owners': int}}
user_state: dict = {}

# Feedback storage: list of {'chat_id': int, 'rating': int, 'brand': str}
user_feedback: list = []

# Car catalogue: brand -> list of (model, price)
CAR_CATALOGUE: dict = {
    'Toyota':      [('Corolla', 20000), ('Camry', 28000), ('Hilux', 35000)],
    'BMW':         [('3 Series', 45000), ('X5', 65000), ('Z4', 55000)],
    'Mercedes':    [('C-Class', 50000), ('E-Class', 65000), ('G-Class', 130000)],
    'Audi':        [('A4', 42000), ('Q5', 55000), ('A6', 60000)],
    'Honda':       [('Civic', 22000), ('Accord', 30000), ('HR-V', 27000)],
    'Hyundai':     [('Elantra', 18000), ('Tucson', 26000), ('Santa Fe', 34000)],
    'Volkswagen':  [('Golf', 25000), ('Passat', 33000), ('Tiguan', 36000)],
    'Ford':        [('Focus', 21000), ('Mustang', 38000), ('F-150', 40000)],
    'Mazda':       [('Mazda3', 22000), ('CX-5', 30000), ('MX-5', 28000)],
    'Renault':     [('Clio', 15000), ('Captur', 20000), ('Koleos', 27000)],
}

BRANDS_LIST = ', '.join(CAR_CATALOGUE.keys())


def normalize_brand(text: str) -> str:
    """Return the catalogue key that matches *text* case-insensitively, or title-case fallback."""
    return next(
        (k for k in CAR_CATALOGUE if k.upper() == text.upper()),
        text.title(),
    )


def get_recommendations(budget: int, owners: int, brand: str) -> str:
    """Return a recommendation message based on budget, owners and brand."""
    models = CAR_CATALOGUE.get(brand)
    if not models:
        return (
            f"Sorry, I don't have listings for '{brand}'.\n"
            f"Available brands: {BRANDS_LIST}"
        )

    # Filter by budget; for used cars (owners > 1) apply a 15 % discount per extra owner
    # Cap at 75 % so prices never become unrealistically low
    discount = min(max(0, (owners - 1) * 0.15), 0.75)
    affordable = [
        (model, int(price * (1 - discount)))
        for model, price in models
        if price * (1 - discount) <= budget
    ]

    if not affordable:
        min_price = min(int(price * (1 - discount)) for _, price in models)
        return (
            f"No {brand} models fit your budget of ${budget:,}.\n"
            f"The cheapest option starts at ~${min_price:,}."
        )

    lines = '\n'.join(f"• {model} — ~${price:,}" for model, price in affordable)
    return f"Recommended {brand} models within ${budget:,}:\n{lines}"


# ── Handlers ──────────────────────────────────────────────────────────────────

@bot.message_handler(commands=['start', 'restart'])
def cmd_start(message):
    chat_id = message.chat.id
    user_state[chat_id] = {'state': BUDGET}
    bot.send_message(
        chat_id,
        "Welcome to the Car Recommendation Bot! 🚗\n\n"
        "What is your budget in USD? (enter a number, e.g. 30000)\n"
        "Type /cancel at any time to stop."
    )


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(
        message.chat.id,
        "🚗 *Car Recommendation Bot — commands:*\n\n"
        "/start — begin a new car search\n"
        "/restart — start over at any point\n"
        "/cancel — cancel the current search\n"
        "/skip — skip the feedback rating step\n"
        "/help — show this message\n\n"
        "During a search you will be asked for:\n"
        "1️⃣ Budget (USD)\n"
        "2️⃣ Number of previous owners\n"
        f"3️⃣ Brand — choose from: {BRANDS_LIST}\n"
        "4️⃣ Rating (1–5 stars) for the recommendations",
        parse_mode='Markdown',
    )


@bot.message_handler(commands=['cancel'])
def cmd_cancel(message):
    chat_id = message.chat.id
    user_state.pop(chat_id, None)
    bot.send_message(chat_id, "Conversation cancelled. Type /start to begin again.")


@bot.message_handler(commands=['skip'])
def cmd_skip(message):
    chat_id = message.chat.id
    data = user_state.get(chat_id)
    if data and data.get('state') == FEEDBACK:
        user_state.pop(chat_id, None)
        bot.send_message(chat_id, "Feedback skipped. Type /start to search again.")
    else:
        bot.send_message(chat_id, "Nothing to skip. Type /start to begin a search.")


@bot.message_handler(func=lambda msg: True, content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    data = user_state.get(chat_id)

    if data is None:
        bot.send_message(chat_id, "Type /start to begin.")
        return

    state = data['state']

    if state == BUDGET:
        text = message.text.strip().replace(',', '').replace('$', '')
        if not text.isdigit() or int(text) <= 0:
            bot.send_message(chat_id, "Please enter a valid positive number for your budget (e.g. 30000).")
            return
        budget_value = int(text)
        data['budget'] = budget_value
        data['state'] = OWNERS
        bot.send_message(chat_id, "How many previous owners should the car have had? (enter 0 for brand new, 1, 2, …)")

    elif state == OWNERS:
        text = message.text.strip()
        if not text.isdigit():
            bot.send_message(chat_id, "Please enter a valid number of owners (0, 1, 2, …).")
            return
        data['owners'] = int(text)
        data['state'] = BRAND
        bot.send_message(
            chat_id,
            f"Which car brand are you interested in?\nAvailable: {BRANDS_LIST}"
        )

    elif state == BRAND:
        typed = message.text.strip()
        brand = normalize_brand(typed)
        result = get_recommendations(data['budget'], data['owners'], brand)
        bot.send_message(chat_id, result)
        data['brand'] = brand
        data['state'] = FEEDBACK
        bot.send_message(
            chat_id,
            "How would you rate these recommendations? (1–5, or /skip to skip)\n"
            "⭐ 1 — Poor   ⭐⭐ 2 — Fair   ⭐⭐⭐ 3 — Good\n"
            "⭐⭐⭐⭐ 4 — Very good   ⭐⭐⭐⭐⭐ 5 — Excellent"
        )

    elif state == FEEDBACK:
        text = message.text.strip()
        if not text.isdigit() or not (1 <= int(text) <= 5):
            bot.send_message(chat_id, "Please enter a number from 1 to 5, or /skip to skip.")
            return
        rating = int(text)
        user_feedback.append({
            'chat_id': chat_id,
            'rating': rating,
            'brand': data.get('brand', ''),
        })
        stars = '⭐' * rating
        bot.send_message(chat_id, f"Thank you for your feedback! You rated: {stars}")
        user_state.pop(chat_id, None)
        bot.send_message(chat_id, "Type /start to search again.")


if __name__ == '__main__':
    bot.infinity_polling()