import sys

from argparse import ArgumentParser
from subprocess import Popen


def main(args):
    for ii in range(3):
        cmd = [
            sys.executable, 'mpiwrapper.py', '-n', '2',
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
        '-n', '--minutes',
        help='length of test in minutes',
        type=int,
        required=True
    )
    args = parser.parse_args()
    main(args)
