import psutil

from collections import defaultdict
from itertools import pairwise
from shlex import split
from time import time

from .process import Row


class DisplayError(Exception):
    ''' Error displaying information
    '''
    pass


# Basic table formats
_ascii_single = """
+-+-+-+
| | | |
+-+-+-+
| | | |
+-+-+-+
| | | |
+-+-+-+
"""
_ascii_double = """
#=#=#=#
# # # #
#=#=#=#
# # # #
#=#=#=#
# # # #
#=#=#=#
"""
_single_wall_rounded = """
╭─┬─┬─╮
│ │ │ │
├─┼─┼─┤
│ │ │ │
├─┼─┼─┤
│ │ │ │
╰─┴─┴─╯
"""
_bold_outline = """
┏━┳━┯━┓
┃ ┃ │ ┃
┣━╋━┿━┫
┃ ┃ │ ┃
┠─╂─┼─┨
┃ ┃ │ ┃
┗━┻━┷━┛
"""
_double_wall = """
╔═╦═╦═╗
║ ║ ║ ║
╠═╬═╬═╣
║ ║ ║ ║
╠═╬═╬═╣
║ ║ ║ ║
╚═╩═╩═╝
"""


class TerminalScreen:
    ''' Information about the terminal screen.
    '''
    def __init__(self, width=80, unicode=False):
        self.width = width
        self.unicode = unicode


class Decorator:
    ''' Codified table format for use as a base class in creating boxes and
    tables.
    '''
    def __init__(self, format_=_ascii_single):
        self._format = format_
        table = [r for r in format_.split('\n') if r]
        # Top left, top right, bottom left, bottom right -- corners
        self.tl = table[0][0]
        self.tr = table[0][-1]
        self.bl = table[-1][0]
        self.br = table[-1][-1]
        # Outside horizontal, outside vertical
        self.oh = table[0][1]
        self.ov = table[1][0]
        # HEADING horizontal, HEADING vertical
        self.Hh = table[2][1]
        self.Hv = table[1][2]
        # Inside horizontal, inside vertical
        self.ih = table[4][1]
        self.iv = table[1][4]
        # Top HEADING vertical, top vertical -- intersections
        self.tHv = table[0][2]
        self.tv = table[0][4]
        # Bottom HEADING vertical, bottom vertical -- intersections
        self.bHv = table[-1][2]
        self.bv = table[-1][4]
        # Left HEADING horizontal, left horizontal -- intersections
        self.lHh = table[2][0]
        self.lh = table[4][0]
        # Right HEADING horizontal, right horizontal -- intersections
        self.rHh = table[2][-1]
        self.rh = table[4][-1]
        # HEADING HEADING, inside inside --instersections
        self.HH = table[2][2]
        self.ii = table[4][4]
        # HEADING inside horizontal, HEADING inside vertical --instersections
        self.Hih = table[4][2]
        self.Hiv = table[2][4]

    def __repr__(self):
        return self.__name__ + '(' + str(self._format) + '\n)'


class Box(Decorator):
    def __init__(self, screen, width, text='', boxformat=_ascii_double):
        super().__init__(boxformat)
        if width > screen.width:
            raise DisplayError('Box width wider than screen width')
        self.width = width
        self.text = text

    def __str__(self):
        iw = self.width - 2
        string = self.tl + self.oh*(iw) + self.tr + '\n'
        for line in self.text.split('\n'):
            string += self.ov + f'{line:^{iw}s}' + self.ov + '\n'
        string += self.bl + self.oh*(iw) + self.br
        return string


class Table(Decorator):
    def __init__(
        self, screen, widths, alignment=None, tableformat=_ascii_single
    ):
        super().__init__(tableformat)
        free = screen.width - 1 - len(widths) \
            - sum(filter(lambda x: isinstance(x, int), widths))
        if free < 0:
            raise DisplayError('Table width wider than screen width')
        nflex_cols = widths.count('*')
        if nflex_cols:
            min_flex_width = free//nflex_cols
            remainder = free - (nflex_cols*min_flex_width)
            flex_widths = [min_flex_width + 1] * remainder
            flex_widths.extend([min_flex_width] * (nflex_cols - remainder))

            fixed_widths = []
            for w in widths:
                if isinstance(w, int):
                    fixed_widths.append(w)
                else:
                    fixed_widths.append(flex_widths.pop(0))
            self.widths = fixed_widths
        else:
            self.widths = widths
        self.alignment = alignment or ('^',)*len(widths)
        self.type_dict = {
            int: 'd',
            float: 'f',
            str: 's'
        }

    def bar(self, left, horizontal, intersection, right):
        return left + \
            intersection.join([horizontal*w for w in self.widths]) + right

    @property
    def top_bar(self):
        return self.bar(self.tl, self.oh, self.tv, self.tr)

    @property
    def heading_bar(self):
        return self.bar(self.lHh, self.Hh, self.Hiv, self.rHh)

    @property
    def horizontal_bar(self):
        return self.bar(self.lHh, self.Hh, self.Hiv, self.rHh)

    @property
    def bottom_bar(self):
        return self.bar(self.bl, self.oh, self.bv, self.br)

    def row(self, row, alignment=None):
        alignment = alignment or self.alignment
        return self.ov + self.iv.join([
            f'{col:{a}{w}{self.type_dict[type(col)]}}'
            for col, w, a in zip(row, self.widths, alignment)
        ]) + self.ov

    def heading(self, heading, alignment=None):
        return self.row(heading, alignment)

    def footer(self, footer, alignment=None):
        return self.row(footer, alignment)


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
                raise RuntimeError(
                    'No keys left! This is not a good hash table'
                )

    def __getitem__(self, user):
        try:
            return self._table[user]
        except KeyError as e:
            raise e


