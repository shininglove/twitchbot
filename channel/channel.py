import os,requests
from isodate import parse_duration
from channel.models import SongDetails
from logger import logger

channel_id = os.getenv("BOT_CHANNEL_ID")
api_key = os.getenv("JWT_TOKEN")
youtube_api_key = os.getenv("YT_API_KEY")
limit_duration = os.getenv("LIMIT_SONG_LENGTH","true").lower() == "true"
max_duration = int(os.getenv("MAX_SONG_DURATION"))


def post_song(youtube_url):
    """
    YT URL: Cut after '?'
    """
    url_base = youtube_url.split("?")[-1].split("&")
    key, video_id = url_base[0].split("=")
    if check_duration(video_id) is None:
        logger.debug(youtube_url)
        return "No Song Found."
    if limit_duration:
        if check_duration(video_id) > max_duration:
            return f"No Songs over {max_duration} mins."
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
    response = requests.get(song_api_url,headers=headers)
    song_data = response.json()
    song_data['user']['displayName'] = user
    song_details = SongDetails(song_data)
    return song_details.current_message()

def video_info(video_id):
    """
    Youtube Video Info Search
    """
    video_info_url = 'https://www.googleapis.com/youtube/v3/videos'

    params = {
        'key': youtube_api_key,
        'id': video_id,
        'part': 'snippet,contentDetails',
        'maxResults': 5
    }

    response = requests.get(video_info_url,params=params)

    data = response.json()

    if data['items']:
        content_details = data['items'][0]['contentDetails']
    else:
        return None

    return content_details

def check_duration(video_id):
    """
    Use YT Video ID to check video's length (in minutes)
    """
    content_details = video_info(video_id)

    if content_details is None:
        return None

    duration_info = content_details['duration']

    video_duration = parse_duration(duration_info).total_seconds() // 60

    return video_duration

def wrong_song(user):
    current_queue = song_queue()
    user_songs = []
    for song in current_queue:
        if song["user"]["username"] == user:
            user_songs.append(song["_id"])
    if user_songs == []:
        return "No songs in the queue."
    last_song_requested = user_songs[-1]
    song_api_url = (
        f"https://api.streamelements.com/kappa/v2/songrequest/{channel_id}/queue/{last_song_requested}"
    )
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.delete(song_api_url,headers=headers)
    return f"@{ user } Your last song was deleted."

def song_queue():
    song_api_url = (
        f"https://api.streamelements.com/kappa/v2/songrequest/{channel_id}/queue/public"
    )
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(song_api_url,headers=headers)
    queue_data = response.json()
    return queue_data

def search_youtube(search_term):
    """
    Youtube Terms Search
    """
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': youtube_api_key,
        'q': search_term,
        'part': 'snippet',
        'type': 'video',
        'videoDuration':'medium',
        'maxResults': 5
    }

    response = requests.get(search_url,params=params)

    data = response.json()

    if data['items'] == []:
        return None

    video_id = data['items'][0]['id']['videoId']

    return video_id

# search_youtube("dorime ameno")

# video_info("gVUIDqtw1bk")

# search_youtube("glass sky")

# post_song("https://www.youtube.com/watch?v=gVUIDqtw1bk")

