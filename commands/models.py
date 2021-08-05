import os
from channel.youtube import check_duration
from logger import logger


class ChatSound:
    def __init__(self, name, url, start, end, sound_type="sound"):
        self.name = name
        self.url = url
        self.start = self.parse_time(start)
        self.end = self.parse_time(end)
        self.type = sound_type

    def parse_time(self, time_command):
        mins, secs = time_command.split(":")
        minutes_in_seconds = int(mins) * 60
        seconds = int(secs)
        return minutes_in_seconds + seconds

    def valid_sound_duration(self):
        max_duration = int(os.getenv("MAX_SOUND_DURATION")) * 60
        max_play_length = int(os.getenv("MAX_ALLOWED_PLAY_LENGTH"))
        if self.start > self.end:
            return False
        if self.end > max_duration:
            logger.debug(f"End:{self.end}")
            return False
        if (self.end - self.start) > max_play_length:
            logger.debug(f"Length: {self.end - self.start}")
            return False
        url_base = self.url.split("?")[-1].split("&")
        key, video_id = url_base[0].split("=")
        vid_duration = check_duration(video_id)
        if vid_duration > max_duration:
            logger.debug("Vid Duration: {vid_duration}")
            return False
        logger.debug(f"MAX:{vid_duration} START:{self.start} END:{self.end} ")
        if self.start > vid_duration or self.end > vid_duration:
            logger.debug("Length doesn't make sense")
            return False
        return True
