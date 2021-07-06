from datetime import datetime

class Message:
    prefix = "!"
    output = None
    content = None

    def __init__(self, user, message):
        self.user = user
        self.content = message
        if message.startswith(self.prefix):
            command = message.replace(self.prefix, "")
            self.parse(command)

    def parse(self, command):
        if command == "month":
            self.output = datetime.now().strftime("%B")
        if command.startswith("say"):
            self.output = " ".join(command.split(" ")[1:])
        if command == "hi":
            self.output = f"@{self.user} HELLO"
        if command == "bye":
            self.output = f"@{self.user} EVERYONE LOVES YOU"
