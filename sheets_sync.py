import os
import gspread
from dotenv import load_dotenv

worksheet = None
last_row = None

def gspread_setup():
    #Load all my var's from hidden env file
    load_dotenv()

    #Rebuild creditentials dictionary 
    credentials_dict = {
        "type": os.getenv("GCP_PROJECT_ID"),
        "project_id": os.getenv("GCP_PROJECT_ID"),
        "private_key_id": os.getenv("GCP_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GCP_PRIVATE_KEY"),
        "client_email": os.getenv("GCP_CLIENT_EMAIL"),
        "client_id": os.getenv("GCP_CLIENT_ID"),
        "auth_uri": os.getenv("GCP_AUTH_URI"),
        "token_uri": os.getenv("GCP_TOKEN_URI")
    }

    #Handshake with google via the credentials
    gc = gspread.service_account_from_dict(credentials_dict)

    # Test
    global worksheet,last_row
    file = os.getenv("FILE_URL")
    sh = gc.open_by_url(file)
    worksheet = sh.get_worksheet(2)
    worksheet.update_nam
    table_range = worksheet.range("MyTable")
    last_row = table_range[-1].row

    return worksheet

def save_trans_to_gspread(list_trans: list):
    '''
        Save transaction to gspread by appending a row
    '''
    new_row_data = list_trans
    global worksheet,last_row

    worksheet.insert_row(
        values=new_row_data,
        index=last_row +1,
        value_input_option="USER_ENTERED",
        inherit_from_before=True
    )
    #table_range = worksheet.
    print("Sync successful with in-memory credentials!")




#Setting up a new table
'''
    1. Define a named range (including title) - call it MyTable
    2. Update the workseet number in line 26
'''