# Further Resources

Here is a collection of links to more resources for further learning.
We have also added to this file based upon questions and topics raised during the tutorial.

## More Tutorials/Docs for Getting Started with Containers

* [Docker tutorial](https://docker-curriculum.com/)
* [Docker documentation](https://docs.docker.com/get-started/overview/)
* [Singularity tutorial](https://singularity-tutorial.github.io/)
* [Singularity documentation](https://sylabs.io/guides/3.5/user-guide/quick_start.html)

## More Examples of Containers
* [MATLAB Runtime Container](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/files/Example_MCR_Dockerfile)
* [XSEDE Container Template Library](https://github.com/XSEDE/container-template-lib)
    * A growing library of container templates for use on XSEDE systems
    * Version pinning, reproducible build and run
    * Examples include benchmarks, GPU samples, and more
* Radio Astronomy Container(s) - see last few slides of [Advanced Topics](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/10_AdvancedTopics.pdf)
* Weather Research and Forcasting model (WRF) containers
    * [NCAR - WRF Docker container](https://github.com/NCAR/WRF_DOCKER)
        * WRF Version 4.0.3
        * Compiled with GNU, uses OpenMPI
        * Designed as a tutorial for using WRF, not intended for production runs
    * [Aristotle Cloud Federation - WRF 3.8.1 Docker and Singularity Containers](https://github.com/federatedcloud/Docker-WRF-3.8.1-Fitch)
        * WRF Version 3.8.1 with patches for [known issues](https://www2.mmm.ucar.edu/wrf/users/wrfv3.8/known-prob-3.8.1.html)
        * Compiled with GNU, uses OpenMPI
        * Tested and usable for production runs
    * [Aristotle Cloud Federation - WRF 4.2.2 Docker and Singularity Containers](https://github.com/federatedcloud/WRFv4-Benchmarking)
        * WRF Version 4.2.2
        * Compiled with Intel, uses Intel MPI
        * Uses the Intel OneAPI HPC Toolkit container as a base image (see below)
        * Set up for running the CONUS 12km and 2.5km benchmarks
        * Configurations tested on bare metal and Docker in public cloud (`dev` branch)
        * Ongoing development for Singularity on Stampede2 (check back later)
* Intel OneAPI HPC Toolkit containers
    * [GitHub repository](https://github.com/intel/oneapi-containers)
    * [Toolkit Documentation](https://software.intel.com/content/www/us/en/develop/tools/oneapi/hpc-toolkit.html)
    * [Toolkit Containers Documentation](https://software.intel.com/content/www/us/en/develop/articles/containers/oneapi-hpc-toolkit.html)
    * [Dockerfiles](https://github.com/intel/oneapi-containers/tree/master/images/docker)
    * [DockerHub Images](https://hub.docker.com/r/intel/oneapi-hpckit)
    * [Singularity Definition files](https://github.com/intel/oneapi-containers/tree/master/images/singularity)

## Using R in Containers

There was a lot of discussion about R containers, so here are some relevant links.  There are several projects providing containers with R.  Some container images include other software as well.  Here's a small sample of what's available:

* [Official R Docker images on DockerHub](https://hub.docker.com/_/r-base) 
* [R and Singularity](https://rviews.rstudio.com/2017/03/29/r-and-singularity/)
* [The Rocker Project](https://www.rocker-project.org/) - Docker containers for R
* [Running Rocker in Singularity](https://www.rocker-project.org/use/singularity/)
* [Jupyter Docker containers](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html), including several oriented toward Data Science and including R
  * [Docker images on DockerHub](https://hub.docker.com/u/jupyter)
  * [Running a container](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/running.html)

# Containers with GPUs

Here are just a few links on getting started with containers with GPUs.  This is not comprehensive by any stretch.

* Some GPU examples exist in the [XSEDE Container Template Library](https://github.com/XSEDE/container-template-lib)
* [Docker with GPUs](https://docs.docker.com/config/containers/resource_constraints/#gpu)
* [Singularity with GPUs](https://sylabs.io/guides/3.5/user-guide/gpu.html)
* [NVIDIA article on NGC Deep Learning Containers with Singularity](https://developer.nvidia.com/blog/how-to-run-ngc-deep-learning-containers-with-singularity/)
* [NVIDIA Container Toolkit (Docker)](https://github.com/NVIDIA/nvidia-docker)
* [Tensorflow Docker](https://www.tensorflow.org/install/docker)
* [PyTorch Docker](https://github.com/pytorch/pytorch#docker-image)

