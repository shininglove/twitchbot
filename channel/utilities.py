import os 
from channel.youtube import check_duration

limit_duration = os.getenv("LIMIT_SONG_LENGTH","true").lower() == "true"
max_duration = int(os.getenv("MAX_SONG_DURATION"))

def verify_video(video_id):
    if check_duration(video_id) is None:
        logger.debug(video_id)
        return "No Song Found."
    if limit_duration:
        if check_duration(video_id) > max_duration:
            return f"No Songs over {max_duration} mins."
    return None
