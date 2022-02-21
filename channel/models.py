import datetime


class SongDetails:
    def __init__(self, data):
        self.data = data
        self.id = data.get("_id")
        self.title = data.get("title")
        self.video_id = data.get("videoId")
        self.duration = self.parse_duration(data.get("duration", 0))
        self.user = data.get("user", {"displayName": "You"}).get("displayName")
        self.channel = data.get("channel")
        self.position = None

    @staticmethod
    def parse_duration(duration):
        raw_duration = datetime.timedelta(seconds=int(duration))
        _, mins, secs = str(raw_duration).split(":")
        return f"{mins} mins {secs} secs"

    def message(self):
        user_message = f'Song Posted. @{self.user} added {self.channel} - "{self.title}" to queue at #{self.position} ({self.duration})'
        return user_message

    def current_message(self):
        user_message = f'@{self.user}, Song: {self.channel} - "{self.title}" to queue ({self.duration}) by {self.data["user"]["username"]}'
        return user_message
