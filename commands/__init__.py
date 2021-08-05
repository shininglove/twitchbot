import os
from datetime import datetime
from commands.handler import (
    soundeffect,
    add_theme_song,
    songrequest,
    currentsong,
    wrongsong,
    save_user_message,
    approve_sound,
    search_sound,
    play_soundeffect,
    theme_song,
    search_command,
    delete_sound,
    command_updater
)


class Message:
    prefix = "!"
    output = None
    content = None

    def __init__(self, user, message):
        self.user = user
        self.username = user.display_name
        self.content = message
        user_message = save_user_message(user, message)
        if message.startswith(self.prefix):
            command = message.replace(self.prefix, "")
            self.parse(command)
        if user_message.first_message:
            print("First User Message")
            theme_song(self.username)

    def parse(self, raw_command):
        command_parts = raw_command.lower().split()
        if not command_parts:
            return None
        command = command_parts[0].lower()
        command_params = " ".join(command_parts[1:])
        saved_command = search_command(command)
        keyword = os.getenv("COMMAND_KEYWORD")

        if command == "time":
            self.output = datetime.now().strftime("%B %d %Y | %I:%M:%S %p")
        elif command == "currentsong" or command == "song":
            self.output = currentsong(self.username)
        elif command == "wrongsong" or command == "removesong":
            self.output = wrongsong(self.username)
        elif command == "sr" or command == "songrequest":
            self.output = songrequest(self.user, raw_command)
        elif command == "soundeffect":
            self.output = soundeffect(self.user, raw_command)
        elif command == "hi":
            self.output = f"@{self.username} HELLO"
        elif command == "approve":
            self.output = approve_sound(self.username,command_params)
        elif command == "deny":
            self.output = deny_sound(self.username,command_params)
        elif command == "themesong":
            self.output = add_theme_song(self.user, raw_command)
        elif command == "deletesound":
            self.output = delete_sound(command_params)
        elif command == keyword:
            self.output = command_updater(self.user,command_params)
        elif search_sound(command):
            play_soundeffect(command)
        if saved_command:
            self.output = saved_command.message
