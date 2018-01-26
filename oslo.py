# -*- coding: utf-8 -*-
import numpy as np
import random as rdm
import matplotlib.pyplot as plt


class System:
    '''
    System class for given Oslo model lattice.
    '''
    
    def __init__(self, L, N, p=0.5): 
        self.L = L
        self.N = N
        self.p = p
        self.zth = [self.set_thr() for i in range(L)]
        self.z = np.zeros(L)
        self.h = np.zeros(L)
        self.total_height = 0
        self.t_c_flag = False
        self.count = 0 # counting number of iterations
        
    def __iter__(self):
        return self
    
    def __next__(self):
        
        if self.count >= self.N:
            raise StopIteration
        
        self.count +=1
        self.drive()
        self.relax()
        
        return self
        
    def set_thr(self):
        '''Initialises threshold values'''
         
        if rdm.uniform(0,1) < self.p: 
            return 1
        else: 
            return 2
    
    def drive(self):
        
        self.z[0] += 1
        self.h[0] += 1
        self.total_height += 1
        
    def relax(self):
        
        relax = True # carry out initial check for relaxation
        self.relaxed_sites = []
        
        while relax == True:
            
            for i in range(self.L):
                
                relax = False # assume no relaxation has occured 
                
                # check first site
                if i == 0:
                    if self.z[0] > self.zth[0]: # is gradient above threshold?
                        self.z[0] -= 2
                        self.z[1] += 1
                        
                        self.h[0] -= 1
                        self.h[1] += 1
                        self.relaxed_sites.append(i) # store which sites have relaxed
                        self.zth[0] = self.set_thr() # assign new threshold value
                        self.total_height -= 1
                        relax = True # relaxation has occured
                        
                    # only check rest of sites if 1st site has relaxed    
                    else: 
                        continue 
                        
                # check last site
                if i == self.L - 1:
                    if self.z[self.L - 1] > self.zth[self.L - 1]: # is gradient above threshold?
                        self.z[self.L - 1] -= 1
                        self.z[self.L - 2] += 1
                        
                        self.h[self.L - 1] -= 1
                        self.relaxed_sites.append(i) # store which sites have relaxed
                        self.zth[self.L - 1] = self.set_thr() # assign new threshold value
                        relax = True # relaxation has occured
                        if self.t_c_flag == False:
                            self.t_c = self.count
                            
                            self.t_c_flag = True # cross over has occured                        
                        # total height of pile only decreases if last site relaxes
                        #total_height -= 1 
    
                        
                # check all other sites
                if i != 0 and i != self.L - 1: 
                    if self.z[i] > self.zth[i]: # is gradient above threshold?
                        self.z[i] -= 2
                        self.z[i - 1] += 1
                        self.z[i + 1] += 1
                        
                        self.h[i] -= 1
                        self.h[i + 1] += 1
                        self.relaxed_sites.append(i) # store which sites have relaxed
                        self.zth[i] = self.set_thr() # assign new threshold value
                        relax = True # relaxation has occured
                        
class SystemIterator(System): 
    ''' Defines iteration behaviour for a system '''
    
    def __init__(self, system, W=25): 
        self.avalanche_sizes = []
        self.total_height_hist = []
        self.W = W
        self.h1_hist = []
        self.N_scaled = [a / system.L**2 for a in range(system.N)]        
        
        for s in system:
            self.avalanche_sizes.append(len(s.relaxed_sites))
            self.total_height_hist.append(s.total_height)
            self.h1_hist = [s.h[0]] 
        
        self.processed_height = np.convolve(self.total_height_hist, 
                                            np.ones((2 * self.W + 1,)) / (2 * self.W + 1), 
                                            mode='valid')
        
        self.z_mean = sum(system.z) / len(system.z)
        self.h1_mean = sum(self.h1_hist) / len(self.h1_hist)
        self.total_height_hist_scaled = [i / system.L for i in self.total_height_hist]
        self.avalanche_sizes_scaled = [i / max(self.avalanche_sizes) for i in self.avalanche_sizes]
        self.t_c_theory = (self.z_mean / 2) * system.L**2 * (1 + 1. / system.L)
        
if __name__ == "__main__":
    
    N = 6000
    L = 64
    
    system = System(L, N)
    systemiterator = SystemIterator(system)
    
    print("Average height of site 1: {}".format(systemiterator.h1_mean))
    print("Cross-over time: {}".format(system.t_c))
    print("Average slope <z>: {}".format(systemiterator.z_mean))

    fig2, ax2 = plt.subplots()
    ax2.plot(range(len(system.h)), system.h, marker='.')
    
    ax2.grid()
    
    fig3, ax3 = plt.subplots()
    ax3.plot(range(len(systemiterator.avalanche_sizes)), systemiterator.avalanche_sizes)
    ax3.axvline(system.t_c, color='red')
    ax3.grid()
    
    fig4, ax4 = plt.subplots()
    ax4.plot(range(N), systemiterator.total_height_hist)
    ax4.axvline(system.t_c, color='red')
    ax4.grid()

    fig5, ax5 = plt.subplots()
    ax5.plot(range(len(systemiterator.processed_height)), systemiterator.processed_height)
    ax5.grid()
    ax5.axvline(system.t_c, color='red')
    plt.show()