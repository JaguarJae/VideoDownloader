from datetime import datetime, timedelta
import requests

def get_video_url_from_url(url):
    url_parts = url.split("/")
    video_uuid = url_parts[5]
    video_channel = url_parts[3]
    video = search_video(video_channel, video_uuid)
    video_url = get_video_url(video)
    return video_url




def get_all_vods(channel_name):
    response = requests.get(f"https://kick.com/api/v1/channels/{channel_name}")
    videos = response.json()["previous_livestreams"]

    return videos

def search_video(channel_name, video_uuid):
    videos = get_all_vods(channel_name)

    for video in videos:
        if video["video"]["uuid"] == video_uuid:
            return video
        
    print("No video found")
    return None

def get_video_url(video):
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
