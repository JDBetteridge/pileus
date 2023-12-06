# Installing PETSc on Pileus

This serves as a reference for updating PETSc (and SELPc) on Pileus in case JDBetteridge is not about.

The installation lives in `/data/shared/pileus/`.

The update process may take a long time to run and you may want to start a session in a terminal multiplexer such as `tmux` or `screen`

To update:

1. Clone this repo, I will assume it is checked out in `~/workspace/`.
2. Change into the Pileus shared data directory `cd /data/shared/pileus`.
3. Remove or rename any old backup installations named `petsc.bak` or `slepc.bak`.
**NOTE** `rm -rf` is very dangerous, if you do not understand what you are doing stop here.
`rm -rf petsc.bak slepc.bak`
4. Backup the current PETSc and SLEPc installation in case anything goes wrong.
`mv petsc petsc.bak`
`mv slepc slepc.bak`
5. Run the script in this repository from the `/data/shared/pileus` directory.
**NOTE** This will take a long time to run, be patient
`~/workspace/pileus/petsc/install_petsc.sh`
6. Link the `mpiexec` and `mpirun` scripts to `/data/shared/pileus/pileustop/mpiwrapper.py`. (This is the special sauce that make `pileustop` work.)
```bash
rm /data/shared/pileus/petsc/packages/bin/{mpiexec,mpirun}
ln -s /data/shared/pileus/pileustop/mpiwrapper.py /data/shared/pileus/petsc/packages/bin/mpiexec
ln -s /data/shared/pileus/pileustop/mpiwrapper.py /data/shared/pileus/petsc/packages/bin/mpirun
```
7. Install Firedrake using a copy of `/data/shared/pileus/firedrake/standard_firedrake_build.sh` **OR** activate your existing Firedrake virtual environment and run `firedrake-update --rebuild`
8. Change into the Firedrake directory and run the test suite.
```bash
cd $VIRTUAL_ENV/src/firedrake
pytest \
    --timeout=1800 \
    --timeout-method=thread \
    -o faulthandler_timeout=1860 \
    -n 32 --dist worksteal \
    -v tests
```
9. Change into the Gusto directory and run the test suite
```bash
cd $VIRTUAL_ENV/src/gusto
pytest \
    --timeout=1800 \
    --timeout-method=thread \
    -o faulthandler_timeout=1860 \
    -n 32 --dist worksteal \
    -v unit-tests
```
