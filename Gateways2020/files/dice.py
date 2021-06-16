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
