import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import base64

#!/usr/bin/env python3.13
# Retrieves a contact associated with a specific textword and phone number

# Load environment variables from .env file
load_dotenv()

# Get current file directory
current_file = Path(__file__).absolute()
parent_folder = current_file.parent
root_dir = parent_folder

# Load secrets file
os.chdir(root_dir)
client_secrets = 'client_secrets.json'
with open(client_secrets) as file:
    data = json.load(file)

# Access specific info from the loaded client secrets
api_key = data["installed"]["guest_id"]
textword_id = data["installed"]["textword_id"]
guests_url = data["installed"]["guests"]
reservations_url = data["installed"]["reservations"]
contacts_url = data["installed"]["contacts"]

# Public and private keys
public_key = os.getenv("SLICKTEXT_PUBLIC_KEY")
private_key = os.getenv("SLICKTEXT_PRIVATE_KEY")

if not public_key or not private_key:
    raise ValueError("Public and private keys must be set in the environment variables.")


# Generate the base64-encoded string for Basic Authentication
credentials = f"{public_key}:{private_key}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')


# Set the URL for the API endpoint
url = f'https://api.slicktext.com/v1/textwords/{textword_id}/contacts'

# Make the GET request with Basic Authentication
response = requests.get(url, headers={
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
})

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("Contacts Retrieved:")
    for contact in data['contacts']:
        print(f"ID: {contact['id']}")
        print(f"Number: {contact['number']}")
        print(f"City: {contact['city']}")
        print(f"State: {contact['state']}")
        print(f"Zip Code: {contact['zipCode']}")
        print(f"Country: {contact['country']}")
        print(f"Textword: {contact['textword']}")
        print(f"Subscribed Date: {contact['subscribedDate']}")
        print(f"First Name: {contact['firstName']}")
        print(f"Last Name: {contact['lastName']}")
        print(f"Email: {contact['email']}")
        print(f"Opt-In Method: {contact['optInMethod']}")
        print("----")
else:
    print(f"Failed to retrieve contacts. Status Code: {response.status_code}")
    print("Response:", response.text)