import os
from irc.bot import SingleServerIRCBot
import requests
from bot import TwitchBot

NAME = os.getenv("USERNAME")
CHANNEL = os.getenv("CHANNEL")
NICKNAME = os.getenv("USERNAME")

if __name__ == "__main__":
    bot = TwitchBot(NAME, NICKNAME, CHANNEL)
    print(bot.get_channel_id(CHANNEL))
    try:
        bot.start()
    except KeyboardInterrupt:
        print("Gracefully exiting ♥")
