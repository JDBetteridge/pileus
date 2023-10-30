#!/usr/bin/python3.11
import os
import sys

from argparse import ArgumentParser
from getpass import getuser
from subprocess import Popen

from .process import ProcessFile, count_ranks


# True location of MPI launcher
MPI_EXEC = '/data/shared/pileus/petsc/packages/bin/mpiexec.hydra'


def print_user_info():
    print(f'Username   : {getuser()}')
    print(f'Loginname  : {os.getlogin()}')
    print(f'UID        : {os.getuid()}')
    print(f'Python PID : {os.getpid()}')
    print()


def main():
    parser = ArgumentParser(add_help=False)
    known, unknown = parser.parse_known_args()

    mpiexec = MPI_EXEC
    status = Popen(
        [mpiexec] + unknown,
        stdout=sys.stdout,
        stderr=sys.stderr,
        start_new_session=True
    )

    user_process_file = ProcessFile()
    user_process_file.add_pid(status.pid, size=count_ranks(unknown))

    status.wait()

    user_process_file.remove_pid(status.pid)


if __name__ == '__main__':
    main()
