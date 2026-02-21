import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

BUDGET, OWNERS, CAR_BRAND = range(3)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Welcome! Please enter your budget.")
    return BUDGET

def budget(update: Update, context: CallbackContext) -> int:
    context.user_data['budget'] = update.message.text
    update.message.reply_text("How many owners has the car had?")
    return OWNERS

def owners(update: Update, context: CallbackContext) -> int:
    context.user_data['owners'] = update.message.text
    update.message.reply_text("Which car brand are you interested in? (Toyota, BMW, Mercedes, Audi, Honda, Hyundai, Volkswagen, Ford, Mazda, Renault)")
    return CAR_BRAND

def car_brand(update: Update, context: CallbackContext) -> int:
    brand = update.message.text
    budget = context.user_data['budget']
    owners = context.user_data['owners']
    
    # Sample car recommendation logic (dummy implementation)
    car_recommendations = {
        'Toyota': ['Corolla', 'Camry', 'Hilux'],
        'BMW': ['X5', '3 Series', 'Z4'],
        'Mercedes': ['C-Class', 'E-Class', 'G-Class'],
        'Audi': ['A4', 'Q5', 'A6'],
        'Honda': ['Civic', 'Accord', 'HR-V'],
        'Hyundai': ['Elantra', 'Tucson', 'Santa Fe'],
        'Volkswagen': ['Golf', 'Passat', 'Tiguan'],
        'Ford': ['Focus', 'F-150', 'Mustang'],
        'Mazda': ['Mazda3', 'CX-5', 'MX-5'],
        'Renault': ['Clio', 'Captur', 'Koleos']
    }

    recommendations = car_recommendations.get(brand, [])
    if recommendations:
        update.message.reply_text(f"Based on your inputs, we recommend: {', '.join(recommendations[:3])}")
    else:
        update.message.reply_text("Sorry, I couldn't find any recommendations for that brand.")
        
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Conversation cancelled. You can start again by typing /start.')
    return ConversationHandler.END

def main():
    token = os.getenv('API_TOKEN')
    if not token:
        raise ValueError("API_TOKEN environment variable is not set.")
    updater = Updater(token)
    
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            BUDGET: [MessageHandler(Filters.text & ~Filters.command, budget)],
            OWNERS: [MessageHandler(Filters.text & ~Filters.command, owners)],
            CAR_BRAND: [MessageHandler(Filters.text & ~Filters.command, car_brand)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()