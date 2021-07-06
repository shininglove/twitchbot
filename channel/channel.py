import os,requests
from dotenv import load_dotenv
load_dotenv()

channel_id = os.getenv("CHANNEL_ID")
api_key = os.getenv("API_KEY")


def post_song(youtube_url):
    """
    YT URL: Cut after '?'
    """
    url_base = youtube_url.split("?")[-1].split("&")
    print(url_base[0].split("="))
    key, video_id = url_base[0].split("=")
    song_api_url = (
        f"https://api.streamelements.com/kappa/v2/songrequest/{channel_id}/queue"
    )
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"video": f"{video_id}"}
    response = requests.post(song_api_url, json=data, headers=headers)
    print(response.status_code)
    print(response.content)


post_song("https://www.youtube.com/watch?v=gVUIDqtw1bk")
