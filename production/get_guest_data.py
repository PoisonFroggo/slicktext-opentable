import requests
import json
import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from datetime import date
from datetime import datetime, timezone
#!/usr/bin/env python3.13

#Gets the guest info (specifically phone number)
now = datetime.now(timezone.utc)
formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S")  # Basic format
fractional_seconds = f"{now.microsecond // 1000:03d}"  # Milliseconds
timezone_offset = "+0000"  # Assuming UTC timezone
current_date = f"{formatted_date}.{fractional_seconds}{timezone_offset}"

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
guests_url = "https://platform.opentable.com/sync/v2/guests/1027723-6585f1fcb20d97d744d17511"
reservations_url = data["installed"]["reservations"]
contacts_url = data["installed"]["contacts"]
client_id = os.getenv("OPENTABLE_CLIENT_ID")
client_secret = os.getenv("OPENTABLE_CLIENT_SECRET")

url = "https://platform.opentable.com/sync/v2/guests"

#public and private keys
public_key = os.getenv("SLICKTEXT_PUBLIC_KEY")
private_key = os.getenv("SLICKTEXT_PRIVATE_KEY")

if not public_key or not private_key:
    raise ValueError("Public and private keys must be set in the environment variables.")


# Step 1: Concatenate client_id and client_secret with a colon
credentials = f"{client_id}:{client_secret}"
# Step 2: Base64 encode the result
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer cdb0aac7-8b06-4e9f-8f14-a35c187a7aab",
    "Cache-Control": "no-cache"
}

params = {
    "email_optin": "true",
    "updated_after": "2020-01-07T00:00:01Z",
    "limit": 1000,
    "offset": 0,
    "rid": 1027723
}

response = requests.get(guests_url, headers=headers, params=params)

def get_guest_info(api_url, headers, params):
    """Fetches guest information from the provided API URL.

    Args:
        api_url (str): The URL of the guest information API.
        headers (dict): Headers to include in the request.
        params (dict): Query parameters to include in the request.

    Returns:
        list: A list of guest information dictionaries, or an empty list if the request fails.
    """
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("items", [])
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return []


# Fetch and print guest info
guests = get_guest_info(url, headers, params)
#if guests:
    #for guest in guests:
        #print(guest)