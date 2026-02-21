import telebot

TOKEN = '8544600427:AAFCHHUWToctTqRruO6yo-da1psoHkyS7go'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Welcome to the Car Selection Bot! Please select a car type:')

@bot.message_handler(func=lambda message: True)
def select_car(message):
    car_type = message.text
    response = f'You have selected: {car_type}'
    bot.send_message(message.chat.id, response)

if __name__ == '__main__':
    bot.polling()