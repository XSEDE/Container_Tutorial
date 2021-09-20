# PEARC21
This tutorial was presented at PEARC21 as a full day (~8 hrs) tutorial.
The materials in the [PEARC21 directory](https://github.com/XSEDE/Container_Tutorial/tree/main/PEARC21) are organized in accordance with the schedule of events at
the conference, as detailed in the list below.  Supplemental materials, such as Dockerfiles and Exercise instructions, have been included as well.

## Schedule
1. [**Introduction to Containers**](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/1_Introduction-to-Containers.pdf) by [Jeremy Fischer](https://github.com/jlf599), Indiana University
    * What is Docker?
    * DockerHub
    * What is Singularity?
    * Singularity Image hosting (goodbye SingularityHub)
    * Differences / relationship to each other

2. **Gateways Tie-in** by [Suresh Marru](https://github.com/smarru), Indiana University
    * Overview of components in a Gateway lifecycle
    * Big picture in a Gateways context

3. [**Environment Introduction**](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/3_Environment-Introduction.pdf) by [Eric Coulter](https://github.com/ECoulter), Indiana University
    * Distributed login credentials for tutorial resources (not available outside of conference attendance)
    * Overview of container development environment
    * See [Exercise 1 Part A - Overview and Login](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/3_Ex%201%20Part%20A%20-%20Overview%20and%20Login.md)

4. [**Simple (Docker) Container Creation**](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/4_Simple_Container_Creation.pdf) by [Sanjana Sudarshan](https://github.com/sanjanasudarshan), Indiana University
    * Build via Dockerfile
    * Exploring Dockerfile structure/conventions
    * Container examples

5. [**Exercise 1 Part B - Docker Build**](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/5_Ex%201%20Part%20B%20-%20Docker%20Build.md) by [Stephen Bird](https://github.com/stebird), Indiana University
    * Build simple Docker container

6. [**Singularity Overview**](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/6_Singularity_Overview.pdf) by [Eric Coulter](https://github.com/ECoulter), Indiana University
    * Definition Files
    * Creating Singularity containers (from scratch)
    * Singularity user environment

7. **Exercise 1 Part C and D - Singularity** by [Eric Coulter](https://github.com/ECoulter), Indiana University
    * [Singularity Conversion](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/7_Ex%201%20Part%20C%20-%20Singularity%20Conversion.md)
    * [Run via SLURM](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/7_Ex%201%20Part%20D%20-%20Running.md)

8. [**Best Practices & Advanced Topics**](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/8_AdvancedTopics.pdf) by [Peter Vaillancourt](https://github.com/sk8forether), Cornell University
    * [Docker To Singularity Conversion](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/8_DockerToSingularity.pdf) (quick overview)
    * Lifecycle of Containers
    * Development vs. Production
    * Reducing container sizes
    * Data management
    * Reproducibility
    * Security
    * Container Orchestration

9. **Open Q&A** by [Jeremy Fischer](https://github.com/jlf599), Indiana University
    * Catchup and unresolved questions

10. **Containers for Gateways with Exercises** by [Suresh Marru](https://github.com/smarru), Indiana University
    * Intro to Gateways
    * Sign in to a gateway and run a pre-packaged containerized application with pre-provided inputs
    * Execute applications with user provided input files and plot outputs
    * Add a Containerized application to the Gateway
    * Goals to Cover:
      * What is a Gateway for?
      * What features do Gateways add when using containers?
      * How can Gateways now enable the community with these containers?
      * Run/provide your app via a gateway!

11. [**Further References**](https://github.com/XSEDE/Container_Tutorial/blob/main/PEARC21/11_Further_References.md)
    * More Tutorials/Docs for Getting Started with Containers
    * More Examples of Containers
    * Using R in Containers
    * Containers with GPUs