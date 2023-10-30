import random

myList = [1, 2, 3, 4, 5, 6, 7, 8, 9]

diff = 9 - 3
for x in range(diff):
    del myList[8-x]

print(myList)