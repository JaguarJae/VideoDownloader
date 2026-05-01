import yt_dlp

def download_video(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    }

    yt_dlp.YoutubeDL(ydl_opts).download(url)