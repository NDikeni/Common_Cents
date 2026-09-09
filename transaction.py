from datetime import date

class Transaction:
    ''' The class holds the attributes for a given transaction record(income/expense) to be
    recorded in the SQL table. 

    Attributes:
        trans
    '''
    def __init__(self, TRANSACTION_DATE="Missing", SOURCE="Missing", DESCRIPTION="Missing", AMOUNT="Missing", CATEGORY="Missing"):
        self.TRANSACTION_DATE = TRANSACTION_DATE
        self.SOURCE = SOURCE
        self.DESCRIPTION = DESCRIPTION
        self.AMOUNT = AMOUNT
        self.CATEGORY = CATEGORY

    def complete(self):
        '''
        Formats a message for Richie, to tell the users which attributes are missing. 

        Return:
            String for Richie to say to user. 
        '''

        message = self.completeness_message()
        if message == "Missing":
            return True
        else:
            return False

    def completeness_message(self):
        '''
            Formats a message for Richie, to tell the users which attributes are missing. 
        
            Return:
                String for Richie to say to user. 
        '''
        list_missing_attributes = []
        for attr,value in vars(self).items():
            if value == "Missing":
                list_missing_attributes.append(attr)
        
        if list_missing_attributes == []:
            #If message is complete it should run function that provides a summary pf the transaction
            final_message = "Awesome! Record complete"
            return list_missing_attributes, final_message
        else:
            final_message = "It appears at though I'm missing some information.\n"
            attributes = ""
            for attr in list_missing_attributes:
                attributes += f"\n{attr}"
            final_message += f"\nPlease provide the following: {attributes.lower()}"
            return list_missing_attributes, final_message

