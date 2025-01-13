import base64
import requests
#Use this to request a new access token if the error 401 was returned when requesting info

# Replace with your actual client ID and secret
client_id = "cpa_7993_generic"
client_secret = "qGhWiSaMJKIP6jXo4EMjL6zeS44drSE3"

# Step 1: Concatenate client_id and client_secret with a colon
credentials = f"{client_id}:{client_secret}"

# Step 2: Base64 encode the result
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

# Step 3: Make the POST request to get the OAuth token
url = "https://oauth-pp.opentable.com/api/v2/oauth/token?grant_type=client_credentials"
headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Length": "0"
}

response = requests.post(url, headers=headers)

# Step 4: Parse and print the response
if response.status_code == 200:
    token_data = response.json()
    print("Access Token:", token_data.get("access_token"))
else:
    print("Error:", response.status_code, response.text)