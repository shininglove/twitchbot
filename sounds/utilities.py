from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import normalize

max_volume = -20
min_volume = max_volume - 10


def play_song(song):
    dbs = song.dBFS
    difference = dbs - max_volume
    if dbs > max_volume or dbs < min_volume:
        song = song - difference
    play(song)


def play_song_limits(song_path, start, end):
    song = AudioSegment.from_mp3(song_path)
    seconds = 1000
    time_start = start * seconds
    time_end = end * seconds
    if song.duration_seconds > end:
        print("Trimming the song now...")
        limited_song = song[time_start:time_end]
        limited_song.export(song_path)
        play_song(limited_song)
    else:
        play_song(song)


# user_song = "./effects/turbo.mp3"
# play_song_limits(user_song,5,20)


def locate_sound(sound_name):
    sounds_location = Path("sounds/effects")
    full_sound_name = f"{sound_name}.mp3"
    sound_path = sounds_location / full_sound_name
    if sound_path.exists():
        return sound_path
    return False


def remove_sound(sound_name):
    sounds_location = Path("sounds/effects")
    full_sound_name = f"{sound_name}.mp3"
    sound_path = sounds_location / full_sound_name
    if sound_path.exists():
        sound_path.unlink()


def rename_sound(sound_name, new_name):
    sounds_location = Path("sounds/effects")
    full_sound_name = f"{sound_name}.mp3"
    sound_path = sounds_location / full_sound_name
    if sound_path.exists():
        sound_path.rename(sounds_location / f"{new_name}.mp3")
