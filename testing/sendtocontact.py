import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv
#!/usr/bin/env python3.13
#Adds a defined user to the Textword

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
api_key = data["installed"]["guest_id"]
textword_id = data["installed"]["textword_id"]
guests_url = data["installed"]["guests"]
reservations_url = data["installed"]["reservations"]
contacts_url = data["installed"]["contacts"]

#public and private keys
public_key = os.getenv("SLICKTEXT_PUBLIC_KEY")
private_key = os.getenv("SLICKTEXT_PRIVATE_KEY")

if not public_key or not private_key:
    raise ValueError("Public and private keys must be set in the environment variables.")

def msg_contact(
    public_key,
    private_key,
    #textword,
    number,
    msg="Test",
    first_name=None,
    last_name=None,
    email=None,
    birth_date=None,
    city=None,
    state=None,
    zip_code=None,
    country=None,
    **custom_fields
):
    """
    Double opts a contact into a specific textword list.
    """
    url = "https://api.slicktext.com/v1/messages/"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "action": "SEND",
        #"textword": textword,
        "number": number
    }
    
    # Optional parameters
    if msg_contact:
        payload["doubleOptInMessage"] = msg
    if first_name:
        payload["firstName"] = first_name
    if last_name:
        payload["lastName"] = last_name
    if email:
        payload["email"] = email
    if birth_date:
        payload["birthDate"] = birth_date
    if city:
        payload["city"] = city
    if state:
        payload["state"] = state
    if zip_code:
        payload["zipCode"] = zip_code
    if country:
        payload["country"] = country
    
    # Add custom fields if provided
    payload.update(custom_fields)

    #Debug: log payload
    print("Payload:", json.dumps(payload, indent=4))

    #Make request with Basic Auth
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        auth=(public_key, private_key)
    )

    print("Response Status Code: ", response.status_code)
    print("Response Body: ", response.text)

    response.raise_for_status()
    return response.json()

# Example Usage
try:
    response = msg_contact(
        public_key=public_key,
        private_key=private_key,
        number="+6056951184"
    )
    print("Response: ", response)
except requests.exceptions.RequestException as e:
    print("Error: ",e)