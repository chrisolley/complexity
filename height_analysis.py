# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class Height_Analysis:
    
    def __init__(self, L, N, recurrent_h_data):
        
        self.L = L
        self.N = N
        
        self.log_L = [np.log(i) for i in self.L]
        
        self.recurrent_h_data = recurrent_h_data
        self.sd_h_data = []
        self.mean_h_data = []
        self.prob_dist_data = []
        
        for i, l in enumerate(L):
            self.mean_h_data.append(self.mean(self.recurrent_h_data[i]))
    
    def mean(self, height_data):
        return sum(height_data) / len(height_data)
        
    
    def plot_sd(self):
        
        sd_h_data = []
    
        for i, l in enumerate(self.L):
            sd_h_data.append(np.std(self.recurrent_h_data[i]))
    
        log_sd_h = [np.log(i) for i in sd_h_data]
        linregsoln = stats.linregress(self.log_L, log_sd_h)
        slope, intercept, r_value, p_value, std_err = linregsoln
        print("Slope: {}, Intercept: {}, R-Val: {}, S.D.: {}".format(slope, intercept, r_value, std_err))
        print('Implies: sigma ~ L^{}'.format(slope))
        
        fig1, ax1 = plt.subplots()
        ax1.plot(self.L, self.mean_h_data, linestyle='', marker='.')
        ax1.grid()
        ax1.set_xlabel('System Size, L')
        ax1.set_ylabel('Average Height')
        
        fig2, ax2 = plt.subplots()
        ax2.plot(self.L, sd_h_data, linestyle = '', marker='.')
        ax2.grid()
        ax2.set_xlabel('System Size, L')
        ax2.set_ylabel('Standard Deviation of Height')
        
        fig3, ax3 = plt.subplots()
        ax3.plot(self.log_L, log_sd_h, linestyle='', marker='.')
        ax3.plot(self.log_L, [slope * i + intercept for i in self.log_L])
        ax3.grid()
        ax3.set_xlabel('log(L)')
        ax3.set_ylabel('log(s.d.)')
    
    def plot_scaling_correction(self):
        
        a_0 = np.linspace(1.73, 1.75, 100)
        log_mean_h_data = []
        slope_data = []
        intercept_data = []
        r_value_data = []
        
        for a in a_0:
            log_mean_h = [np.log(1. - h / (a * self.L[i])) for i, h in enumerate(self.mean_h_data)]
            linregsoln = stats.linregress(self.log_L, log_mean_h)
            slope, intercept, r_value, p_value, std_err = linregsoln
            slope_data.append(slope)
            intercept_data.append(intercept)
            r_value_data.append(r_value)
            log_mean_h_data.append(log_mean_h)
            
        min_r, min_r_index = min([(r, i) for i, r in enumerate(r_value_data)])
        min_a_0 = a_0[min_r_index]
        print('Best fitting a_0: {} with R-Val: {}'.format(min_a_0, min(r_value_data)))
        print('Implies omega_1: {}'.format(-slope_data[min_r_index]))
        
    
        
        fig1, ax1 = plt.subplots()
        ax1.plot(self.log_L, log_mean_h_data[min_r_index], linestyle='', marker='.')
        ax1.plot(self.log_L, [slope_data[min_r_index] * i + intercept_data[min_r_index] for i in self.log_L])
        ax1.grid()
        ax1.set_xlabel('log(L)')
        ax1.set_ylabel('log(1-<h>/(a0L))')
    
    def plot_height_probability(self):
        
        val_data = []
        freq_data = []
            
        for i, l in enumerate(self.L):
            val, freq = np.unique(self.recurrent_h_data[i], return_counts=True)
            val_data.append(val)
            freq_data.append(freq)
        
        fig1, ax1 = plt.subplots()
        for i, l in enumerate(self.L): 
            ax1.plot(val_data[i], freq_data[i]/len(self.recurrent_h_data[i]), label='L: {}'.format(l))
        
        ax1.grid()
        ax1.legend(loc='best')


