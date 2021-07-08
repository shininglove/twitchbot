from datetime import datetime
from commands.handler import soundeffect, songrequest,currentsong,wrongsong

class Message:
    prefix = "!"
    output = None
    content = None

    def __init__(self, user, message):
        self.user = user
        self.username = user.display_name
        self.content = message
        if message.startswith(self.prefix):
            command = message.replace(self.prefix, "")
            self.parse(command)

    def parse(self, raw_command):
        command = raw_command.split()[0]
        if command == "time":
            self.output = datetime.now().strftime("%B %d %Y | %I:%M:%S %p")
        if command == "currentsong" or command == "song":
            self.output = currentsong(self.username)
        if command == "wrongsong" or command == "removesong":
            self.output = wrongsong(self.username)
        if command == "sr" or command == "songrequest":
            self.output = songrequest(raw_command)
        if command == "soundeffect":
            self.output = soundeffect(raw_command)
        if command == "hi":
            self.output = f"@{self.user} HELLO"
