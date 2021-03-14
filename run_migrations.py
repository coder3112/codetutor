import os

commands = [
    "piccolo migrations forwards user",
    "piccolo migrations forwards session_auth",
    "piccolo migrations forwards models;",
]

for command in commands:
    os.system(command)
