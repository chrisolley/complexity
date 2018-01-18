# -*- coding: utf-8 -*-
import numpy as np 
import matplotlib.pyplot as plt
import random 

L = 10 # number of lattice sites
N = 50 # number of iterations
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

# initialise array to hold size of avalanches
avalanche_sizes = []

# run loop for the specified number of iterations
#TODO run until steady state reached
#TODO measure heights

for i in range(N): 
    
    # drive phase
    z[0] += 1
    print("zth: ", zth)
    print("z before relaxation: ", z)
    # relaxation phase
    # initialise array to hold value of sites that have relaxed
    relaxed_sites = []
    
    # check all sites to see if gradient above threshold
    for j in range(L):
        
        # check first site
        if j == 0:
            if z[0] > zth[0]:
                z[0] -= 2
                z[1] += 1
                relaxed_sites.append(j)
            
        # check last site
        if j == L - 1:
            if z[L - 1] > zth[L - 1]: 
                z[L - 1] -= 1
                z[L - 2] += 1
                relaxed_sites.append(j) 
            
        # check all other sites
        if j != 0 and j != L - 1: 
            if z[j] > zth[j]:
                z[j] -= 2
                z[j - 1] += 1
                z[j + 1] += 1
                relaxed_sites.append(j)
    
    # assign new threshold value for every site that relaxed this iteration
    for a in relaxed_sites:
        zth[a] = thr_init(0.5)
    
    
    #print("slist: ", relaxed_sites)
    print("z after relaxation: ", z)
    # record size of avalanche that occured on this iteration
    avalanche_sizes.append(len(relaxed_sites))
    
    #print(s_list)
    
#print("Record of avalanche sizes: ", avalanche_sizes)

fig, ax = plt.subplots()
ax.hist(avalanche_sizes, bins = int(np.sqrt(len(avalanche_sizes))), edgecolor = 'black')
        

plt.show()