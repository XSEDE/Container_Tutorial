# Day 1, Part 2 Build-Convert-Run Exercise: Conversion to Singularity
## Build, Convert, and Run an HPC job with a Container


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
Now, take a look in an editor **(there is a $USERNAME variable that must be changed on line 2)**:
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
sudo command. Shell expansion happens **before** the sub-process, however, 
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


[Continue to the upload exercise - Day1 Part2d](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day1%20Part2d%20-%20Build-Convert-Run%20Exercise%20-%20Upload.md)
