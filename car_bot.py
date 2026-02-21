import os
import telebot
from telebot import types

API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise ValueError("API_TOKEN environment variable is not set.")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome! What car are you looking for?")

@bot.message_handler(func=lambda message: True)
def car_selection(message):
    bot.send_message(message.chat.id, "Let's find a car for you! Please tell me your budget.")
    
    @bot.message_handler(func=lambda message: True)
    def budget_selection(message):
        budget = message.text
        # Here you would add logic to process the budget and respond to the user.
        bot.send_message(message.chat.id, f"Great! You're looking for a car under {budget}.")
        bot.send_message(message.chat.id, "Now, how many owners should the car have?")
        
        @bot.message_handler(func=lambda message: True)
        def owners_selection(message):
            owners = message.text
            bot.send_message(message.chat.id, f"You're looking for a car that has had {owners} owners.")
            bot.send_message(message.chat.id, "Finally, which brand do you prefer?")
            
            @bot.message_handler(func=lambda message: True)
            def brand_selection(message):
                brand = message.text
                # Final response mimicking a search for a car based on criteria
                bot.send_message(message.chat.id, f"Searching for a {brand} car under {budget} with {owners} owners.")
    
bot.polling()