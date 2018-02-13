# -*- coding: utf-8 -*-
import ctypes
import numpy as np
import numpy.ctypeslib as ctl
import oslo as oslo
from timeit import default_timer as timer

def run_oslo(mode, N, L, p):
    

    recurrent_s_data = []
    recurrent_h_data = []
    heights_data = []
    t_c_data = []
    t_c_th_data = []
    
    if mode == 'cpp':
        
        for l in L: 

            t_c = np.zeros(1, np.int)
            t_c_theory = np.zeros(1, np.float)
            h = np.zeros(l + 1, np.int)
            zth = np.zeros(l, np.int)
            heights = np.zeros(N, np.int)
            avalanche_sizes = np.zeros(N, np.int)
            
            lib = ctypes.cdll.LoadLibrary('./oslo.dll')
            py_oslo = lib.oslo        
            py_oslo.restype = None
            py_oslo(ctypes.c_int(N), ctypes.c_int(l), ctypes.c_double(p), ctl.as_ctypes(t_c),
                    ctl.as_ctypes(t_c_theory), ctl.as_ctypes(h), ctl.as_ctypes(zth), 
                    ctl.as_ctypes(heights), ctl.as_ctypes(avalanche_sizes))
            heights_data.append(heights)
            recurrent_s_data.append(avalanche_sizes[t_c[0]:])
            recurrent_h_data.append(heights[t_c[0]:])
            t_c_data.append(t_c[0])
            t_c_th_data.append(t_c_theory[0])
        
    if mode == 'python':
    
        for l in L:
            system = oslo.System(l)
            system.iterate(N)
            heights_data.append(system.heights)
            recurrent_s_data.append(system.recurrent_s())
            recurrent_h_data.append(system.recurrent_h())
            t_c_data.append(system.t_c)
            t_c_th_data.append(system.t_c_theory())
    
    if mode == 'use_data':
        
        start = timer()
        for l in L:
            fname = 'data/avalanche_data/avalanche_sizes_{}_{}.npy'.format(l, N)
            recurrent_s = (np.load(fname)).astype(int)
            print('Dataset size for L={}: {}'.format(l, len(recurrent_s)))
            # store temporary array in the permanent array
            recurrent_s_data.append(recurrent_s)
        end = timer()
        print('Read time: {} s.'.format((end-start)))
        
    
    return heights_data, recurrent_h_data, recurrent_s_data, t_c_data, t_c_th_data