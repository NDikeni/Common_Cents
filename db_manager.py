import sqlite3

#Setup connection and cursor to my db
conn = sqlite3.connect('finances.db')
cursor = conn.cursor()

#Function to save an expense
def add_expense(trans_id, store, description, amount, category):
    """"Inserts an expense record into the expenses table within finances.db
    
    Args:
        trans_id: forgein id mapping to transactions table
        store: Where item was purchased
        description: Short informaiton about purchase
        amount: price of purchase
        categpry: expenses category limited to ('Hair', 'Clothes', 'Medical',
        'Tech', 'Dorm room', 'Cleaning', 'Misc', 'Toiletries',
        'Stationery', 'Fun', 'Travel', 'Fixed', 'Taxes')

        Returns: 
            True for succesful addition
            False for unsuccesful addition
    """
    try:
        cursor.execute("INSERT INTO expenses (trans_id, store, description, amount, category) VALUES (?,?,?,?,?)",(trans_id, store, description, amount, category))
        conn.commit()
    except sqlite3.IntegrityError as e: 
        print(f"Expense addition failed: {e}")
    

#Testing function
add_expense(2, 'Samsung','Galaxy',250,'Tech')
    
