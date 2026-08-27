#Meet Richie, your personal finance assistant powered by Common Cents.
from dotenv import load_dotenv
import asyncio
import telegram
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import MessageHandler
import telegram.ext.filters as filters

#logging module to know when (and why) things don't work as expected
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#Function callled everytime /start command sent
#update - contains all the info coming from Telegram
#context - contains infor about the status of the library
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm Richie, let's START saving money! Get it😂!")
    

'''async def main():
    # Load the keys fromm the local .env file
    load_dotenv()

    # Safely retrieve the hidden token
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    # Generate an instance of the Bot class
    bot = telegram.Bot(BOT_TOKEN)

    #Same as opening a file it intiliases the bot
    #async with bot:

    #Create an application
    application = ApplicationBuilder().token(BOT_TOKEN).build()
            

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
            
    application.run_polling()'''
        
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Repeat everything back to the user
    chat_id = update.effective_chat.id
    text = update.effective_message.text
    await context.bot.send_message(chat_id=chat_id,text=text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

if __name__ == '__main__':
    #asyncio.run(main())
 # Load the keys fromm the local .env file
    load_dotenv()

    # Safely retrieve the hidden token
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    # Generate an instance of the Bot class
    bot = telegram.Bot(BOT_TOKEN)

    #Same as opening a file it intiliases the bot
    #async with bot:

    #Create an application
    application = ApplicationBuilder().token(BOT_TOKEN).build()
            

    start_handler = CommandHandler('start', start)
    #filter.Text = message sent by user
    #Basically the trigger is all messsgaes that are not a command 
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    application.add_handler(caps_handler)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    
        
    application.run_polling()


#Nisema tinkerig
#print(await bot.get_me())
#The brackets is the message number
#updates = (await bot.get_updates())[1]
#chat_id = updates.effective_chat.id
#username = updates.effective_user.first_name
#await bot.send_message(chat_id=chat_id, text=f"Hi {username}!")