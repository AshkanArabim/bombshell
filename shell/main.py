import os, sys, re
from pprint import pprint


def printlist(X: list):
    for x in X:
        print(x)


def invalidArgs(arg):
    sys.stderr.write(f"{arg}: invalid argument!\n")


def notEnoughArgs():
    sys.stderr.write(f"Required arguments not provided!\n")


def invalidCommand(cmd):
    sys.stderr.write(f"{cmd}: command not found.\n")


# ques: how would you handle argument checking?
# I was thinking about having a dictionary of valid flags / parameters
if __name__ == "__main__":

    # main loop
    while True:
        command = input("$ ")
        command = command.strip()
        command = command.split(" ")

        # shell commands
        if command[0] == "ls":
            if len(command) > 1:
                invalidArgs(command[1])
                continue

            printlist(os.listdir())
            continue

        if command[0] == "exit":
            if len(command) > 1:
                invalidArgs(command[1])
                continue

            sys.exit()

        if command[0] == "cd":
            if len(command) > 2:
                invalidArgs(command[2])
                continue

            if len(command) < 2:
                notEnoughArgs()
                continue

            os.chdir(command[1])
            continue

        # current dir executables
        # TODO:

        # path commands
        # TODO:

        # if command not matched
        invalidCommand(command[0])