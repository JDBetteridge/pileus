import ctypes

from argparse import ArgumentParser
from time import sleep


def main(args):
    try:
        mpi = ctypes.CDLL('libmpi.so')
        err = mpi.MPI_Init()
        MPI_COMM_WORLD = ctypes.c_int(0x44000000)  # Lifted from mpi.h

        csize = ctypes.c_int()
        err = mpi.MPI_Comm_size(MPI_COMM_WORLD, ctypes.byref(csize))
        size = csize.value

        crank = ctypes.c_int()
        err = mpi.MPI_Comm_rank(MPI_COMM_WORLD, ctypes.byref(crank))
        rank = crank.value

        if args.verbose:
            print(f'Using MPI, allocating {args.memory}MB over {size} ranks for {args.time}sec')
            print(f'Using MPI, allocating {args.memory//size}MB on rank {rank}')
    except OSError:
        print('No MPI found')
        if args.verbose:
            print(f'No MPI found, allocating {args.memory}MB on ALL ranks for {args.time}sec')
        mpi = None
        size = 1

    memblock = bytearray(1024*1024*args.memory//size)
    sleep(args.time)
    del memblock

    if mpi:
        mpi.MPI_Finalize()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-m', '--memory', help='memory to consume (in MB)', type=int, required=True)
    parser.add_argument('-t', '--time', help='time to consume', type=int, required=True)
    parser.add_argument('-v', '--verbose', help='print information as we go', action='store_true')
    parser.add_argument('-n', '--nothing', help='unused', type=int)

    args = parser.parse_args()
    main(args)
