import telebot

API_TOKEN = 'YOUR_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Sample car recommendations based on user input
car_recommendations = {
    'Toyota': ['Toyota Corolla', 'Toyota Camry', 'Toyota RAV4'],
    'Mazda': ['Mazda 3', 'Mazda CX-5', 'Mazda MX-5'],
    'Hyundai': ['Hyundai Elantra', 'Hyundai Tucson', 'Hyundai i10'],
    'Honda': ['Honda Civic', 'Honda Accord', 'Honda CR-V'],
    'Ford': ['Ford Focus', 'Ford Fiesta', 'Ford Kuga'],
    'Volkswagen': ['Volkswagen Golf', 'Volkswagen Passat', 'Volkswagen Tiguan'],
    'BMW': ['BMW 3 Series', 'BMW X5', 'BMW X1'],
    'Mercedes': ['Mercedes A-Class', 'Mercedes C-Class', 'Mercedes GLC'],
    'Audi': ['Audi A3', 'Audi Q5', 'Audi A4'],
    'Renault': ['Renault Clio', 'Renault Captur', 'Renault Koleos']
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! I can help you find a car.\nPlease tell me your budget.")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def ask_for_budget(message):
    chat_id = message.chat.id
    budget = message.text  # Extract user budget
    bot.send_message(chat_id, "How many owners should the car have?")

    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def ask_for_owners(owners_message):
        owners = owners_message.text  # Extract number of owners
        bot.send_message(chat_id, "What brand are you interested in? (e.g., Toyota, Mazda, etc.)")

        @bot.message_handler(func=lambda message: True, content_types=['text'])
        def recommend_cars(brand_message):
            brand = brand_message.text  # Extract brand
            recommendations = car_recommendations.get(brand, [])
            if recommendations:
                response = f"Based on your criteria, I recommend:\n" + "\n".join(recommendations[:3])
            else:
                response = "Sorry, I don't have recommendations for that brand."
            bot.send_message(chat_id, response)

bot.polling()