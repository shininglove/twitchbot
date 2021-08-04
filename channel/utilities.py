import os, json
from channel.youtube import check_duration
from database.models import User, SongRequests, UserMessages, SoundEffects
from sounds.utilities import locate_sound, play_song_limits

limit_duration = os.getenv("LIMIT_SONG_LENGTH", "true").lower() == "true"
max_duration = int(os.getenv("MAX_SONG_DURATION"))


def verify_video(video_id):
    duration = check_duration(video_id)
    if duration is None:
        logger.debug(video_id)
        return "No Song Found."
    if limit_duration:
        max_duration_limit = max_duration * 60
        if duration > max_duration_limit:
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


def save_sound_effect(user, sound):
    """
    TODO: Auto approve mods and vips: scheduler download
    """
    current_user = User(user_id=user.user_id, name=user.display_name)
    saved_user = current_user.save()
    sound_effect = SoundEffects(
        user_id=saved_user.id,
        name=sound.name,
        url=sound.url,
        start_time=sound.start,
        end_time=sound.end,
        sound_type=sound.type
    )
    sound_status = sound_effect.save()
    return sound_status


def approve_sound_effect(username,sound_num):
    sound_effect = SoundEffects(id=sound_num)
    approved_status = sound_effect.approve()
    if approved_status is None:
        return "Sound effect doesn't exist."
    return f"@{username}, {approved_status}"


def find_sound_effect(sound_name):
    sound_effect = SoundEffects.find_sound(sound_name)
    return True if sound_effect else False


def play_sound_effect(sound_name):
    sound_effect = SoundEffects.find_sound(sound_name)
    sounds_location = locate_sound(sound_effect.name)
    if sounds_location:
        play_song_limits(sounds_location,sound_effect.start_time,sound_effect.end_time)


def play_theme_song(username):
    theme_sound_effect = SoundEffects.find_sound(username,sound_type="theme")
    sounds_location = locate_sound(theme_sound_effect.name)
    if sounds_location:
        play_song_limits(sounds_location,theme_sound_effect.start_time,theme_sound_effect.end_time)


def remove_sound_effect(sound_name):
    pass
