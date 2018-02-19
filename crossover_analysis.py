# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
#from run_oslo import Run

class Crossover_Analysis:
    '''
    Crossover_Analysis: class for carrying out analysis of the crossover time
    and plotting basic time series of the oslo model. Loads data that has already 
    been generated using the run_oslo.py script.
    Important methods:
        plot_heights: plots the (un)processed heights as a time series for the
                      specified system sizes and performs a data collapse.
        plot_crossover: plots the crossover time for the specified system sizes
                        alongside the theoretical crossover time.
    '''

    def __init__(self, L, N, h_data, t_c_data, t_c_th_data):
        
        self.L = L # array-like, system sizes to investigate
        self.N = N # number of iterations to run for
        self.h_data = h_data 
        self.N_scaled_list = []
        self.t_c_data = t_c_data
        self.t_c_th_data = t_c_th_data
        self.processed_heights_list = []
        self.processed_heights_scaled = []
        
        for i, l in enumerate(self.L):
            # unscaled processed heights and scaled processed heights for data collapse
            ph, ns, phs = self.processed_heights(self.h_data[i], l)
            self.processed_heights_list.append(ph)
            self.N_scaled_list.append(ns)
            self.processed_heights_scaled.append(phs)
        
    def processed_heights(self, data, L):
        
        W = 25
        # carry out time averaging of system heights using a convolution 
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
        fig5, ax5 = plt.subplots()
        ax5.grid()
        
        for i, l in enumerate(self.L):
            
            # plot unprocessed system height time series 
            ax1.plot(range(len(self.h_data[i])), self.h_data[i], label=l)
            ax1.set_xlabel(r'$t$')
            ax1.set_ylabel(r'$h(t;L)$')
            #ax1.legend(loc='best')
            
            # plot processed system height time series
            ax2.plot(range(len(self.processed_heights_list[i])), self.processed_heights_list[i], label=l)
            ax2.set_xlabel(r'$t$')
            ax2.set_ylabel(r'$\tilde{h}(t;L)$')
            #ax2.legend(loc='best')
            
            # plot processed, x axis scaled system height time series
            ax3.plot(range(len(self.processed_heights_scaled[i])), self.processed_heights_scaled[i], label=l)
            ax3.set_xlabel(r'$t$')
            ax3.set_ylabel(r'$\tilde{h}(t;L)/L$')
            #ax3.legend(loc='best')
            
            # plot data collapse of system height time series
            ax4.plot(self.N_scaled_list[i], self.processed_heights_scaled[i], label=l)
            ax4.set_ylabel(r'$\tilde{h}(t;L)/L$')
            ax4.set_xlabel(r'$t/L^2$')
            #ax4.legend(loc='best')
            ax4.set_xlim(0,5)
            
            # log-log plot of data collapse showing transient phase follows a x^0.5 trend
            ax5.plot(self.N_scaled_list[i], self.processed_heights_scaled[i], label=l)
            ax5.set_ylabel(r'$\tilde{h}(t;L)/L$')
            ax5.set_xlabel(r'$t/L^2$')
            #ax4.legend(loc='best')
            #ax5.set_xlim(0,5)
            x = np.linspace(0.01,1,1000)
            ax5.plot(x, x**(0.5))
            ax5.set_yscale('log')
            ax5.set_xscale('log')
        
            
    def plot_t_c(self):
        
        # plot observed and theoretical cross over time for specified system sizes
        fig1, ax1 = plt.subplots()
        ax1.plot(self.L, self.t_c_data, label = 'Observed')
        ax1.plot(self.L, self.t_c_th_data, label = 'Theory', color = 'red', linestyle = '--')
        ax1.set_xlabel(r'$L$')
        ax1.set_ylabel(r'$t_c$')
        ax1.legend(loc='best')
        ax1.grid()
        
class Crossover_Analysis_Multi:
    '''
    Crossover_Analysis_Multi: class for analysing cross over time dependence on
    system size for multiple runs to calculate sd/mean values of calculated quantities.
    Loads data generated from run_oslo_multi.py
    '''

    
    def __init__(self, L, t_c_multi, t_c_th_multi):
        
        self.L = L
        self.t_c_multi = t_c_multi
        self.t_c_th_multi = t_c_th_multi
    
    def plot_t_c_multi(self):
        
        # calculates the mean (theoretical/obs) crossover time and the sd on crossover time for
        # different system sizes averaged over multiple runs
        self.t_c_m_mean = np.mean(self.t_c_multi, axis=0)
        self.t_c_m_sd = np.std(self.t_c_multi, axis=0)
        
        self.t_c_th_m_mean = np.mean(self.t_c_th_multi, axis=0)
        self.t_c_th_m_sd = np.std(self.t_c_th_multi, axis=0)
        # plots mean obs and th. crossover times for specified system sizes with sd 
        fig1, ax1 = plt.subplots()
        ax1.errorbar(self.L, self.t_c_m_mean, yerr=self.t_c_m_sd, linestyle='',
                     marker='.', ms=3, capsize=3, elinewidth=1, label='Observed')
        ax1.errorbar(self.L, self.t_c_th_m_mean, yerr=self.t_c_th_m_sd, linestyle='--',
                     color='red', marker='.', ms=3, capsize=3, elinewidth=1, label='Theory')      
        ax1.grid()
        ax1.set_xlabel(r'$L$')
        ax1.set_ylabel(r'$\langle t_c\rangle^{th/obs}$')
        ax1.legend(loc='best')
        