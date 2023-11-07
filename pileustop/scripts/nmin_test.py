import sys

from argparse import ArgumentParser
from subprocess import Popen


def main(args):
    for ii in range(args.jobs):
        cmd = [
            sys.executable, 'mpiwrapper.py', '-n', str(args.ranks),
            sys.executable, 'block.py',
            '-t', str(args.minutes*60),
            '-m', str(100*(ii + 1)),
            '-v'
        ]
        _ = Popen(
                cmd,
                stdout=sys.stdout,
                stderr=sys.stderr,
                start_new_session=True
            )


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-t', '--minutes',
        help='length of test in minutes',
        type=int,
        default=1
    )
    parser.add_argument(
        '-n', '--jobs',
        help='jobs to launch',
        type=int,
        default=3
    )
    parser.add_argument(
        '-r', '--ranks',
        help='number of MPI ranks per job',
        type=int,
        default=2
    )

    args = parser.parse_args()
    main(args)
