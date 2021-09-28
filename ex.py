import numpy as np

x = np.zeros((5,5))
y = np.zeros((5,5))

for row in x:
    for element in row:
        element = '?'
        print(element,end="")

