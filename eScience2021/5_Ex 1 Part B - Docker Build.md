# Day 1, Ex 1 Part B: Docker Build
## Build, Convert, and Run an HPC job with a Container

First of all, the example files we'll be using are all available
in `/opt/ohpc/pub/examples`.

We''l be building an app that creates a gif file showing a 'zoom in' along a 
straight trajectory of the Mandlebrot set plotted in black and white.
Once we've built the container, we'll take a look at how to actually use the app.

# Step 1: The Dockerfile
This particular example will use a local git repository with built-in 
Dockerfile to build a simple container. The repository is available at
```/opt/oh/c/pub/exampled/mandle-zoom-py```

#### 1(a) - Create a local repo
Create a work directory in your homedir:
```$ mkdir ~/ex1-workdir```

and cd into it:
```$ cd ~/ex1-workdir```

Now, make your own copy of the git repository:
```$ git clone /opt/ohpc/pub/examples/mandle-zoom-py```

Move into your local copy of the repository and examine the contents:
```$ cd ./mandle-zoom-py && ls 
Dockerfile      parallel_mandle.py  zoom_mandle.py Mandle.def      README.md
```

#### 1(b) - Examine the Dockerfile
Examine the contents:
```$ cd ~/ex1-workdir
$ cat ./Dockerfile
#Using a slim Debian base image tagged at a specific date
FROM debian:buster-20210621-slim

#The next two steps install OS-level dependencies
RUN apt update

RUN apt install -y zlib1g-dev \
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

#Here, we install python deps - this could be done via a requirements.txt file as well
#  but left explicit here for illustrative purposes
RUN  python3 --version && \
     python3 -m pip install --upgrade pip wheel && \
     python3 -m pip install --upgrade Pillow numpy && \
     python3 -m pip list && \
     which python3

#Add our python scripts into the container where they're available to the
# default $PATH
COPY  ./parallel_mandle.py /usr/local/bin/mandle/parallel_mandle.py
COPY  ./zoom_mandle.py /usr/local/bin/mandle/zoom_mandle.py

#Make the main script executable
RUN chmod 755 /usr/local/bin/mandle/zoom_mandle.py

#Set the entrypoint to our app with extra CMD to run --help by default
ENTRYPOINT ["/usr/local/bin/mandle/zoom_mandle.py"]
CMD ["--help"]
```

#### 1(c) - Docker environment
Now, we can check which Docker images are built on the system with:
```bash
$ docker images
```

We won't see many built images on the system, but we can change that by building
 the image from the Dockerfile via the following command:

```$ docker build -t $USER:mandle-zoom .```

The build should take around 3-4 minutes, and generate quite a bit of output.
The final output should appear something like the following:
```
...
Package       Version
------------- -------
asn1crypto    0.24.0
cryptography  2.6.1
entrypoints   0.3
keyring       17.1.1
keyrings.alt  3.1.1
numpy         1.21.0
Pillow        8.3.1
pip           21.1.3
pycrypto      2.6.1
PyGObject     3.30.4
pyxdg         0.25
SecretStorage 2.3.1
setuptools    40.8.0
six           1.12.0
wheel         0.36.2
/usr/bin/python3
Removing intermediate container 9654cfaa2dae
 ---> 6908e8eddf4b
Step 7/9 : RUN chmod 755 /usr/local/bin/mandle/zoom_mandle.py
 ---> Running in 1ee44e03d219
Removing intermediate container 1ee44e03d219
 ---> a50f70e6b1d3
Step 8/9 : ENTRYPOINT ["/usr/local/bin/mandle/zoom_mandle.py"]
 ---> Running in e72a081ac76b
Removing intermediate container e72a081ac76b
 ---> 4169a0c07b8e
Step 9/9 : CMD ["--help"]
 ---> Running in 0873c0629748
Removing intermediate container 0873c0629748
 ---> 4b5f99edff97
Successfully built 4b5f99edff97
Successfully tagged train99:mandle-zoom
```

If we check the list of built images, we can see our built image with:
```bash
$ docker images
```

We can check which containers are running locally with the following command:
```bash
$ docker ps
```
However, this won't show any containers running yet.  To run this container, we can use 
the following to view help for the application:
```bash
$ docker run <USER>:mandle-zoom
usage: zoom_mandle.py [-h] [-n NPROCS] [-d DUR] [-s NSTEPS] [-w SWIN]
                      [-f FWIN] [-o ORIGIN ORIGIN]
                      output_file

positional arguments:
  output_file           Output filename - in GIF format

optional arguments:
  -h, --help            show this help message and exit
  -n NPROCS, --nprocs NPROCS
                        Number of multiprocessing threads to spawn
  -d DUR, --dur DUR     Frame speed of GIF in microseconds
  -s NSTEPS, --nsteps NSTEPS
                        Number of steps in the zoom
  -w SWIN, --swin SWIN  Size of the starting frame
  -f FWIN, --fwin FWIN  Size of the ending frame
  -o ORIGIN ORIGIN, --origin ORIGIN ORIGIN
                        Center of the frame in c-space, space delimited
```

For now, we'll just use the default arguments for the app, and supply an output filename
to verify that things are working:

```
docker run -u $(id -u):$(id -g) -v ${PWD}:${PWD} --rm=true <USER>:mandle-zoom ${PWD}/test.gif
```

While that's running (should take only 30 seconds or so), take a moment to look 
at that command in more detail:

There are three extra flags we used with ```docker run``` to make this work nicely:

```-u $(id -u):$(id -g)```
tells Docker to run the process as your CURRENT USER - otherwise it would run
as root, and you wouldn't be able to open the resulting file!

The second piece, 
```-v ${PWD}:${PWD}```
bind-mounts your current directory to the container, so that you're able to
actually *get* your output file. Without this, the file would be written to
the internal container filesystem, and wouldn't be available after the script 
finishes.

Finally, 
```--rm true```
makes sure that the container is removed after the script finishes. Docker typically
expects to keep a container around in cached memory, but for this case it isn't necessary
or helpful.

This will create a file in your current directory - you can transfer it to your 
local machine by running the following:

```scp <USER>@pearc21-contut.jetstream-cloud.org:ex1-workdir/mandle-zoom-py/test.gif ./```

[Continue to the convert exercise - Day1 Part C](https://github.com/XSEDE/Container_Tutorial/blob/main/eScience2021/Day1%20Ex%201%20Part%20C%20-%20Singularity%20Conversion.md)
