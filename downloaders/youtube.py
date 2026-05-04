import yt_dlp

def download_url(url):
    ydl_opts = {
        'outtmpl': f'downloads/youtube/%(title)s.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    }

    yt_dlp.YoutubeDL(ydl_opts).download(url)