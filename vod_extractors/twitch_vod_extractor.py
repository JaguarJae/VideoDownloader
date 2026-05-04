import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

def get_token(client_id, client_secret):
    url = "https://id.twitch.tv/oauth2/token"

    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    r = requests.post(url, params=params)
    return r.json()["access_token"]

def get_user_id(channel_name):
    url = f"https://api.twitch.tv/helix/users/"
    
    params = {
        "login": channel_name
    }
    r = requests.get(url, headers=headers, params=params)
    return(r.json()["data"][0]["id"])

def all_vods_extractor(channel_name):
    user_id = get_user_id(channel_name)
    url = "https://api.twitch.tv/helix/videos/"
    params = {
        "user_id": user_id,
        "period": "month"
    }

    r = requests.get(url, headers=headers, params=params)
    return r.json()["data"]

def vod_filter(vods, days):
    now = datetime.now(timezone.utc)
    limit = now - timedelta(days=days)
    valid = []
    for vod in vods:
        created_at = vod["created_at"]
        video_date = datetime.fromisoformat(created_at)
        if (video_date >= limit):
            valid.append(vod["url"])
    return valid

def get_vods(channel_name, days):
    if channel_name == "" or days == "":
        return "No channel or days"
    all_vods = all_vods_extractor(channel_name)
    vods = vod_filter(all_vods, float(days))
    return vods

load_dotenv()

client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")

token = get_token(client_id, client_secret)

headers = {
    "Client-ID": client_id,
    "Authorization": f"Bearer {token}"
}