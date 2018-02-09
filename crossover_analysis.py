# -*- coding: utf-8 -*-
import oslo as oslo
import numpy as np
import matplotlib.pyplot as plt

class Crossover_Analysis:

    def __init__(self, L, N):
        
        self.L = L
        self.N = N
        self.heights = []
        self.processed_heights_list = []
        self.processed_heights_scaled = []
        self.N_scaled_list = []
        self.t_c_list = []
        self.t_c_theory_list = []
        
        for i, l in enumerate(self.L):
            system = oslo.System(l)
            system.iterate(self.N)
            ph, ns, phs = self.processed_heights(system)
            self.heights.append(system.heights)
            self.processed_heights_list.append(ph)
            self.N_scaled_list.append(ns)
            self.processed_heights_scaled.append(phs)
            if system.t_c == None:
                raise ValueError('System L: {} has not reached cross-over in {} iterations.'.format(l, self.N))
            else:
                self.t_c_list.append(system.t_c)
                self.t_c_theory_list.append(system.t_c_theory())
        
    def processed_heights(self, system):
        
        W = 25
        
        processed_heights = np.convolve(system.heights, np.ones((2 * W + 1,)) / (2 * W + 1), 
                                           mode='same')
        # remove the end of the temporally smoothed height for edge effects
        processed_heights = processed_heights[:-W]
        # define a scaled height history h/L
        processed_heights_scaled = [a / system.L for a in processed_heights]
        # define a scaled total iteration number N/L^2
        N_scaled = [a / (system.L**2) for a in range(len(processed_heights))]
        
        return processed_heights, N_scaled, processed_heights_scaled
        
    def plot_heights(self):
        
        fig1, ax1 = plt.subplots()
        ax1.grid()
        fig2, ax2 = plt.subplots()
        ax2.grid()
        fig3, ax3 = plt.subplots()
        ax3.grid()
        fig4, ax4 = plt.subplots()
        ax4.grid()
        
        for i, l in enumerate(self.L):
            
            ax1.plot(range(len(self.heights[i])), self.heights[i], label=l)
            ax1.set_xlabel('t')
            ax1.set_ylabel('h')
            ax1.legend(loc='best')
            
            ax2.plot(range(len(self.processed_heights_list[i])), self.processed_heights_list[i], label=l)
            ax2.set_xlabel('t')
            ax2.set_ylabel('h')
            ax2.legend(loc='best')
            
            ax3.plot(range(len(self.processed_heights_scaled[i])), self.processed_heights_scaled[i], label=l)
            ax3.set_xlabel('t')
            ax3.set_ylabel('h/L')
            ax3.legend(loc='best')
            
            ax4.plot(self.N_scaled_list[i], self.processed_heights_scaled[i], label=l)
            ax4.set_ylabel('h/L')
            ax4.set_xlabel('t/L^2')
            ax4.legend(loc='best')
            ax4.set_xlim(0,5)
    
    def plot_t_c(self):
        
        fig1, ax1 = plt.subplots()
        ax1.plot(self.L, self.t_c_list, label = 'Observed')
        ax1.plot(self.L, self.t_c_theory_list, label = 'Theory', color = 'red', linestyle = '--')
        ax1.set_xlabel('System Size, L')
        ax1.set_ylabel('Cross-over time, t_c')
        ax1.legend(loc='best')
        ax1.grid()