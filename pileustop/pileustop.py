import psutil

from collections import namedtuple
from pathlib import Path
from pprint import pprint
from process import ProcessFile
from time import time

Row = namedtuple('Row', ['pid', 'user', 'command', 'ncpu', 'mem', 'start'])



def main():
    rows = []
    for db in Path('proc').glob('*.db'):
        print(db)
        user, uid = db.stem.split('-')
        pf = ProcessFile(filename=db)
        print(user)
        pprint(pf.pidmap)
        for pid in pf.pidmap.keys():
            p = psutil.Process(pid)
            with p.oneshot():
                rpid = p.pid
                # ~ print(f'PID:            {rpid}')
                rcmd = " ".join(p.cmdline())
                # ~ print(f'Command         {rcmd}')
                # ~ rcpu = p.cpu_percent()
                # ~ print(f'CPU percent:    {rcpu}')
                # ~ print(f'Mem info:       {p.memory_info()}')
                rtime = p.create_time()
                # ~ print(f'Started at:     {rtime}')
                # ~ print(f'Children:       {p.children()}')
                # ~ print(f'Children (rec): {p.children(recursive=True)}')
                # ~ pprint(p.as_dict())

            # Calculate total memory consumed
            mem = 0
            for cid in [p] + p.children(recursive=True):
                cm = cid.memory_info().rss
                mem += cm
                # ~ print(f'\t{cm}')
            # ~ print(f'\tTotal: {mem} ~= {mem/(1024*1024)} MB')
            rows.append(Row(rpid, user, rcmd, pf.pidmap[pid], mem, rtime))

    print()
    print()
    print()
    now = time()
    print(f'NOW: {now}')
    for r in rows:
        walltime = now - r.start
        hh = int(walltime//3600)
        mm = int((walltime//60) % 60)
        ss = walltime % 60
        print(r, f'{hh:d}:{mm:02d}:{ss:05.2f}')

if __name__ == '__main__':
    main()
