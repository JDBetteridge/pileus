import psutil

from argparse import ArgumentParser
from pathlib import Path

from .display import display_cores, display_memory, display_jobs
from .process import RUN_DIR, Row, ProcessFile


def pileustop(args):
    rows = []
    for db in Path(RUN_DIR).glob('*.db'):
        user, uid = db.stem.split('-')
        pf = ProcessFile(filename=db)
        for pid in pf.pidmap.keys():
            try:
                p = psutil.Process(pid)
            except psutil.NoSuchProcess:
                pf.remove_pid(pid)
                continue

            try:
                with p.oneshot():
                    rpid = p.pid
                    rcmd = " ".join(p.cmdline())
                    rtime = p.create_time()

                # Calculate total memory consumed
                mem = 0
                for cid in [p] + p.children(recursive=True):
                    cm = cid.memory_info().rss
                    mem += cm
                rows.append(Row(rpid, user, rcmd, pf.pidmap[pid], mem, rtime))
            except psutil.NoSuchProcess:
                continue

    display_cores(rows, args.wide)
    display_memory(rows, args.wide)
    display_jobs(rows, args.wide)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-w', '--wide',
        help='Use 120 character wide display rather than 80',
        action='store_true'
    )
    args = parser.parse_args()
    pileustop(args)


if __name__ == '__main__':
    main()
