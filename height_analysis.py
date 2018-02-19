# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
#from run_oslo import Run

class Height_Analysis:
    '''
    Height_Analysis: class for carrying out analysis of the height/height probability
    distributions observed for specified system sizes of the oslo model.Loads data 
    that has already been generated using the run_oslo.py script.
    Important methods:
        plot_sd: plots the variation of system height standard deviation for
                 specified system.
        plot_scaling_correction: plots the results of analysing scaling correction
                                 to average system height, estimating omega_1, a_0.
        plot_height_probabiity: plots the system height probability distribution
                                for specified values of L and performs a data collapse.
    '''    
    
    def __init__(self, L, N, recurrent_h_data):
        
        self.L = L
        self.N = N
        
        self.log_L = [np.log(i) for i in self.L] # log L values for plotting
        
        self.recurrent_h_data = recurrent_h_data
        self.sd_h_data = []
        self.mean_h_data = []
        self.prob_dist_data = []
        
        for i, l in enumerate(L):
            self.mean_h_data.append(self.mean(self.recurrent_h_data[i]))
        
        for i, l in enumerate(self.L):
            self.sd_h_data.append(np.std(self.recurrent_h_data[i]))
    
    def mean(self, height_data):
        return sum(height_data) / len(height_data)
        
    def sd(self, L, data):
        
        # calculates the sd of the system height in system size of L and plots
        # on a log log plot against system size.
        
        log_L = [np.log(i) for i in L]
        log_sd_h = [np.log(i) for i in data]
        linregsoln = stats.linregress(log_L, log_sd_h)
        slope, intercept, r_value, p_value, std_err = linregsoln
        print("Slope: {}, Intercept: {}, R-Val: {}, S.D.: {}".format(slope, intercept, r_value, std_err))
        print('Implies: sigma ~ L^{}'.format(slope))
        return log_sd_h, slope, intercept
        
    def plot_sd(self):
        
        # carries out the plotting of the sd against system size L
        
        log_sd_h, slope, intercept = self.sd(self.L, self.sd_h_data)
        
        fig1, ax1 = plt.subplots()
        ax1.plot(self.L, self.mean_h_data, linestyle='', marker='.')
        ax1.grid()
        ax1.set_xlabel(r'$L$')
        ax1.set_ylabel(r'$\langle{h}(L)\rangle$')
        
        fig2, ax2 = plt.subplots()
        ax2.plot(self.L, self.sd_h_data, linestyle='', marker='.')
        ax2.grid()
        ax2.set_xlabel(r'$L$')
        ax2.set_ylabel(r'$\sigma_h$')
        
        fig3, ax3 = plt.subplots()
        ax3.plot(self.log_L, log_sd_h, linestyle='', marker='.')
        ax3.plot(self.log_L, [slope * i + intercept for i in self.log_L])
        ax3.grid()
        ax3.set_xlabel(r'$\log(L)$')
        ax3.set_ylabel(r'$\log(\sigma_h)$')

    def scaling_correction(self, data):
        
        # determines the parameter values for corrections to scaling by analysing
        # which parameter values produce the most linear relationship
        # returns the parameter values found
        
        # range of a_0 values to test for good fit 
        a_0 = np.linspace(1.73, 1.75, 100) 
        log_mean_h_data = [] # log_mean_h is in fact the log{(1-\langle{h}\rangle/a_0L)} quantity in the report.
        slope_data = []
        intercept_data = []
        r_value_data = []
        
        for a in a_0:
            log_mean_h = [np.log(1. - h / (a * self.L[i])) for i, h in enumerate(data)]
            linregsoln = stats.linregress(self.log_L, log_mean_h)
            # carry out a linear regression for each value of a0 to find the best value from the R value
            slope, intercept, r_value, p_value, std_err = linregsoln
            slope_data.append(slope)
            intercept_data.append(intercept)
            r_value_data.append(r_value)
            log_mean_h_data.append(log_mean_h)
        
        # as negative linear relationship, best value is found from lowest negative R value
        min_r, min_r_index = min([(r, i) for i, r in enumerate(r_value_data)])
        min_a_0 = a_0[min_r_index]
        min_slope = slope_data[min_r_index]
        min_intercept = intercept_data[min_r_index]
        min_log_mean_h_data = log_mean_h_data[min_r_index]
        omega_1 = -slope_data[min_r_index]
        
            
        return min_r, min_a_0, min_slope, min_intercept, min_log_mean_h_data, omega_1
    
    def plot_scaling_correction(self):
        
        # plots the results from the fit to corrections to scaling ansatz
        
        min_r, min_a_0, min_slope, min_intercept, min_log_mean_h_data, omega_1 = self.scaling_correction(self.mean_h_data)
        
        print('Best fitting a_0: {} with R-Val: {}'.format(min_a_0, min_r))
        print('Implies omega_1: {}'.format(omega_1))
        
        fig1, ax1 = plt.subplots()
        ax1.plot(self.log_L, min_log_mean_h_data, linestyle='', marker='.')
        ax1.plot(self.log_L, [min_slope * i + min_intercept for i in self.log_L])
        ax1.grid()
        ax1.set_xlabel(r'$log(L)$')
        ax1.set_ylabel(r'$\log{(1-\langle{h}\rangle/a_0L)}$')

    def plot_height_probability(self):
        
        # plots the steady state height probability distribution for the specified
        # system sizes L
        
        val_data = []
        freq_data = []
        # populates the probability distribution arrays
        for i, l in enumerate(self.L):
            val, freq = np.unique(self.recurrent_h_data[i], return_counts=True)
            val_data.append(val)
            freq_data.append(freq)
        
        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        # plots probability distributions and resulting data collapse
        for i, l in enumerate(self.L): 
            ax1.plot(val_data[i], freq_data[i]/len(self.recurrent_h_data[i]), 
                     label='L: {}'.format(l))
            ax2.plot((val_data[i] - self.mean_h_data[i]) / (self.sd_h_data[i]), 
                     (freq_data[i] / len(self.recurrent_h_data[i])) * self.sd_h_data[i], 
                     linestyle='', marker='.')
        
        ax1.grid()
        ax1.set_ylabel(r'$P(h;L)$')
        ax1.set_xlabel(r'$h$')
        #ax1.legend(loc='best')
        ax2.grid()
        ax2.set_ylabel(r'$\sigma_hP(h;L)$')
        ax2.set_xlabel(r'$(h-\langle{h}\rangle)/\sigma_h$')
        

