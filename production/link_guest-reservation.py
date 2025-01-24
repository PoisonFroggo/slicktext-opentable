import requests
import json
import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from get_guest_data import get_guest_info
from get_reservation_data import fetch_reservations

guest_url = "https://platform.opentable.com/sync/v2/guests"

def link_guest_and_reservation_data(guests, reservations):
    """Links guest and reservation data based on the matching 'id' field.

    Args:
        guests (list): List of guest dictionaries.
        reservations (list): List of reservation dictionaries.

    Returns:
        list: List of combined dictionaries where the 'id' matches.
    """
    # Create a dictionary for quick lookup of reservations by id
    reservation_dict = {reservation["id"]: reservation for reservation in reservations}

    combined_data = []

    for guest in guests:
        guest_id = guest.get("id")
        if guest_id in reservation_dict:
            combined_entry = {**guest, **reservation_dict[guest_id]}
            combined_data.append(combined_entry)

    return combined_data

def search_reservations_by_guest_id(reservation_api_url, headers, base_params, guest_id):
    """Searches reservations for a specific guest ID, returning reservations marked as 'Done'.

    Args:
        reservation_api_url (str): The URL of the reservation API.
        headers (dict): Headers to include in the request.
        base_params (dict): Base query parameters.
        guest_id (str): The guest ID to search for.

    Returns:
        list: A list of reservations marked as 'Done'.
    """
    # Extract the part after the hyphen in the guest ID
    filtered_id = guest_id.split("-")[-1]

    # Update the query parameters with the filtered guest ID
    params = base_params.copy()
    params["guest_id"] = filtered_id

    # Fetch reservations
    response = requests.get(reservation_api_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return [reservation for reservation in data.get("items", []) if reservation.get("state") == "Done"]
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return []

if __name__ == "__main__":
    # API endpoint and headers for guest data
    guest_api_url = "https://platform.opentable.com/sync/v2/guests"
    guest_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer cdb0aac7-8b06-4e9f-8f14-a35c187a7aab",
        "Cache-Control": "no-cache"
    }
    guest_params = {
        "email_optin": "true",
        "updated_after": "2020-01-07T00:00:01Z",
        "limit": 1000,
        "offset": 0,
        "rid": 1027723
    }

    # API endpoint and headers for reservation data
    reservation_api_url = "https://platform.opentable.com/sync/v2/reservations"
    reservation_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer cdb0aac7-8b06-4e9f-8f14-a35c187a7aab",
        "Cache-Control": "no-cache"
    }
    reservation_params = {
        "rid": 1027723,
        "limit": 10
    }

    # Fetch guest and reservation data
    guests = get_guest_info(guest_api_url, guest_headers, guest_params)
    reservations = fetch_reservations(reservation_api_url, reservation_headers, reservation_params)

    # Extract and process each guest's ID
    if guests:
        for guest in guests:
            guest_id = guest.get("id")
            if guest_id:
                # Search reservations for the guest ID
                done_reservations = search_reservations_by_guest_id(
                    reservation_api_url,
                    reservation_headers,
                    reservation_params,
                    guest_id
                )
                # If there are reservations marked as 'Done', print and return guest info
                if done_reservations:
                    full_name = f"{guest.get('first_name', 'Unknown')} {guest.get('last_name', 'Guest')}"
                    phone = guest.get("phone", "NULL")
                    print(f"Guest Name: {full_name}, Phone: {phone}")
                    #DEBUG PRINT. Use this to make sure all the information is associated properly. This will overflow the terminal window, recommend printing to a txt file later lol
                    #print(json.dumps(done_reservations, indent=4))