def display_cores(screen, jobs):
    ''' Display CPU allocation information.
    '''
    # Title
    print(Box(
        screen,
        10,
        'CPU',
        boxformat=_double_wall if screen.unicode else _ascii_double
    ))

    # Count allocated cores
    system_cores = psutil.cpu_count(logical=False)
    symbol = AlphaHashTable()

    allocation = defaultdict(int)
    for j in jobs:
        symbol.add(j.user)
        allocation[j.user] += j.ncpu
    cpu_alloc = sorted(allocation.items(), key=lambda x: x[1], reverse=True)

    print('CPU occupancy diagram:')
    block = min(16, system_cores)
    cpu = Table(
        screen,
        widths=(3, )*block,
        alignment=('^', )*block,
        tableformat=_single_wall_rounded if screen.unicode else _ascii_single
    )
    print(cpu.top_bar)
    data = []
    left = system_cores
    for user, cores in cpu_alloc:
        data.extend([symbol[user]]*cores)
        left -= cores
    data.extend(['']*left)
    rows = [
        data[block*ii:block*(ii + 1)] for ii in range(len(data)//block + 1)
    ]
    for r, nxt in pairwise(rows):
        print(cpu.row(r))
        if nxt:
            print(cpu.horizontal_bar)
    if rows[-1]:
        print(cpu.row(rows[-1]))
    print(cpu.bottom_bar)

    print('Key:')
    key = Table(
        screen,
        widths=(3, 15, 3),
        tableformat=_single_wall_rounded if screen.unicode else _ascii_single
    )
    print(key.top_bar)
    print(key.heading(['SYM', 'User', 'CPU']))
    print(key.heading_bar)
    for user, cores in cpu_alloc:
        print(key.row([symbol[user], user, cores]))
    print(key.row(['', 'FREE', left]))
    print(key.bottom_bar)
    print()


def display_memory(screen, jobs):
    ''' Display Memory allocation information.
    '''
    # Title
    print(Box(
        screen,
        10,
        'MEMORY',
        boxformat=_double_wall if screen.unicode else _ascii_double
    ))

    # Count allocated memory
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

    print('Memory occupancy diagram:')
    memory = Table(
        screen,
        widths=('*'),
        tableformat=_single_wall_rounded if screen.unicode else _ascii_single
    )
    print(memory.top_bar)
    width = screen.width - 2
    magic_string = '*'*int(width*allocation['system']/system_memory)
    for user, mem in mem_alloc:
        if user != 'system':
            magic_string += symbol[user]*int(width*mem/system_memory)
    magic_string += '.'*int(width*memory_info.available/system_memory)
    print(memory.row([magic_string]))
    print(memory.bottom_bar)

    print('Key:')
    key = Table(
        screen,
        widths=(3, 15, 7),
        tableformat=_single_wall_rounded if screen.unicode else _ascii_single
    )
    print(key.top_bar)
    print(key.heading(['SYM', 'User', 'Memory']))
    print(key.heading(['', '', 'GB']))
    print(key.heading_bar)
    for user, mem in mem_alloc:
        if user == 'system':
            print(key.row(['*', user, nice_mem(mem)]))
        else:
            print(key.row([symbol[user], user, nice_mem(mem)]))
    print(key.row(['.', 'FREE', nice_mem(memory_info.available)]))
    print(key.bottom_bar)
    print()


def sniff_command(command):
    ''' Return only relevant parts of command
    '''
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
    ''' Memory in gigabytes
    '''
    nice = mem/(1024*1024*1024)
    if nice < 0.01:
        nicestring = '<0.01'
    else:
        nicestring = f'{nice: 7.2f}'
    return nicestring


def calculate_walltime(start, now):
    ''' String format of time difference from start to now
    '''
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


def display_jobs(screen, jobs):
    ''' Display a table of running jobs.
    '''
    # Title
    print(Box(
        screen,
        10,
        'JOBS',
        boxformat=_double_wall if screen.unicode else _ascii_double
    ))

    # Setup table and print top matter
    headings = ['PID', 'User', 'Command', 'CPU', 'Memory', 'Walltime']
    widths = (8, 15, '*', 3, 7, 15)
    units = ['']*4 + ['GB', 'DAYdHH:MM:SS.xx']
    table = Table(
        screen,
        widths=widths,
        alignment=['>', '>', '<', '>', '>', '>'],
        tableformat=_single_wall_rounded if screen.unicode else _ascii_single
    )
    print(table.top_bar)
    print(table.heading(headings, alignment=['^']*len(widths)))
    print(table.heading(units, alignment=['^']*len(widths)))
    print(table.heading_bar)
    # Calculate row data and display
    job_alloc = sorted(jobs, key=lambda x: x.start)
    now = time()
    total_cpu = 0
    total_mem = 0
    for j in job_alloc:
        command = sniff_command(j.command)
        # Truncate the command to fit the column width
        if len(command) > table.widths[2]:
            command = command[:table.widths[2] - 3] + '...'
        row = [
            j.pid,
            j.user,
            command,
            j.ncpu,
            nice_mem(j.mem),
            calculate_walltime(j.start, now)
        ]
        total_cpu += j.ncpu
        total_mem += j.mem
        print(table.row(row))

    # Display totals
    footer = ['TOTAL: ', '', '', total_cpu, nice_mem(total_mem), '']
    print(table.horizontal_bar)
    print(table.footer(footer))
    print(table.bottom_bar)
