from downloader import kickBackup
import yt_dlp
from urllib.parse import urlparse



def download_video(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    }

    yt_dlp.YoutubeDL(ydl_opts).download(url) # type: ignore

url = input("URL: ")

url_domain = urlparse(url).netloc

match url_domain:
    case "www.youtube.com":
        print(url_domain, "--> Youtube")
        download_video(url)

    case "www.twitch.tv":
        print(url_domain, "--> Twitch")
        download_video(url)

    case "kick.com":
        print(url_domain, "--> Kick")
        kick_url = (kickBackup.get_video_stream_url(url, "auto"))

        if (kick_url != None):

            print (kick_url)            
            download_video(kick_url)
        else:

            print("No url found")

    case "*kick.com":
        print(url_domain, "--> Kick")        

        download_video(url)



#print (url_domain)
#outube.download_video(url)