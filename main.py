from downloaders import kick ,twitch, youtube
from urllib.parse import urlparse
import os
from vod_extractors import kick_vod_extractor, twitch_vod_extractor

#url = input("Video URL: ")
#url_domain = urlparse(url).netloc
days = 10
paths = [
    "downloads",
    "downloads/youtube",
    "downloads/twitch",
    "downloads/kick"
]
for path in paths:
    os.makedirs(path, exist_ok=True)

twitch_videos = twitch_vod_extractor.get_vods("peereira7", 6)
print("videos:", twitch_videos)


for video in twitch_videos:
    url = video
    print("URL:", url)
    url_domain = urlparse(url).netloc

    match url_domain:
        case "www.youtube.com":
            print(url_domain, "--> Youtube")
            #youtube.download_url(url)

        case "www.twitch.tv":
            print(url_domain, "--> Twitch")
            #twitch.download_url(url)

        case "kick.com":
            print(url_domain, "--> Kick")
            #kick.download_url(url)