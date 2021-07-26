# Example Endpoint: http://tmi.twitch.tv/group/user/samora/chatters
from channel.twitch import post_song, current_song, wrong_song
from channel.youtube import search_youtube
from channel.utilities import save_song_request, save_message, save_sound_effect
from commands.models import ChatSound


def songrequest(user, command):
    if "youtube" not in command:
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


def soundeffect(user,command):
    """
    Add Sounds to DB to be approved.
    """
    raw_sound_req = command.split()[1:]
    # hello https://youtube.com/watch? 00:05 00:10
    try:
        name, url, start_time, end_time = raw_sound_req
        if "youtube" not in url:
            raise ValueError
        if ":" not in start_time or ":" not in end_time:
            raise ValueError
    except ValueError:
        return f"@{ user.display_name }, example format: !soundeffect [name] [url] 00:00 00:05."
    sound = ChatSound(name,url,start_time,end_time)
    valid_sound = sound.valid_sound_duration()
    if valid_sound:
        sound_effect = save_sound_effect(user,sound)
    else:
        return "Sound Length is not allowed"
    if sound_effect is not None:
        return f"{sound_effect.name} has been added and not approved yet."
    return f"@{ user.display_name }, that sound name is already added"


def wrongsong(user):
    return wrong_song(user)

def save_user_message(user, message):
    return save_message(user, message)

