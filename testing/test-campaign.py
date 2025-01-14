import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import base64

#!/usr/bin/env python3.13
# Sends a message to a specific contact using the SlickText API

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
url = 'https://api.slicktext.com/v1/messages/'

# Define the payload for sending the message
payload = {
    "action": "SEND",
    "textword": textword_id,  # Replace with the actual Textword ID
    "contact": "+16056951184",  # The recipient's phone number
    "body": "Hello! This is a test message sent via the SlickText API.",
    "campaign": "Test Campaign"
}

# Send the POST request
response = requests.post(
    url,
    headers={
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    },
    data=json.dumps(payload)  # Convert the payload to a JSON string
)

# Check the response
if response.status_code == 200:
    print("Message Sent Successfully!")
    print("Response:", response.json())
else:
    print(f"Failed to send message. Status Code: {response.status_code}")
    print("Response:", response.text)