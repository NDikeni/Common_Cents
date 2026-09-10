import os
import gspread
from dotenv import load_dotenv

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
file = os.getenv("FILE_URL")
sh = gc.open_by_url(file)
worksheet = sh.sheet1

worksheet.append_row(["Target","Coffee", 4.50, "Fun","Day-to-day"])
print("Sync successful with in-memory credentials!")