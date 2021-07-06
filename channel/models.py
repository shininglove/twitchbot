import datetime

class SongDetails:

    def __init__(self,data):
        self.title = data['title']
        self.duration = self.parse_duration(data['duration'])
        self.user = data['user']['displayName']

    @staticmethod
    def parse_duration(duration):
        raw_duration = datetime.timedelta(seconds=int(duration))
        hour,mins,secs = str(raw_duration).split(":")
        return f"{mins} mins {secs} secs"

    def message(self):
        user_message = f'@{self.user} added "{self.title}" to queue ({self.duration})'
        return user_message

