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
    

def application_setup():

    # Load the keys fromm the local .env file
    load_dotenv()

    # Safely retrieve the hidden token
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    # Generate an instance of the Bot class
    bot = telegram.Bot(BOT_TOKEN)    

    return ApplicationBuilder().token(BOT_TOKEN).build()

async def provide_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Richie will provide the proper format for an expense or income as per user request

    It returns the handler
    '''

    text = (update.effective_message.text).lower()
    print(f"{text}")
    template = ""
    income = "income"
    expense = "expense"

    #Retrieve template based on user message
    if expense in text:
        template = "YYYY-MM-DD store description amount category"
        trans_type = "expense"
        print(f'The transaction type is: {trans_type}')
    elif income in text:
        template = "YYYY-MM-DD source description amount category"
        trans_type = "income"
        print(f'The transaction type is: {trans_type}')

    if template != "":
        message = f"Of course {update.effective_user.first_name}! \n" + f"To record a {trans_type}, follow the below message structure: \n"
        message += f"\n {template}"
        await context.bot.send_message(chat_id= update._effective_chat.id, text=message)    
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Repeat everything back to the user
    chat_id = update.effective_chat.id
    text = update.effective_message.text
    await context.bot.send_message(chat_id=chat_id,text=text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

if __name__ == '__main__':
    #Create an application
    application = application_setup()
    
    start_handler = CommandHandler('start', start)
    #filter.Text = message sent by user
    #Basically the trigger is all messsgaes that are not a command 
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    provide_template_handler = MessageHandler(filters.Regex(r'income') | filters.Regex(f'expense'),provide_template)
    application.add_handler(caps_handler)
    application.add_handler(start_handler)
    #application.add_handler(echo_handler)
    application.add_handler(provide_template_handler)
    
        
    application.run_polling()


#Nisema notes:
'''
First version of Richie 
    -> Take a message in the correct format
    -> Parse the information and return it:
        -> Example: 2026-10-14 Bread Food
        -> Transaction date: 2026-10-14
        -> Description: Bread
        -> Type: Food
'''