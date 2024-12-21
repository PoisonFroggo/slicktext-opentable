import requests
import os
import pickle
#!/usr/bin/env python3.13

url = "https://platform.opentable.com/sync/v2/reservations"

query_params = {
    "confirmation_id": "7009",
    "state": "Done",
    "limit": 10,
    "offset": 0,
    "rid": 1027723
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 5b864d7a-99ba-40c8-9781-aa7f1a5aac89",
    "Cache-Control": "no-cache"
}

response = requests.get(url, headers=headers, params=query_params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")