import os, sys, re, socket
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
    
    # set the PS1 shell variable
    PS1 = r"\u@\h \W$ "

    # main loop
    while True:
        # ans: does the PS1 prompt actually have to be the system one or is it just a local config? I assumed the latter --> an actual config
        
        hostname = socket.gethostname()
        username = os.getlogin()
        working_dir = os.getcwd()
        shell_prompt = PS1.replace(r"\u", username).replace("\h", hostname).replace("\W", working_dir) if len(PS1) > 0 else "$ "
        command = input(shell_prompt)
        
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
        
        # output redirection, if specified
        temp_stdout = -1
        out_file_path = ""
        if '>' in command:
            redirect_idx = command.index('>')
            out_file_path = command[redirect_idx + 1] if redirect_idx + 1 < len(command) else ""
            
            if out_file_path:
                temp_stdout = os.dup(1)
                os.close(1)
                fd = os.open(out_file_path, os.O_WRONLY | os.O_CREAT)
                os.set_inheritable(fd, True)
                command = command[:redirect_idx]

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

        except FileNotFoundError as e:
            invalidCommand(command[0])
            sys.exit(1)  # if the command isnt' found, child should exit with err
        
        
        # remove output redirection, if opened before
        if out_file_path:
            os.close(1)
            os.dup(temp_stdout)
            os.close(temp_stdout)
            
        
