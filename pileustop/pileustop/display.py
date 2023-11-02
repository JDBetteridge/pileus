import psutil

from collections import defaultdict
from pprint import pprint
from shlex import split
from time import time

from .process import Row


class AlphaHashTable:
    def __init__(self):
        self._alpha = ''.join(u + l for u, l in zip(
            (chr(ii) for ii in range(65, 91)),
            (chr(ii) for ii in range(97, 123))
        ))
        self.available_keys = set(self._alpha)
        self._table = {}
    def add(self, user, alt=None):
        if user not in self._table.keys():
            key = alt or user[0].upper()
            for _ in self._alpha:
                if key not in self.available_keys:
                    new_idx = (self._alpha.find(key) + 1) % len(self._alpha)
                    key = self._alpha[new_idx]
                else:
                    self.available_keys.remove(key)
                    self._table[user] = key
                    break
            else:
                raise RuntimeError('No keys left! This is not a good hash table')
    def __getitem__(self, user):
        try:
            return self._table[user]
        except KeyError as e:
            raise e


def display_cores(jobs, wide=False):
    print('#========#')
    print('#  CPU   #')
    print('#========#')
    system_cores = psutil.cpu_count(logical=False)
    symbol = AlphaHashTable()

    allocation = defaultdict(int)
    for j in jobs:
        symbol.add(j.user)
        allocation[j.user] += j.ncpu
    cpu_alloc = sorted(allocation.items(), key=lambda x: x[1], reverse=True)
    pprint(cpu_alloc)

    left = system_cores
    magic_string = ''
    for user, cores in cpu_alloc:
        magic_string += f' {symbol[user]}'*cores
        left -= cores
    magic_string += ' .'*left
    print(magic_string)
    print()


def display_memory(jobs, wide=False):
    print('#========#')
    print('# MEMORY #')
    print('#========#')
    memory_info = psutil.virtual_memory()
    system_memory = memory_info.total
    symbol = AlphaHashTable()

    allocation = defaultdict(int)
    for j in jobs:
        symbol.add(j.user)
        allocation[j.user] += j.mem
    allocation['system'] = system_memory \
        - memory_info.available \
        - sum(allocation.values())

    mem_alloc = sorted(allocation.items(), key=lambda x: x[1], reverse=True)
    pprint([(k, nice_mem(v) + 'GB') for k, v in mem_alloc])
    width = 120 if wide else 80
    magic_string = '*'*int(width*allocation['system']/system_memory)
    for user, mem in mem_alloc:
        if user != 'system':
            magic_string += symbol[user]*int(width*mem/system_memory)
    magic_string += '.'*int(width*memory_info.available/system_memory)
    print(magic_string)
    print()


def sniff_command(command):
    parts = split(command)
    if any(filter(lambda x: x.endswith('python'), parts)):
        name = 'python ' + ' '.join(filter(lambda x: x.endswith('.py'), parts))
    elif parts[0].endswith('mpiexec.hydra'):
        parts[0] = 'mpiexec'
        name = ' '.join(parts)
    else:
        name = command
    return name


def nice_mem(mem):
    nice = mem/(1024*1024*1024)
    if nice < 0.01:
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
    print('#========#')
    print('#  JOBS  #')
    print('#========#')
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
    totals += '|'.join([' '*ww for ww in width[1:3]])
    totals += '|' + f'{total_cpu: {width[3]}d}|'
    totals += f'{nice_mem(total_mem):>{width[4]}s}|'
    totals += ' '*width[-1] + '|'
    print(totals)
    print(sep)
    print()


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

    display_cores(jobs, wide=True)
    display_jobs(jobs, wide=True)
