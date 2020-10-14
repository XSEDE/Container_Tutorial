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

We are going to write some simple matlab code using your favorite editor.  Make sure when you name the file it ends in a ".m" or the MATLAB compiler won't be able to read the file.  Add in the following code:
```
A = [1 2 3; 4 5 6; 7 8 9]
A(:,:,2) = [10 11 12; 13 14 15; 16 17 18]
B = cat(3,A,[3 2 1; 0 9 8; 5 3 7])
```

*You can use alternative code if you would like, however we may not be able to debug it if something goes awry.*

Then we can compile the code for the standalone MCR program:
``` bash
mcc -m mdimensionalArray.m
```

Now we need to move the compiled code over to 149.165.157.56.
``` bash
scp mdimensionalArray train**@149.165.157.56:~/
```

*Notice we are only copying the compiled executable and NOT what we wrote!*

Or the compiled code can be found here, on the container host:
``` bash
cp /opt/ohpc/pub/examples/ ~/
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
mkdir matlab-dir
cd matlab-dir/
```

Create a file named `dockerfile` and include this:
```
FROM centos:7

RUN mkdir /opt/mcr                     && \
yum install wget unzip libXmu -y       && \
mkdir /mcr-install                     && \
cd /mcr-install                        && \
wget https://ssd.mathworks.com/supportfiles/downloads/R2018a/deployment_files/R2018a/installers/glnxa64/MCR_R2018a_glnxa64_installer.zip && \
unzip MCR_R2018a_glnxa64_installer.zip && \
./install -mode silent -agreeToLicense yes -destinationFolder /opt/mcr && \
rm -Rf /mcr-install

ENV LD_LIBRARY_PATH=/opt/mcr/v94/runtime/glnxa64:/opt/mcr/v94/bin/glnxa64:/opt/mcr/v94/sys/os/glnxa64:/opt/mcr/v94/extern/bin/glnxa64
ENV XAPPLRESDIR=/usr/share/X11/app-defaults

ADD mdimensionalArray /mdimensionalArray
RUN chmod +x mdimensionalArray
```

Build our container with the following:  *This WILL take some time!*
```bash
docker build --tag train**-mcr .
```
*Also, make sure you change train**-mcr to your current username!*

While we build, we can answer questions and go over what's in the dockerfile.

Once the build has completed, we can run our container:
``` bash
docker run train**-mcr ./mdimensionalArray
```
*Watch out for that tricky train**-mcr again!*

