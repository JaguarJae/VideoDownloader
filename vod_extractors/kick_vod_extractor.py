import requests
from datetime import datetime, timedelta


def get_all_vods(channel_name):
    response = requests.get(f"https://kick.com/api/v1/channels/{channel_name}")
    videos = response.json()["previous_livestreams"]

    return videos


def filter_videos(videos, days):
    limit = datetime.now() - timedelta(days=days)
    valid = []
    for video in videos:
        created_at = video["created_at"]
        video_date = datetime.fromisoformat(created_at)
        if video_date >= limit:
            valid.append(video)
    return valid

def get_vod_url(video):
    start_time = datetime.strptime(video["start_time"], "%Y-%m-%d %H:%M:%S")
    base_urls = [
            "https://stream.kick.com/ivs/v1/196233775518",
            "https://stream.kick.com/3c81249a5ce0/ivs/v1/196233775518",                        
            "https://stream.kick.com/0f3cb0ebce7/ivs/v1/196233775518"
        ]
    thumbnail_src_parts = video["thumbnail"]["src"].split("/")
    channel_id = thumbnail_src_parts[4]
    video_id = thumbnail_src_parts[5]
    video_url = search_url(start_time, base_urls, channel_id, video_id)
    return video_url

def search_url(start_time, base_urls, channel_id, video_id):
    urls = []
    for offset in range(-5, 6):
        adjusted_time = start_time + timedelta(minutes=offset)

        for base in base_urls:                                                    
            url = (
                    f"{base}/{channel_id}/{adjusted_time.year}/{adjusted_time.month}/"
                    f"{adjusted_time.day}/{adjusted_time.hour}/{adjusted_time.minute}/"
                    f"{video_id}/media/hls/master.m3u8"
                    )
            result = try_url(url)
            if result is not None:
                return url
    return "No URL found"

def try_url(url):
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return url
    return None

def get_vods(channel_name, days):
    all_videos = get_all_vods(channel_name)
    filtered_videos = filter_videos(all_videos, days)

    video_urls = []
    for video in filtered_videos:
        video_url = get_vod_url(video)
        video_urls.append(video_url)
    return video_urls
