from downloaders import kick ,twitch, youtube
from urllib.parse import urlparse
import os
from vod_extractors import kick_vod_extractor, twitch_vod_extractor
import json
import argparse

def download_url(url):
    url_domain = urlparse(url).netloc

    match url_domain:
        case "www.youtube.com":
            print(url_domain, "--> Youtube")
            youtube.download_url(url)

        case "www.twitch.tv":
            print(url_domain, "--> Twitch")
            twitch.download_url(url)

        case "kick.com" | "stream.kick.com":
            print(url_domain, "--> Kick")
            kick.download_url(url)
        case _:
            print("Platform not supported")
    
def create_default_config():    
    default_config = {    
        "twitch": {
            "channels": "",
            "days": ""
        },        
        "kick": {
            "channels": "",
            "days": ""
        }
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
    print("Searching videos...")
    twitch_vods = twitch_vod_extractor.get_vods(twitch_channels, twitch_days)
    kick_vods = kick_vod_extractor.get_vods(kick_channels, kick_days)

    print("Downloading vods...")
    for twitch_vod in twitch_vods:
        download_url(twitch_vod)
        print("twitch downloaded")
        
    for kick_vod in kick_vods:
        download_url(kick_vod)
        print("kick downloaded")
else:
    for url in urls:
        download_url(url)
