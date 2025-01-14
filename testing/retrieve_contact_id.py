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

# Define the URL for retrieving contacts based on textword
contacts_api_url = f"https://api.slicktext.com/v1/contacts?textword={textword_id}"

# Function to retrieve a contact by phone number associated with a specific textword
def get_contact_by_phone(phone_num):
    params = {
        'limit': 30,  # Adjust limit as needed
        'offset': 0,  # Pagination (start at the first page)
    }

    while True:
        # Make the API call to get contacts for the specified textword
        response = requests.get(contacts_api_url, headers={'Authorization': f'Bearer {api_key}'}, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        
        data = response.json()

        # Loop through contacts and check for a match with the phone number
        for contact in data['contacts']:
            if contact['number'] == phone_num:
                print(f"Contact found: {json.dumps(contact, indent=4)}")
                return contact['id']  # Return the contact ID

        # Handle pagination if there are more contacts to fetch
        if 'next' in data['links']:
            params['offset'] += params['limit']  # Increase offset to fetch the next batch of contacts
        else:
            break

    return None  # Return None if no contact is found

# Function to retrieve contact details by ID
def get_contact_details(contact_id):
    url = f"https://api.slicktext.com/v1/contacts/{contact_id}"
    response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})

    if response.status_code == 200:
        contact_data = response.json()
        print(f"Contact Details: {json.dumps(contact_data, indent=4)}")
    else:
        print(f"Error retrieving contact details: {response.status_code}")

# Example Usage
phone_num = '+16056951184'  # The phone number you are looking for
contact_id = get_contact_by_phone(phone_num)

if contact_id:
    get_contact_details(contact_id)
else:
    print(f"No contact found with phone number {phone_num} under textword {textword_id}")