# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from timeit import default_timer as timer

class System:
    '''
    System class for the Oslo model system. 
    Important methods: 
        drive: drives the model one iteration
        relax: carries out one relaxation
        iterate: iterates the model through required number of iterations
    '''
    
    def __init__(self, L, p=0.5, animate=False): 
        
        '''
        Initialises an Oslo Model System
        
        Args: 
            L: system size e.g. number of sites. 
            p: probability of a threshold gradient of 1, used to set threshold values. 
            animate: runs animation or not.
        '''
            
        self.L = L 
        self.p = p # probability of seting a threshold value of 1
        self.animate = animate 
        self.h = np.zeros(L + 1) # array to hold value of height at each site, height at L+1=0
        self.zth = np.zeros(L)
        self.count = 0 # counts number of iterations
        self.t_c = None # crossover time not yet reached
        
        self.recurrent = False # boolean to remember if the system has reached recurrent phase
    
    def drive(self):
        # drive method
        self.h[0] += 1
        
    def relax(self, n):
        # relaxation method
        relax = True # assume relaxation is necessary
        s=0 # reset avalanche size
        while relax == True: 
            
            relax = False # no sites have yet relaxed
            
            for i in range(self.L): # cycle over each site in the systme
                z = self.h[i] - self.h[i + 1] # calculate gradient at each site
                if z > self.zth[i]: # compare to threshold gradient
                    if i < self.L - 1: # check non-final sites
                        self.h[i] -= 1
                        self.h[i + 1] += 1
                    else: # check final site
                        self.h[i] -= 1
                        if self.recurrent == False: # check if recurrent phase already reached    
                            self.t_c = self.count # if not, calculate t_c value
                            self.recurrent = True # recurrent phase has been reached
    
                    s += 1 # increment avalanche size
                    # reset threshold value for relaxed sites
                    self.zth[i] = np.random.choice([1, 2], p=[self.p, 1-self.p]) 
                    # relaxation has occured
                    relax = True
        self.avalanche_sizes[n] = s # store avalanche size
            
                
    def iterate(self, N=10**4):
        # iteration method, should be called with required number of iterations
        self.N = N
        # numpy arrays to hold avalanche sizes and heights
        self.avalanche_sizes = np.zeros(N)
        self.heights = np.zeros(N)
        # sets initial threshold gradients
        for i in range(self.L): 
            self.zth[i] = np.random.choice([1, 2], p=[self.p, 1-self.p])
        
        if self.animate == True:
            fig, ax = plt.subplots()
        
        # iterates over required number of iterations
        for n in range(N):
            
            self.drive() # relaxation phase
            self.relax(n) # drive phase
            self.heights[n] = self.h[0] # stores height value history
            self.count += 1 # increments iteration number
            if self.animate == True: # animation loop if required
                ax.clear()
                #ax.bar(range(self.L),self.h[:-1], width = 1.0)
                ax.plot(range(self.L),self.h[:-1], marker='o', markerfacecolor='red')
                #fig.canvas.draw()
                plt.pause(0.01)
    
    
    def heights(self):
        return self.heights
    
    def avalanche_sizes(self):
        return self.avalanche_sizes
    
    def z_mean(self): 
        # calculates average gradient of pile
        return self.h[0]/self.L
    
    def t_c_theory(self):
        # calculates theoretical crossover time
        return (self.z_mean() / 2) * self.L**2 * (1. + 1. / self.L)
    
    def recurrent_s(self): 
        # cuts off avalanche sizes at t_c for recurrent avalanche sizes
        return self.avalanche_sizes[self.t_c:]
    
    def recurrent_h(self):
        # cuts of height history at t_c for recurrent heights
        return self.heights[self.t_c:]
    
    def mean_recurrent_h(self):
        # calculates mean recurrent height 
        return sum(self.recurrent_h())/len(self.recurrent_h())
    
    

if __name__ == "__main__":
    
    # script to test the python code is working 
    
    L = 64
    
    system = System(L, animate=False) # set animate to true to see oslo model in action!
    start = timer()
    system.iterate(10**4)
    end = timer()
    print('Run time for L={}: {} s.'.format(L, (end-start)))
    print("Cross-over time: {}".format(system.t_c))
    print("Max avalanche size: {}".format(max(system.avalanche_sizes)))
    print("Average height of site 1 in transient phase: {}".format(system.mean_recurrent_h()))

    # plot of system heights as a function of time
    fig2, ax2 = plt.subplots()
    ax2.plot(range(system.N), system.heights)
    ax2.axvline(system.t_c, color='red')
    ax2.grid()
    
    # plot of normalised avalanche sizes as a function of time
    fig3, ax3 = plt.subplots()
    ax3.plot(range(system.N), (system.avalanche_sizes)/max(system.avalanche_sizes))
    ax3.axvline(system.t_c, color='red')
    ax3.grid()
    
    plt.show()