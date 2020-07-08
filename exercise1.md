# Exercise 1: 
## Build, Convert, and Run an HPC job with a Container

# Overview

We're going to take one one of the Dockerfiles you've already seen,
build the docker image, convert it to Singularity, and run
a job using the Slurm job scheduler. 

We will also walk through the workflow needed to authenticate to
and use a remote container registry - this will be basically the 
same as what's used on DockerHub and Singularity-Hub.  It is also
similar to the Sylabs cloud repository, but we'll be using a 
Jetstream-local instance of the Singularity Registry (the software 
underlying S-Hub).

*PLEASE NOTE*: The instructor will be using vim for any file editing
that needs to be done - you may also use nano. 

## The Infrastructure

You'll be using a virtual cluster in the Jetstream cloud
for these exercises. This is a multi-user system, so please be careful!

-----
*If you have not received your login information, please let us know
via chat!*
=====

First of all, the example files we'll be using are all available
in `/opt/ohpc/pub/examples`.

# Step 1: The Dockerfile
To begin with, we've got a dockerfile similar to what you've
seen already available in:
```/opt/ohpc/pub/examples/ex1_docker.txt```

#### 1(a)
Create a work directory in your homedir:
```$ mkdir ~/ex1-workdir```

and cd into it:
```$ cd ~/ex1-workdir```

now, make your own copy of the dockerfile mentioned above named `Dockerfile`:
```$ cp /opt/ohpc/pub/examples/ex1_docker.txt ~/ex1-workdir/Dockerfile```

#### 1(b)
Examine the contents:
```$ cd ~/ex1-workdir
$ cat ./Dockerfile
# our base image
FROM alpine:3.9

# install python and pip
RUN apk add --update py3-pip

# copy files required for the app to run
COPY dice.py /usr/src/app/

# run the application
CMD python3 /usr/src/app/dice.py
```

#### 1(c)
Notice that the COPY directive refers to a file we don't have in
the current working directory. It's not possible to COPY or ADD files from 
"above" the current location, so we'll need to grab that as well:

```$ cp /opt/ohpc/pub/examples/dice.py ~/ex1-workdir/dice.py```

The dice.py script will "roll" a pair of dice a certain number
of times, and return some very basic information about the results:

```$ cat /opt/ohpc/pub/examples/dice.py
#!/usr/bin/env python3
import random
minimum = 1
maximum = 6
number_of_rolls=int(input("How many times would you like to roll the dice?"))

print("Rolling the dice",str(number_of_rolls),"times...")
results=[]
for i in range(0,number_of_rolls):
# Roll two dice for each step
#  and gather into a list of tuples [(roll1_1,roll1_2),(roll2_1,roll2_2)...]
  results+=[(random.randint(minimum, maximum),random.randint(minimum,maximum))]

#add both die in each round, getting a list of round totals
totals=list(map(sum,results))

average=sum(totals)/len(totals)

print("You rolled the dice ",number_of_rolls,"times, getting an average value of ",average,".")
print("The highest round was:",max(totals))
print("The lowest round was:",min(totals))
```

#### 1(d)
Now, you can build the image from the Dockerfile via the following
command, but be sure to replace $USERNAME with you current username:

```$ sudo docker build -t $USERNAME/py3-dice .```

Which should generate output similar to:
```
Sending build context to Docker daemon 3.584 kB
Step 1/4 : FROM alpine:3.9
 ---> 78a2ce922f86
Step 2/4 : RUN apk add --update py3-pip
 ---> Using cache
 ---> 9f3157db35ca
Step 3/4 : COPY dice.py /usr/src/app/
 ---> 7e6a1a4603d1
Removing intermediate container eda9b8c81a12
Step 4/4 : CMD python3 /usr/src/app/dice.py
 ---> Running in a76788b898d7
 ---> d7bb6e1691d8
Removing intermediate container a76788b898d7
Successfully built d7bb6e1691d8
```

To view the list of images available locally, run
```
$ sudo docker images
```

# Step 2: Conversion to Singularity
Now that you've built a Dockerfile, it's time to make it useable in our 
HPC environment.

#### 2(a)
First, load the `singularity` module:
```$ module load singularity```

This will give your shell session access to the Singularity executable, etc.
We're going to convert by simply including the Docker image
in our Singularity Definition file. It's also possible to convert the image
directy, but we want to illustrate the use of a Docker image as a base 
for cases where it's necessary to modify the environment further.

#### 2(b)
Make a local copy of the example Singularity definition file available in
our examples folder:

```$ cp /opt/ohpc/pub/examples/ex1_singularity.txt ~/ex1-workdir/Dice.def```

(notice the .def extension - it's still just a text file, but
this is the convention used in Singularity documentation for 
human-friendliness!)

#### 2(c)
Now, take a look in an editor:
```
$ cd ~/ex1-workdir
$ vim ./Dice.def
Bootstrap: docker-daemon
From: $USERNAME/py3-dice:latest
# BE SURE TO REPLACE THE ABOVE WITH YOUR USERNAME AND IMAGE NAME

%post

  chmod 755 /usr/src/app/dice.py

%runscript
#This allows us to pass the number of runs as an argument in the
# slurm script.
  echo ${1} | /usr/src/app/dice.py

%help
 This container will run a python script that simulates some
 number of dice rolls.
```

#### 2(d)
Now, to build the container:

