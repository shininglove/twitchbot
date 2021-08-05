import os, argparse
from dotenv import load_dotenv

load_dotenv()
from database.models import (
    User,
    SoundEffects,
    SongRequests,
    UserCommands,
    UserMessages,
    db,
)
from database.utilities import create_table, delete_table, engine

parser = argparse.ArgumentParser()

parser.add_argument("operation", nargs="+", help="create all or delete all")

args = parser.parse_args()

print(args.operation)

operation = " ".join(args.operation)

operation_names = args.operation[0].split(" ")

database_names = [UserCommands, UserMessages, SongRequests, SoundEffects]

if operation == "build":
    create_names = database_names
    first_db = create_names.pop()
    print(create_table(first_db))
    for names in create_names:
        print(create_table(names))
elif operation == "destroy":
    for names in database_names:
        print(delete_table(names))
elif operation.startswith("create"):
    if operation_names[1].lower() == "user":
        print(create_table(User))
    elif operation_names[1].lower() == "requests":
        print(create_table(SongRequests))
    elif operation_names[1].lower() == "messages":
        print(create_table(UserMessages))
    elif operation_names[1].lower() == "effects":
        print(create_table(SoundEffects))
    elif operation_names[1].lower() == "commands":
        print(create_table(UserCommands))
elif operation.startswith("delete"):
    if operation_names[1].lower() == "user":
        print(delete_table(User))
    elif operation_names[1].lower() == "requests":
        print(delete_table(SongRequests))
    elif operation_names[1].lower() == "messages":
        print(delete_table(UserMessages))
    elif operation_names[1].lower() == "effects":
        print(delete_table(SoundEffects))
    elif operation_names[1].lower() == "commands":
        print(delete_table(UserCommands))