class Height_Analysis_Multi:
    
    '''
    Height_Analysis_Multi: class for analysing height corrections to scaling/
    probability distributions for over multiple runs to calculate mean/sd
    values of calculated quantities (here: a_0, omega_1).
    Loads data generated from run_oslo_multi.py
    Code is fairly long but essentially just carries out the same analysis as 
    Height_Analysis class just over M runs, and then averages/takes the sd.
    '''
    
    def __init__(self, L, height_mean_multi, height_sd_multi):
        
        self.L = L
        self.log_L = [np.log(l) for l in L]
        self.h_mean_m = height_mean_multi
        self.h_sd_m = height_sd_multi
        
    def sd_fit(self, sd_data):
        
        log_sd_h = [np.log(i) for i in sd_data]
        linregsoln = stats.linregress(self.log_L, log_sd_h)
        slope, intercept, r_value, p_value, std_err = linregsoln
        return slope, intercept
        
    def plot_mean_multi(self):
        
        self.h_mean_m_mean = np.mean(self.h_mean_m, axis=0)
        self.h_mean_m_sd = np.std(self.h_mean_m, axis=0)
        linregsoln = stats.linregress(self.L, self.h_mean_m_mean)
        slope, intercept, r_value, p_value, std_err = linregsoln
        
        fig1, ax1 = plt.subplots()
        ax1.errorbar(self.L, self.h_mean_m_mean, yerr=self.h_mean_m_sd, linestyle='',
                     marker='.', ms=3, capsize=3, elinewidth=1)
        ax1.plot(self.L, [slope * i + intercept for i in self.L], linestyle='--', color='red')
        
        ax1.grid()
        ax1.set_xlabel(r'$L$')
        ax1.set_ylabel(r'$\langle{h}(L)\rangle$')
        
    def plot_sd_multi(self):
        
        self.h_sd_m_mean = np.mean(self.h_sd_m, axis=0)
        self.h_sd_m_sd = np.std(self.h_sd_m, axis=0)
        log_h_sd_m_mean = [np.log(i) for i in self.h_sd_m_mean]
        log_h_sd_m_sd = [np.log(i) for i in self.h_sd_m_sd]
        
        slope_multi = []
        intercept_multi = []
        
        for h in self.h_sd_m:
            slope, intercept = self.sd_fit(h)
            slope_multi.append(slope)
            intercept_multi.append(intercept)
        
        average_slope = np.mean(slope_multi)
        average_intercept = np.mean(intercept_multi)
        error_slope = np.std(slope_multi)
        
        print('Slope implies: sigma ~ L^{} +- {}'.format(average_slope, error_slope))
        
        fig1, ax1 = plt.subplots()
        ax1.errorbar(self.log_L, log_h_sd_m_mean, yerr=log_h_sd_m_sd, linestyle='',
                     marker='.', ms=3, capsize=3, elinewidth=1)
        ax1.plot(self.log_L, [average_slope * i + average_intercept for i in self.log_L], 
                 linestyle='--', color='red')
        
        ax1.grid()
        ax1.set_xlabel(r'$\log(L)$')
        ax1.set_ylabel(r'$\log(\langle{\sigma(L)}\rangle)$')
        
    def scaling_correction(self, data):
        
        a_0 = np.linspace(1.73, 1.75, 100)
        log_mean_h_data = []
        slope_data = []
        intercept_data = []
        r_value_data = []
        
        for a in a_0:
            log_mean_h = [np.log(1. - h / (a * self.L[i])) for i, h in enumerate(data)]
            linregsoln = stats.linregress(self.log_L, log_mean_h)
            slope, intercept, r_value, p_value, std_err = linregsoln
            slope_data.append(slope)
            intercept_data.append(intercept)
            r_value_data.append(r_value)
            log_mean_h_data.append(log_mean_h)
            
        min_r, min_r_index = min([(r, i) for i, r in enumerate(r_value_data)])
        min_a_0 = a_0[min_r_index]
        min_slope = slope_data[min_r_index]
        min_intercept = intercept_data[min_r_index]
        min_log_mean_h_data = log_mean_h_data[min_r_index]
        omega_1 = -slope_data[min_r_index]
        
            
        return min_r, min_a_0, min_slope, min_intercept, min_log_mean_h_data, omega_1
    
    def plot_scaling_correction_multi(self):
        
        a_0_multi = []
        omega_1_multi = []
        min_slope_multi = []
        min_intercept_multi = []
        min_r_multi = []
        min_log_mean_h_data_multi = []
        
        for h in self.h_mean_m:
            min_r, min_a_0, min_slope, min_intercept, min_log_mean_h_data, omega_1 = self.scaling_correction(h)
            a_0_multi.append(min_a_0)
            omega_1_multi.append(omega_1)
            min_slope_multi.append(min_slope)
            min_intercept_multi.append(min_intercept)
            min_r_multi.append(min_r)
            min_log_mean_h_data_multi.append(min_log_mean_h_data)
        
        a_0_mean = np.mean(a_0_multi)
        a_0_sd = np.std(a_0_multi)
        omega_1_mean = np.mean(omega_1_multi)
        omega_1_sd = np.std(omega_1_multi)
        slope_mean = np.mean(min_slope_multi)
        intercept_mean = np.mean(min_intercept_multi)
        r_val_mean = np.mean(min_r_multi)
        log_mean_h_data_mean = np.mean(min_log_mean_h_data_multi, axis=0)
        log_mean_h_data_std = np.std(min_log_mean_h_data_multi, axis=0)
        
        print('Average best fitting a_0: {}, s.d.: {}, with average R-Val: {}'.format(a_0_mean, a_0_sd, r_val_mean))
        print('Implies average omega_1: {}, s.d.: {}'.format(omega_1_mean, omega_1_sd))
        
        fig1, ax1 = plt.subplots()
        ax1.errorbar(self.log_L, log_mean_h_data_mean, yerr=log_mean_h_data_std, linestyle='', capsize=3, elinewidth=1)
        ax1.plot(self.log_L, [slope_mean * i + intercept_mean for i in self.log_L], linestyle='--', color='red')
        ax1.grid()
        ax1.set_xlabel(r'$\log(L)$')
        ax1.set_ylabel(r'$\log{(1-\langle{h}\rangle/a_0L)}$')