```$ sudo $(which singularity) build ex1.sif Dice.def```

The reason we're using `which` is thanks to the combination of Singularity's 
trust model and the module system - users are not allowed to build containers
without root permissions (because the build process can require touching
files that require root access), and the environment variables loaded by
the singularity modules do not transfer to the sub-process spawned by the
sudo command. Shell expansion happens *before* the sub-process, however, 
so we're still able to leverage environment settings, rather than using
the whole path to the binary.

This will produce an image file in .sif format in your local directory.

You should see output like the following:
```
INFO:    Starting build...
Getting image source signatures
Copying blob sha256:89ae5c4ee501a09c879f5b58474003539ab3bb978a553af2a4a6a7de248b5740
 5.54 MiB / 5.54 MiB [======================================================] 0s
Copying blob sha256:b880f6d68a318af60dffdfb6cafdf70c99efa6b73c04758b90ef89583e6c9352
 55.54 MiB / 55.54 MiB [====================================================] 3s
Copying blob sha256:884fad4b91b39f1aa3418da9b7222e6e3ad9966d20a769ce138d342ea669d15b
 4.50 KiB / 4.50 KiB [======================================================] 0s
Copying config sha256:37b96c85a80240b47d8274c28bc906978b0480b1768fa7b8dc82e5150452e40a
 1.16 KiB / 1.16 KiB [======================================================] 0s
Writing manifest to image destination
Storing signatures
2020/06/29 16:35:11  info unpack layer: sha256:31603596830fc7e56753139f9c2c6bd3759e48a850659506ebfb885d1cf3aef5
2020/06/29 16:35:11  info unpack layer: sha256:9c536910693f7e20b11c6930e24b7e05d7264fe9bec0bdb581cbc5a689a817c4
2020/06/29 16:35:13  info unpack layer: sha256:2da056d84117dace00a51b38c64d3cda7b8e6fb25cf7f4890193309e3f6d6d63
INFO:    Running post scriptlet
+ chmod 755 /usr/src/app/dice.py
INFO:    Adding help info
INFO:    Adding runscript
INFO:    Creating SIF file...
INFO:    Build complete: ex1.sif
```
Most of this is the actual Docker-Singularity conversion taking place automatically!
Each layer of the Docker container is copied into a temporary space, 
unpacked, the steps in the definition file are applied, and then the result is 
packed in a SIF file.

# Step 3: Upload to a Registry

<!--
works: singularity pull shub://tutorial.jetstream-cloud.org/tutorial-containers/numpy-pillow:latest
 when did this work? it doesn't now. Maybe due to the push command used...
works: singularity pull library://ECoulter/tutorial-containers/mymandle:latest
fails: singularity pull library://ECoulter/tutorial-containers/numpy-pillow:latest
works: singularity push -U mymandle.sif library://ECoulter/tutorial-containers/mymandle:latest
fails: singularity push -U mymandle.sif library://tutorial.jetstream-cloud.org/ECoulter/tutorial-containers/mymandle:latest
-->

We're going to share our containers via a registry, now, since in
normal practice, you won't be able to build containers on the same
host that you're submitting jobs from. This also aids the goal
of reproducible science - once your container is shared, you can share 
with collaborators (and enemies) or a community of users.

#### 3(a)
So, switch to your  brower and go to 
<https://tutorial.jetstream-cloud.org>.

Select **Login** on the top bar, and you'll be asked to authenticate
via Github (you will need to allow the application read-only access to your
GitHub profile).

#### 3(b)
Now, you'll have the ability to create "collections" of containers for other
users to access, and for yourself. This is an instance of the "SRegistry" software,
which underlies the main Singularity-Hub. 
Unlike Dockerhub, the SRegistry software organizes container images by
collection, in addition to username, so 
*click "New Collection" to create one now.*

Once you've created a collection, you're ready to upload via the Singularity client.
(Will everyone need a unique name here?!)

#### 3(c)
Register the remote:

```
singularity remote add --no-login TutorialSRegistry https://tutorial.jetstream-cloud.org
```

#### 3(d)
And authenticate:
```singularity remote login TutorialSRegistry```

Now you've got a token stored on this machine that will allow you continued access to the
registry.

#### 3(e)
Next, set that repository as your default:
```singularity remote use TutorialSRegistry```

(If you don't do this, be prepared for subsequent commands to fail without
adding --library https://tutorial.jetstream-cloud.org/).

#### 3(d)
Upload your container via the following, 
remembering to replace `$GITHUB_USERNAME` with your actual github username
used to authenticate to the registry and `YOUR-COLLECTION-NAME` with the name of
the collection you created earlier.
*Be sure to replace USERNAME with your current username, so you don't conflict with any other 
extant containers!*
```$ singularity push -U ex1.sif library://$GITHUB_USERNAME/$COLLECTION_NAME/$USERNAME-py3-dice:latest```

# Step 4: Running a job

Now, we're going to walk through using our container *from the registry* with an
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
module load gnu
module load openmpi
module load singularity

USERNAME="ECoulter"
COLLECTION_NAME="tutorial-containers"

singularity remote list
singularity remote use TutorialSRegistry

singularity run library://${USERNAME}/${COLLECTION_NAME}/py3-dice-example:latest 10
...
```

#### 4(b)
Go ahead and edit `GIT_USERNAME` and `COLLECTION_NAME` to fit your user, 
and submit to the scheduler via:
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
