import os, requests
from channel.models import SongDetails
from channel.utilities import verify_video
from channel.youtube import check_duration, search_youtube, video_info
from logger import logger

channel_id = os.getenv("BOT_CHANNEL_ID")
api_key = os.getenv("JWT_TOKEN")


def post_song(youtube_url):
    """
    YT URL: Cut after '?'
    """
    url_base = youtube_url.split("?")[-1].split("&")
    key, video_id = url_base[0].split("=")
    correct_video_response = verify_video(video_id)
    if correct_video_response is not None:
        return correct_video_response
    song_api_url = (
        f"https://api.streamelements.com/kappa/v2/songrequest/{channel_id}/queue"
    )
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"video": f"{video_id}"}
    response = requests.post(song_api_url, json=data, headers=headers)
    song_details = SongDetails(response.json())
    current_queue = song_queue()
    queue_ids = [item["_id"] for item in current_queue if current_queue]
    song_details.position = queue_ids.index(song_details.id) + 1
    return song_details.message()


def current_song(user):
    """
    Current YT URL: Cut after '?'
    """
    song_api_url = (
        f"https://api.streamelements.com/kappa/v2/songrequest/{channel_id}/playing"
    )
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(song_api_url, headers=headers)
    song_data = response.json()
    song_data["user"]["displayName"] = user
    song_details = SongDetails(song_data)
    return song_details.current_message()


def wrong_song(user):
    current_queue = song_queue()
    user_songs = []
    for song in current_queue:
        if song["user"]["username"] == user:
            user_songs.append(song["_id"])
    if user_songs == []:
        return "No songs in the queue."
    last_song_requested = user_songs[-1]
    song_api_url = f"https://api.streamelements.com/kappa/v2/songrequest/{channel_id}/queue/{last_song_requested}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.delete(song_api_url, headers=headers)
    return f"@{ user } Your last song was deleted."


def song_queue():
    song_api_url = (
        f"https://api.streamelements.com/kappa/v2/songrequest/{channel_id}/queue/public"
    )
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(song_api_url, headers=headers)
    queue_data = response.json()
    return queue_data


# post_song("https://www.youtube.com/watch?v=gVUIDqtw1bk")