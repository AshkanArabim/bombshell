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


def forkError():
    sys.stderr.write("Failed to create fork...")


# waits for child. if it has an error, it writes to stdout
def waitForChild(pid: int):
    exit_status = os.waitid(os.P_PID, pid, os.WEXITED)
    exit_code = os.waitstatus_to_exitcode(exit_status.si_status)

    if exit_code != 0:
        sys.stderr.write(f"Process exited with error code: {exit_code}\n")

    # TODO: add reaping here?


# ans: should we also handle #! executables? --> no


# I was thinking about having a dictionary of valid flags / parameters
if __name__ == "__main__":

    # main loop
    while True:
        command = input("$ ")
        command = command.strip()
        command = command.split(" ")

        # shell commands
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

        # path commands
        # check if the command is in the path. if so, run it, if not, raise err
        try:
            pid = os.fork()

            if pid < 0:
                forkError()
            elif pid == 0:
                # child
                os.execvpe(command[0], command, os.environ)
            else:
                # parent
                waitForChild(pid)

            continue

        except FileNotFoundError as e:
            invalidCommand(command[0])
            sys.exit(1)  # if the command isnt' found, child should exit with err
