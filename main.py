from downloaders import kick ,twitch, youtube
from urllib.parse import urlparse
import os
from vod_extractors import kick_vod_extractor, twitch_vod_extractor
import json

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
youtube_channels = config["youtube"]["channels"]
kick_channels = config["kick"]["channels"]

twitch_days = config["twitch"]["days"]
youtube_days = config["youtube"]["days"]
kick_days = config["kick"]["days"]

def ask_input():
    print("Input URL --> 0 \nRead config.json --> 1 ")
    option = input("Choose Option: ")
    if option == "0":
        url = input("URL: ")
        print("Downloadng URL...")
        option_url(url)
    elif option == "1":
        print("Reading File...")
        print("Searching Videos...")
        option_config()
    else:
        print("Bad Input")
        ask_input()

def option_url(url):
    download_url(url)

def option_config():
    twitch_vods = twitch_vod_extractor.get_vods(twitch_channels, twitch_days)
    kick_vods = kick_vod_extractor.get_vods(kick_channels, kick_days)
    print("twitch vods", twitch_vods)
    print("kick vods", kick_vods)
    download_confirmation = input("Do you want to download this vods? y/n: ")
    if download_confirmation in ["y", "Y"]:
        print("Downloading vods...")
        for twitch_vod in twitch_vods:
            download_url(twitch_vod)
            print("twitch downloaded")
        
        for kick_vod in kick_vods:
            print("Downloading kick")
            download_url(kick_vod)
            print("kick downloaded")

ask_input()