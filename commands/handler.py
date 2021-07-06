# Example Endpoint: http://tmi.twitch.tv/group/user/samora/chatters
from channel.channel import post_song

def songrequest(command):
    raw_song_req = command.split()[1:]
    parsed_song_req = ",".join(raw_song_req)
    if "youtube" not in parsed_song_req:
        return "Provide URL!"
    status = post_song(parsed_song_req)
    return f"Song Posted. {status}"

def soundeffect(command):
    raw_sound_req = command.split()[1:]
    parsed_sound_req = ",".join(raw_sound_req)
    return parsed_sound_req



