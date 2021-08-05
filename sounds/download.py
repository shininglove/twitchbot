from __future__ import unicode_literals
from pathlib import Path
import youtube_dl
from sounds.output import logger

sounds_path = Path("sounds/effects").resolve()


def download_song(sound_effect):
    sound_name = sound_effect.name
    ydl_opts = {
        "outtmpl": f"{sounds_path}/{sound_name}.%(ext)s",
        "format": "bestaudio/best",
        "logger": logger,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([sound_effect.url])
    except Exception as e:
        logger.debug(f"Error while downloading {e}")
        return False
    return True
