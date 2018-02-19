# -*- coding: utf-8 -*-
import ctypes
import numpy as np
import numpy.ctypeslib as ctl
import oslo as oslo
from timeit import default_timer as timer
   
def run_oslo(mode, N, L, p):
    '''
    run_oslo: Runs the oslo model for a single run.
    Params: 
        mode: 'cpp' runs the algorithm in C++ for a significant speedup,
              'python' runs the algorithm in Python,
              'use_data' loads existing data files from saved runs.
        N: Number of iterations.
        L: array-like, system sizes to run the model for. 
        p: probability of setting threshold gradients to 1.
    
    Returns:
        heights_data: array-like, array containing arrays of system height 
                      data for each system size.
        recurrent_h_data: array-like, array containing arrays of recurrent height
                          data for each system size.
        recurrent_s_data: array-like, array containing arrays of recurrent avalanche
                          size data for each system size.            
        t_c_data: array-like, containing crossover times for each system size.
        t_c_th_data: array-like, containing theoretical cross over times for 
                     each system size.
    '''

    # initialise arrays to hold arrays of data for each L value
    recurrent_s_data = []
    recurrent_h_data = []
    heights_data = []
    t_c_data = []
    t_c_th_data = []
    
    if mode == 'cpp':
        # run for each system size specified
        for l in L: 
            
            # initalise arrays to pass into c++ code for each system size
            t_c = np.zeros(1, np.int)
            t_c_theory = np.zeros(1, np.float)
            h = np.zeros(l + 1, np.int)
            zth = np.zeros(l, np.int)
            heights = np.zeros(N, np.int)
            avalanche_sizes = np.zeros(N, np.int)
            
            # load shared library dll source for c++ code
            lib = ctypes.cdll.LoadLibrary('./oslo.dll')
            py_oslo = lib.oslo        
            py_oslo.restype = None
            # pass python parameters into c++ types to call function in python
            py_oslo(ctypes.c_int(N), ctypes.c_int(l), ctypes.c_double(p), ctl.as_ctypes(t_c),
                    ctl.as_ctypes(t_c_theory), ctl.as_ctypes(h), ctl.as_ctypes(zth), 
                    ctl.as_ctypes(heights), ctl.as_ctypes(avalanche_sizes))
            # append filled arrays to relevant containers
            heights_data.append(heights)
            recurrent_s_data.append(avalanche_sizes[t_c[0]:]) # cut off at t_c for recurrent data
            recurrent_h_data.append(heights[t_c[0]:])
            t_c_data.append(t_c[0])
            t_c_th_data.append(t_c_theory[0])
        
    if mode == 'python':    
        # run for each system size specified
        for l in L:
            # instantiate a system object and iterate N times using method
            system = oslo.System(l)
            system.iterate(N)
            # populate relevant containers with system data
            heights_data.append(system.heights)
            recurrent_s_data.append(system.recurrent_s())
            recurrent_h_data.append(system.recurrent_h())
            t_c_data.append(system.t_c)
            t_c_th_data.append(system.t_c_theory())
    
    if mode == 'use_data':
        
        start = timer()
        # run for each system size specified
        for l in L:
            # load up stored .npy files from previous runs
            fname = 'data/avalanche_data/avalanche_sizes_{}_{}.npy'.format(l, N)
            recurrent_s = (np.load(fname)).astype(int)
            print('Dataset size for L={}: {}'.format(l, len(recurrent_s)))
            # store temporary array in the permanent array
            recurrent_s_data.append(recurrent_s)
        end = timer()
        print('Read time: {} s.'.format((end-start)))
        
    
    return heights_data, recurrent_h_data, recurrent_s_data, t_c_data, t_c_th_data

def run_oslo_multi(mode, M, N, L, p):
    '''
    run_oslo_multi: Run oslo model multiple times to calculate error on 
    calculated values.
    Params: 
        mode: 'cpp' runs the algorithm in C++ for a significant speedup,
              'python' runs the algorithm in Python,
              'use_data' loads existing data files from saved runs.
        M: Number of runs to carry out.
        N: Number of iterations.
        L: array-like, system sizes to run the model for. 
        p: probability of setting threshold gradients to 1.
    Returns:
        height_mean_multi: array of array-like, contains arrays of mean recurrent height
                           for each system size, contained in an array for each run.
        height_sd_multi: array of array-like, contains arrays of sd on recurrent height
                         for each system size, contained in an array for each run.
        t_c_multi: array of array-like, contains arrays of t_c for each system
                   system  size, contained in an array for each run.
        t_c_th_multi: array of array-like, contains arrays of theoretical t_c for each system
                      system  size, contained in an array for each run.
        s_data_multi: array of array of array-like, contains output from recurrent
                      avalanche size data for each run.
    '''

    t_c_multi = []
    t_c_th_multi = []
    height_mean_multi = []
    height_sd_multi = []
    s_data_multi = []
    
    for m in range(M):
        # run oslo model M times
        heights_data, recurrent_h_data, recurrent_s_data, t_c_data, t_c_th_data = run_oslo(mode, N, L, p)
        # populate output arrays using processed data from each run
        h_mean_data = [np.mean(h) for h in recurrent_h_data]
        h_sd_data = [np.std(h) for h in recurrent_h_data]
        height_mean_multi.append(h_mean_data)
        height_sd_multi.append(h_sd_data)     
        t_c_multi.append(t_c_data)
        t_c_th_multi.append(t_c_th_data)
        s_data_multi.append(recurrent_s_data)
        
    return height_mean_multi, height_sd_multi, t_c_multi, t_c_th_multi, s_data_multi
        