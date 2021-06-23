# Ex1 Part D - Running
## Build, Convert, and Run an HPC job with a Container

# Step 4: Running a job

Now, we're going to walk through using our container **from the local filesystem** with an
HPC job scheduler, Slurm. We'll submit a batch job file to the scheduler, watch the
job run, and view the output files - this workflow is basically what happens on the
background when using a science gateway.

#### 4(a)
Please make a local copy of the Slurm example job file and open in an editor:
```
$ cp /opt/ohpc/pub/examples/slurm_dice.job ~/ex1-workdir
$ vim slurm_dice.job
#!/bin/bash
#SBATCH -N 1 #Number of nodes
#SBATCH -n 1 #Number of "tasks"
#SBATCH -p cloud #Run in the "cloud" partition
#SBATCH -o dice_test_%A.out #The %A refers to the slurm job ID, this is useful for distinguishing output files

module purge
module load gnu9
module load openmpi4
module load singularity

singularity run ex1.sif 10
...
```

#### 4(b)
Go ahead and submit to the scheduler via:
```$ sbatch slurm_dice.job```

#### 4(c)
Now, check your job status via the `squeue` command:
```$ squeue
             JOBID PARTITION     NAME     USER  ST       TIME  NODES NODELIST(REASON)
                63     cloud slurm_di jecoulte  CF      0:01      1 tg829096-compute-0
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

------------------------------------- /opt/ohpc/pub/moduledeps/gnu -------------------------------------
   openmpi/1.10.7 (L)

-------------------------------------- /opt/ohpc/pub/modulefiles ---------------------------------------
   gnu/5.4.0 (L)    gnu7/7.3.0    ohpc (L)    pmix/2.2.2    prun/1.3 (L)    singularity/3.4.1 (L)

  Where:
   L:  Module is loaded

Use "module spider" to find all possible modules.
Use "module keyword key1 key2 ..." to search for all possible modules matching any of the "keys".
```

In this environment, modules only shown based on compatibility with your currently loaded
compilers - so there are other MPI implementations available if you switch via
`module swap gnu7`. 

Your current module environment is also inherited by your Slurm script,
hence the `module purge` command - better to be absolutely clear what will
be loaded in your job environment.


#### 4(d)
You should see an output file in your current directory that looks like:
```$ cat dice_test_63.out
NAME                 URI                           GLOBAL
SylabsCloud          cloud.sylabs.io               YES
[TutorialSRegistry]  tutorial.jetstream-cloud.org  NO
INFO:    Remote "TutorialSRegistry" now in use.
INFO:    Downloading library image
 18.73 MiB / 18.73 MiB  100.00% 115.54 MiB/s 0s
WARNING: group: unknown groupid 1003
How many times would you like to roll the dice?Rolling the dice 10 times...
You rolled the dice  10 times, getting an average value of  6.7 .
The highest round was: 10
The lowest round was: 2

```

If you run this job again, you'll notice the absence of the 
download progress line - Singularity keeps a local cache of containers
used recently, and matches the sha256 hash of cached vs. remote 
containers before downloading - notice that if the remote container
has been updated, using the `singularity run` command with a remote URI will
result in running the new version, rather than the local version.
If that's a potential stumbling block, it's safest to use
```singularity pull -U library://${USERNAME}/${COLLECTION_NAME}/py3-dice:latest```
for example, and then run jobs using the local .sif file.
