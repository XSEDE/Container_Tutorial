# Build-Convert-Run Exercise: 
## Build, Convert, and Run an HPC job with a Container

# Overview and Login

We're going to take one one of the Dockerfiles you've already seen, build the docker image, convert it to Singularity, and run a job using the Slurm job scheduler. 


**PLEASE NOTE**: The instructor will be using vim for any file editing that needs to be done - you may also use nano. 

## The Infrastructure

You'll be using a virtual cluster in the Jetstream cloud for these exercises. This is a multi-user system, so please be careful!

Host name is: ***sgci21-contut.jetstream-cloud.org***

Please login now via ssh, using your username and password provided via email!

``` bash
ssh trainXX@sgci21-contut.jetstream-cloud.org
```

-----
**If you have not received your login information, please let us know via chat!**
=====

First of all, the example files we'll be using are all available in `/opt/ohpc/pub/examples`.

If you've logged in, great! Feel free to look around while we ensure everyone has access to the system.
Take a moment to try out the environment module system, via the 'module' command:
```
$ module avail
$ module show singularity
```

[Continue to the build exercise - Ex 1 Part B](https://github.com/XSEDE/Container_Tutorial/blob/main/SGCI2021/Ex%201%20Part%20B%20-%20Docker%20Build.md)
