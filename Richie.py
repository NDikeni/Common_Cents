#Meet Richie, your personal finance assistant powered by Common Cents.
from dotenv import load_dotenv
import asyncio
import telegram
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import MessageHandler, ConversationHandler
import telegram.ext.filters as filters
from transaction import Transaction
import spacy
from spacy.pipeline import EntityRuler
import db_manager
from sheets_sync import gspread_setup, save_trans_to_gspread


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
    #Creates transaction object and saves the type of transaction
    current_transaction = Transaction()
    context.user_data["current_transaction"] = current_transaction
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

    #Save transaction type for function that saves transaction to database
    context.user_data["trans_type"] = trans_type 

    if template != "":
        message = f"Of course {update.effective_user.first_name}! \n" + f"To record a {trans_type}, follow the below message structure: \n"
        message += f"\n {template}"
        await context.bot.send_message(chat_id= update._effective_chat.id, text=message) 

        return COMPLETENESS_CHECK  

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
    current_transaction: Transaction = context.user_data.get("current_transaction")
    trans_type = context.user_data.get("trans_type")
    for ent in doc.ents:
        current_attr = ent.label_
        current_text = ent.text.capitalize()
        if current_attr == "DATE": current_attr = "TRANSACTION_DATE"
        if current_attr == "DESCRIPTION": current_text = current_text[1:-1] #Ensure description doesn't have hashes
        if current_attr == "AMOUNT": current_text = current_text[1:] #Ensure amount doesn't have dollar sign in front
        if hasattr(current_transaction,current_attr): setattr(current_transaction,current_attr,current_text)
        

    missing_attributes, message = current_transaction.completeness_message()
    await context.bot.send_message(chat_id=update.effective_chat.id,text=message)

    if missing_attributes == []:
        "End the conversation handler"
        result_message = await save_to_db(current_transaction,trans_type)
        trans_list = current_transaction.convert_to_list()
        save_trans_to_gspread(trans_list)
        await context.bot.send_message(chat_id=update.effective_chat.id,text=result_message)
        return ConversationHandler.END
    else:
        return COMPLETENESS_CHECK

async def save_to_db(transaction: Transaction, trans_type: Str):
    '''Saves the user input to the SQL server

        Returns the result messgae
    '''
    current_transaction = transaction
    trans_type = trans_type
    if trans_type == "expense":
        result_message = db_manager.add_expense(
            current_transaction.TRANSACTION_DATE,
            current_transaction.SOURCE,
            current_transaction.DESCRIPTION,
            current_transaction.AMOUNT,
            current_transaction.CATEGORY)
    elif trans_type == "income":
        result_message = db_manager.add_income(
            current_transaction.TRANSACTION_DATE,
            current_transaction.SOURCE,
            current_transaction.DESCRIPTION,
            current_transaction.AMOUNT,
            current_transaction.CATEGORY)

    return result_message



'''async def recieve_missing_transaction_attribute(missing_attribute: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """"
    Recieve missing attribute and request user input until it meets format expectations
    """
    text = update.effective_message.text
    doc = nlp(text)

    while (doc.label != missing_attribute):
         text =  await update.effective_message.text
         await context.bot.send_message(f"Please provide the missing attribute: {missing_attribute}")
    
    setattr(current_transaction,current_attr,ent.text)'''
        


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

    #-------Setup spaCy and gspread-----------------------
    #Create an instance of default spaCy pipeline
    nlp = spacy.load("en_core_web_sm")
    gspread_setup()
    
        
    #Add entity recogintion rule to pipeline
    config = {
    "overwrite_ents": True,
    "validate": True}
    patterns = return_EntityRuler_patterns() #Produce pattern recognition
    ruler = nlp.add_pipe("entity_ruler", after="ner",config=config) #creates an instance of the entity_ruler class
    ruler.add_patterns(patterns) #adds functionality to the entity_ruler by adding a class rule
    ruler.overwrite_ents = True

    #----Add in state number for conversation handler---------------------#
    COMPLETENESS_CHECK = 0
    #--Add in event handlers----------------------------------------------#

    
    conversation_handler = ConversationHandler(
        entry_points=[ MessageHandler(filters.TEXT & (filters.Regex(r'income') | filters.Regex(f'expense')),provide_template)],
        states={COMPLETENESS_CHECK: [MessageHandler(filters.TEXT & (~filters.COMMAND),completeness_check)]},
        fallbacks=[]
    )
    application.add_handler(conversation_handler)
    start_handler = CommandHandler('start', start)
    #Basically the trigger is all messsgaes that are not a command 
    mock_handler = CommandHandler('mock',completeness_check)
    application.add_handler(start_handler)
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