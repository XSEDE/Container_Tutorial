# Mandlebrot Zoom Gif generator

This app allows you to create a GIF file with a straight-line zoom-in of the Mandlebrot set.
Running the bare container will show the various commandline options available, which
may be confusing, as this was written immediately following in-depth perusal of
[The Wikipedia article on the Mandlebrot Set](https://en.wikipedia.org/wiki/Mandelbrot_set).
If you have some time available and are interested in this sort of thing, please go down
the rabbithole, but otherwise view this as a somewhat helpful example.

The following steps should allow you to test this out on a system with docker and singularity installed:

1. `docker build -t $USER/python-mandle .`

1. `docker run -u $(id -u) -g $(id -g) -v $PWD:$PWD -it $USER/python-mandle $PWD/mandle_ex.gif`

1. `sudo singularity build mandle.sif Mandle.def`

1. `singularity run mandle.sif -n 2 sing_mandle_ex.gif`

For submission on an HPC system using SLURM, you could use the following:
(Assuming you've uploaded this .sif file locally to APPDIR)

```
#/bin/bash
#SBATCH -N 1
#SBATCH -n 24
#SBATCH -o mandle_%A.out

module load singularity/3.5 #Versions above 3.6 are incompatible with lower versions!

WORKDIR=/scratch/myuser
APPDIR=/home/myuser/images/

singularity run $APPDIR/mandle.sif -n 24 $WORKDIR/my_mandle.gif
```
