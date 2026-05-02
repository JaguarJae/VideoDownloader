from kickapi import KickAPI
from datetime import datetime, timedelta

kick_api = KickAPI()

def get_kick_vods(username, days):
    channel = kick_api.channel(username)
    allvideos = channel.videos
    print(allvideos[1].title, allvideos[1].stream)
    filtered_videos = filter_recent(allvideos, days)
    return filtered_videos

def filter_recent(vods, days):
    now = datetime.now()
    limit = now - timedelta(days=days)

    valid = []

    for vod in vods:
        created = vod.created_at
        video_date = datetime.fromisoformat(created)

        if video_date >= limit:
            print("video link:", vod.stream)
            valid.append(vod.stream)

    return valid

#it needs a functionaly api, as this api cannot retrieve the url from the videos