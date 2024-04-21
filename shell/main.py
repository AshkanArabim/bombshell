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
        command = [word for word in command.split(" ") if len(word) > 0]

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
        
        command_chop_positions = []
        
        # output redirection, if specified
        out_redirect_idxs = [i for i, e in enumerate(command) if e == ">"]
        if out_redirect_idxs: # if it's not empty
            out_redirect_idx = out_redirect_idxs[0]
            out_file_path = command[out_redirect_idx + 1] if out_redirect_idx + 1 < len(command) else ""
            
            temp_stdout = os.dup(1)
            os.close(1)
            fd = os.open(out_file_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
            os.set_inheritable(fd, True)
            command_chop_positions.append(out_redirect_idx)
        
        # input redirection, if specified
        in_redirect_idxs = [i for i, e in enumerate(command) if e == "<"]
        if in_redirect_idxs: # if it's not empty
            in_redirect_idx = in_redirect_idxs[0]
            in_file_path = command[in_redirect_idx + 1] if in_redirect_idx + 1 < len(command) else ""
            
            temp_stdin = os.dup(0)
            os.close(0)
            fd = os.open(in_file_path, os.O_RDONLY)
            os.set_inheritable(fd, True)
            command_chop_positions.append(in_redirect_idx)
        
        # chop of the redirection part of the command
        if command_chop_positions:
            command = command[:min(command_chop_positions)]

        # path commands
        # check if the command is in the path. if so, run it, if not, raise err
        try:
            pid = os.fork()

            if pid < 0:
                forkError()
            elif pid == 0:
                # child
                if command[0][:2] == "./":
                    os.execvp(command[0], command)
                else:
                    os.execvpe(command[0], command, os.environ)
            else:
                # parent
                waitForChild(pid)

        except FileNotFoundError as e:
            invalidCommand(command[0])
            sys.exit(1)  # if the command isnt' found, child should exit with err
        
        
        # remove output redirection, if used before
        if out_redirect_idxs:
            os.close(1)
            fd = os.dup(temp_stdout)
            os.set_inheritable(fd, True)
            os.close(temp_stdout)
        
        # remove input redirection, if used before
        # TODO: 
        if in_redirect_idxs:
            os.close(0)
            fd = os.dup(temp_stdin)
            os.set_inheritable(fd, True)
            os.close(temp_stdin)
        