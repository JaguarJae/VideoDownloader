import yt_dlp
from downloaders.free_patches import kick_free_patch

video_title = "default"

def raw_download(url, path, channel, platform, date):
    ydl_opts = {
        'outtmpl': f'{path}kick/{channel}/%(title)s-%(upload_date>%d-%m-%Y)s.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',

        "addmetadata": True,
        "parse_metadata": [
            f"{date}:%(meta_creation_time)s",
            f"{channel}:%(meta_artist)s",
            f"kick:%(meta_platform)s",
        ],
    }

    yt_dlp.YoutubeDL(ydl_opts).download(url)

def download_url(url, path):
    try: 
        raw_download(url, path)
    except:
        print("Trying another way...")
        raw_url = kick_free_patch.get_video_url_from_url(url)
        if (raw_url != None):
            print("Found URL:", raw_url)
            raw_download(raw_url, path)
        else:
            print("No URL found")

def download_video(video):
    video_url = kick_free_patch.get_video_url_from_url(video)
    video_channel = kick_free_patch.video_channel
    raw_download(video_url)
