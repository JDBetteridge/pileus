from argparse import ArgumentParser
from subprocess import run, PIPE
from sys import stdout, stderr

parser = ArgumentParser(add_help=False)
known, unknown = parser.parse_known_args()

print(f'{known._get_args() = }')
print(f'{unknown = }')

mpiexec = 'mpiexec.orig'
status = run(['ls'] + unknown, stdout=stdout, stderr=stderr)
print('Hello')
print(status)
exit(status.returncode)
