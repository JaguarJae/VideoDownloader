import downloader
from urllib.parse import urlparse




url = input("Video URL: ")

url_domain = urlparse(url).netloc

match url_domain:
    case "www.youtube.com":
        print(url_domain, "--> Youtube")
        downloader.download_video(url)

    case "www.twitch.tv":
        print(url_domain, "--> Twitch")
        downloader.download_video(url)

    case "kick.com":
        print(url_domain, "--> Kick")

        try: 
            downloader.download_video(url)
        except:
            print("Trying another way")
            kick_url = downloader.get_video_stream_url(url)
            if (kick_url != None):
                print("Found URL:", kick_url)
                downloader.download_video(kick_url)       