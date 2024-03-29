# Day 1, Ex 1 Part A Build-Convert-Run Exercise: 
## Build, Convert, and Run an HPC job with a Container

# Overview and Login

We're going to take a Dockerfiles similar to those you've already seen, build the docker image, convert it to Singularity, and run a job using the Slurm job scheduler. 

**PLEASE NOTE**: The instructor will be using vim for any file editing that needs to be done - you may also use nano. 

# Conventions:
We use a few conventions throught these exercises that are important to keep
in mind while reading here. Lines that begin with a ```$``` denote a command to be run
on the remote system, like
```$ whoami```
This is common when indicating a shell prompt on a Linux-based machine.

Output will sometimes follow these!

The second thing to watch for is the presence of all-caps variables inside angle 
brackets, like ```<USERNAME>``` - 
this means YOU need to replace this with the username you use to login to
the remote system with when running the command!
```$ echo "I am <USERNAME>"```

## Usernames

Please go to 

```https://bit.ly/3CgeoKv```

to select your username!

## The Infrastructure

You'll be using a virtual cluster in the Jetstream cloud for these exercises. This is a multi-user system, so please be careful!

Host name is: ***sc21-contut.jetstream-cloud.org***

``` bash
ssh <USERNAME>@sc21-contut.jetstream-cloud.org
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

[Continue to the build exercise - Day1 Part B](https://github.com/XSEDE/Container_Tutorial/blob/main/SC21/5_Ex%201%20Part%20B%20-%20Docker%20Build.md)
