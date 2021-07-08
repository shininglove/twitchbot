import os
from irc.bot import SingleServerIRCBot
import requests
from logger import logger
from commands import Message

CLIENT_ID = os.getenv("CLIENT_ID")
TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")

class TwitchBot(SingleServerIRCBot):

    host = "irc.chat.twitch.tv"
    port = 6667
    client_id = CLIENT_ID
    token = TOKEN

    def __init__(self, name, nickname, channel):
        self.username = name
        self.nickname = nickname
        self.channel = f"#{channel}"
        super().__init__(
            [(self.host, self.port, f"{self.token}")],
            self.username,
            self.nickname,
        )

    def get_channel_id(self, channel):
        url = f"https://api.twitch.tv/kraken/users?login={channel}"
        headers = {
            "Client-ID": self.client_id,
            "Accept": "application/vnd.twitchtv.v5+json",
        }
        response = requests.get(url, headers=headers).json()
        self.channel_id = response["users"][0]["_id"]
        return self.channel_id

    def on_welcome(self, conn, event):
        for req in ("membership", "tags", "commands"):
            conn.cap("REQ", f":twitch.tv/{req}")
        conn.join(self.channel)
        print("Now online")

    def on_pubmsg(self, conn, event):
        tags = Tags(event.tags)
        message = event.arguments[0]
        cmd = Message(tags, message).output
        if cmd:
            self.send_message(cmd)
        # print(event.tags)
        logger.debug(f"Message from {tags.display_name} (user_id:{tags.user_id}) : {message}")

    def send_message(self, message):
        self.connection.privmsg(self.channel, message)


class Tags:
    def __init__(self, user_info):
        for item in user_info:
            item["key"] = self.parse_tag(item["key"])
            setattr(self, item["key"], item["value"])

    @staticmethod
    def parse_tag(item):
        if "-" in item:
            item = item.replace("-", "_")
        return item


