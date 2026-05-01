import yt_dlp
from kickapi import KickAPI
import cloudscraper
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
api = KickAPI()
session = cloudscraper.CloudScraper()

def get_video_stream_url(video_url: str) -> str | None:
        try:
            parts = video_url.split("/")
            if len(parts) < 6:
                return None
            
            channel_name = parts[3]
            video_slug = parts[5]
            print("Searching Videos...")
            video = search_video(channel_name, video_slug)

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
            if (stream_url is not None):
                return stream_url
            else:
                print("No stream URL found")
                return None
        except Exception as e:
            print(f"Error: {e}")
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
            urls.append(url)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(try_url, url): url for url in urls}
        for future in as_completed(futures):
            result = future.result()

            if result is not None:
                return result
    return None

def search_video(channel_name, video_slug):
    channel = api.channel(channel_name)

    for video in channel.videos:
        if video.uuid == video_slug:
            return video
        
    print("No video found")
    return None

def try_url(url):
    try:
        res = session.head(url, timeout=2)
        if res.status_code == 200:
            return url
    except:
        return None
    return None

def download_video(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    }

    yt_dlp.YoutubeDL(ydl_opts).download(url)