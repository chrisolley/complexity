# -*- coding: utf-8 -*-
import numpy as np
import random as rdm
import matplotlib.pyplot as plt
from timeit import default_timer as timer

class System:
    '''
    System class for given Oslo model lattice.
    '''
    
    def __init__(self, L, p=0.5): 
        self.L = L           
        self.p = p
        self.zth = [self.set_thr() for i in range(L)]
        self.z = np.zeros(L)
        self.h = np.zeros(L)
        self.total_height = 0
        self.t_c_flag = False
        self.count = 0 # counting number of iterations
        self.cycle = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        
        if self.t_c_flag == True:
            if self.count >= self.N:
                raise StopIteration
        
        self.count += 1
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
        
        print("Adding a grain")
        self.z[0] += 1
        self.h[0] += 1
        self.total_height += 1
        
    def relax(self):
        
        relax = True # carry out initial check for relaxation
        self.relaxed_sites = []
        while relax == True:
            
            relax = False # assume no relaxation has occured 
            
            for i in range(self.L):

                if i == 0:  
                    # check first site
                    print("Checking site: {}".format(i))
                    if self.z[0] > self.zth[0]: # is gradient above threshold?
                        print("Relaxed")
                        self.z[0] -= 2
                        self.z[1] += 1
                        
                        self.h[0] -= 1
                        self.h[1] += 1
                        self.relaxed_sites.append(0) # store which sites have relaxed
                        self.zth[0] = self.set_thr() # assign new threshold value
                        self.total_height -= 1
                        relax = True # relaxation has occured
                        self.cycle += 1
                    
                
                    # only check rest of sites if 1st site has relaxed    

                #relax = False # assume no relaxation has occured 


                # check all other sites
                if i != 0 and i != self.L - 1:
                    print("Checking site: {}".format(i))
                    if self.z[i] > self.zth[i]: # is gradient above threshold?
                        print("Relaxed")
                        self.z[i] -= 2
                        self.z  [i - 1] += 1
                        self.z[i + 1] += 1
                        
                        self.h[i] -= 1
                        self.h[i + 1] += 1
                        self.relaxed_sites.append(i) # store which sites have relaxed
                        self.zth[i] = self.set_thr() # assign new threshold value
                        relax = True # relaxation has occured
                        self.cycle += 1
                        
                # check last site                      
                if i == self.L - 1:
                    print("Checking site: {}".format(i))
                    if self.z[self.L - 1] > self.zth[self.L - 1]: # is gradient above threshold?
                        print("Relaxed")
                        self.z[self.L - 1] -= 1
                        self.z[self.L - 2] += 1
                        
                        self.h[self.L - 1] -= 1
                        self.relaxed_sites.append(i) # store which sites have relaxed
                        self.zth[self.L - 1] = self.set_thr() # assign new threshold value
                        relax = True # relaxation has occured
                        self.cycle += 1
                        
                        if self.t_c_flag == False:
                            self.t_c = self.count
                            self.N = self.t_c + 1000
                            
                            self.t_c_flag = True # cross over has occured                        
                        # total height of pile only decreases if last site relaxes
                        #total_height -= 1 
                        
#                    else: 
#                        continue
                        
class SystemIterator(System): 
    ''' Defines iteration behaviour for a system '''
    
    def __init__(self, system, W=25): 
        self.avalanche_sizes = []
        self.total_height_hist = []
        self.W = W
        self.h1_hist = []
       
        
        for s in system:
            self.avalanche_sizes.append(len(s.relaxed_sites))
            self.total_height_hist.append(s.total_height)
            self.h1_hist.append(s.h[0]) 
        
        self.N_scaled = [a / (1.2 * system.L**2 ) for a in range(system.N)]        
        self.processed_height = np.convolve(self.total_height_hist, 
                                            np.ones((2 * self.W + 1,)) / (2 * self.W + 1)   , 
                                            mode='same')
        
        self.processed_height = self.processed_height[:-2*self.W]
        self.z_mean = sum(system.z) / len(system.z)

        self.total_height_hist_scaled = [i / system.L for i in self.total_height_hist]
        self.avalanche_sizes_scaled = [i / max(self.avalanche_sizes) for i in self.avalanche_sizes]
        self.t_c_theory = (self.z_mean / 2) * system.L**2 * (1 + 1. / system.L)
        self.transient_h1 = self.h1_hist[system.t_c:]
        self.transient_mean_h1 = sum(self.transient_h1) / len(self.transient_h1)
        self.mean_square_h1 = sum(i**2 for i in self.transient_h1) / len(self.transient_h1)
        self.sd_h1 = np.sqrt(self.mean_square_h1 - self.transient_mean_h1**2)
        self.prob_dist = []
        
        
    def prob(self, h): 
        '''Observed probability of a system height h'''
        
        self.n = self.transient_h1.count(h)
        self.probability = self.n/len(self.transient_h1)
        return self.probability
        
if __name__ == "__main__":
    
    L = 8
    
    
    system = System(L)
    start = timer()
    systemiterator = SystemIterator(system)
    end = timer()
    print('Run time for L={}: {} s.'.format(L, (end-start)))
    print('Number of cycles for L={}: {}.'.format(L, system.cycle))
    print("Cross-over time: {}".format(system.t_c))
    print("Average slope <z>: {}".format(systemiterator.z_mean))
    print("Average height of site 1 in transient phase: {}".format(systemiterator.transient_mean_h1))
    print("S.D of height of site 1 in transient phase: {}".format(systemiterator.sd_h1))
    print("Probability of heights 1-32: ")  
    probdist = []
    for i in range(70): 
        probdist.append(systemiterator.prob(i))
    
    print(sum(probdist))
    
    fig2, ax2 = plt.subplots()
    ax2.plot(range(len(system.h)), system.h, marker='.')
    
    ax2.grid()
    
    fig3, ax3 = plt.subplots()
    ax3.plot(range(len(systemiterator.avalanche_sizes)), systemiterator.avalanche_sizes)
    ax3.axvline(system.t_c, color='red')
    ax3.grid()
    
    fig4, ax4 = plt.subplots()
    ax4.plot(range(system.N), systemiterator.total_height_hist)
    ax4.axvline(system.t_c, color='red')
    ax4.grid()

    fig5, ax5 = plt.subplots()
    ax5.plot(range(len(systemiterator.processed_height)), systemiterator.processed_height)
    ax5.grid()
    ax5.axvline(system.t_c, color='red')
    plt.show()