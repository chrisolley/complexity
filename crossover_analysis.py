# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

class Crossover_Analysis:

    def __init__(self, L, N, h_data, t_c_data, t_c_th_data):
        
        self.L = L
        self.N = N
        self.h_data = h_data
        self.N_scaled_list = []
        self.t_c_data = t_c_data
        self.t_c_th_data = t_c_th_data
        self.processed_heights_list = []
        self.processed_heights_scaled = []
        
        for i, l in enumerate(self.L):
            ph, ns, phs = self.processed_heights(self.h_data[i], l)
            self.processed_heights_list.append(ph)
            self.N_scaled_list.append(ns)
            self.processed_heights_scaled.append(phs)
        
    def processed_heights(self, data, L):
        
        W = 25
        
        processed_heights = np.convolve(data, np.ones((2 * W + 1,)) / (2 * W + 1), 
                                           mode='same')
        # remove the end of the temporally smoothed height for edge effects
        processed_heights = processed_heights[:-W]
        # define a scaled height history h/L
        processed_heights_scaled = [a / L for a in processed_heights]
        # define a scaled total iteration number N/L^2
        N_scaled = [a / (L**2) for a in range(len(processed_heights))]
        
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
            
            ax1.plot(range(len(self.h_data[i])), self.h_data[i], label=l)
            ax1.set_xlabel(r'$t$')
            ax1.set_ylabel(r'$h(t;L)$')
            #ax1.legend(loc='best')
            
            ax2.plot(range(len(self.processed_heights_list[i])), self.processed_heights_list[i], label=l)
            ax2.set_xlabel(r'$t$')
            ax2.set_ylabel(r'$\tilde{h}(t;L)$')
            #ax2.legend(loc='best')
            
            ax3.plot(range(len(self.processed_heights_scaled[i])), self.processed_heights_scaled[i], label=l)
            ax3.set_xlabel(r'$t$')
            ax3.set_ylabel(r'$\tilde{h}(t;L)/L$')
            #ax3.legend(loc='best')
            
            ax4.plot(self.N_scaled_list[i], self.processed_heights_scaled[i], label=l)
            ax4.set_ylabel(r'$\tilde{h}(t;L)/L$')
            ax4.set_xlabel(r'$t/L^2$')
            #ax4.legend(loc='best')
            ax4.set_xlim(0,5)
    
    def plot_t_c(self):
        
        fig1, ax1 = plt.subplots()
        ax1.plot(self.L, self.t_c_data, label = 'Observed')
        ax1.plot(self.L, self.t_c_th_data, label = 'Theory', color = 'red', linestyle = '--')
        ax1.set_xlabel(r'$L$')
        ax1.set_ylabel(r'$t_c$')
        ax1.legend(loc='best')
        ax1.grid()