import requests
import json
import os
from datetime import datetime, timezone

def get_current_date():
    """Gets the current date and time in the required format."""
    now = datetime.now(timezone.utc)
    formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S")
    fractional_seconds = f"{now.microsecond // 1000:03d}"
    timezone_offset = "+0000"  # Assuming UTC timezone
    return f"{formatted_date}.{fractional_seconds}{timezone_offset}"

def fetch_reservations(api_url, headers, params):
    """Fetches reservation data from the provided API URL.

    Args:
        api_url (str): The URL of the reservation API.
        headers (dict): Headers to include in the request.
        params (dict): Query parameters to include in the request.

    Returns:
        list: A list of reservation data dictionaries, or an empty list if the request fails.
    """
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("items", [])
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return []

if __name__ == "__main__":
    # Define API endpoint and headers
    url = "https://platform.opentable.com/sync/v2/reservations"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer cdb0aac7-8b06-4e9f-8f14-a35c187a7aab",
        "Cache-Control": "no-cache"
    }

    query_params = {
        "rid": 1027723,
        "limit": 1000,
        "guest_id": '6585f1fcb20d97d744d17511'
    }

    # Example: Fetch and print reservation data
    reservations = fetch_reservations(url, headers, query_params)
    #if reservations:
        #print(json.dumps(reservations, indent=4))
        #for reservation in reservations:
            #print(json.dumps(reservation, indent=4))