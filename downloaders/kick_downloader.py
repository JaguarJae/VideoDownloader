import yt_dlp
from downloaders.free_patches import kick_free_patch

video_title = "default"

def raw_download(url, title):
    ydl_opts = {
        'outtmpl': f'downloads/kick/{title}_%(title)s.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    }

    yt_dlp.YoutubeDL(ydl_opts).download(url)

def download_url(url):
    try: 
        raw_download(url, "master")
    except:
        print("Trying another way...")
        raw_url = kick_free_patch.get_video_url_from_url(url)
        if (raw_url != None):
            print("Found URL:", raw_url)
            raw_download(raw_url, video_title)
        else:
            print("No URL found")

def download_video(video):
    video_url = kick_free_patch.get_video_url_from_url(video)
    raw_download(video_url)
