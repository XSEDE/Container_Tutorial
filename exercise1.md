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

Create a local work directory:
```$ mkdir ./ex1-workdir```
and make your own copy named `Dockerfile`:
```cp /opt/ohpc/pub/examples/ex1_docker.txt ~/ex1-workdir/Dockerfile```

Examine the contents:
```cd ~/ex1-workdir```
```cat ./Dockerfile
# our base image
FROM alpine:3.9

# install python and pip
RUN apk add --update py3-pip

# copy files required for the app to run
COPY /opt/ohpc/pub/examples/dice.py /usr/src/app/

# run the application
CMD python3 /usr/src/app/dice.py
```

The dice.py script will "roll" a pair of dice a certain number
of times, and return some very basic information about the results:
```cat /opt/ohpc/pub/examples/dicy.py
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

Now, you can build the image from the Dockerfile via:
```sudo docker build -t $USERNAME/py3-dice .```

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
docker images
```

# Step 2: Conversion to Singularity
Now that you've built a Dockerfile, it's time to make it useable in our 
HPC environment.

First, load the `singularity` module:
```$ module load singularity```

This will give your shell session access to the Singularity executable, etc.
We're going to convert by simply including the Docker image
in our Singularity Definition file. It's also possible to convert the image
directy, but we want to illustrate the use of a Docker image as a base 
for cases where it's necessary to modify the environment further.

Make a local copy of the example Singularity definition file available in
our examples folder:

```$ cp /opt/ohpc/pub/examples/ex1_singularity.txt ~/ex1-workdir/Dice.def```

(notice the .def extension - it's still just a text file, but
this is the convention used in Singularity documentation for 
human-friendliness!)

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

Now, to build the container:

```sudo $(which singularity) build ex1.sif Dice.def```

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

#Step 3: Upload to a Registry
;works: singularity pull shub://tutorial.jetstream-cloud.org/tutorial-containers/numpy-pillow:latest
;works: singularity pull library://ECoulter/tutorial-containers/mymandle:latest
;fails: singularity pull library://ECoulter/tutorial-containers/numpy-pillow:latest
;works: singularity push -U mymandle.sif library://ECoulter/tutorial-containers/mymandle:latest
;fails: singularity push -U mymandle.sif library://tutorial.jetstream-cloud.org/ECoulter/tutorial-containers/mymandle:latest

We're going to share our containers via a registry, now, since in
normal practice, you won't be able to build containers on the same
host that you're submitting jobs from. This also aids the goal
of reproducible science - once your container is shared, you can share 
with collaborators (and enemies) or a community of users.

So, switch to your  brower and go to 
<https://tutorial.jetstream-cloud.org>.

Select **Login** on the top bar, and you'll be asked to authenticate
via Github (you will need to allow the application read-only access to your
GitHub profile).

Now, you'll have the ability to create "collections" of containers for other
users to access, and for yourself. This is an instance of the "sregistry" software,
which underlies the main Singularity-Hub.
(MORE DESCRIPTION HERE)

Once you've created a collection, you're ready to upload via the Singularity client.
(Will everyone need a unique name here?!)

Register the remote:
```singularity remote add --no-login TutorialSRegistry https://tutorial.jetstream-cloud.org```

And authenticate:
```singularity remote login TutorialSRegistry```

Now you've got a token stored on this machine that will allow you continued access to the
registry.

Upload your container via the following, 
remembering to replace `$USERNAME` with your actual github username
used to authenticate to the registry and `YOUR-COLLECTION-NAME` with the name of
the collection you created earlier.
```$ singularity push -U Dice.sif library://$USERNAME/$COLLECTION_NAME/py3-dice:latest```

# Step 4: Running a job
Please make a local copy of the Slurm example job file:
```
$ cp /opt/ohpc/examples/slurm_example.job ~/ex1-workdir
$ cat slurm_example.job
...
```

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