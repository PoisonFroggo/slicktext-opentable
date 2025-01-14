import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

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


# API endpoint
url = "https://api.slicktext.com/v1/textwords"

# API key (you need to replace 'YOUR_API_KEY' with your actual API key)
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Parameters for the request
limit = 30  # The number of textwords to fetch per request
offset = 0  # The offset for pagination

# Function to retrieve all textwords
def get_all_textwords():
    all_textwords = []
    while True:
        params = {
            "limit": 30,
            "offset": 0
        }
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            textwords = data.get("textwords", [])
            
            if not textwords:
                break  # Exit if no more textwords are available
            
            all_textwords.extend(textwords)
            offset += limit  # Update offset to fetch the next set of results
        else:
            print(f"Error: {response.status_code}")
            break

    return all_textwords

# Fetch all textwords
textwords = get_all_textwords()

# Print the retrieved textwords
for textword in textwords:
    print(textword)
