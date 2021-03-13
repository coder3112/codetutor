import os

commands = [
    "piccolo migrations new user; piccolo migrations forwards user",
    "piccolo migrations new session_auth; piccolo migrations forwards session_auth",
    f"piccolo migrations new models; piccolo migrations forwards models;",
]

for command in commands:
    os.system(command)
