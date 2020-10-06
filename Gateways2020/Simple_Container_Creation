# Simple Container Build

Here is what we are going to do for simple container creation.

We are going to build containers.  

Check out these commands:

``` bash
Docker images
Docker ps --all
```

Here is the provided code:

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

``` bash
Docker build -t DiceRoller .

Docker run -i DiceRoller
```

