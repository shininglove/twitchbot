import os
from dotenv import load_dotenv

load_dotenv()
from channel.bot import TwitchBot

NAME = os.getenv("USERNAME")
CHANNEL = os.getenv("CHANNEL")
NICKNAME = os.getenv("USERNAME")

bot = TwitchBot(NAME, NICKNAME, CHANNEL)

if __name__ == "__main__":
    try:
        bot.start()
    except KeyboardInterrupt:
        print("Gracefully exiting ♥")
