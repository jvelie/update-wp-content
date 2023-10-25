import requests 
import json
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()    

api_key = os.getenv("API_KEY")
channel_id = os.getenv("CHANNEL_ID")

def get_live_video_id(api_key, channel_id):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': api_key,
        'channelId': channel_id,
        'part': 'snippet',
        'type': 'video',
        'eventType': 'completed',
        'maxResults': 1
    }
    
    response = requests.get(base_url, params=params)
    response_json = response.json()
    video_id = response_json['items'][0]['id']['videoId'] if response_json['items'] else None
    return video_id

video_id = get_live_video_id(api_key, channel_id,)

auth_value = os.getenv('AUTH_VALUE')
url_value = os.getenv('URL_VALUE')
url_encoded = urllib.parse.quote(url_value, safe=":/?&=")

headers = {
    'Authorization': auth_value,
    'User-Agent': '',
    'Content-Type': 'application/json'
}

response = requests.get(url_encoded, headers=headers)  

if response.status_code == 200:
    # If successful, parse the JSON response
    data = response.json()
else:
    # Handle unsuccessful response
    print(f"Unsuccessful request. Status code: {response.status_code}\nError message: {response.content}")

#Replace 'rendered' key 
if video_id:
    new_iframe = f'<iframe width="1080" height="566" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" loading="lazy"></iframe>'
    payload = {"content": {"rendered": new_iframe}}
    # Convert dictionary
    json_payload = json.dumps(payload)
    # Update content 
    update_response = requests.put(url_value, headers=headers, json=payload)
    print("Updated Rendered Content:", payload["content"]["rendered"])
    if update_response.status_code == 200:
        print("Updated successful")
    else:
        print("Update Failed", update_response.text)