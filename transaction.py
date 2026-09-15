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
            final_message = "Awesome! I will save it to your google sheets."
            for attr,value in vars(self).items():
                final_message += f"\n{attr.capitalize()}: {value}"
            return list_missing_attributes, final_message
        else:
            final_message = "It appears at though I'm missing some information."
            attributes = ""
            for attr in list_missing_attributes:
                attributes += f"\n{attr}"
            final_message += f"\nPlease provide the following: {attributes.lower()}"
            return list_missing_attributes, final_message

    def convert_to_list(self):
        '''
        Receive a transaction object and for each item add it to the list that will be passed to insert the row
        '''
        #Vars turns the object attributes into a dictionery {"amount":100,"category":"Tech"}
        #.values is only the arguments passed into the object attributes
        new_row_data = list(vars(self).values())
        print(new_row_data)
        return new_row_data

