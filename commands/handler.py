# Example Endpoint: http://tmi.twitch.tv/group/user/samora/chatters
from channel.twitch import post_song,current_song,wrong_song
from channel.youtube import search_youtube

def songrequest(command):
    if "youtube" not in command:
        raw_song_req = command.split()[1:]
        search_term = " ".join(raw_song_req)
        video_id = search_youtube(search_term)
        if video_id is None:
            return "Cannot find video."
        parsed_song_req = f"https://www.youtube.com/watch?v={video_id}"
    else:
        parsed_song_req = command.split()[1]
    status = post_song(parsed_song_req)
    return f"{status}"

def currentsong(user):
    return current_song(user)

def soundeffect(command):
    raw_sound_req = command.split()[1:]
    parsed_sound_req = ",".join(raw_sound_req)
    return parsed_sound_req

def wrongsong(user):
    return wrong_song(user)
