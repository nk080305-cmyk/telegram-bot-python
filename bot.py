import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Conversation states
BUDGET, OWNERS, BRAND, RECOMMEND = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Welcome to the Car Recommendation Bot! What is your budget?')
    return BUDGET

async def budget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['budget'] = update.message.text
    await update.message.reply_text('How many owners have the car had?')
    return OWNERS

async def owners(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['owners'] = update.message.text
    await update.message.reply_text('What car brand are you interested in?')
    return BRAND

async def brand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['brand'] = update.message.text
    # Recommend cars based on the input
    budget = context.user_data['budget']
    owners = context.user_data['owners']
    brand = context.user_data['brand']
    
    # Placeholder recommendation logic
    recommendations = f"Based on your inputs: Budget: {budget}, Owners: {owners}, Brand: {brand}, we recommend:\n1. Car A\n2. Car B\n3. Car C"

    await update.message.reply_text(recommendations)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Conversation cancelled.')
    return ConversationHandler.END

def main() -> None:
    # Read token from environment variable
    token = os.getenv('API_TOKEN')
    application = ApplicationBuilder().token(token).build()

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, budget)],
            OWNERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, owners)],
            BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, brand)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()