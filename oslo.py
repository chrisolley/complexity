# -*- coding: utf-8 -*-
import numpy as np
import random as rdm
import matplotlib.pyplot as plt
import logbin18 as lb
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
        '''
        
        self.L = L 
        self.p = p # probability of seting a threshold value of 1
        self.z = np.zeros(L) # array to hold value of gradient at each site
        self.h = np.zeros(L) # array to hold value of height at each site
        #self.total_height = 0 # total height
        
        self.t_c_flag = False # boolean to remember if the system has reached recurrent phase
        self.count = 0 # counting number of drive phases
        self.cycle = 0 # counting number of relaxations
        
        self.zth = [self.set_thr() for i in range(L)] # set the threshold values
        
    def __iter__(self):
        '''
        Carries out the __next__ method.
        '''
        return self
    
    def __next__(self):
        '''
        Defines the iteration behaviour of the model.
        '''
        
        # Defines the condition for stopping the iteration: i.e. if number of
        # iterations reaches N, set to be 1000 iterations after cross over.
        
        if self.t_c_flag == True: 
            if self.count >= self.N: 
                raise StopIteration
        
        self.count += 1 # increment number of iterations
        self.drive() # drive phase
        self.relax() # relaxation phase
        
        return self
        
    def set_thr(self):
        '''
        set_thr: randomly initialises model's site threshold values.
        Args:
            p: probability of setting threshold value to 1. (1-p): P(2).
        Return:
            1 or 2 depending on threshold value produced.
        '''
         
        if rdm.uniform(0,1) < self.p: 
            return 1
        else: 
            return 2
    
    def drive(self):
        '''
        drive: carries out drive phase of the oslo model. 
        '''
        
        self.z[0] += 1 # increments gradient of site 1
        self.h[0] += 1 # increments height of site 1
        #self.total_height += 1
        
    def relax(self):
        '''
        relax: carries out relaxation phase of the oslo model. 
        '''
        
        # relax: boolean that determines if relaxation should occur
        relax = True # assume that relaxation should occur
        self.relaxed_sites = [] # array to store sites which relaxed in this relaxation phase
        
        # loop over all sites to check for relaxation unless relax is set to False
        while relax == True:
            
            relax = False # no relaxation has occured yet so no need to check again
            
            # loop over all sites 
            for i in range(self.L):

                # check first site
                if i == 0:  
                    if self.z[0] > self.zth[0]: # check if gradient above threshold
                        
                        self.z[0] -= 2 # increment gradients of required sites
                        self.z[1] += 1 
                        
                        self.h[0] -= 1 # increment heights of required sites
                        self.h[1] += 1

                        self.relaxed_sites.append(0) # store which site has relaxed
                        
                        self.zth[0] = self.set_thr() # assign new threshold value
                        relax = True # relaxation has occured
                        self.cycle += 1 # increment relaxation phase counter

                # check all other sites except the last site
                if i != 0 and i != self.L - 1:
                    if self.z[i] > self.zth[i]: # check if gradient above threshold

                        self.z[i] -= 2 # increment gradients of required sites
                        self.z[i - 1] += 1
                        self.z[i + 1] += 1
                        
                        self.h[i] -= 1 # increment heights of required sites
                        self.h[i + 1] += 1
                              
                        self.relaxed_sites.append(i) # store which site has relaxed
                        
                        self.zth[i] = self.set_thr() # assign new threshold value
                        relax = True # relaxation has occured
                        self.cycle += 1 # increment relaxation phase counter
                        
                # check last site                      
                if i == self.L - 1:
                    if self.z[self.L - 1] > self.zth[self.L - 1]: # check if gradient above threshold

                        self.z[self.L - 1] -= 1 # increment gradients of required sites
                        self.z[self.L - 2] += 1
                        
                        self.h[self.L - 1] -= 1 # increment heights of required sites
                              
                        self.relaxed_sites.append(i) # store which site has relaxed
                        
                        self.zth[self.L - 1] = self.set_thr() # assign new threshold values
                        relax = True # relaxation has occured
                        self.cycle += 1 # increment relaxation phase counter
                        
                        
                        if self.t_c_flag == False:
                            # if cross over hasn't already occured, store the current iteration value
                            self.t_c = self.count
                            # set the total iteration number to the cross over time + 1000 iterations
                            self.N = self.t_c + 10000
                            self.t_c_flag = True # cross over has occured                        
                            
                        
class SystemIterator(System): 
    '''
    Class to iterate a system created by the System class.
    '''
    
    def __init__(self, system, W=25): 
        '''
        Initialises the SystemIterator.
        Args: 
            system: a System object.
            W: size of temporal smoothing window.
        '''
        
        self.avalanche_sizes = [] # array to store the sizes of avalanches observed
        self.height_hist = [] # array to store the evolution o the height of the pile
        self.W = W # size of temporal smoothing window
        #self.h1_hist = []
       
        # iterates the system
        for s in system:
            print('\r Iterating system of size: {}'.format(s.L), end="")
            # populates avalanche size array
            self.avalanche_sizes.append(len(s.relaxed_sites))
            # populating height history arrays
            self.height_hist.append(s.h[0])
            #self.h1_hist.append(s.h[0]) 
        
        # define a temporally smoothed height
        self.processed_height = np.convolve(self.height_hist, 
                                            np.ones((2 * self.W + 1,)) / (2 * self.W + 1), 
                                            mode='same')
        # remove the end of the temporally smoothed height for edge effects
        self.processed_height = self.processed_height[:-2*self.W]
        # define a scaled total iteration number N/L^2
        self.N_scaled = [a / (system.L**2 ) for a in range(len(self.processed_height))]        
        # define a scaled height history h/L
        self.height_hist_scaled = [i / system.L for i in self.processed_height]
        # scale the avalanche sizes
        self.avalanche_sizes_scaled = [i / max(self.avalanche_sizes) for i in self.avalanche_sizes]
        # define the mean gradient across the system once iteration complete
        self.z_mean = sum(system.z) / len(system.z)
        # define the theoretical cross over time 
        self.t_c_theory = (self.z_mean / 2) * system.L**2 * (1 + 1. / system.L)
        # slice the avalanche time series, keeping only the recurrent phase avalanche sizes
        self.recurrent_s = self.avalanche_sizes[system.t_c:]
        # slice the heights time series, keeping only the recurrent heights
        self.recurrent_h = self.height_hist[system.t_c:]
        # mean recurrent configuration height
        self.recurrent_mean_h = sum(self.recurrent_h) / len(self.recurrent_h)
        # mean square recurrent configuration height
        self.mean_square_h = sum(i**2 for i in self.recurrent_h) / len(self.recurrent_h)
        # standard deviation of recurrent configuration height
        self.sd_h = np.sqrt(self.mean_square_h - self.recurrent_mean_h**2)
        # array of the probability distribution of different configuration heights
        # in the recurrent phase
        self.height_prob_dist = []
        self.s_prob_dist = []
        for i in range(int(min(self.recurrent_h)), int(max(self.recurrent_h))):
            self.height_prob_dist.append(self.height_prob(i))
        for i in range(int(min(self.recurrent_s)), int(max(self.recurrent_s))):
            self.s_prob_dist.append(self.avalanche_prob(i))
        
        self.s_prob_dist_log_bin = self.avalanche_prob_log_bin()
    
        
    def height_prob(self, h): 
        '''
        height_prob: Observed probability of a system height h in the recurrent phase.
        Args: 
            h: height to find probability of. 
        Return: 
            probability: P(h) in recurrent phase. 
        '''
        
        self.n = self.recurrent_h.count(h) # counts number of instances of h
        self.probability = self.n / len(self.recurrent_h) # observed probability
        
        return self.probability
    
    def avalanche_prob(self, s):
        '''
        avalanche_prob: Observed probability of a system avalanche size s in the recurrent phase.
        Args: 
            s: avalanche size to find probability of.
        Return: 
            probability: P(s) in recurrent phase.
        '''
        
        self.n = self.recurrent_s.count(s) # counts number of instances of s
        self.probability = self.n / len(self.recurrent_s) # observed probability
        
        return self.probability
    
    def avalanche_prob_log_bin(self):
        '''
        avalanche_prob_log_bin: Log binned probability distribution of the system
        avalanche sizes in the recurrent state.
        Returns: 
            x: Array of coordinates for bin centres calculated using geometric 
            mean of bin edges.
            y: Normalised array of frequency couns within each bin.
        
        '''
        self.s_log_bin = lb.logbin(self.recurrent_s, scale=1.4, zeros=True)
        
        x = self.s_log_bin[0]
        y = [i / len(self.recurrent_s) for i in self.s_log_bin[1]]
        
        return x, y
        
if __name__ == "__main__":
    
    L = 64
    
    system = System(L)
    start = timer()
    systemiterator = SystemIterator(system)
    end = timer()
    print('Run time for L={}: {} s.'.format(L, (end-start)))
    print('Number of cycles for L={}: {}.'.format(L, system.cycle))
    print("Cross-over time: {}".format(system.t_c))
    print("Max avalanche size: {}".format(max(systemiterator.avalanche_sizes)))
    print("Average slope <z>: {}".format(systemiterator.z_mean))
    print("Average height of site 1 in transient phase: {}".format(systemiterator.recurrent_mean_h))
    print("S.D of height of site 1 in transient phase: {}".format(systemiterator.sd_h))
    print("Sum of probability of heights: ")
    print(sum(systemiterator.height_prob_dist))
    
    fig2, ax2 = plt.subplots()
    ax2.plot(range(len(system.h)), system.h, marker='.')
    ax2.grid()
    
    fig3, ax3 = plt.subplots()
    ax3.plot(range(len(systemiterator.avalanche_sizes)), systemiterator.avalanche_sizes)
    ax3.axvline(system.t_c, color='red')
    ax3.grid()
    
    fig4, ax4 = plt.subplots()
    ax4.plot(range(system.N), systemiterator.height_hist)
    ax4.axvline(system.t_c, color='red')
    ax4.grid()

    fig5, ax5 = plt.subplots()
    ax5.plot(range(len(systemiterator.processed_height)), systemiterator.processed_height)
    ax5.grid()
    ax5.axvline(system.t_c, color='red')
    
    fig6, ax6 = plt.subplots()
    ax6.plot(range(int(min(systemiterator.recurrent_h)), int(max(systemiterator.recurrent_h))), systemiterator.height_prob_dist)
    ax6.grid()
    
    fig7, ax7 = plt.subplots()
    ax7.loglog(range(int(min(systemiterator.recurrent_s)), int(max(systemiterator.recurrent_s))), systemiterator.s_prob_dist)
    ax7.grid()
    
    fig8, ax8 = plt.subplots()
    ax8.loglog(systemiterator.s_prob_dist_log_bin[0], systemiterator.s_prob_dist_log_bin[1])
    ax8.grid()
    
    plt.show()