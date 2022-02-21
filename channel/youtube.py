import os, requests
from isodate import parse_duration

youtube_api_key = os.getenv("YT_API_KEY")


def search_youtube(search_term):
    """
    Youtube Terms Search
    """
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": youtube_api_key,
        "q": search_term,
        "part": "snippet",
        "type": "video",
        "maxResults": 5,
    }

    response = requests.get(search_url, params=params)

    data = response.json()

    if data["items"] == []:
        return None

    video_id = data["items"][0]["id"]["videoId"]

    return video_id


def check_duration(video_id):
    """
    Use YT Video ID to check video's length (in minutes)
    """
    content_details = video_info(video_id)

    if content_details is None:
        return None

    duration_info = content_details["duration"]

    video_duration = parse_duration(duration_info).total_seconds()

    return video_duration


def video_info(video_id):
    """
    Youtube Video Info Search
    """
    video_info_url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "key": youtube_api_key,
        "id": video_id,
        "part": "snippet,contentDetails",
        "maxResults": 5,
    }

    response = requests.get(video_info_url, params=params)

    data = response.json()

    if data["items"]:
        content_details = data["items"][0]["contentDetails"]
    else:
        return None

    return content_details
