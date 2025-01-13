import requests
import json
import os
import pickle
from datetime import date
from datetime import datetime, timezone
#!/usr/bin/env python3.13

now = datetime.now(timezone.utc)
formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S")  # Basic format
fractional_seconds = f"{now.microsecond // 1000:03d}"  # Milliseconds
timezone_offset = "+0000"  # Assuming UTC timezone
current_date = f"{formatted_date}.{fractional_seconds}{timezone_offset}"

url = "https://platform.opentable.com/sync/v2/reservations"

query_params = {
    "rid": 1027723,
    "limit" : 10
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer cdb0aac7-8b06-4e9f-8f14-a35c187a7aab",
    "Cache-Control": "no-cache"
}

response = requests.get(url, headers=headers, params=query_params)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))

    #print(data)

else:
    print(f"Request failed with status code {response.status_code}: {response.text}")