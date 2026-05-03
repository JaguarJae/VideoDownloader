import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

def get_token(client_id, client_secret):
    url = "https://id.kick.com/oauth/token"
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    r = requests.post(url, data=data, headers=token_headers)
    return r.json()["access_token"]

def get_broadcaster_user_id(channel_name):
    url = f"https://api.kick.com/public/v1/channels"
    
    params = {
        "slug": channel_name
    }
    r = requests.get(url, headers=headers, params=params)
    return(r.json()["data"][0]["broadcaster_user_id"])


def get_all_vods(channel_name):
    broadcaster_user_id = get_broadcaster_user_id(channel_name)
    url = f"https://api.kick.com/public/v1/livestreams"
    params = {
        "broadcaster_user_id": broadcaster_user_id,
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
    
    all_vods = get_all_vods(channel_name)
    vods = vod_filter(all_vods, days)
    return vods

load_dotenv()

client_id = os.getenv("KICK_CLIENT_ID")
client_secret = os.getenv("KICK_CLIENT_SECRET")

token = get_token(client_id, client_secret)

headers = {
    "Authorization": f"Bearer {token}"
}

print(get_all_vods("xQc"))