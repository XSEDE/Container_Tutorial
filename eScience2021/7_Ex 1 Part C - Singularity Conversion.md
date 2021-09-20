# Day 1, Ex 1 Part C: Conversion to Singularity
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

#### 2(b) - Quick Look at a .def file
In your local copy of the mandle-zoom-py repo, you may have noticed a file
earlier called ```Mandle.def``` 
Take a look in an editor:
```
$ cd ~/ex1-workdir/mandle-zoom-py
$ vim ./Mandle.def
BootStrap: docker
From: library/debian:buster-20210621-slim

%files

  ./parallel_mandle.py /usr/local/bin/mandle/parallel_mandle.py
  ./zoom_mandle.py /usr/local/bin/mandle/zoom_mandle.py

%post
  apt update
  apt install -y zlib1g-dev \
                 libjpeg-dev \
                 libfreetype6-dev \
                 liblcms2-dev \
                 libopenjp2-7-dev \
                 libtiff-dev \
                 tk-dev \
                 tcl-dev \
                 libharfbuzz-dev \
                 libfribidi-dev \
                 python3 \
                 python3-pip

  python3 --version
  python3 -m pip install --upgrade pip wheel
  python3 -m pip install --upgrade Pillow numpy
  python3 -m pip list
  which python

  chmod 755 /usr/local/bin/mandle/zoom_mandle.py

%runscript
  /usr/local/bin/mandle/zoom_mandle.py

%help
 This container includes the python Pillow and numpy libraries, needed to run
 Eric's Mandlebrot gif generator, at /usr/local/bin/mandle/zoom_mandle.py.
```

This does the exact same thing as the Dockerfile we used earlier! 
Notice the syntax is a little simpler - no need to prepend every command with RUN.

However, we've already done the work of building this in Docker, why not just convert?

#### 2(d)
Now, to let Singularity do the work of converting the container:

```$ singularity pull mandle.sif docker-daemon:<USERNAME>:mandle-zoom```

The output should look like:

```
INFO:    Converting OCI blobs to SIF format
INFO:    Starting build...
Getting image source signatures
Copying blob 764055ebc9a7 done  
Copying blob b5826c81c1c5 done  
Copying blob 281c9068b2be done  
Copying blob 12b71f64dde8 done  
Copying blob 48309e996d01 done  
Copying blob 4a67c9195176 done  
Copying blob 3297a8df8bfe done  
Copying config 32644cd2aa done  
Writing manifest to image destination
Storing signatures
2021/07/13 19:48:15  info unpack layer: sha256:b12657fc275830d8d55d4d00fc003bd809f937f9d31055b771932980f1b34987
2021/07/13 19:48:17  info unpack layer: sha256:e9d8f68ca0663ab46620208c91518684ae4613f446d13fa0a57e32ab86827942
2021/07/13 19:48:17  info unpack layer: sha256:3c8049f01c4ae822016494d3a9a1cf46f83813fe7f3b20de2f8d827d5eb9df7b
2021/07/13 19:48:17  info unpack layer: sha256:30c8416db8be56b2e40d686502db8edc84d588fda25a825a346abd3c8366902b
2021/07/13 19:48:17  info unpack layer: sha256:b382c95ce3e94494edd4eb1a2ad20a4fd040ce28e920b02004bdc73a824a530e
2021/07/13 19:48:26  info unpack layer: sha256:7e9c594472a090ef94067770035e775983f3bca73c5f5419e52b614e13dc816a
2021/07/13 19:48:28  info unpack layer: sha256:b5f7283d69c5094d2e4e1a820e8bbe008bd914c58707c9b42f1c3a80191dfaf4
INFO:    Creating SIF file...
```

<!--
The reason we're using `which` is thanks to the combination of Singularity's 
trust model and the module system - users are not allowed to build containers
without root permissions (because the build process can require touching
files that require root access), and the environment variables loaded by
the singularity modules do not transfer to the sub-process spawned by the
sudo command. Shell expansion happens **before** the sub-process, however, 
so we're still able to leverage environment settings, rather than using
the whole path to the binary.
-->

This will produce an image file in .sif format in your local directory.

Most of this is the actual Docker-Singularity conversion taking place automatically!
Each layer of the Docker container is copied into a temporary space, 
unpacked, the steps in the definition file are applied, and then the result is 
packed in a SIF file.

We can see some interesting details about our new Singularity container via the
```singularity inspect```
command:

```$ singularity inspect mandle.sif```

We can also see the Definition file used to create the container:

```$ singularity inspect -d mandle.sif```

In this case, there isn't much information - if we were handing this off to 
someone else, it would be kinder to build via a proper definition file!

[Continue to the next exercise - Day1 Part D](https://github.com/XSEDE/Container_Tutorial/blob/main/eScience2021/7_Ex%201%20Part%20D%20-%20Running.md)
