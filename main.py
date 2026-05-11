from downloaders import kick_downloader ,twitch_downloader, youtube_downloader
from vod_extractors import kick_vod_extractor, twitch_vod_extractor
from urllib.parse import urlparse
import os
import json
import argparse

def download_url(url):
    url_domain = urlparse(url).netloc

    match url_domain:
        case "www.youtube.com":
            youtube_downloader.download_url(url, path)

        case "www.twitch.tv":
            twitch_downloader.download_url(url, path)

        case "kick.com" | "stream.kick.com":
            kick_downloader.download_url(url, path)
        case _:
            print("Platform not supported")
    
def create_default_config():
    default_config = {    
        "twitch": {
            "channels": [""],
            "days": ""
        },        
        "kick": {
            "channels": [""],
            "days": ""
        },
        "path": ""
    }
    if not os.path.exists("config.json"):
        with open("config.json", "w") as file:
            json.dump(default_config, file, indent=4)

def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config

create_default_config()

config = load_config()

path = config["path"]

twitch_channels = config["twitch"]["channels"]
kick_channels = config["kick"]["channels"]

twitch_days = config["twitch"]["days"]
kick_days = config["kick"]["days"]

parser = argparse.ArgumentParser()

parser.add_argument("--url", nargs="+",type=str)

args = parser.parse_args()

urls = args.url

if urls == None:
    print("Reading config.json...")
    if twitch_channels != ['']:
        print("twitch channels", twitch_channels)
        for twitch_channel in twitch_channels:
            print(f"Searching {twitch_channel} videos...")
            twitch_vods = twitch_vod_extractor.get_vods(twitch_channel, twitch_days)
            if twitch_vods != None:
                for twitch_vod in twitch_vods:
                    download_url(twitch_vod)
            print(f"{twitch_channel} downloaded")

    if kick_channels != ['']:
        print("kick channels", kick_channels)
        for kick_channel in kick_channels:
            print(f"Searching {kick_channel} videos...")
            kick_vods = kick_vod_extractor.get_vods(kick_channel, kick_days)
            if kick_vods != None:
                for kick_vod in kick_vods:
                    download_url(kick_vod)
            print(f"{kick_channel} downloaded")
else:
    for url in urls:
        download_url(url)
