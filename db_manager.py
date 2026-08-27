import sqlite3


#Setup connection and cursor to my db
conn = sqlite3.connect('finances.db')
cursor = conn.cursor()

#Enable foreign key support for this session
cursor.execute("PRAGMA foreign_keys = ON;")

#Functions to control the database
def add_new_transaction(transaction_date,type):
    """Inserts a transaction into the transactions table within finances.db

    Args:
        transaction_date: Given in format 'YYYY-MM-DD'
        type: Either 'income' or 'expense'

    Return:
        The ID of the transaction record to link it to the expense and income tables in the finances.db
    """
    try:
        cursor.execute("INSERT INTO transactions (transaction_date, type) VALUES (?,?)",(transaction_date,type))
        conn.commit()
        # Return the transaction ID to link the transaction to the income or expense
        trans_id = cursor.lastrowid
        return trans_id;
    except sqlite3.IntegrityError as e: 
        print(f"Transaction record addition failed: {e}") 

#Function to add an expense
def add_expense(transaction_date, store, description, amount, category):
    """"Inserts an expense record into the expenses table within finances.db
    
    Args:
        trans_id: forgein id mapping to transactions table
        store: Where item was purchased
        description: Short informaiton about purchase
        amount: price of purchase
        categpry: expenses category limited to ('Hair', 'Clothes', 'Medical',
        'Tech', 'Dorm room', 'Cleaning', 'Misc', 'Toiletries',
        'Stationery', 'Fun', 'Travel', 'Fixed', 'Taxes')
    """
    try:
        trans_id = add_new_transaction(transaction_date,'expense')
        cursor.execute("INSERT INTO expenses (trans_id, store, description, amount, category) VALUES (?,?,?,?,?)",(trans_id, store, description, amount, category))
        conn.commit()
    except sqlite3.IntegrityError as e: 
        print(f"Expense addition failed: {e}")

#Function to add an income
def add_income(transaction_date,source, description, amount, category):
    """"Inserts an income record into the income table within finances.db
        
        Args:
            trans_id: forgein id mapping to transactions table
            source: Where income came from
            description: Short informaiton about purchase
            amount: price of purchase
            category: incomes source 

            Returns: 
                True for succesful addition
                False for unsuccesful addition
      """
    try:
        trans_id = add_new_transaction(transaction_date,'income')
        cursor.execute("INSERT INTO income (trans_id, source, description, amount, category) VALUES (?,?,?,?,?)",(trans_id, source, description, amount, category))
        conn.commit()
    except sqlite3.IntegrityError as e: 
        print(f"Income addition failed: {e}")







#Testing function
#add_expense('2026-08-20','Amazon','Sony Headphones',150,'Tech') - Sucess
#add_income('2025-10-14','Mr Wilhelm','Babysitting',400,'Other') - Sucess
