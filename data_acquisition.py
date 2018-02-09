# -*- coding: utf-8 -*-
import oslo as oslo
from timeit import default_timer as timer
import numpy as np

def acquire_avalanche_data(L, N):
    
    '''
    acquire_avalanche_data: acquires and saves avalanche size time series
    for recurrent phase.
    produces file of form: 'avalanche_sizes_L_N.csv'.
    Args: 
        L: system size.
        N: number of avalanches/number of iterations model runs for after cross over.
    '''
    
    # array of system objects for different sizes
    start = timer()
    for i, l in enumerate(L):
        start1 = timer()
        system = oslo.System(l)
        system.iterate(N)
        end1 = timer()
        print('Run time for L={}: {} s.'.format(l, (end1-start1)))
        np.save('data/avalanche_data/avalanche_sizes_{}_{}'.format(l, N), system.recurrent_s())
        
    end = timer()
    print('Total run time: {} s.'.format((end-start)))

def acquire_height_data(L, N):
    
    '''
    acquire_height_data: acquires and saves system height time series for recurrent phase.
    produces file of form: 'height_data_L.csv'.
    Args: 
        L: system size.
        N: number of data points/number of iterations model runs for after cross over.
    '''
        
    # array of system objects for different sizes
    start = timer()
    for i, l in enumerate(L):
        start1 = timer()
        system = oslo.System(l)
        system.iterate(N)
        end1 = timer()
        print('Run time for L={}: {} s.'.format(l, (end1-start1)))
        np.save('data/height_data/height_data_{}_{}'.format(l, N), system.recurrent_h())
        
    end = timer()
    print('Total run time: {} s.'.format((end-start)))

L = [8, 16, 32, 64, 128, 256]
#acquire_avalanche_data(L, 10**4)
#acquire_avalanche_data(L, 10**5)
acquire_height_data(L, 10**5)