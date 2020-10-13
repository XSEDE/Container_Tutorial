# Day 1, Part 2 Build-Convert-Run Exercise: Build and Convert
## Build, Convert, and Run an HPC job with a Container

First of all, the example files we'll be using are all available
in `/opt/ohpc/pub/examples`.

# Step 1: The Dockerfile
To begin with, we've got a dockerfile similar to what you've
seen already available in:
```/opt/ohpc/pub/examples/ex1_docker.txt```

#### 1(a)
Create a work directory in your homedir:
```$ mkdir ~/ex1-workdir```

and cd into it:
```$ cd ~/ex1-workdir```

now, make your own copy of the dockerfile mentioned above named `Dockerfile`:
```$ cp /opt/ohpc/pub/examples/ex1_docker.txt ~/ex1-workdir/Dockerfile```

#### 1(b)
Examine the contents:
```$ cd ~/ex1-workdir
$ cat ./Dockerfile
# our base image
FROM alpine:3.9

# install python and pip
RUN apk add --update py3-pip

# copy files required for the app to run
COPY dice.py /usr/src/app/

# run the application
CMD python3 /usr/src/app/dice.py
```

#### 1(c)
Notice that the COPY directive refers to a file we don't have in
the current working directory. It's not possible to COPY or ADD files from 
"above" the current location, so we'll need to grab that as well:

```$ cp /opt/ohpc/pub/examples/dice.py ~/ex1-workdir/dice.py```

The dice.py script will "roll" a pair of dice a certain number
of times, and return some very basic information about the results:

```$ cat /opt/ohpc/pub/examples/dice.py
#!/usr/bin/env python3
import random
minimum = 1
maximum = 6
number_of_rolls=int(input("How many times would you like to roll the dice?"))

print("Rolling the dice",str(number_of_rolls),"times...")
results=[]
for i in range(0,number_of_rolls):
# Roll two dice for each step
#  and gather into a list of tuples [(roll1_1,roll1_2),(roll2_1,roll2_2)...]
  results+=[(random.randint(minimum, maximum),random.randint(minimum,maximum))]

#add both die in each round, getting a list of round totals
totals=list(map(sum,results))

average=sum(totals)/len(totals)

print("You rolled the dice ",number_of_rolls,"times, getting an average value of ",average,".")
print("The highest round was:",max(totals))
print("The lowest round was:",min(totals))
```

#### 1(d)
Now, you can build the image from the Dockerfile via the following
command, but be sure to replace $USERNAME with you current username:

```$ sudo docker build -t $USERNAME/py3-dice .```

Which should generate output similar to:
```
Sending build context to Docker daemon 3.584 kB
Step 1/4 : FROM alpine:3.9
 ---> 78a2ce922f86
Step 2/4 : RUN apk add --update py3-pip
 ---> Using cache
 ---> 9f3157db35ca
Step 3/4 : COPY dice.py /usr/src/app/
 ---> 7e6a1a4603d1
Removing intermediate container eda9b8c81a12
Step 4/4 : CMD python3 /usr/src/app/dice.py
 ---> Running in a76788b898d7
 ---> d7bb6e1691d8
Removing intermediate container a76788b898d7
Successfully built d7bb6e1691d8
```

To view the list of images available locally, run
```
$ sudo docker images
```
