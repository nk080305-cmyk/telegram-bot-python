import os
import re
import telebot
from telebot import types
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

# Last completed search per user: {chat_id: {'budget': int, 'owners': int, 'brand': str}}
last_session: dict = {}

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

# Natural-language phrase: "what changed since the last time I logged in" (Russian)
_WHATS_NEW_QUERY = re.compile(
    r'^\s*что\s+изменилось\s+с\s+последнего\s+раза\s+когда\s+я\s+заходил\s*[?,!.]*\s*$',
    re.IGNORECASE,
)

# Natural-language status query: "at what stage" (Russian)
_STATUS_QUERY = re.compile(r'^\s*на\s+каком\s+этапе\s*[?,!.]*\s*$', re.IGNORECASE)


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


# ── Helpers ───────────────────────────────────────────────────────────────────

def _send_status(chat_id, data) -> None:
    """Send the current conversation step to *chat_id*."""
    if data is None:
        bot.send_message(chat_id, "No active search. Type /start to begin.")
        return
    state = data['state']
    if state == BUDGET:
        bot.send_message(chat_id, "Step 1/4 — Waiting for your budget (USD).")
    elif state == OWNERS:
        bot.send_message(
            chat_id,
            f"Step 2/4 — Budget: ${data['budget']:,}. Waiting for number of previous owners."
        )
    elif state == BRAND:
        bot.send_message(
            chat_id,
            f"Step 3/4 — Budget: ${data['budget']:,}, Owners: {data['owners']}. "
            f"Waiting for brand.\nAvailable: {BRANDS_LIST}"
        )
    elif state == FEEDBACK:
        bot.send_message(
            chat_id,
            f"Step 4/4 — Recommendations shown for {data.get('brand', 'your brand')}. "
            "Waiting for your rating (1–5) or /skip."
        )


def _send_whats_new(chat_id, last) -> None:
    """Respond to the 'what changed since last time' natural-language query."""
    if last is None:
        bot.send_message(
            chat_id,
            "No previous search found. Type /start to begin your first search."
        )
        return
    bot.send_message(
        chat_id,
        "The car catalogue has not changed since your last visit.\n\n"
        f"Your last search:\n"
        f"• Budget: ${last['budget']:,}\n"
        f"• Previous owners: {last['owners']}\n"
        f"• Brand: {last['brand']}\n\n"
        "Type /start to search again."
    )


def _transition_to_feedback(chat_id, data, brand) -> None:
    """Show recommendations, save session, and advance to FEEDBACK state."""
    result = get_recommendations(data['budget'], data['owners'], brand)
    bot.send_message(chat_id, result)
    last_session[chat_id] = {'budget': data['budget'], 'owners': data['owners'], 'brand': brand}
    data['brand'] = brand
    data['state'] = FEEDBACK
    bot.send_message(
        chat_id,
        "How would you rate these recommendations? (1–5, or /skip to skip)\n"
        "⭐ 1 — Poor   ⭐⭐ 2 — Fair   ⭐⭐⭐ 3 — Good\n"
        "⭐⭐⭐⭐ 4 — Very good   ⭐⭐⭐⭐⭐ 5 — Excellent"
    )


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
        "/status — show current search step\n"
        "/list — show all available brands and models\n"
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


@bot.message_handler(commands=['status'])
def cmd_status(message):
    _send_status(message.chat.id, user_state.get(message.chat.id))


@bot.message_handler(commands=['list'])
def cmd_list(message):
    """Show all brands and their models with prices."""
    lines = []
    for brand, models in CAR_CATALOGUE.items():
        model_str = ', '.join(f"{m} (${p:,})" for m, p in models)
        lines.append(f"*{brand}*: {model_str}")
    bot.send_message(
        message.chat.id,
        "🚗 *Available cars:*\n\n" + '\n'.join(lines),
        parse_mode='Markdown',
    )


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

    # Natural-language "what changed" query
    if _WHATS_NEW_QUERY.match(message.text):
        _send_whats_new(chat_id, last_session.get(chat_id))
        return

    # Natural-language status query (e.g. "на каком этапе", "на каком этапе?")
    if _STATUS_QUERY.match(message.text):
        _send_status(chat_id, data)
        return

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
        markup = types.InlineKeyboardMarkup(row_width=3)
        buttons = [
            types.InlineKeyboardButton(brand, callback_data=f'brand_{brand}')
            for brand in CAR_CATALOGUE
        ]
        markup.add(*buttons)
        bot.send_message(
            chat_id,
            f"Which car brand are you interested in?\nAvailable: {BRANDS_LIST}",
            reply_markup=markup,
        )

    elif state == BRAND:
        typed = message.text.strip()
        brand = normalize_brand(typed)
        _transition_to_feedback(chat_id, data, brand)

    elif state == FEEDBACK:
        text = message.text.strip()
        if not text.isdigit():
            bot.send_message(chat_id, "Please enter a number from 1 to 5, or /skip to skip.")
            return
        rating = int(text)
        if not (1 <= rating <= 5):
            bot.send_message(chat_id, "Please enter a number from 1 to 5, or /skip to skip.")
            return
        user_feedback.append({
            'chat_id': chat_id,
            'rating': rating,
            'brand': data.get('brand', ''),
        })
        stars = '⭐' * rating
        bot.send_message(chat_id, f"Thank you for your feedback! You rated: {stars}")
        user_state.pop(chat_id, None)
        bot.send_message(chat_id, "Type /start to search again.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('brand_'))
def handle_brand_callback(call):
    """Handle brand selection from inline keyboard."""
    chat_id = call.message.chat.id
    data = user_state.get(chat_id)

    if data is None or data.get('state') != BRAND:
        bot.answer_callback_query(call.id, "Session expired. Use /start to begin again.")
        return

    brand = call.data.removeprefix('brand_')
    bot.answer_callback_query(call.id)
    _transition_to_feedback(chat_id, data, brand)


if __name__ == '__main__':
    bot.infinity_polling()