# Day 2, Part 1 MATLAB Container Build and Run

First, ensure we can login to the MATLAB Licensed host.  This host is different from the host we used yesterday:
```bash
ssh train**@149.165.170.239
```

Make a working directory for our MATLAB code:
``` bash
mkdir workdir
cd workdir/
```

We are going to write some simple matlab code using your favorite editor.  For this tutorial, I will be using 'mdimensionalArray.m'.  Make sure when you name the file it ends in a ".m" or the MATLAB compiler won't be able to read the file.  Add in the following code:
```
A = [1 2 3; 4 5 6; 7 8 9]
A(:,:,2) = [10 11 12; 13 14 15; 16 17 18]
B = cat(3,A,[3 2 1; 0 9 8; 5 3 7])
```

__You can use alternative code if you would like, however we may not be able to debug it if something goes awry.__

Then we can compile the code for the standalone MCR program:
``` bash
mcc -m mdimensionalArray.m
```

Now we need to move the compiled code over to 149.165.157.56.
``` bash
scp mdimensionalArray train**@149.165.157.56:~/
```

__Notice we are only copying the compiled executable and NOT what we wrote!__

Or the compiled code can be found here, on the container host:
``` bash
cp /opt/ohpc/pub/examples/mdimensionalArray ~/
```

Login back into the container host.  
```bash
ssh train**@149.165.157.56
```

Then we can create a new directory and copy the file in it:
```bash
mkdir matlab-dir
cp mdimensionalArray matlab-dir/
```

 Then we move into a new directory:
```
cd matlab-dir/
```

Let's copy a few files into our new directory.  First, let's grab the Dockerfile with:
```bash
cp /opt/ohpc/pub/examples/ex2_matlab.txt ~/matlab-dir/Dockerfile
```

Next, we need to copy over the MATLAB container runtime:
```bash
cp /opt/ohpc/pub/examples/MCR_R2018a_glnxa64_installer.zip ~/matlab-dir/mcr_installer.zip
```

Once we copy that, we can take a look at our Dockerfile with cat or less:
```
FROM centos:7

RUN mkdir /opt/mcr                      && \
yum install wget unzip libXmu -y        && \
mkdir /mcr-install

ADD MCR_R2018a_glnxa64_installer.zip /mcr-install/MCR_installer.zip

RUN cd /mcr-install && \
ls -l && pwd && \
unzip MCR_installer.zip    && \
./install -mode silent -agreeToLicense yes -destinationFolder /opt/mcr && \
rm -Rf /mcr-install

ENV LD_LIBRARY_PATH=/opt/mcr/v94/runtime/glnxa64:/opt/mcr/v94/bin/glnxa64:/opt/mcr/v94/sys/os/glnxa64:/opt/mcr/v94/extern/bin/glnxa64
ENV XAPPLRESDIR=/usr/share/X11/app-defaults

ADD mdimensionalArray /mdimensionalArray
RUN chmod +x mdimensionalArray
```

Alternatively, you can copy the dockerfile from the shared directory:
```bash
cp /opt/ohpc/pub/examples/ex2_matlab.txt ~/matlab-dir/Dockerfile
```

__If you used a different name for your MATLAB code, you will have to change it in the final line of the Dockerfile!__


Build our container with the following:  *This WILL take some time!*
```bash
docker build --tag train**-mcr .
```
__Also, make sure you change train\*\*-mcr to your current username!__

While we build, we can answer questions and go over what's in the dockerfile.

Once the build has completed, we can run our container:
``` bash
docker run train**-mcr ./mdimensionalArray
```
__Watch out for that tricky train\*\*-mcr again! Also, watch the name of the file that was transfered into your container!__

