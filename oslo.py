# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer

class System:
    '''
    System class for the Oslo model system. 
    '''
    
    def __init__(self, L, p=0.5): 
        
        '''
        Initialises an Oslo Model System
        
        Args: 
            L: system size e.g. number of sites. 
            p: probability used to set threshold values. Default 0.5.
            N: number of iterations model will run for after cross over time
        '''
        
        self.L = L 
        self.p = p # probability of seting a threshold value of 1
        self.h = np.zeros(L + 1) # array to hold value of height at each site, height at L+1=0
        self.zth = np.zeros(L)
        self.avalanche_sizes = []
        self.heights = []
        self.count = 0 # counts number of iterations
        self.t_c = None
        
        self.recurrent = False # boolean to remember if the system has reached recurrent phase
    
    def drive(self):
        
        self.h[0] += 1
        
    def relax(self, n):
        
        relax = True
        s=0
        while relax == True: 
            
            relax = False
            
            for i in range(self.L):
                z = self.h[i] - self.h[i + 1] # calculate gradient at each site
                if z > self.zth[i]:
                    if i < self.L - 1:
                        self.h[i] -= 1
                        self.h[i + 1] += 1
                    else: 
                        self.h[i] -= 1
                        if self.recurrent == False: 
                            self.t_c = self.count
                            self.recurrent = True
    
                    s += 1
                    self.zth[i] = np.random.choice([1, 2], p=[self.p, 1-self.p])
                    relax = True
        self.avalanche_sizes[n] = s
            
                
    def iterate(self, N=10**4):
        
        self.N = N
        self.avalanche_sizes = np.zeros(N)
        self.heights = np.zeros(N)
        
        for i in range(self.L): 
            self.zth[i] = np.random.choice([1, 2], p=[self.p, 1-self.p])
        
        for n in range(N):
            
            self.drive()
            self.relax(n)
            self.heights[n] = self.h[0]
            self.count += 1
    
    
    def heights(self):
        return self.heights
    
    def avalanche_sizes(self):
        return self.avalanche_sizes
    
    def z_mean(self): 
        return self.h[0]/self.L
    
    def t_c_theory(self):
        return (self.z_mean() / 2) * self.L**2 * (1. + 1. / self.L)
    
    def recurrent_s(self): 
        return self.avalanche_sizes[self.t_c:]
    
    def recurrent_h(self):
        return self.heights[self.t_c:]
    
    def mean_recurrent_h(self):
        return sum(self.recurrent_h())/len(self.recurrent_h())
    
    

if __name__ == "__main__":
    
    L = 64
    
    system = System(L)
    start = timer()
    system.iterate(10**4)
    end = timer()
    print('Run time for L={}: {} s.'.format(L, (end-start)))
    print("Cross-over time: {}".format(system.t_c))
    print("Max avalanche size: {}".format(max(system.avalanche_sizes)))
    print("Average height of site 1 in transient phase: {}".format(system.mean_recurrent_h()))

    fig2, ax2 = plt.subplots()
    ax2.plot(range(system.N), system.heights)
    ax2.axvline(system.t_c, color='red')
    ax2.grid()
    
    fig3, ax3 = plt.subplots()
    ax3.plot(range(system.N), (system.avalanche_sizes)/max(system.avalanche_sizes))
    ax3.axvline(system.t_c, color='red')
    ax3.grid()
    
    plt.show()