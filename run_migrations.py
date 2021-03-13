import os

commands = [
    "piccolo migrations new user --auto; piccolo migrations forwards user",
    "piccolo migrations new session_auth --auto; piccolo migrations forwards session_auth",
    f"piccolo migrations new models --auto; piccolo migrations forwards models;",
]

for command in commands:
    os.system(command)
