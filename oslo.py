# -*- coding: utf-8 -*-
import numpy as np 
import matplotlib.pyplot as plt
import random 

L = 100 # system size
N = 10000 # number of iterations
z = np.zeros(L)


def thr_init(p):
    '''
    Initialises threshold values by randomly choosing either 1 or 2.
    Args: 
        p: probability of choosing a 1. (1-p) = P(2).
    Return: 
        x: random choice of value.
    '''
    
    rdm = random.uniform(0,1)
    
    if rdm < p: 
        x = 1
    else: 
        x = 2
    
    return x

# initialisation of threshold values
zth = [thr_init(0.5) for i in range(L)]
    
print(zth)
print(z)

avalanche_sizes = []

for i in range(N): 
    
    # drive phase
    z[0] += 1

    # relaxation phase
    s_list = []
    for j in range(L):
        
        if j == 0:
            if z[0] > zth[0]:
                z[0] -= 2
                z[1] += 1
                s_list.append(j)
            
        elif j == L - 1:
            if z[L - 1] > zth[L - 1]: 
                z[L - 1] -= 1
                z[L - 2] += 1
                s_list.append(j) 
            
        else: 
            if z[j] > zth[j]:
                z[j] -= 2
                z[j - 1] += 1
                z[j + 1] += 1
                s_list.append(j)
    
    for a in s_list:    
        zth[a] = thr_init(0.5)
    
    print("zth: ", zth)
    print("slist: ", s_list)
    print("z: ", z)
    
    avalanche_sizes.append(len(s_list))
    
    #print(s_list)
print("Record of avalanche sizes: ", avalanche_sizes)

fig, ax = plt.subplots()
ax.hist(avalanche_sizes, bins = int(np.sqrt(len(avalanche_sizes))), edgecolor = 'black')

plt.show()