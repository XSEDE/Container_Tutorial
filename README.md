# XCRI Presents: Deep Dive into Constructing Containers for Scientific Computing and Gateways

## Abstract
In recent years, using containers has been rapidly gaining traction as a solution to lower the barriers to using more software on HPC and cloud resources. However, significant barriers still exist to actually doing this in practice, particularly for well-established community codes which expect to run on a particular operating system version or resource. Additional barriers exist for researchers unfamiliar with containerization technologies. While many beginner tutorials are available for building containers, they often stop short of covering the complexities that can arise when containerizing scientific computing software. The goal of this full-day tutorial is to demonstrate and work through building and running non-trivial containers with users. We will containerize community scientific software, exhibit how to share with a larger community via a container registry, and then run on a completely separate HPC resource, with and without the use of a Science Gateway. The subject matter will be approachable for intermediate to advanced users, and is expected to be of interest to a diverse audience including researchers, support staff, and teams building science gateways.

## PEARC20

All tutorials at PEARC20 were shortened to half-day (~4 hrs), so the resulting tutorial is shorter than our planned full-day (~8 hrs).  If you are interested in the full-day tutorial, we presented it at Gateways2020 and the materials are shared here also.  The materials in the [PEARC20 directory](https://github.com/XSEDE/Container_Tutorial/tree/master/PEARC20) have been organized in order of how they were originally presented:

1. [**Introduction to Containers**](https://github.com/XSEDE/Container_Tutorial/blob/master/PEARC20/1_Introduction-to-Containers.pdf) by [Jeremy Fischer](https://github.com/jlf599), Indiana University
2. [**Simple Container Creation**](https://github.com/XSEDE/Container_Tutorial/blob/master/PEARC20/2_Simple-Container-Creation.pdf) by [Sanjana Sudarshan](https://github.com/sanjanasudarshan), Indiana University
3. [**Docker to Singularity Conversion**](https://github.com/XSEDE/Container_Tutorial/blob/master/PEARC20/3_Docker-To-Singularity.pdf) by [Peter Vaillancourt](https://github.com/sk8forether), Cornell University
4. [**Exercise 1 - Build, Share, and Run a Container**](https://github.com/XSEDE/Container_Tutorial/blob/master/PEARC20/4_Exercise-1.pptx) by [Eric Coulter](https://github.com/ECoulter), Indiana University
5. [**Docker MATLAB Runtime Container**](https://github.com/XSEDE/Container_Tutorial/blob/master/PEARC20/5_MATLAB.pptx) by [Stephen Bird](https://github.com/stebird), Indiana University
6. [**Containerization: Best Practices and Advanced Topics**](https://github.com/XSEDE/Container_Tutorial/blob/master/PEARC20/6_Advanced-Topics.pdf) by [Peter Vaillancourt](https://github.com/sk8forether)
7. [**Science Gateways**](https://github.com/XSEDE/Container_Tutorial/blob/master/PEARC20/7_Science-Gateways-Container-Tutorial.pdf) by [Suresh Marru](https://github.com/smarru), Indiana University

Supplemental materials, such as Dockerfiles and Exercise instructions, have been included as well.

## Gateways2020
The tutorial was presented at Gateways 2020 as a full day (~8 hrs) in total split up across 2 days.  The materials in the [Gateways2020 directory](https://github.com/XSEDE/Container_Tutorial/tree/master/Gateways2020) are organized in accordance with the schedule of events at the conference, as detailed in the list below.  Supplemental materials, such as Dockerfiles and Exercise instructions, have been included as well.

### Day 1
#### Part 1 (1 hr 30 min)
1. [**Introduction to Containers**](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day1_1_Introduction-to-Containers.pdf) by [Jeremy Fischer](https://github.com/jlf599), Indiana University
    * Discussion of how containers can help Gateways
    * What is Docker?
    * Docker Hub
    * What is Singularity?
    * SingularityHub
    * Differences / relationship to each other

2. [**Environment Introduction**](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day1%20Ex%201%20Part%20A%20-%20Overview%20and%20Login.md) by [Eric Coulter](https://github.com/ECoulter), Indiana University
    * Distributed login credentials for tutorial resources (not available outside of conference attendance)
    * Overview of container development environment

3. [**Simple (Docker) Container Creation**](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day_1_3_Simple_Container_Creation.pdf) by [Sanjana Sudarshan](https://github.com/sanjanasudarshan), Indiana University
    * Build via Dockerfile
    * Exploring Dockerfile structure/conventions
    * Container examples

4. [**Exercise - Docker Build**](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day1%20Ex%201%20Part%20B%20-%20Docker%20Build.md) by [Stephen Bird](https://github.com/stebird), Indiana University
    * Build simple Docker container

#### Part 2 (1 hr 30 min)
5. [**Singularity Containers**](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day_1_5_Singularity_Overview.pdf) by [Eric Coulter](https://github.com/ECoulter), Indiana University
    * Definition Files
    * Creating Singularity containers (from scratch)
    * Singularity user environment

6. [**Docker To Singularity Conversion**](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day1_6_DockerToSingularity.pdf) by [Peter Vaillancourt](https://github.com/sk8forether), Cornell University
    * Best Practices for conversion
    * Example conversion

7. [**Exercise - Singularity**](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day1%20Ex%201%20Part%20C%20-%20Singularity%20Conversion.md) by [Eric Coulter](https://github.com/ECoulter), Indiana University
    * Convert to Singularity
    * Build via definition file
    * [Upload to registry](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day1%20Ex%201%20Part%20D:%20%20Upload.md)
    * [Run via SLURM](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day1%20Ex%201%20Part%20E:%20%20Running.md)

8. **Gateways Tie-in** by [Suresh Marru](https://github.com/smarru), Indiana University
    * Overview of components in a Gateway lifecycle
    * Big picture in a gateways context
    * Discuss Part 4 Bucket choice

### Day 2
#### Part 3 (1 hr 30 min)
1. **Open Q&A** by [Jeremy Fischer](https://github.com/jlf599), Indiana University
    * Catchup and unresolved questions

2. [**Exercise - MATLAB Container Build**](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day2_2_MATLAB_Container_Build.pdf) by [Stephen Bird](https://github.com/stebird), Indiana University
    * [Dockerfile](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/MCR_Dockerfile) walkthrough
    * [Container build and run](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day2%20Ex%202:%20MATLAB-Container-Run%20Exercise.md)
    * Conversion

3. [**Best Practices & Advanced Topics**](https://github.com/XSEDE/Container_Tutorial/blob/master/Gateways2020/Day2_3_AdvancedTopics.pdf) by [Peter Vaillancourt](https://github.com/sk8forether), Cornell University
    * Lifecycle of Containers
    * Development vs. Production
    * Reducing container sizes
    * Data management
    * Reproducibility
    * Security
    * Container Orchestration

#### Part 4 (1 hr 30 min)
4. **Containers for Gateways with Exercises** by [Suresh Marru](https://github.com/smarru), Indiana University
    * Intro to Gateways
    * Sign in to a gateway and run a pre-packaged containerized application with pre-provided inputs
    * Execute applications with user provided input files and plot outputs
    * Add a Containerized application to the Gateway
    * Goals to Cover:
      * What is a Gateway for?
      * What features do Gateways add when using containers?
      * How can Gateways now enable the community with these containers?
      * Run/provide your app via a gateway!

5. **Bucket of Topics (Open to Audience Input)** by [Eric Coulter](https://github.com/ECoulter) and [Suresh Marru](https://github.com/smarru), Indiana University
    * Gateway Hosting
    * Container Orchestration and management
    * CI/CD Overview (Code -> Gateways pipelines)
    * Container Registries (Building or usage of public registries)
    * Decisions about container vs. host for software/dependency locality

## Questions?
If you have Questions, please contact us via
`help@xsede.org` with XCRI in the subject line. 
