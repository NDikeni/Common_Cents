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
from transaction import Transaction
import spacy
from spacy.pipeline import EntityRuler


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
        template = "YYYY-MM-DD store #description# amount category"
        trans_type = "expense"
        print(f'The transaction type is: {trans_type}')
    elif income in text:
        template = "YYYY-MM-DD source #description# amount category"
        trans_type = "income"
        print(f'The transaction type is: {trans_type}')

    if template != "":
        message = f"Of course {update.effective_user.first_name}! \n" + f"To record a {trans_type}, follow the below message structure: \n"
        message += f"\n {template}"
        await context.bot.send_message(chat_id= update._effective_chat.id, text=message)    

async def completeness_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """"
    This function checks that the user provided the date, store/source, description amount and category. 
    If not everything is provided Richie asks for the remaining data
    """
    #Store user text message
    text = update.effective_message.text

    #Processes user test
    doc = nlp(text)
    
    #Loop through each word and assign it to it's given attribute
    current_transaction = Transaction()
    for ent in doc.ents:
        current_attr = ent.label_
        if current_attr == "DATE": current_attr = "TRANSACTION_DATE"
        if hasattr(current_transaction,current_attr): setattr(current_transaction,current_attr,ent.text)
        

    missing_attribute, message = current_transaction.completeness_message()
    await context.bot.send_message(chat_id=update.effective_chat.id,text=message)
    #if not current_transaction.complete():
        #Go through each empty attribute and wait for the user to respond

async def recieve_missing_transaction_attribute(missing_attribute: Str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """"
    Recieve missing attribute and request user input until it meets format expectations
    """
    text = update.effective_message.text
    doc = mlp(text)

    while (doc.label != missing_attribute):
        
    if doc.label == missing_attribute:
        setattr(current_transaction,current_attr,ent.text)
    else:
        


def return_EntityRuler_patterns():
    """
    Adds common user companies, expenses and income to spaCy EntityRuler to identify these words as mentioned here before.  

    Return: List of dictionaries for EntityRuler patterns
    """

    #Add context to spacy
    SOURCE = ["woolworths", "picknpay", "checkers", "hm", "zara", "takealot","amazon","target","other","CVS", "World Market","Mint Mobile","Ventra"]
    CATEGORY = ["hair","clothes","medical","tech","cleaning","toiletries","stationery","fun","misc","dorm room","fixed"]
    CATEGORY += ["job","fin-aid","other"]

    patterns = []

    #Descriptions are wrapped in hashes
    patterns.append({"label": "DESCRIPTION", "pattern": [
            {"TEXT": "#"}, 
            {"TEXT": {"REGEX": ".*"}, "OP": "+"}, 
            {"TEXT": "#"}
        ]})

    #Money will be considerd an amount
    # Matches a dollar sign, followed by any token that looks like a number (including decimals)
    patterns.append({
        "label": "AMOUNT", 
        "pattern": [
            {"TEXT": "$"},
            {"LIKE_NUM": True}
        ]
    })

    # Rename DATE to "TRANSACTION_DATE"
    '''patterns.append({
        "label": "TRANSACTION_DATE", 
        "pattern": [{"ENT_TYPE": "DATE"}]
    })'''

    #Include the companies, expense categoreis and income categories as common words
    for company in SOURCE:
        patterns.append({"label": "SOURCE", "pattern": [{"LOWER": company}]})

    for expense in CATEGORY:
        patterns.append({"label":"CATEGORY", "pattern": [{"LOWER": expense}]})

    for income in CATEGORY:
        patterns.append({"label":"CATEGORY", "pattern": [{"LOWER": income }] })

    return patterns
    

if __name__ == '__main__':

    #-----Create an application--------
    application = application_setup()

    #-------Setup spaCy-----------------------
    #Create an instance of default spaCy pipeline
    nlp = spacy.load("en_core_web_sm")
    
        
    #Add entity recogintion rule to pipeline
    config = {
    "overwrite_ents": True,
    "validate": True}
    patterns = return_EntityRuler_patterns() #Produce pattern recognition
    ruler = nlp.add_pipe("entity_ruler", after="ner",config=config) #creates an instance of the entity_ruler class
    ruler.add_patterns(patterns) #adds functionality to the entity_ruler by adding a class rule
    ruler.overwrite_ents = True

    #--Add in event handlers----------------------------------------------#

    start_handler = CommandHandler('start', start)
    #Basically the trigger is all messsgaes that are not a command 
    provide_template_handler = MessageHandler(filters.Regex(r'income') | filters.Regex(f'expense'),provide_template)
    mock_handler = CommandHandler('mock',completeness_check)
   
    application.add_handler(start_handler)
    application.add_handler(provide_template_handler)
    application.add_handler(mock_handler)
    
        
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