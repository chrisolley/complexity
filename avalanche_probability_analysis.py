# -*- coding: utf-8 -*-
import logbin2018 as lb
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class Avalanche_Probability_Analysis:
    
    '''
    Avalanche_Probability_Analysis: class for carrying out analysis of the 
    avalanche size probability distributions for specified system sizes. Loads data 
    that has already been generated using the run_oslo.py script.
    Important methods:
        plot_log_binned_pdf: plots the log binned avalanche size pdfs for specified
                             system sizes and performs a data collapse using
                             specified critical exponents.
        plot_pdf: plots the unbinned avalanche size pdfs.
        plot_moments: plots the moments for specified system sizes and carries out
                      moment analysis to estimate critical exponents.
    '''
    
    def __init__(self, L, N, t_s, D, a, recurrent_s_data):
        
        self.recurrent_s_data = recurrent_s_data
        self.L = L
        self.N = N
        self.t_s = t_s
        self.D = D
        self.a = a
                                 
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
        
        # plot the log binned avalanche size probability distribution, scaled
        # and unscaled.
        for i, l in enumerate(self.L):
            x, y, x_scaled, y_scaled = self.prob_binning(self.recurrent_s_data[i], self.a, l)
            ax1.loglog(x,y, label='L={}'.format(l))
            ax2.loglog(x, y_scaled, label='L={}'.format(l))
            ax3.loglog(x_scaled, y_scaled, label='L={}'.format(l))
        
        ax1.grid()
        ax1.set_xlabel(r'$s$')
        ax1.set_ylabel(r'$P(s;L)$')
        #ax1.legend(loc='best')
        
        ax2.grid()
        ax2.set_xlabel(r'$s$')
        ax2.set_ylabel(r'$s^{\tau_s}P(s;L)$')
        #ax2.legend(loc='best')
        
        ax3.grid()
        ax3.set_xlabel(r'$s/L^D$')
        ax3.set_ylabel(r'$s^{\tau_s}P(s;L)$')
        #ax3.legend(loc='best')
    
    def moment(self, data, k):
        # calculate the kth moment of a set of data, for each value of L required
        
        moment_data = []
        for i, l in enumerate(self.L):
            power = np.power(np.float64(data[i]), k)
            moment = np.sum(power)/len(data[i])
            moment_data.append(moment)
        return moment_data
    
    def moment_theoretical(self, k):
        moment_th_data = []
        for i, l in enumerate(self.L):
            moment_th = l**(self.D * (1.0 + k - self.t_s))
            moment_th_data.append(moment_th)
        return moment_th_data
    
    def plot_pdf(self):
        
        # plot the unbinned pdfs for avalanche size distribution
    
        val_data = []
        freq_data = []
        
        for i, l in enumerate(self.L):
            val, freq = np.unique(self.recurrent_s_data[i], return_counts=True)
            val_data.append(val)
            freq_data.append(freq)
            
        fig1, ax1 = plt.subplots()
        for i, l in enumerate(self.L):
            ax1.loglog(val_data[i], freq_data[i]/len(self.recurrent_s_data[i]), linestyle='', marker='.', label='L: {}'.format(l))
        
        ax1.set_xlabel(r'$s$')
        ax1.set_ylabel(r'$P(s;L)$')
        #ax1.legend(loc='best')
        ax1.grid()
    
    def plot_moments(self):
        
        # plot the moments of different system sizes and carries out moment analysis
        # to estimate critical exponents
        
        fig1, ax1 = plt.subplots()
        k_range = range(1, 5)
        log_L = [np.log(l) for l in self.L]
        log_moments = []
        exponent_values = []
        
        for i in k_range:
            moment = self.moment(self.recurrent_s_data, i)
            log_moments.append(np.log(moment))
            # calculate line of best fit using only the three largest system sizes
            linregsoln = stats.linregress(log_L[-3:], np.log(moment)[-3:])
            m = linregsoln[0]
            c = linregsoln[1]
            exponent_values.append(m)
            ax1.plot(log_L, np.log(moment), label='k: {}'.format(i), marker='o', linestyle='')
            ax1.plot(log_L, [m*l + c for l in log_L])
            
        ax1.set_xlabel(r'$\log(L)$')
        ax1.set_ylabel(r'$\log(\langle{s^k}\rangle)$')
        #ax1.legend(loc='best')
        ax1.grid()
   
        fig2, ax2 = plt.subplots()
        ax2.plot(k_range, exponent_values,  marker='o')
        ax2.set_ylabel(r'$D(1+k-\tau_s)$')
        ax2.set_xlabel(r'$k$')
        ax2.grid()
        
        # calculate line of best fit between calculated kth moment gradients and 
        # value of k, in order to estimate critical exponents t_s and D
        linregsoln = stats.linregress(k_range, exponent_values)
        m = linregsoln[0]
        c = linregsoln[1]
        print("Slope: {}, Intercept: {}".format(m, c))
        print("Implies: D={}, t_s={}".format(m, 1 - c/m))        
    
class Avalanche_Probability_Analysis_Multi:
    
    '''
    Avalanche_Probability_Analysis_Multi: class for analysing avalanche size 
    probability distributions for over multiple runs to calculate mean/sd
    values of calculated quantities (here: critical exponents).
    Loads data generated from run_oslo_multi.py
    '''
    
    def __init__(self, L, s_data_multi):
        
        self.L = L
        self.s_data_multi = s_data_multi
        
    def moment(self, data, k):
        # calculates kth moment of a set of data
        moment_data = []
        for i, l in enumerate(self.L):
            power = np.power(np.float64(data[i]), k)
            moment = np.sum(power)/len(data[i])
            moment_data.append(moment)
        return moment_data
    
    def exponents(self, data):
        
        # calculates the critical exponents from a set of data
        
        k_range = range(1, 5)
        log_L = [np.log(l) for l in self.L]
        log_moments = []
        exponent_values = []
        
        for i in k_range:
            moment = self.moment(data, i)
            log_moments.append(np.log(moment))
            linregsoln = stats.linregress(log_L[-3:], np.log(moment)[-3:])
            exponent_values.append(linregsoln[0])
        
        linregsoln = stats.linregress(k_range, exponent_values)
        m = linregsoln[0]
        c = linregsoln[1]
        
        D = m
        t_s = 1 - c/m
        
        return D, t_s
        
    def exponents_multi(self):
        
        # calculates the critical exponents for each of the M runs carried out
        # and averages/finds the sd on these values
        
        D_multi = []
        t_s_multi = []
        
        for s in self.s_data_multi:
            D, t_s = self.exponents(s)
            D_multi.append(D)
            t_s_multi.append(t_s)
        
        D_multi_mean = np.mean(D_multi)
        D_multi_sd = np.std(D_multi)
        t_s_multi_mean = np.mean(t_s_multi)
        t_s_multi_sd = np.std(t_s_multi)
        
        print("Moment Analysis averaged over {} runs:".format(len(self.s_data_multi)) )
        print("D={} +- {}, ".format(D_multi_mean, D_multi_sd)) 
        print("t_s={} +- {}".format(t_s_multi_mean, t_s_multi_sd))  
        
        
        
    