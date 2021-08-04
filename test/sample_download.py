from __future__ import unicode_literals
from pathlib import Path
import youtube_dl

ydl_opts = {
    'outtmpl': './sounds/background_sound.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=06EUC53ooH0'])
