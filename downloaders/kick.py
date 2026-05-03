import yt_dlp
from kickapi import KickAPI
import requests
from datetime import datetime, timedelta

api = KickAPI()

def get_raw_stream_url(video_url):

    parts = video_url.split("/")
    if len(parts) < 6:
        return None
            
    channel_name = parts[3]
    video_slug = parts[5]
    print("Searching Videos...")
    video = search_videos(channel_name, video_slug)

    thumbnail_url = video.thumbnail["src"]
    start_time = datetime.strptime(video.start_time, "%Y-%m-%d %H:%M:%S")
    path_parts = thumbnail_url.split("/")
    channel_id, video_id = path_parts[4], path_parts[5]
    base_urls = [
        "https://stream.kick.com/ivs/v1/196233775518",
        "https://stream.kick.com/3c81249a5ce0/ivs/v1/196233775518",                        
        "https://stream.kick.com/0f3cb0ebce7/ivs/v1/196233775518"
    ]
    print("Searching URL...")

    stream_url = search_url(start_time, base_urls, channel_id, video_id)
    return stream_url

def search_videos(channel_name, video_slug):
    channel = api.channel(channel_name)

    for video in channel.videos:
        if video.uuid == video_slug:
            return video
        
    print("No video found")
    return None

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

def raw_download(url, platform):
    ydl_opts = {
        'outtmpl': f'downloads/{platform}/%(title)s.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    }

    yt_dlp.YoutubeDL(ydl_opts).download(url)

def download_url(url):
    try: 
        raw_download(url, "kick")
    except:
        print("Trying another way")
        raw_url = get_raw_stream_url(url)
        if (raw_url != None):
            print("Found URL:", raw_url)
            raw_download(raw_url, "kick")