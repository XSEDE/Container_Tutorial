# Day 1, Ex1 Part D: Running
## Build, Convert, and Run an HPC job with a Container

# Step 4: Running a job

Now, we're going to walk through using our container with an
HPC job scheduler, Slurm. We'll submit a batch job file to the scheduler, watch the
job run, and view the output files - this workflow is basically what happens on the
background when using a science gateway.

#### 4(a)
Please make a local copy of the Slurm example job file and examine the contents:
```
$ cp /opt/ohpc/pub/examples/mandle-zoom.job ~/ex1-workdir
$ cat mandle-zoom.job
#!/bin/bash
#SBATCH -N 1 #Number of nodes
#SBATCH -n 4 #Number of "tasks"
#SBATCH -p cloud #Run in the "cloud" partition
#SBATCH -o mandle_%A.out #The %A refers to the slurm job ID, this is useful for distinguishing output files

module purge
module load gnu9
module load singularity

singularity run ./mandle-zoom-py/mandle.sif -n 4 -d 50 -s 20 -w 2 -f 0.05 ./better_zoom.gif
...
```

#### 4(b)
Go ahead and submit to the scheduler via:
```$ sbatch mandle-zoom.job```

#### 4(c)
Now, check your job status via the `squeue` command:
```$ squeue
             JOBID PARTITION     NAME     USER  ST       TIME  NODES NODELIST(REASON)
                63     cloud mandle-z  train99  CF       0:01      1 tg829096-compute-0
```
(Note the 'ST' or State column: the 'CF' state indicates that nodes for the job are 
being created, 'R' indicates a currently
running job, PD means the job will run as soon as there are slots available, CD is a completed job,
and F means some process exited with an error code).

While we wait for that to run, let's discuss the module commmands:

Notice that in the beginning, we're purging and re-loading
several modules. For the sake of completeness, let's quickly explore
what modules are available on the system:
```$ module avail

------------------------------- /opt/ohpc/pub/moduledeps/gnu9 --------------------------------
   openmpi4/4.0.5 (L)

--------------------------------- /opt/ohpc/pub/modulefiles ----------------------------------
   gnu9/9.3.0       (L)    ohpc (L)    prun/2.1          (L)    ucx/1.9.0 (L)
   libfabric/1.12.1 (L)    os          singularity/3.7.1

  Where:
   L:  Module is loaded

Use "module spider" to find all possible modules and extensions.
Use "module keyword key1 key2 ..." to search for all possible modules matching any of the
"keys".

```

In this environment, modules only shown based on compatibility with your currently loaded
compilers - so there are other MPI implementations available if you switch via
`module swap gnu7`. 

Your current module environment is also inherited by your Slurm script,
hence the `module purge` command - better to be absolutely clear what will
be loaded in your job environment.


#### 4(d)
You should see a gif file in your current directory!
```$ ls 
mandle_2.out  mandle-zoom.job  mandle-zoom-py  better_zoom.gif
```

Feel free to try again with different parameters! 
The default origin of the zoom is at (-1.4011552,0) - interesting
features can also be seen at (0.444,0.374) or (0.24,0). 
It might be worth increasing the number of frames or changing the speed as well!
The current cluster only uses 4 cores on each compute node, so increasing 
the number of cores is not a viable option at the moment.
