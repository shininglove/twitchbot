import os,requests
from channel.models import SongDetails

channel_id = os.getenv("BOT_CHANNEL_ID")
api_key = os.getenv("JWT_TOKEN")


def post_song(youtube_url):
    """
    YT URL: Cut after '?'
    """
    url_base = youtube_url.split("?")[-1].split("&")
    # print(url_base[0].split("="))
    key, video_id = url_base[0].split("=")
    song_api_url = (
        f"https://api.streamelements.com/kappa/v2/songrequest/{channel_id}/queue"
    )
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"video": f"{video_id}"}
    response = requests.post(song_api_url, json=data, headers=headers)
    song_details = SongDetails(response.json())
    return song_details.message()

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

    content_details = data['items'][0]['contentDetails']

    # duration_info = content_details['duration']

    # video_duration = parse_duration(duration_info).total_seconds() // 60

    return content_details

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

    print(data['items'][0])

# search_youtube("dorime ameno")

# video_info("gVUIDqtw1bk")

# search_youtube("glass sky")

# post_song("https://www.youtube.com/watch?v=gVUIDqtw1bk")

