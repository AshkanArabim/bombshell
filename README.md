# Bombshell

A basic UNIX shell written in Python.

Originally a class assignment, it was fun enough for me to fork and expand it after the semester ended!

## Features
- Customizable PS1 variable
  - Currently only supports showing the username, machine name, and current directory.
- Pipes (e.g. `cat myfile.txt | tee copy.txt | wc`)
- PATH support - All installed binaries should work out of the box!
  - Local binaries can be used by adding a `./` to the beginning of their name.
- I/O redirection (e.g. `tar c < myfile > archive.tar`)
  - This can also be combined with pipes!
- Background tasks: just add a `&` at the end of your command.

## Usage
- Make sure you have Python installed.
- `python ./main.py`

## Implementation
- Uses the following POSIX calls:
  - `pipe()`
  - `fork()`
  - `dup()`
  - `execv()` and friends
  - `wait()`
  - `open()` and `close()`
  - `chdir()`

## Acknowledgements
Credits to [Eric Freudenthal](https://www.linkedin.com/in/eric-freudenthal-30503024/), professor
at the University of Texas at El Paso, for the assignment idea and part of the implementation.
