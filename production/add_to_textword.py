import requests
import json
import os
import base64
from pathlib import Path
from dotenv import load_dotenv
#!/usr/bin/env python3.13
#Adds the input guest data to the textword, making sure that the user has not already
#been a part of the textword
    

#load environment variables from .env file
load_dotenv

#get current file directory
current_file = Path(__file__).absolute()
parent_folder = current_file.parent
root_dir = parent_folder

#load secrets file
os.chdir(root_dir)
client_secrets = 'client_secrets.json'
with open(client_secrets) as file:
    data=json.load(file)

#Access specific info
api_key = os.getenv("SLICKTEXT_GUEST_ID")
textword_id = os.getenv("SLICKTEXT_TEXTWORD_ID")
guests_url = data["installed"]["guests"]
reservations_url = data["installed"]["reservations"]
contacts_url = data["installed"]["contacts"]
client_id = os.getenv("OPENTABLE_CLIENT_ID")
client_secret = os.getenv("OPENTABLE_CLIENT_SECRET")

#public and private keys
public_key = os.getenv("SLICKTEXT_PUBLIC_KEY")
private_key = os.getenv("SLICKTEXT_PRIVATE_KEY")