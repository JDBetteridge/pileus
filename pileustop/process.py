import os

from collections import namedtuple
from getpass import getuser


Row = namedtuple('Row', ['pid', 'user', 'command', 'ncpu', 'mem', 'start'])


RUN_DIR = '/run/pileustop'


def split_colon(alist):
    returnlist = []
    block = []
    for item in alist:
        if item == ':':
            returnlist.append(block)
            block = []
        else:
            block.append(item)
    returnlist.append(block)
    return returnlist


def count_ranks(mpiargs):
    split = split_colon(mpiargs)
    total = 0
    for block in split:
        for ii, item in enumerate(block):
            if item in ['-n', '-np', '-ppn']:
                total += int(block[ii + 1])
                break
    return total


def ensure_directory():
    prev = os.umask(0)
    try:
        # Create a directory with 777 permissions in system location
        # This requires sudo :-/
        os.makedirs(RUN_DIR, mode=0o777, exist_ok=True)
    except PermissionError as e:
        print(
            'Insufficent permission, ask your administrator to run\n'
            f'\tsudo mkdir {RUN_DIR}; sudo chmod 777 {RUN_DIR}'
        )
        raise e
    os.umask(prev)


def opw_opener(filename, flags):
    # Create a file with 666 permissions
    prev = os.umask(0)
    descriptor = os.open(filename, flags, mode=0o666)
    os.umask(prev)
    return descriptor


class ProcessFile:
    def __init__(self, filename=None):
        ensure_directory()
        if filename:
            self.filename = filename
        else:
            self.filename = f'{RUN_DIR}/{getuser()}-{os.getuid()}.db'

    def add_pid(self, pid, size=1):
        with open(self.filename, 'a', opener=opw_opener) as fh:
            fh.write(f'{pid},{size}\n')

    @property
    def pidmap(self):
        with open(self.filename, 'r') as fh:
            pidmap = {}
            for line in fh.readlines():
                pid, size = line.split(',')
                pidmap[int(pid)] = int(size)
        return pidmap

    def remove_pid(self, pid):
        # Read
        pidmap = self.pidmap
        # Remove
        try:
            del pidmap[pid]
        except KeyError:
            print(f'Key {pid} not in file')
        # Write
        with open(self.filename, 'w', opener=opw_opener) as fh:
            for key, value in pidmap.items():
                fh.write(f'{key},{value}\n')
