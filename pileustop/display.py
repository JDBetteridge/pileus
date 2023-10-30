from time import time
from shlex import split

from process import Row


def display_cores():
    pass


def display_memory():
    pass


def sniff_command(command):
    parts = split(command)
    if any(filter(lambda x: x.endswith('python'), parts)):
        name = 'python ' + ' '.join(filter(lambda x: x.endswith('.py'), parts))
    else:
        name = command
    return name


def nice_mem(mem):
    nice = mem/(1024*1024*1024)
    if nice < 0.1:
        nicestring = '<0.01'
    else:
        nicestring = f'{nice: 7.2f}'
    return nicestring


def calculate_walltime(start, now):
    minute = 60
    hour = 60*minute
    day = 24*hour

    walltime = now - start
    dd = int(walltime/day)
    hh = int((walltime/hour) % 60)
    mm = int((walltime/minute) % 60)
    ss = walltime % minute

    blank = ' '*3
    wstring = f'{dd}d' if dd else blank
    wstring += f'{hh:02d}:' if hh else blank
    wstring += f'{mm:02d}:' if mm else blank
    wstring += f'{ss:05.2f}'
    return wstring


def display_jobs(jobs, wide=False):
    # Choose command to fit 25x80 or 25x120 Terminal width
    tmp_width = (8, 15, 0, 3, 7, 15)
    if wide:
        command_width = 120 - 8 - sum(tmp_width)
    else:
        command_width = 80 - 8 - sum(tmp_width)
    width = (8, 15, command_width, 3, 7, 15)
    sep = '+' + '+'.join(['-'*ww for ww in width]) + '+'
    heading = [
        'PID',
        'User',
        'Command',
        'CPU',
        'Memory',
        'Walltime'
    ]
    unit = ['']*4 + ['GB', 'DAYdHH:MM:SS.xx']
    titles = '|' \
        + '|'.join([f'{hh:^{ww}s}' for hh, ww in zip(heading, width)]) + '|'
    unitrow = '|' \
        + '|'.join([f'{uu:^{ww}s}' for uu, ww in zip(unit, width)]) + '|'
    print(sep)
    print(titles)
    print(unitrow)
    print(sep)
    now = time()
    total_cpu = 0
    total_mem = 0
    for row in jobs:
        rowstring = '|'
        rowstring += f'{row.pid: {width[0]}d}|'
        rowstring += f'{row.user:>{width[1] - 1}s} |'
        command = sniff_command(row.command)
        if len(command) > width[2] - 1:
            command = command[:width[2] - 4] + '...'
        rowstring += f' {command :<{width[2] - 1}s}|'
        rowstring += f'{row.ncpu: {width[3]}d}|'
        total_cpu += row.ncpu
        rowstring += f'{nice_mem(row.mem):>{width[4]}s}|'
        total_mem += row.mem
        rowstring += f'{calculate_walltime(row.start, now):>{width[5]}s}|'
        print(rowstring)
    print(sep)
    totals = '| TOTAL: |'
    totals += '|'.join(['-'*ww for ww in width[1:3]])
    totals += '|' + f'{total_cpu: {width[3]}d}|'
    totals += f'{nice_mem(total_mem):>{width[4]}s}|'
    totals += '-'*width[-1] + '|'
    print(totals)
    print(sep)


if __name__ == '__main__':
    r = Row(
        pid=12987,
        user='jack',
        command='/opt/mpich/bin/mpiexec.hydra -n 3 sleep 60',
        ncpu=3,
        mem=11927552,
        start=1697795306.76
    )
    jobs = [r]
    display_jobs(jobs, wide=True)
