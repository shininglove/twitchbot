import os, json
from channel.youtube import check_duration
from database.models import User, SongRequests, UserMessages, SoundEffects

limit_duration = os.getenv("LIMIT_SONG_LENGTH", "true").lower() == "true"
max_duration = int(os.getenv("MAX_SONG_DURATION"))


def verify_video(video_id):
    if check_duration(video_id) is None:
        logger.debug(video_id)
        return "No Song Found."
    if limit_duration:
        max_duration_limit = max_duration * 60
        if check_duration(video_id) > max_duration_limit:
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

def save_sound_effect(user,sound):
    current_user = User(user_id=user.user_id, name=user.display_name)
    saved_user = current_user.save()
    sound_effect = SoundEffects(
        user_id=saved_user.id,
        name = sound.name,
        url = sound.url,
        start_time = sound.start,
        end_time = sound.end
    )
    sound_status = sound_effect.save()
    return sound_status

def approve_sound_effect(sound):
    pass


def play_sound_effect(user,sound):
    pass

def play_theme_song(user):
    pass
