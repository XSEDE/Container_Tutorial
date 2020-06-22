# Exercise 1: 
## Build, Convert, and Run an HPC job with a Container

# Overview

We're going to take one one of the dockerfiles you've already seen,
build the docker image, convert it to Singularity, and run
a job using the Slurm job scheduler. 

We will also walk through the workflow needed to authenticate to
and use a remote container registry - this will be basically the 
same as what's used on DockerHub and Singularity-Hub (or the Sylabs
cloud repository, but we'll be using a Jetstream-local instance
of the Singularity Registry (the software underlying S-Hub).

## The Infrastructure

You'll be using a virtual cluster in the Jetstream cloud
for these exercises. This is a multi-user system, so please be careful!

-----
*If you have not received your login information, please let us know
via chat!*
=====

# Step 1: The Dockerfile
Please look in 
```/opt/ohpc/pub/examples/ex1_docker.txt```

# Step 2: Conversion to Singularity
Now that you've build a dockerfile, it's time to make it useable in our 
HPC environment.

First, load the `singularity` module:
```$ module load singularity```

This will give your shell session access to the singularity executable, etc.
We're going to convert by simply including the docker image
in our Singularity Definition file. It's also possible to convert the image
directy, but we want to illustrate the use of a Docker image as a base 
for cases where it's necessary to modify the environment further.

Make a local copy of the example Singularity definition file available in
our examples folder:

```$ cp /opt/ohpc/pub/examples/ex1_singularity.def ~/sing-workdir```

(notice the .def extension - it's still just a text file, but
this is the convention used in Singularity documentation for 
human-friendliness!)

Now, take a look in an editor:
```
$ cd ~/sing-workdir
$ vim ./ex1_singularity.def
```

You should see the following:
```
COPY-PASTE HERE
```

Now, to build the container:

```singularity build --fakeroot ex1_singularity.def ex1.sif```

You should see output like the following:
```
COPY-PASTE OUTPUT
```

#Step 3: Upload to a Registry

We're going to share our containers via a registry, now, since in
normal practice, you won't be able to build containers on the same
host that you're submitting jobs from. This also aids the goal
of reproducible science - once your container is shared, you can share 
with collaborators (and enemies) or a community of users.

So, open up a brower and go to 
```https://tutorial.jetstream-cloud.org```

Select 'Login' on the top bar, and you'll be asked to authenticate
via Github (you will need to allow the application read-only access to your
Git profile).

Now, you'll have the ability to create "collections" of containers for other
users to access, and for yourself. This is an instance of the "sregistry" software,
which underlies the main Singularity-Hub.
(MORE DESCRIPTION HERE)

Once you've created a collection, you're ready to upload via the singularity client.
(Will everyone need a unique name here?!)

Register the remote:
```singularity remote add --no-login TutorialSRegistry https://tutorial.jetstream-cloud.org```

And authenticate:
```singularity remote login TutorialSRegistry```

Now you've got a token stored on this machine that will allow you continued access to the
registry.

Upload your container via
EDIT THIS
```singularity push -U /opt/ohpc/pub/images/mandle_geom.sif library://ECoulter/tutorial-containers/mandle-geom:latest```

# Step 4: Running a job
Please make a local copy of the slurm example job file:
```
$ cp /opt/ohpc/examples/slurm_example.job ~/sing-workdir
$ cat slurm_example.job
...
```

Notice that in the beginning, we're purging and re-loading
several modules. For the sake of completeness, let's quickly explore
what modules are available on the sysem:
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
