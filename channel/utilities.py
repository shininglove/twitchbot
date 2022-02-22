import os
from logger import logger
from channel.youtube import check_duration
from database.models import User, SongRequests, UserMessages, SoundEffects, UserCommands
from sounds.utilities import locate_sound, play_song_limits, remove_sound

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


def update_command(user, action, command_name, message):
    current_user = User(user_id=user.user_id, name=user.display_name)
    saved_user = current_user.save()
    user_command = UserCommands(
        user_id=saved_user.id, command_name=command_name, message=message
    )
    if action == "add":
        user_command.save()
    elif action == "edit":
        user_command.update_command()
    elif action == "delete":
        user_command.delete_command()
    return user_command


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
        sound_type=sound.type,
    )
    sound_status = sound_effect.save()
    return sound_status


def approve_sound_effect(username, sound_num):
    sound_effect = SoundEffects(id=sound_num)
    approved_status = sound_effect.approve()
    if approved_status is None:
        return "Sound effect doesn't exist."
    return f"@{username}, {approved_status}"


def deny_sound_effect(username, sound_num):
    sound_effect = SoundEffects(id=sound_num)
    deny_status = sound_effect.delete_sound()
    if deny_status is None:
        return "Sound effect doesn't exist."
    return f"@{username}, {deny_status}"


def rename_sound_effect(username, sound_name, new_name):
    sound_effect = SoundEffects.find_sound(sound_name)
    if sound_effect is None:
        return "Sound effect doesn't exist."
    sound_effect.name = new_name
    sound_status = sound_effect.save()
    return f"@{username}, {sound_name} changed to {sound_status.name}"


def rename_theme_song(username, theme_name, new_name):
    sound_effect = SoundEffects.find_sound(theme_name, sound_type="theme")
    if sound_effect is None:
        return "Sound effect doesn't exist."
    sound_effect.name = new_name
    sound_status = sound_effect.save()
    return f"@{username}, {theme_name} changed to {sound_status.name}"


def find_sound_effect(sound_name):
    sound_effect = SoundEffects.find_sound(sound_name)
    return True if sound_effect else False


def find_all_sounds():
    sound_list = SoundEffects.find_all_sounds()
    return ", ".join([sound.name for sound in sound_list])


def play_sound_effect(sound_name):
    sound_effect = SoundEffects.find_sound(sound_name)
    sounds_location = locate_sound(sound_effect.name)
    if sounds_location:
        play_song_limits(
            sounds_location, sound_effect.start_time, sound_effect.end_time
        )


def play_theme_song(username):
    theme_sound_effect = SoundEffects.find_sound(username, sound_type="theme")
    if theme_sound_effect:
        sounds_location = locate_sound(theme_sound_effect.name)
        if sounds_location:
            play_song_limits(
                sounds_location,
                theme_sound_effect.start_time,
                theme_sound_effect.end_time,
            )


def remove_sound_effect(sound_name):
    sound_effect = SoundEffects.find_sound(sound_name)
    sounds_location = locate_sound(sound_effect.name)
    if sounds_location:
        remove_sound(sound_name)
        sound_effect.delete_sound()
    return f"Sound Effect: {sound_effect.name} has been deleted"


def find_command(command):
    user_command = UserCommands(command_name=command)
    return user_command.find_command()
