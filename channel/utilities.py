import os, json
from channel.youtube import check_duration
from database.models import User, SongRequests, UserMessages

limit_duration = os.getenv("LIMIT_SONG_LENGTH", "true").lower() == "true"
max_duration = int(os.getenv("MAX_SONG_DURATION"))


def verify_video(video_id):
    if check_duration(video_id) is None:
        logger.debug(video_id)
        return "No Song Found."
    if limit_duration:
        if check_duration(video_id) > max_duration:
            return f"No Songs over {max_duration} mins."
    return None


def save_song_request(user, request):
    current_user = User(user_id=user.user_id, name=user.display_name)
    saved_user = current_user.save()
    song_request = SongRequests(user_id=saved_user.id, url=request)
    song_request.save()


def save_message(user, message):
    current_user = User(user_id=user.user_id, name=user.display_name)
    saved_user = current_user.save()
    user_message = UserMessages(user_id=saved_user.id, message=message)
    user_message.save()
    return user_message

