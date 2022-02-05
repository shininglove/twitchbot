# Example Endpoint: http://tmi.twitch.tv/group/user/samora/chatters
import os
from channel.twitch import post_song, current_song, wrong_song,control_song
from channel.youtube import search_youtube
from channel.utilities import (
    save_song_request,
    save_message,
    save_sound_effect,
    approve_sound_effect,
    find_sound_effect,
    play_sound_effect,
    play_theme_song,
    find_command,
    remove_sound_effect,
    deny_sound_effect,
    update_command,
    find_all_sounds,
    rename_sound_effect,
    rename_theme_song
)
from commands.models import ChatSound

"""
TODO: Locking down approve.
"""


def songrequest(user, command):
    if "youtube" not in command and "youtu.be" not in command:
        raw_song_req = command.split()[1:]
        search_term = " ".join(raw_song_req)
        video_id = search_youtube(search_term)
        if video_id is None:
            return "Cannot find video."
        parsed_song_req = f"https://www.youtube.com/watch?v={video_id}"
    else:
        parsed_song_req = command.split()[1]
    save_song_request(user, parsed_song_req)
    status = post_song(parsed_song_req)
    return f"{status}"


def currentsong(user):
    return current_song(user)


def soundeffect(user, command):
    """
    Add Sounds to DB to be approved.
    """
    raw_sound_req = command.split()[1:]
    # hello https://youtube.com/watch? 00:05 00:10
    try:
        name, url, start_time, end_time = raw_sound_req
        sound = ChatSound(name, url, start_time, end_time)
        valid_sound = sound.valid_sound_duration()
    except ValueError as ve:
        print(ve)
        return f"@{ user.display_name }, example format: !soundeffect name url 00:00 00:05."
    if valid_sound:
        sound_effect = save_sound_effect(user, sound)
    else:
        return "Sound Length is not allowed"
    if sound_effect is not None:
        return f"{sound_effect.name} has been added and not approved yet. id: #{sound_effect.id}."
    return f"@{ user.display_name }, that sound name or url is already added"


def add_theme_song(user, command):
    """
    Add Sounds to DB to be approved.
    """
    raw_sound_req = command.split()[1:]
    # https://youtube.com/watch? 00:05 00:10
    name = user.display_name
    try:
        url, start_time, end_time = raw_sound_req
        sound = ChatSound(name, url, start_time, end_time, sound_type="theme")
        valid_sound = sound.valid_sound_duration()
    except ValueError as ve:
        print(ve)
        return f"@{ name }, example format: !themesong url 00:00 00:05."
    if valid_sound:
        sound_effect = save_sound_effect(user, sound)
    else:
        return "Theme Length is not allowed"
    if sound_effect is not None:
        return f"{sound_effect.name} has been added and not approved yet. id: #{sound_effect.id}."
    return f"@{ user.display_name }, you've already added your theme."


def wrongsong(user):
    return wrong_song(user)


def save_user_message(user, message):
    return save_message(user, message)


def approve_sound(username, sound_num):
    sound_num = sound_num.replace("#", "")
    try:
        sound_id = int(sound_num)
    except ValueError:
        return "Enter a valid number. example: !approve 1"
    return approve_sound_effect(username, sound_id)


def deny_sound(username, sound_num):
    sound_num = sound_num.replace("#", "")
    try:
        sound_id = int(sound_num)
    except ValueError:
        return "Enter a valid number. example: !deny 1"
    return deny_sound_effect(username, sound_id)


def search_sound(command):
    return find_sound_effect(command)


def get_sound_list(username):
    all_sounds = find_all_sounds()
    return f"@{username}, {all_sounds}"


def play_soundeffect(sound_name):
    with control_song(sound_name) as sound:
        play_sound_effect(sound)


def delete_sound(command_params):
    command_parts = command_params.split()
    if len(command_parts) != 1:
        return "Format: !deletesound sound_name"
    sound_name = command_parts[0]
    return remove_sound_effect(sound_name)


def theme_song(username):
    # change to decorator potentially
    with control_song(username) as song:
        play_theme_song(song)


def search_command(command):
    return find_command(command)

def rename_sounds(username,command_params, sound_type="sound"):
    try:
        sound_name, new_name = command_params.strip().split()
    except ValueError:
        return f"@{username}, too many paramaters!"
    if sound_type == "sound":
        return rename_sound_effect(username,sound_name,new_name)
    return rename_theme_song(username, sound_name, new_name)


def command_updater(user, command_params):
    keyword = os.getenv("COMMAND_KEYWORD")
    name = user.display_name
    try:
        command_parts = command_params.split()
        action = command_parts[0].lower()
        command_name = command_parts[1].lower()
        message = ""
        if action == "add" or action == "edit":
            message = " ".join(command_parts[2:])
            if not message:
                return (
                    f"@{ name }, example format: !{keyword} add/edit/delete [command]"
                )
    except IndexError:
        return f"@{ name }, example format: !{keyword} add/edit/delete [command]"
    update_status = update_command(user, action, command_name, message)
    if update_status is not None:
        return f"{command_name} has been {action}ed."
    return f"{command_name} command was already added."
