# -*- coding: utf-8 -*-
import logbin2018 as lb
import numpy as np
import matplotlib.pyplot as plt

class Avalanche_Probability_Analysis:
    
    def __init__(self, L, N, t_s, D, a, recurrent_s_data):
        
        self.recurrent_s_data = recurrent_s_data
        self.L = L
        self.N = N
        self.t_s = t_s
        self.D = D
        self.a = a
        self.moments = []
        self.moments_data = []
        for i, l in enumerate(L):
            self.moments.append(np.sum([a**2 for a in self.recurrent_s_data[i]]) / len(self.recurrent_s_data[i]))    
        

    def prob_binning(self, avalanche_data, scale, L):
        '''
        prob_binning: Carries out log binning for a set of avalanche size data.
        Args: 
            avalanche_data: array_like, contains avalanche size data.
            scale: float, log binning scale.
            L: int, system size for avalanche data.
        Returns: 
            x: array_like, log binned x values.
            y: array_like, log binned y values.
            x_scaled: array_like, data collapse scaled log binned x values.
            y_scaled: array_like, data collapse scaled log binned y values.
        '''
        # carries out log binning using provided module
        x, y = lb.logbin(avalanche_data, scale=scale, zeros=True)
        x_scaled = [] # array to hold scaled x values
        y_scaled = [] # array to hold scaled y values
        
        # carry out scaling for x values
        for i, x_i in enumerate(x):
            x_scaled.append(x_i/L**self.D)
        
        # carry out scaling for y values
        for i, y_i in enumerate(y):
            y_scaled.append(y_i * x[i]**self.t_s)
        
        return x, y, x_scaled, y_scaled
    
    def plot_log_binned_pdf(self):
    
        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        fig3, ax3 = plt.subplots()
        
        for i, l in enumerate(self.L):
            x, y, x_scaled, y_scaled = self.prob_binning(self.recurrent_s_data[i], self.a, l)
            ax1.loglog(x,y, label='L={}'.format(l))
            ax2.loglog(x, y_scaled, label='L={}'.format(l))
            ax3.loglog(x_scaled, y_scaled, label='L={}'.format(l))
        
        ax1.grid()
        ax1.legend(loc='best')
        ax2.grid()
        ax2.legend(loc='best')
        ax3.grid()
        ax3.legend(loc='best')
    
    def plot_pdf(self):
    
        val_data = []
        freq_data = []
        
        for i, l in enumerate(self.L):
            val, freq = np.unique(self.recurrent_s_data[i], return_counts=True)
            val_data.append(val)
            freq_data.append(freq)
            
        fig1, ax1 = plt.subplots()
        for i, l in enumerate(self.L):
            ax1.loglog(val_data[i], freq_data[i]/len(self.recurrent_s_data[i]), linestyle='', marker='.', label='L: {}'.format(l))
        
        ax1.legend(loc='best')
        ax1.grid()
    
    def plot_moments(self):
    
        fig1, ax1 = plt.subplots()
        ax1.loglog(self.L, self.moments, label='k: {}'.format(1))
        
        ax1.legend(loc='best')
        ax1.grid()
        
        
        