import requests
import json
import os
import uuid
import time
from rich.console import Console
from rich.progress import track
from file_cruncher import files_to_write

console = Console()

# Get access token

data = {
    "client_id": os.environ.get("CLIENT_ID"),
    "client_secret": os.environ.get("CLIENT_SECRET"),
    "username": os.environ.get("API_USER"),
    "password": os.environ.get("API_PASSWORD"),
    "grant_type": "password",
}
token_url = "https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token"

response = requests.post(token_url, data=data)
if response.status_code == 200:
    response_data = response.json()
    access_token = response_data.get("access_token")
else:
    print("Failed to retrieve access token.")

# Get custom image ID

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
    "x-request-id": str(uuid.uuid4()),
    "x-trace-id": "123213",
}
image_url = "https://api.contabo.com/v1/compute/images?standardImage=false"

response = requests.get(image_url, headers=headers)
if response.status_code == 200:
    response_data = response.json()
    custom_image_id = response_data["data"][0]["imageId"]
else:
    print("Failed to retrieve custom image ID.")

# Reinstall

url = "https://api.contabo.com/v1/compute/instances/201332848"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + access_token,
    "x-request-id": str(uuid.uuid4()),
    "x-trace-id": "123213",
}
with open("base.yaml") as f:
    userData = f.read()

userData = userData + files_to_write()

data = {"imageId": custom_image_id, "userData": userData, "sshKeys": [73745]}

response = requests.put(url, headers=headers, data=json.dumps(data))

# Print response status code and content
if response.status_code == 200:
    console.print(":thumbs_up::thumbs_up::thumbs_up: GREAT SUCCESS!!")
    time_to_wait = 2 * 60
    for step in track(range(time_to_wait)):
        time.sleep(1)
else:
    console.print(
        f":face_vomiting::face_vomiting::face_vomiting: {response.json()['message']}"
    )
