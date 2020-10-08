# Simple Container Build

Ensure you can login to the build environment with your training account to the ip address <Insert ip address here>.

``` bash
ssh train**@<Insert Ip address>
```

First, we can take a look at which container images are built:
``` bash
docker images
```

This will return no images or very few yet.  We can also check running containers with:

``` bash
docker ps --all
```

There probably won't be any images running.  Let's go ahead and write some Python code to put inside a container.  You can write your own code if you want, but we won't be able to debug if the code goes sideways.  Before that, let's create a directory to isolate these files and move into that directory:

``` bash
mkdir diceroll
cd diceroll
```

Create a file with your favorite editor (vi/nano/emacs) like so:

``` bash
vi diceroll.py
```

And add in the following code:

``` Python3
import random
min = 1
max = 6

roll_again = "yes"

while roll_again == "yes" or roll_again == "y":
    print ("Rolling the dice...")
    print ("The values are...")
    print (random.randint(min, max))
    print (random.randint(min, max))
    roll_again = input("Roll the dice again?")
```

Now, we need to create the Dockerfile, which is the recipe for the actual container.  Using your favorite editor, create a file named Dockerfile and add in the following:

``` docker
# our base image
FROM alpine:3.9

# install python and pip
RUN apk add --update py3-pip

# run the application
CMD ["python3" , "/usr/src/app/diceroll/py"]
```

Now we can build the container, named DiceRoller, with the following:

``` bash
docker build -t DiceRoller .
```

This may take a few moments to build, but afterwards we can see the built image with the following:

``` bash
docker images
```

Which will show your built container image.  Let's run the actual container.  The -i flag will allow the container to run in interactive mode, allowing you to pass keystrokes into the container.  Run the container with the following:

``` bash
Docker run -i DiceRoller
```

