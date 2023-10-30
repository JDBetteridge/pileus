import os
import sys

from argparse import ArgumentParser
from getpass import getuser
from process import ProcessFile, count_ranks
from subprocess import Popen


# True location of MPI launcher
MPI_EXEC = '/opt/mpich/bin/mpiexec.hydra'


def print_user_info():
    print(f'Username   : {getuser()}')
    print(f'Loginname  : {os.getlogin()}')
    print(f'UID        : {os.getuid()}')
    print(f'Python PID : {os.getpid()}')
    print()


def main(known, unknown):
    # ~ print(f'{known._get_args() = }')
    # ~ print(f'{unknown = }')
    # ~ print(f'RANKS: {count_ranks(unknown)}')

    mpiexec = MPI_EXEC
    status = Popen(
        [mpiexec] + unknown,
        stdout=sys.stdout,
        stderr=sys.stderr,
        start_new_session=True
    )
    # ~ print(f'PID: {status.pid}')

    user_process_file = ProcessFile()
    # TODO: detect the number of ranks requested
    user_process_file.add_pid(status.pid, size=count_ranks(unknown))

    status.wait()

    user_process_file.remove_pid(status.pid)


if __name__ == '__main__':
    parser = ArgumentParser(add_help=False)
    known, unknown = parser.parse_known_args()
    # ~ print_user_info()
    main(known, unknown)
